---
title: 使用 aiocqhttp 部署到 QQ
nav_order: 1
---

# 使用 aiocqhttp 部署到 QQ
[aiocqhttp](https://github.com/nonebot/aiocqhttp) 是一个 [onebot](https://github.com/botuniverse/onebot) 协议的 Python SDK，是 [nonebot](https://github.com/nonebot/nonebot) 机器人框架对接 QQ 的支持。本章将使用 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)（一个 OneBot 实现）搭配 aiocqhttp 将 Moment 在 QQ 群上跑起来。

## 1. 配置 go-cqhttp

请去 [这里](https://docs.go-cqhttp.org/) 查看 go-cqhttp 的教程。以在终端启动，接收到群聊消息为成功标准。安装成功后进入下一步。

## 2. 配置 aiocqhttp

### 2.1 安装

直接使用诸如 `pip` 或者 `poetry` 等 Python 包管理器即可。

### 2.2 配置 go-cqhttp 向 aiocqhttp 的连接

这里有两种方法：反向 WebSocket 或者 HTTP。

## 编辑 Moment 配置文件

修改 Moment 提供的 `template.yml` 文件为自己的配置文件。

```yaml
# Moment user config template

name:
    Moment

env:
    CentOS

platform:
    graia-v4

graia-v4:
    host:          # mirai 的地址
        your-host
    port:          # mirai 的端口号
        your-port
    author-key:    # mah 的 author key
        your-author-key
    account:       # 机器人qq号
        your-account
    root-accounts: #可以对机器人发送更高命令的用户的qq号
        - root1
        - root2
    working-group: # 工作的群聊
        your-working-qq-group
```

主要修改部分为 `graia-v4` 开头的部分，涉及到 Moment 能否正常使用。其它信息仅作参考。



## 第一次启动

在命令行显式启动 Moment：

```bash
python3 run.py <你的配置文件路径>
```

若你直接在 `template.yml` 上修改，你可以直接

```
python3 run.py template.yml
```

如果配置文件有误，程序会报错并中断。这时请仔细查看报错信息并改正。若成功启动，程序会报出一些调试信息并在命令行阻塞，期间机器人所在群聊的消息也会被转发到终端上予以显示。

