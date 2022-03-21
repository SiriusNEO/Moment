# Moment

新一代便携式群聊气氛机器人。



## Spec

### 可移植

机器人核心与框架部分分离，接口处使用一个 adapter 对接。

可以方便更换框架。

### 功能简单

机器人发消息只会有两种情况：

- 消息触发（Msg）
  - 管理级命令
  - 用户级命令
  - key / full
  - 回复 bot
- 主动触发（Async）
  - 开机触发
  - 时间触发
  - 随机臊皮

### 轻小的数据库

##### 信息数据库

```
(int)  (msg)   (msg)   (msg)   (str)   (str)
 id     cm    key     full     time     typ
```

##### 用户数据库

```
(int)  (int)  (str)  (msg)  (int)  (int)
id     qq     name   prof   priv   coin
```

##### 命令别名数据库

```
(int)	(str)	 (str)
id		alias	 cmd
```

### 命令

##### 管理级命令

- `panic`

  强行令此机器人停止一切响应

- `study`

  此机器人开始收集群聊数据，培养数据库。

  `study`  得到的数据，`tag` 会被打上

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

