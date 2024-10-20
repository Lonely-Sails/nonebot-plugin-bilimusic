<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-mc-watcher

_✨ 一款基于 Motd 监控多个 Minecraft 服务器的 QQ 机器人插件。 ✨_

</div>

## 📖 介绍

本插件可以帮助你监控多个 Minecraft 服务器的状态，并通过 QQ 机器人发送提醒，并且无需额外装任何插件或模组。目前已经实现的功能如下：

- `/mc` 或 `/minecraft` 指令，查看服务器状态。
- 监控多个 Minecraft 服务器的状态，并且发送提醒。

## 💿 安装

你可以使用 `nb plugin install nonebot_plugin_mc_watcher` 来安装此插件。

## ⚙️ 配置

在 NoneBot2 项目的`.env`文件中添加下表中的必填配置

|            配置项             | 必填 |  默认值  |              说明              |
|:--------------------------:|:--:|:-----:|:----------------------------:|
|     minecraft_servers      | 是  |   无   |    要监控的服务器名称和对应的地址（一个字典）     |
| minecraft_update_interval  | 否  |  30   | 向 Minecraft 服务器发送 Motd 请求的间隔 |
| minecraft_broadcast_server | 否  | True  |        是否广播服务器开启/关闭消息        |
| minecraft_broadcast_player | 否  | False |       是否广播服务器玩家离开/加入消息       |
| minecraft_broadcast_groups | 否  |  \[]  |  广播的 QQ 群号列表（若为空则上面的两个不生效）   |

## 🎉 使用

可以在任意群里发送 `/mc` 或 `/minecraft` 指令来查看所有服务器状态。

### 指令表

|       名称       | 权限 | 说明         |
|:--------------:|:--:|:-----------|
| mc / minecraft | 无  | 查看所有的服务器状态 |

## 🙏 鸣谢

> [mcproto](https://pypi.org/project/mcproto/)
