---
title: 为 Moment 编写插件
nav_order: 0
---

# 为 Moment 编写插件
插件是 Moment 对功能的统一抽象。本章将会对开发 Moment 插件提供帮助与指导，推荐阅读之前先阅读前文的 ”什么是插件“ 部分。

## 1. 插件规范

Moment 的插件指的是一个继承了基类 `Plugin`（`core.plugin`） 的 Python 类。每个插件有两个主要功能接口：

- `handle_message`，只在收到消息时触发，负责应对发来的消息。

  有一个参数 `message: Message`，代表接受的消息。

  返回值可以是单个 `Message` 实例，bot 会将其自动发出；或者一个 `List[Message]`，bot 会一条条将其发出；或者一个 `Error` 。bot 会发出带有 `urge` 信息的 `Error` 。

- `plugin_task`，被创建为一个异步的 Task，可以用于后台任务（搭配 `while True` 循环）。

初始化时，一般需要给插件提供如下信息：

- `name`，插件的名字。注意在许多场合这将成为此插件的指代。
- `requirements`，插件的依赖。由此插件的依赖插件的名字组成的 `list`。
- `info`，插件的简述信息。在一些显示场合会用到。
- `doc`，插件的文档。在调用 `Help` 插件时会被显示。

插件的初始化**均无参数**，并且不应该有任何成员在此时被创建。插件的 ”真正初始化“ 应该是安装时。插件的安装接口统一为：

```python
def setup(self, bot):
```

如果没有特殊需求，可以不重载此方法。但当此方法重载时，应当在方法体中调用基类的 `setup`，即

```python
def setup(self, bot: Bot):
    self.bot = bot    # 特殊需求: 需要获得 bot 作为成员
    super().setup(bot) # 调用基类 setup
```

Moment 被执行时应当被安装。这一功能通过一个装饰器 `check_setup` 来实现。在重载 `handle_message` 和 `plugin_task` 时应当记得进行装饰检查

```python
@self.check_setup
async def handle_message(self, message: Message) -> Union[Message, List[Message], Error]:
```



```python
@check_setup
async def plugin_task(self):
```




## 2. 插件消息调度

每次收到消息，bot 会按**安装顺序**遍历所有插件，并将消息喂给此插件的 `handle_message` 方法。当返回值是一个可以发出的对象（`Message`、`List[Message]` 或者带有 `urge` 字段的 `Error`）时，bot 会将此对象发出并中断此次遍历。

因此如果你希望你的插件被优先执行，你应该在顺序上先安装它。但注意，依赖必须先于使用此依赖的插件先安装。

## 3. 提供给插件的功能方法

Moment 为插件提供了简洁但十分有用的几个方法，基本能满足大部分插件开发需求。

### 3.1 随时发送信息

虽然可以使用 `handle_message` 返回一个消息来发送消息，但是有时候我们可能会有这种需求：

```
发送A消息
执行事件
发送B消息
```

即在同一个逻辑中发送两条消息。

作为插件自身，可以直接调用 `await self.send(msg: Message)` 来完成发送。其原理是注册发送方法时同时将此信息暴露给了所有已安装插件。

此外，在 `plugin_task` 中，你能也仅能使用此方法发送信息。

### 3.2 从别的插件获取信息

当插件发生依赖时，往往是因为我们想获得其它插件的成员，甚至对其进行操作。

获取信息过程应当发生在 `setup`  时。使用 `require_info` 来获取别的插件的成员。例如 `Replier` 插件想要获取 `Database` 插件的数据库，其 `setup` 中的语句如下：

```python
self.database = bot.require_info(plugin_name="Database", member_name="database")
```

### 3.3 检查权限

所有插件都可以调用 `self.check_privilege(sender: User)` 来检查此 `sender`  是否是高权限用户。

### 3.4 消息等待

许多功能有着 “连续对话” 的需求，例如：

```
bot:  登录. 请输入账号
user: 123456
bot:  请输入密码
user: abc123
bot:  登录成功!
```

这需要插件本身有一个 “阻塞直到收到某种消息” 的功能。在 Moment 中，其通过 `wait_message` 实现，原型如下：

```python
async def wait_message(self, for_sender = None, checker = None):
```

其中，`for_sender` 参数是一个 `User` 类型，表示只等待该用户的消息；`checker` 是一个参数为 `message`，返回值为 `bool` 的函数，表示检查器。Moment 会一直阻塞直到出现满足 `for_sender` 和 `checker` 的信息，并将其返回。



## 3. 插件载入与安装

### 3.1 手动安装

我们已经提过插件本质就是一个类。因此，要安装自制的插件，只需要创建其的一个实例，然后调用

```python
bot.install(plugin) # plugin 是实例
```

即可。

### 3.2 自动载入与安装

由于插件个数往往不少，如果一个个都采取手动安装，将会出现大量的 `import` 和实例化、`bot.install` 语句。为此，Moment 提供了一个有用的工具 `AutoPluginLoader` 。

```python
class AutoPluginLoader:
    """
        preloaded_plugins: List[Plugin]
    """

    def __init__(self, plugin_dir: str):
```

其需要一个文件夹路径来初始化。它会自动收集该文件夹下所有 `*.py` 文件，提取其中的所有插件（继承 Plugin 的类），实例化它们并放入 `preloaded_plugins` 。

然后可以将 `preloaded_plugins` 放入 `YamlConfig` 的 `"preloaded_plugins"` 字段中，这样在 bot 初始化时会自动载入这些所有插件。

当然，我们要注意区分载入与安装。载入只是调用了其构造函数，但并不意味着一定安装。安装是根据配置文件 `*.yml` 中的 `plugins` 字段下的插件名决定的，Moment 会自动按配置文件此处从上到下的顺序进行安装。