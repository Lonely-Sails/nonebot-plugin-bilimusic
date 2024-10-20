import re
import json
import asyncio
from pathlib import Path
from tempfile import gettempdir
from httpx import HTTPStatusError, AsyncClient

from nonebot.log import logger

from .config import Config


class Downloader:
    config: Config = None
    client: AsyncClient = AsyncClient()
    temp_directory = (Path(gettempdir()) / 'BiliMusic')

    def __init__(self, config: Config):
        self.config = config
        if not self.temp_directory.exists():
            self.temp_directory.mkdir(parents=True)
        if not config.bilimusic_cookie:
            logger.warning(
                '检测到 Cookie 未设置！无法获取到歌词，'
                '请查看 https://github.com/Lonely-Sails/nonebot-plugin-bilimusic#readme 查看如何设置。'
            )
        self.client.headers = {
            'Cookie': (config.bilimusic_cookie if config.bilimusic_cookie else ''),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                          ' (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        }

    async def download_one(self, bvid: str):
        if response := await self.fetch_info(bvid):
            music_url, video_info = response
            title = video_info['videoData']['title']
            headers = {'Referer': F'https://www.bilibili.com/video/{bvid}/'}
            lyric_task = self.fetch_lyric(video_info, title, headers)
            download_task = self.download_music_file(music_url, title, headers)
            if self.config.bilimusic_limit >= 2:
                lyric_task = asyncio.create_task(lyric_task)
                download_task = asyncio.create_task(download_task)
            return await lyric_task, await download_task, title

    async def request(self, url: str, headers: dict, params: dict = {}):
        try:
            logger.debug(F'正在请求 {url}')
            response = await self.client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response
        except HTTPStatusError as error:
            logger.error(F'请求 {url} 失败，错误的状态码 {error.response.status_code}！')
        except (ConnectionError, TimeoutError):
            return None

    async def download_music_file(self, url: str, title: str, headers: dict):
        file_path = (self.temp_directory / F'{title}.mp3')
        if response := await self.request(url, headers=headers):
            with file_path.open('wb') as file:
                async for chunk in response.aiter_bytes(chunk_size=1024):
                    file.write(chunk)
                return file_path.absolute()

    async def fetch_info(self, bvid: str):
        url = F'https://www.bilibili.com/video/{bvid}/'
        headers = {'Referer': url}
        if response := await self.request(url, headers=headers):
            response_data = response.text
            play_info = json.loads(re.findall(r'__playinfo__=(.*?)</script>', response_data)[0])
            video_info = json.loads(re.findall(r'__INITIAL_STATE__=(.*?);\(function', response_data)[0])
            return play_info['data']['dash']['audio'][0]['baseUrl'], video_info

    async def fetch_lyric(self, video_info: dict, title: str, headers: dict):
        if not self.client.headers.get('Cookie'):
            logger.warning('未设置 Cookie，无法获取歌词！')
            return None
        params = {'aid': video_info['aid'], 'cid': video_info['cid']}
        if response := await self.request('https://api.bilibili.com/x/player/wbi/v2', headers, params=params):
            response_data = response.json()
            if response_data := response_data['data']['subtitle']['subtitles']:
                subtitle_url = response_data[0]['url']
                if response := await self.request(subtitle_url, headers):
                    response_data = response.json()
                    lyric_lines = ['[ti:]\n[ar:]\n[al:]\n[by:]\n[offset:0]', F'[00:00.00]{title}']
                    for sentence in response_data['body']:
                        time = sentence['from']
                        content = sentence['content'].replace('♪', '').strip()
                        lyric_lines.append(f'[{int(time // 60):0>2}:{round(time % 60, 2):0>5}]{content}')
                    lyric_file_path = (self.temp_directory / F'{title}.lrc')
                    lyric_file_path.write_text('\n'.join(lyric_lines), encoding='Utf-8')
                    return lyric_file_path.absolute()
        logger.warning(F'获取 {title} 歌词失败！')
        return None


