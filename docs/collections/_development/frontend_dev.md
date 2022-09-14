---
title: 为 Moment 编写新 FrontEnd
nav_order: 0
---

# 为 Moment 编写新 FrontEnd
你可能想把 Moment 部署到一个新的聊天平台上，但是内置并没有提供这个平台的 FrontEnd。本章将会通过简述相关 API 来引导你编写属于自己的 FrontEnd。



## 1. 解析配置文件

你需要自行规定新配置文件格式。规范为：

```yaml
platform: <平台名>

<平台名>:
	# 你需要的信息. 自行规定
```

yaml 的其他部分（`name` , `env`, `plugins` 等）请保持一致。你需要的信息都要在 `<平台名>` 字段下。

使用 `frontend_config` 中的 YamlConfig（一个对 dict 的包装）来解析字典。你可能需要提供一个模板 `.yml` 文件给用户。



## 2. Message 转换

作为功能正常的保证，需要先确保目标平台的 Message 类型功能涵盖 Moment Message 的功能。重要的几点有：

| 消息成员类型 | 确保                                           |
| ------------ | ---------------------------------------------- |
| 文本         | 能获取文本串（str）                            |
| 图片         | 能获取图片 url，并且能够使用网络下载到图片数据 |
| At           | 能获取 At 对象的唯一标识符                     |
| 引用         | 能够获取引用的信息                             |
| 消息发送者   | 能够获取发送者的唯一标识符                     |

然后需要实现目标平台的 Message 类型与 Moment Message 类型的互相转换。可能它们并不完全一致，但至少要做到尽可能的转换。



## 3. 发送消息方法

你需要至少有一个往目标平台发送消息的方法，此方法必须是异步（`async`）的。定义此方法结束后，需要调用机器人的注册方法进行注册

```python
bot.register_send_method(method)
```



## 4. 接受信息

你需要一个能够持续监听聊天平台，并获取消息的手段。在每次获取消息时，使用转换方法将其转换为 Moment Message，然后调用

```python
await bot.handle_message(message)
```



## 5. 创建 plugin 任务

Moment 的定时任务使用 Python 异步框架 asyncio 实现，你需要拥有一个事件循环 `loop`，然后调用

```
bot.create_plugin_task(loop)
```

 在很多异步 SDK 下，框架本身也会创建一个 `loop`，你可以直接使用；若自己创建 `loop`，要在启动时调用

```
loop.run_forever()
```



## 6. 调试与运行

一切就绪后，剩下的就是调试和排查了。当一切都跑通之后，就可以在新平台上体验 Moment 的各种功能了！