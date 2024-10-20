<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-mc-watcher

_✨ 一款基于 Nonebot2 的 Bilibili 视频提取音乐和歌词插件。 ✨_

</div>

## 📖 介绍

本插件可以解析 Bilibili 视频，并提取出视频中的音乐和歌词（基于字幕故可能不准）。

- `/bm` 或 `/bilimusic` 指令来解析视频。

## 💿 安装

你可以使用 `nb plugin install nonebot_plugin_bilimusic` 来安装此插件。

## ⚙️ 配置

在 NoneBot2 项目的 `.env` 文件中添加下表中的配置：

|       配置项        | 必填 | 默认值 |        说明        |
|:----------------:|:--:|:---:|:----------------:|
| bilimusic_limit  | 否  |  2  |     对请求速率的限制     |
| bilimusic_cookie | 否  |  空  | 获取歌词所必须的 B 站账号口令 |

## 🎉 使用

### 指令表

|       名称       | 权限 | 说明                     |
|:--------------:|:--:|:-----------------------|
| bm / bilimusic | 无  | 解析视频，需附带参数（可以是BV号或是链接） |

### 获取 Cookie

> [!CAUTION]
> 此功能需要 Bilibili 账号，对于获取的 Cookie 请妥善保管！如果因此导致账号被盗或是封禁，作者概不负责。

1. 打开浏览器，进入 Bilibili 主页，登陆你的账号。
2. 按 F12 打开开发者工具，切换到 Network 标签。
3. 刷新页面，在 Network 标签下找到并点击 `www.bilibili.com` 请求。
4. 打开 `Headers` 或者 `标头` 标签，找到 Cookie 字段，复制其内容（无需复制 `Cookie: ` 前缀）。
