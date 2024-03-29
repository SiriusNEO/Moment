---
title: Replier - 键值对回复器插件
nav_order: 12
---

# Replier - 键值对回复器插件
## 1. 简介

键值对回复一直都是群聊机器人最重要的功能之一。借助强大的数据库插件，Moment 的 Replier 有着更出色的表现。



## 2. 数据库

Replier 插件有着自己的数据库，这一数据库的每个 Line 可以有如下字段：

| 字段名 | 数据类型      | 简介                                  |
| ------ | ------------- | ------------------------------------- |
| key    | List[Message] | 用于局部匹配的关键词字段              |
| full   | List[Message] | 用于完全匹配的关键词字段              |
| pool   | Message       | 池名，以一个带 text 的 Message 储存。 |
| cm     | List[Message] | 内容字段。                            |
| argmap | dict          | 模板串映射。                          |
| active | int           | 活跃标记，表示此消息不进入冷静期。    |

数据库默认位置在 `local/cmdb.json`。



## 3. 使用

### 3.1 关键词回复

Replier 的 `handle_message` 首先对命令消息进行处理，若均非命令消息，则它会认为这是一句群聊里的 "话"，会尝试在数据库中寻找可能的回复。

形式化地，每收到一条**话** (假设语句是 `asdfasdf`)，Replier 会往数据库发送两个查询：

```
[key@asdfasdf]
```

与

```
[full=asdfasdf]
```

代码上，先判断第一句的查询结果，再判断第二句 (这并不重要)。当某一句查询结果非空时，直接返回查询结果**第一条** Line 的 `cm` 字段内容。

在这个过程中，`cm` 字段缺失的条目将会被忽略。

在功能上，这两句话体现为：

- 判断数据库中是否有 key 值是 `asdfasdf` 子串的数据。有的话，输出对应的 cm 内容。
- 判断数据库中是否有 full 值等于 `asdfasdf` 的数据。有的话，输出对应的 cm 内容。



### 3.2 多 key / 多 full / 多 cm

可以看到设计上，这三个字段的类型都是 `List[Message]`。这是为了更强大的功能作准备的。也因为此，这三个字段均支持 `+/-` 修改符。

---



#### 3.2.1 多键值

对于一个有多个 `key` (或多个 `full` ) 的数据条目，一句话只有满足每个 key(full) 均触发才算触发，即与数据库的查询语句语义保持一致。这带来了一些巧妙的用法，如有一条数据为

```
key=[爸爸, 妈妈] cm=给你的不少不多
```

那么不管你在群聊里说 `爸爸和妈妈` 还是 `妈妈与爸爸`，Moment 均会被触发并回复你 `给你的不少不多` 。

---



#### 3.2.2 多 cm

对于一个 `cm` 条目有多条内容的 Line，当其被触发时，其会将所有内容一并返回。在发送上，其表现为逐条发送。例如若有一条数据为

```
key=测试 cm=[1, 2, 3]
```

那么当你在群聊里的话涉及 `测试`，机器人便会发送

```
bot: 1
bot: 2
bot: 3
```



### 3.2 兼容老命令

由于一些历史原因，Moment 适配了前一代 bot 的命令格式。你既可以直接用数据库命令添加一条关键词回复，还可以用老风格的命令。老风格命令以 `cm` 或者 `。cm` 作为命令头。

---



#### 3.2.1 查询

查询命令格式为：

```
cm <关键词>
```

注意，别带引用。这相当于查询 `key=<关键词>` 或者 `full=<关键词>` 的项，选择第一个 Line 的 `cm` 指向内容进行发送。

---



#### 3.2.2 新建

新建命令格式为：

```
cm <关键词> <字段名, 可省略, 默认为full>
```

并带引用。相当于如下新数据库命令

```
<字段名>=<关键词> cm=%this
```

如引用一张猫图，然后回复并发送命令

```
cm 猫图
```

表示设置一个完全匹配 "猫图" 这两个字的数据，内容是引用的那个猫图。

---



#### 3.2.3 删除

删除命令格式为

```
cm del <关键词>
```

相当于执行

```
[key=<关键词>] del
```

以及

```
[full=<关键词>] del
```



### 3.3. 模板串 Template

模板 (Template) 灵感来自于 Python Flask 框架，简单来说就是带参的回复规则。

我们来看一个需求场景，你可能想建立一个规则：当有人说 "我是XX" 时，机器人回复他 "XX是我爹"。如果不用模板串，那么可能需要添加很多很多条数据来实现差不多的效果。但是有了模板串，我们可以用这种数据：

```
full=我是{name} cm={name}是我爹
```

这里的 `{name}` 被称作一个**参数 (Argument)**。一个参数用一个大括号在文字中表明，大括号中的内容为它的**参数名**。注意，相同参数名在 full 和 cm 间是互相对应的。

---



#### 3.3.1 模板串创建

