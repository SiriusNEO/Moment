from plugins.autotalk.plugin_config import *

PLUGIN_DOC = """自动发病插件. 每过一段时间发送一条发病数据库的信息.

命令:
    - {} (需要引用某个信息. 往发病数据库添加所引用的信息.)
    - {} (主动发一条)""".format(ADD_COMMAND, SEND_COMMAND)