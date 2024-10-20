from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata, get_plugin_config
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, Bot

from .config import Config
from .downloader import Downloader
from .utils import parse_bvid

__plugin_meta__ = PluginMetadata(
    name='MinecraftWatcher',
    description='一款基于 Nonebot2 的 Bilibili 视频提取音乐和歌词插件。',
    usage='通过命令 /bilimusic 或 /bm 解析视频链接，并下载音乐和歌词文件。',
    homepage='https://github.com/Lonely-Sails/nonebot-plugin-mc-watcher',
    type='application',
    config=Config,
    supported_adapters={'~onebot.v11'}
)

config = get_plugin_config(Config)
downloader = Downloader(config)
bilimusic_matcher = on_command('bilimusic', aliases={'bm'}, force_whitespace=True)


@bilimusic_matcher.handle()
async def handle_bilimusic(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    args = parse_bvid(arg.extract_plain_text().strip())
    if not args:
        await bilimusic_matcher.finish('请输入视频链接或 BV 号！', at_sender=True)
    if response := await downloader.download_one(args):
        lyric_file, music_file, title = response
        await bilimusic_matcher.send(F'解析 {arg} 成功：{title}', at_sender=True)
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
