---
title: 从 shell 开始
nav_order: 0

---

# 从 shell 开始

本章会介绍 Moment 的基础配置文件以及怎样在 shell 构建起你的 Moment 机器人。由于 shell 不依赖于任何框架（QQ、微信等），排除了这方面的配置麻烦，因此我将其作为**部署教程的第一篇**。后续的配置将在此章的成功上进行。

本教程从你获取到 Moment 开始。如你还未获取，请先 clone [此仓库](https://github.com/SiriusNEO/Moment)。



## 1. Python 与依赖

你需要先拥有 Python (>=3.7) 的运行环境，此处不多介绍。

启动最纯净的 Moment （也就是 shell Moment）的最小需求是解析配置文件用的 `PyYaml` 库，以及基本的异步网络服务使用的 `aiohttp` 库。使用 `pip` 等包管理器完成安装后继续下一步，以不发生 `ImportError` 为准。



## 2. 配置文件

启动 Moment 需要一个格式为 YAML (YAML Is not markup language, `.yml`) 的配置文件。不同的对接平台要求的配置文件格式不同。

Moment 决定采用指定配置文件启动的考虑主要有：

- 首先，Moment 作为一个跨平台机器人，需要对不同平台作适配，因此我希望能够将平台信息写在文件中。
- 其次，当你有多平台同时启动（多实例）的需求时，你只需要分别撰写配置文件，然后分别指定启动即可。这尤其在开发时（debug、release 分离）以及多群聊（为了稳定，一个 Moment 示例设计为单群聊使用）会很方便。

我们先以启动 shell Moment 为目标，编写 shell 的配置文件。



## 3. 编辑 shell Moment 配置文件

修改 Moment 提供的 `template-shell.yml` 文件为自己的配置文件。

```yaml
# Moment user config template

name:
    moment-shell-test

env:
    CentOS

platform:
    shell

shell:
    username:      # 用于与机器人对话的用户名
      sirius
    root-accounts: # 可以对机器人发送更高命令的用户
      - sirius
    input-offset:  # 此项可删掉. 表示控制input往右偏移的单位数.
      70

plugins: # 想要开启的插件
    - Help
```

其中，

- `name` 和 `env` 字段仅供显示使用，可以随意 DIY。
- `platform` 决定了运行平台，很重要，不同平台的具体配置要求不一样。
- `<platform_name>`（即此章示例中的 `shell` 字段下）中是此平台要求的一些信息。
- `plugins` 表示想要开启的插件名，安装顺序按照 `plugins` 所列顺序。

对于 shell 的 Moment，并没有什么重要的配置。你甚至可以**直接使用 `template-shell.yml` 来启动**。当你对配置文件有了个大概了解后，进入下一部分。



## 4. 第一次启动

在命令行显式启动 Moment：

```bash
python3 run.py <你的配置文件路径>
```

若你直接在 `template-shell.yml` 上修改或者直接使用它，你可以执行

```
python3 run.py template-shell.yml
```

如果配置文件有误，程序会报错并中断。这时请仔细查看报错信息并改正。若成功启动，程序会报出一些调试信息并在命令行阻塞。

尝试调用 Help 插件的 `ping` 命令。对于 shell 而言，你需要手动按回车来刷新消息队列。输入 `ping` 并连续敲回车可以看到

```
[Mog][INFO](2022-09-14 20:48:11): 成功加载配置文件: template-shell.yml
[Mog][INFO](2022-09-14 20:48:12): 配置对接 shell 成功!
[Mog][INFO](2022-09-14 20:48:12): 插件 Help 已植入Bot @moment-shell-test 中.
[Mog][INFO](2022-09-14 20:48:12): Method "send_message" 成功被注册为 Moment 的发送方法 (It must be async)
[Mog][INFO](2022-09-14 20:48:12): 成功在事件循环中启动所有插件的 plugin_task
[Mog][INFO](2022-09-14 20:48:12): FrontEnd shell 启动完成. moment-shell-test(shell) 正式开始工作.
------------ Moment ChatRoom ------------
                                                                      (sirius) >>> ping
[0] sirius: ping
                                                                      (sirius) >>> 
[1] moment-shell-test: 大家好啊, 我是 moment-shell-test
                                                                      (sirius) >>> 
```

表示安装成功。



## 5. 进一步: Moment ChatRoom 规范

当第 4 步成功后，若你的目标是将机器人应用到其它平台上，可以移步文档其他部分了。若你对通过 shell 和 Moment 聊天的更多内容感兴趣，可继续阅读此部分。

### 5.1 终端消息刷新机制

对于 shell 而言，想要做出类似 Telegram 的那种聊天的效果是比较难的，一个难点是 `asyncio` 异步框架和 `input` 函数之间的矛盾关系。因此 Moment 暂时采用了比较懒惰但有效的方式：操作时刷新消息队列。

当我们运行 shell Moment 时，会建立一个称为**聊天室（ChatRoom）**的环境，你将此处与机器人交互。聊天室拥有一个**消息队列（Message Queue）**，机器人的 `send_message` 方法和你的 `input` 产生的信息都将被塞入消息队列尾部。消息队列将在每次你的输入完成按下回车键时完成一次刷新，当消息队列刷新时，它将拿出队首的一条消息，并显示在终端上。

特别地，若你输入的串均为空白字符，则不会产生消息。你可以借此（如不断按回车）来快速将消息队列中的消息刷出来。



### 5.2 发送图片

终端发送文字是简单的事情。那么怎样发送一张图片给机器人呢？目前，Moment ChatRoom 支持发送本地的图片，采用如下的编码格式：

```
{pic:path}
```

其中 `path`  是图片在本地的路径。如：

```
{pic:local/img/1.png}
```

即可将文件 `local/img/1.png` 作为图片发出。你还可以这样发出一份富文本信息（同时带有文字与图片）

```
some text{pic:a_pic_path}
```

直接连在一起即可。



### 5.3 发送引用

Moment 消息类型还有一个重要的概念就是引用（Quote），很多重要功能都基于此。

在 ChatRoom 中，每个消息都带了一个唯一标识数字，可以在消息被发出时于其头部看到（[n]，n 为数字），这样你可以用如下编码方式在你的对话中发起引用

```
{quote:n}
```



