from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata, get_plugin_config
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment, Message, Bot

from .config import Config
from .downloader import Downloader
from .utils import parse_bvid

__plugin_meta__ = PluginMetadata(
    name='BiliMusic Downloader',
    description='一款基于 Nonebot2 的 Bilibili 视频提取音乐和歌词插件。',
    usage='通过命令 /bilimusic 或 /bm 解析视频链接，并下载音乐和歌词文件。',
    homepage='https://github.com/Lonely-Sails/nonebot-plugin-bilimusic',
    type='application',
    config=Config,
    supported_adapters={'~onebot.v11'}
)

config = get_plugin_config(Config)
downloader = Downloader(config)
bilimusic_matcher = on_command('bilimusic', aliases={'bm'}, force_whitespace=True)
bilimusic_group_matcher = on_command('bilimusic group', aliases={'bm group'}, force_whitespace=True)


@bilimusic_matcher.handle()
async def handle_bilimusic(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    args = parse_bvid(args.extract_plain_text().strip())
    if not args:
        await bilimusic_matcher.finish('请输入视频链接或 BV 号！', at_sender=True)
    download_task = downloader.download_one(args)
    if title := await anext(download_task):
        await bilimusic_matcher.send(
            MessageSegment.reply(event.message_id) + F'解析成功！正在尝试下载 {title} 的音乐和歌词文件，请耐心等待……'
        )
        lyric_file, music_file, title = await anext(download_task)
        if lyric_file:
            await bot.call_api('upload_group_file', group_id=event.group_id, file=str(lyric_file), name=F'{title}.lrc')
            lyric_file.unlink()
        if music_file:
            await bot.call_api('upload_group_file', group_id=event.group_id, file=str(music_file), name=F'{title}.mp3')
            music_file.unlink()
        if not (music_file or lyric_file):
            await bilimusic_matcher.finish('音乐或歌词文件下载失败，请检查日志。', at_sender=True)
        await bilimusic_matcher.finish('音乐和歌词文件已上传至群聊！若未找到则是获取失败。', at_sender=True)
    await bilimusic_matcher.finish('请求错误！无法解析视频链接，请稍后再试。', at_sender=True)


@bilimusic_group_matcher.handle()
async def handle_bilimusic_group(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    args = parse_bvid(arg.extract_plain_text().strip())
    if not args:
        await bilimusic_group_matcher.finish('请输入视频链接或 BV 号！', at_sender=True)
    download_task = downloader.download_group(args)
    if section_info := await anext(download_task):
        title, count = section_info
        await bilimusic_group_matcher.send(
            MessageSegment.reply(event.message_id) + F'解析成功！正在尝试解析视频所在集合 {title} 所有的 {count} 个视频，请耐心等待……'
        )
        failed_count = await anext(download_task)
        await bilimusic_group_matcher.send(
            MessageSegment.reply(event.message_id) + F'下载完毕！共下载 {count} 个视频，其中 {failed_count} 个下载失败，请检查日志。'
        )
        file_path = await anext(download_task)
        await bot.call_api('upload_group_file', group_id=event.group_id, file=str(file_path), name=F'{title}.zip')
        file_path.unlink()
        await bilimusic_group_matcher.finish('集合音乐文件已上传至群聊！若未找到则是获取失败。', at_sender=True)
    await bilimusic_matcher.finish('请求错误！无法解析视频链接，请确保链接正确或稍后再试。', at_sender=True)
