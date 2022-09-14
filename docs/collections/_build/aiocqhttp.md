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

这里有两种方法：反向 WebSocket 或者 HTTP。配置可以参考 [aiocqhttp 文档](https://aiocqhttp.nonebot.dev/#/getting-started) 。

## 3. 编辑 Moment 配置文件

修改 Moment 提供的 `template-aiocqhttp.yml` 文件为自己的配置文件。

```yaml
# Moment user config template

name:
    moment-aiocqhttp-test

env:
    CentOS

platform:
    aiocqhttp

aiocqhttp:
    api-root:
        cqhttp host+port  # 若使用反向websocket, 无需此项. 否则若使用http, 填写cqhttp的host+post
    host:          # aiocqhttp server 的地址
        your-host
    port:          # aiocqhttp server 的端口号
        your-port
    account:       # 机器人qq号
        your-account
    root-accounts: #可以对机器人发送更高命令的用户的qq号
        - root1
        - root2
    working-group: # 工作的群聊
        your-working-qq-group

plugins: # 想要开启的插件
    - Help
```

主要修改部分为 `aiocqhttp` 开头的部分，涉及到 Moment 能否正常使用。其它信息仅作参考。

注意 `go-cqhttp` 与 `aiocqhttp` 使用的是反向 WebSocket 还是 HTTP，这涉及到 `api-root`  这一项是否需要填写。



## 4. 测试

在你的 QQ 群发送 `ping`，查看是否回复。