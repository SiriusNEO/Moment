---
title: 基本使用
nav_order: 0
---

# 基本使用
作为一个群聊机器人，使用方式当然是在群聊中发送特定信息来操控或与其交互，Moment 也不例外。



## 1. 获取帮助

除了文档以外，Moment 本身提供了内嵌于程序的帮助文档。

使用

```
help
```

查看目前 Moment 上安装的所有插件、其运行情况。根据安装顺序，其之前会有相应编号（从 0 开始），此编号也为后续查询特定插件提供了索引。当然，也可以通过名字——插件名字即编号后的英文单词，以大写字母开头。

查看特定插件的帮助文档，使用

```
help <插件编号>
```

或者

```
help <插件名字>
```



当内置文档不是很清楚时，你可以查看本文档的插件部分中关于相应插件的介绍。



{: .note }
有趣的是，这个 `help` 的功能本身也作为 Moment 的一个插件存在，因为其在设计上秉持着将所有功能均作为插件进行管理的原则。这一插件相比于其它插件更加根本，类似于一些语言的"包管理器"一样的存在。



## 2. 推荐功能

### Database & Replier

Moment 引以为傲的是它出色的数据库功能，并有着基于数据库的强大的 "键值对回复器" 功能。启用这两个插件可以获得一个简洁明了的键值对回复机器人。实践上，群聊中这个功能有着很强的趣味性和实用性。

{: .note }
什么是键值对回复机器人？简单来说，就是有一个 key-value 数据库，并且当收到匹配 key 消息时回复 value 消息的机器人。别看这很简单，实际上许多智能聊天机器人的原理就是这个。大名鼎鼎的 AIML(Artificial Intelligence Markup Language) 也不外乎如此。

### Random

可能有的朋友有跑团机器人之类的需求。Moment 的 Random 插件完美支持了类似 [Dice!](https://v2docs.kokona.tech/zh/latest/User_Manual.html) 的掷骰功能，并还有其它趣味功能，相信能给你带来不错的体验。

### Alarm

定时是聊天机器人的一个优势所在——它们最擅长干这种规律性、机械性的事情。为特定的时间设好闹钟，然后 Moment 便会在指定的小时、分钟跳出来提醒你。



## 3. 权限账号

有些指令拥有很强的力量（甚至可以摧毁数据库），你可能并不想谁都能使用。Moment 提供了一个 root 用户的概念，你可以在配置文件中写上 `roots` 的相关信息（比如账号），这样一些特定的命令只有这些用户能够执行。

