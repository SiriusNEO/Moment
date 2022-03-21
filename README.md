# Moment

新一代简单、便于部署、可移植的键值对回复（key-value）群聊机器人。

**注意：**此项目处于开发状态（而且作者可能会咕咕咕比较久），目前功能尚不完善且 API 可能发生巨大变动！



## Spec

### 可移植

机器人核心与框架部分分离，接口处使用一个 adapter 对接。

可以方便更换框架。

目前支持的框架：

- [GraiaApplication](https://github.com/GraiaProject/Application)（v4）

### 功能简单

机器人发消息只会有两种事件：

- 消息触发（Msg），由 `msg_handler` 转为 `event`
  - 管理级命令
  - 数据库命令
  - key / full
  - at_who / qt_who（群聊中有谁被 @ 了或被回复了）
- 主动触发（Async），由 `async_handler` 转为 `event`
  - 开机触发
  - 时间触发
  - 随机触发

### 轻小的数据库

由于数据规模很小，数据库统一采用 `.json` 读写，不使用任何外部数据库。

##### 信息数据库

```
(int)  (list)   (list)   (list)   (str)   (int)    (int)    (str)
 id     cm    	 key      full    time   at_who   qt_who     ps
```

##### 用户数据库

```
(int)  (int)  (str)  (msg)  (int)  (int)
id     qq     name   prof   priv   coin
```

##### 命令别名数据库

```
(int)	(str)	 (str)
id		alias	  cmd
```

### 命令

##### 管理级命令

- `panic`

  强行令此机器人停止一切响应


##### 数据库核心命令

通用格式：

```
[index] modify
```

关键字：

```
%this: 表示此值为其引用的这句话
tag_name: 表示对应的 tag 名字

del: 删除
clr: 清空, 重置成空数据条
```

一个示例：

```
[key=test1] key=test2
```

表示访问信息数据库，把所有 `key=test1` 的信息的 `key` 修改成 `test2`

## Thanks

感谢这些项目，没有它们就没有 Moment。

- [mirai](https://github.com/mamoe/mirai) 高效率 QQ 机器人支持库
- [GraiaApplication](https://github.com/GraiaProject/Application)  基于 mirai-api-http 的 Python 框架