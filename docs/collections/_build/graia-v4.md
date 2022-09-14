---
title: 使用 Graia Application 部署到 QQ
nav_order: 1
---

# 使用 Graia Application 部署到 QQ
[Graia Application](https://github.com/GraiaProject/Application) 是一个 Python 的基于 mirai-api-http 的聊天框架，虽然此框架已经停止维护，但仍然能够正常使用并且满足简单的需求。

本教程基于 shell Moment 的配置成功。

## 1. 配置 mirai 与 mirai-api-http 

直接去 [这里](https://github.com/project-mirai/mirai-api-http) 查看 mirai-api-http 的教程。注意，Graia Application 不支持 2.x 的版本。我推荐安装 `mirai-api-http-v1.12.0`。

{: .warning }
当然，由于这些框架相对于 QQ 并不稳定，当配置发生错误时请更换方案，一般是越新的方法越有效。

安装成功后进入下一步。

## 2. 配置 Graia Application

包含两个 python 子包，撰写文档时有效版本如下：

```
graia-application-mirai           0.18.4
graia-broadcast                   0.8.11
```

你可以使用诸如 `pip` 或者 `poetry` 等 Python 包管理器安装对应版本。安装时也请注意参考[其文档](https://graia-document.vercel.app/docs/guides/installation)。

当完成安装后，请照其示例编写一个简单的机器人（比如单纯地发一个 `Hello World`）来确保环境配置无误。如这一步成功，可以进入下一步。

## 3. 编辑 Moment 配置文件

修改 Moment 提供的 `template-graia-v4.yml` 文件为自己的配置文件。

```yaml
# Moment user config template

name:
    moment-graia-test

env:
    CentOS

platform:
    graia-v4

graia-v4:
    host:          # mirai 的地址. e.g. localhost / 127.0.0.1
        your-host
    port:          # mirai 的端口号. e.g. 8000
        your-port
    author-key:    # mah 的 author key
        your-author-key
    account:       # 机器人qq号
        your-account
    root-accounts: #可以对机器人发送更高命令的用户的qq号
        - root1
        - root2
    working-group: # 工作的群聊的群号
        your-working-qq-group

plugins: # 想要开启的插件
    - Help
```

主要修改部分为 `graia-v4` 开头的部分，涉及到 Moment 能否正常使用。其它信息仅作参考。



## 4. 测试

在你的 QQ 群发送 `ping`，查看是否回复。