模板串作为一个 Replier 而非 Database 插件的特性，目前只能通过 Replier 的语法创建。使用 `3.2` 中提到的旧命令风格来创建一个模板串映射。

```
cm <关键词> (引用某消息)
```

注意，模板串不能是 `key` 类型。

在模板串中，使用 `{参数名}` 表示此处有一个参数。你也可以不写参数名，所有无参数名的参数默认名称是从 `0` 开始的递增数字。如

```
我是{}你是{}
```

 相当于

```
我是{0}你是{1}
```

{: .danger }
注意，`key/full` 中的模板串内，参数不能连续出现。即出现 `{}{}` 的情况。因为这会让匹配器不知道把中间的汉字归到哪个参数里。在 `cm` 里，连续参数是可以的。

---



#### 3.3.2 模板串匹配规则

一个参数匹配至少一个非空字符。例如

```
full=我是{name}
```

那么

```
我是猫猫狗狗 / 我是AAA / 我是小明
```

都能匹配。并且，其中 `猫猫狗狗`, `AAA`, `小明` 会被抽取成为 `name` 参数的值。

---



#### 3.3.3 模板串触发规则

一个带模板串的消息会按 `3.3.2` 的匹配规则对信息进行匹配。若成功匹配，其会抽取话语中对应位置参数的值（如上文的 `猫猫狗狗` 等），并用此对 `cm` 串进行**渲染 (render)**。如按上文，`cm` 中 `{name}` 对应位置会被替换为 `猫猫狗狗`。

---



#### 3.3.4 模板串储存方式

不同于普通信息，模板串数据会额外多一个 `argmap` 字段，用于储存模板参数的位置映射关系。这里就不细讲了。对于串本身，在 `key/full` 中它会以抽去参数名，只保留 `{}` 的形式存在；对于 `cm` ，它会以原文形式存在。



### 3.4 抽取池 Pool

考虑一个场景：你希望建立一个这样的回复

```
full=来个水果 cm=给你一个苹果
```

这是一条正常的回复。但有一天你心血来潮，想再来一个

```
full=来个水果 cm=给你一个香蕉
```

并且你希望这两个回复是随机一个出现的。如果你直接新建一条数据，Replier 默认的策略是覆盖而不是随机。因此这里就需要建立一个抽取池。

抽取池也是 Replier 特有的特性，只有通过它触发回复的消息会经过抽取池处理。

---



#### 3.4.1 抽取

一个**抽取**指的是信息文字串中出现的一个抽取声明位置。抽取以 `<>` 作为标志，括号中间的部分成为**抽取池名 (Pool Name)** ，表示从哪个池中抽取。例如

```
full=来个水果 cm=给你一个<水果>
```

其中

```
<水果>
```

是一个抽取，表示从 Pool Name 为 "水果" 的抽取池中选择一个内容，并替代这个位置。

{: .attention }
抽取只能出现在 `cm` 字段中，出现在其它字段和正常的文本是一样的。并且只有 Replier 的回复触发才能对抽取进行渲染替换。

---



#### 3.4.2 抽取池

一个抽取池是一个数据库的 Line，并且带有 `pool` 字段。`pool` 字段的内容需要是一个带有 `text` 的 `Message` 类型，表示这个抽取池的池名，即 Pool Name。

抽取池的内容存在 `cm` 字段。通常作为一个抽取池，`cm` 字段需要有不止一个元素。如为了实现上面的功能，你可以建立一个抽取池如下 (这不是命令, 只是示意)

```
pool=水果 cm=[苹果, 香蕉]
```

---



#### 3.4.3 抽取的渲染规则

对于 `cm` 字段中所有文本消息，在其要被发送时，会对其中所有的抽取进行渲染替换，规则为提取出每个抽取的 Pool Name，并以其为索引去查找池。若成功找到，从这个池的 `cm`  字段抽取一个消息，替换这个抽取的位置。

如要实现上述功能，创建数据

```
full=来个水果 cm=给你一个<水果>
```

然后在发送时，渲染器会进行查询

```
[pool=水果]
```

然后抽取查到的第一个 Line 的 `cm` 字段中的内容，如 "苹果"，最后替换发送

```
bot: 给你一个苹果
```

上述过程中发生找不到，或者抽取的消息无文本时，均会用空串替换。



### 3.5 冷静期机制

当群聊中的人类发生讨论，并且讨论的高频词正好是关键词时，就会发生机器人一直被触发的场景，很影响观感。Replier 采用了冷静期来解决。

冷静期效果是，当一个 key/full 被触发后，会针对**这条数据**设置一个冷静期 (目前是10分钟)，在此期间这条数据不再会被回复出发。(仍可通过数据库手段触发)

你可以使用内置的一个命令 `timejump` 来清除掉所有冷静期。同时，对于某些你不想让 bot 进入冷静期的信息，你可以给其设置 `active` 字段 (值无所谓，只要数据中有这个字段存在即可) 来让其不会进入冷静期。