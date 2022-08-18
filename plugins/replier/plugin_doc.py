from plugins.replier.plugin_config import *

PLUGIN_DOC = """键值回复插件要求数据库中的信息拥有 key 或者 full 属性以及 cm 属性.

其中:
- key 用于关键词回复, 即说话内容包含key则触发
- full 完全匹配, 即说话内容等于full则触发
- cm 匹配后的回复内容
注意数据库中这三个tag都是list类型:
- 多个key/full需要每个都匹配才算匹配成功
- 多个cm会挑选一个回复

兼容老命令:
    - {} <关键词> <属性> (属性可设key/full, 默认为full. 必须有引用内容)
    - {} {} <关键词> (删掉key与full为这个的数据条目)
""".format(OLD_CM_COMMAND, OLD_CM_COMMAND, OLD_DEL_COMMAND)