from plugins.star.plugin_config import *

PLUGIN_DOC = """精选评论插件. 为一些评论设精, 并制作精美的展示框.

设精方法:
    使用数据库命令为数据添加 {} 字段.
    字段格式为: <作者名> + 左圆英文括号 + <时间> + 右圆英文括号

命令:
    - {} <作者名> <日期> (将引用设成精评. 日期可忽略, 默认使用当前日期.)
    - {} <数据编号> (将数据库中的某一条数据制作为精选评论样式并展示.)
    - {} <作者名> (引用某个图片. 将此图片作为该作者的头像.)""".format(TAG_STAR, TAG_STAR, MAKESTAR_COMMAND, AVATAR_COMMAND)