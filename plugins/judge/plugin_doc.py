from plugins.judge.plugin_config import *

PLUGIN_DOC = """锐评插件. 会对一段时间发出的图片进行锐评.

命令:
    - {} (需要引用消息. 把引用的消息加入锐评语录)
    - {} (开始锐评. 会对接下来所有的图片进行评论.)
    - {} (结束锐评. 当评太多后也会自己结束.)""".format(ADD_COMMAND, START_COMMAND, END_COMMAND)