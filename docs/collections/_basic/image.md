---
title: 图片服务
nav_order: 1
---

# 图片服务
本章主要简述 Moment 储存图片数据的策略。



## 1. 图片类

在 Moment 中，图片类被封装为

```python
class Picture:
    
    """
        Three storage approach:
        - pic_url: str
        - pic_bytes: bytes
        - pic_path: str
    """
```

分别为代表着云端存储的 url 链接、代表着纯数据存储的 bytes 以及代表着本地储存的 path。这三种存储方式在不同的框架上侧重不同，并且也往往并非能全部拿到。



## 2. 接受图片

一般的聊天软件，图片都以 url 的形式代表。当 Moment 的 `frontend` 接收到带图片信息时，会尝试获得其 url，并使用 `aiohttp` 下载图片数据（`pic_bytes`），而将 `pic_path` 置为空。



## 3. 存储与载入图片

此处特指数据库中的图片。在 Moment 的 json 数据库中，图片数据被单独放在 `local/img/` 下，并以递增的数字进行编号。当前最高编号数存于一个名为 `0_pic_num_file` 的文件中。

当数据库发生写回（write_back）时，才会真正将图片存到本地，也即 `local/img/` 下，这时才真正出现 `pic_path` 这一字段。

当读取数据库时，会根据其中储存的 `pic_path` 字段从本地载入 `pic_bytes` 。



### 注

`Moment` 的图片删除策略是懒惰删除，也即它只删除 json 文件中的图片索引数据，不删除 `img` 文件底下的图片。因此在长期使用时会出现一部分 “没有被任何地方引用” 的图片（可以叫**野图片**）。野图片在实际使用过程不会太多，也不影响正常使用，可以放任不管。当然，也可以使用脚本选择清理。