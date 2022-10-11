from plugins.replier.plugin_config import *

PLUGIN_DOC = """键值回复插件要求数据库中的信息拥有 key 或者 full 属性以及 cm 属性.

其中:
- key 用于关键词回复, 即说话内容包含key则触发
- full 完全匹配, 即说话内容等于full则触发
- cm 匹配后的回复内容
注意数据库中这三个tag都是list类型:
- 多个key/full需要每个都匹配才算匹配成功
- 多个cm会一起发回去

兼容命令:
    - {} <关键词> (无引用内容. 表示直接触发一个key或者full)
    - {} <关键词> <值> (直接添加一个full为关键词, cm为值的条目)
    - {} <关键词> <属性> (属性可设key/full, 默认为full. 必须有引用内容. 相当于key=关键词 cm=%this)
    - {} {} <关键词> (删掉key与full为这个的数据条目)
    - {} <关键词> (搜索key或者full为这个的数据条目)
    
魔法:
    - 不应期机制. 为了和谐的群环境, 每次回复成功会冷静一段时间. 使用 {} 来清除不应期. 使用 {} 标签 (随便赋一个int) 来使此词条无不应期.
    - pool 机制. 暂略.
    - template 机制. 暂略.""".format(OLD_CM_COMMAND, OLD_CM_COMMAND, OLD_CM_COMMAND, OLD_CM_COMMAND, OLD_DEL_COMMAND, SEARCH_COMMAND, REFLESH_COMMAND, TAG_ACTIVE)