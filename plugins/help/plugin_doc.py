from plugins.help.plugin_config import *

PLUGIN_DOC = """帮助插件. 显示所有已安装的插件以及它们的文档.

命令:
    - {} (显示所有已安装的插件)
    - {} n/<插件名> (显示某个插件的帮助文档)
    - {} n/<插件名> (ban某个插件)
    - {} n/<插件名> (unban某个插件)

注: 后两个命令需要权限. 
""".format(HELP_COMMAND, HELP_COMMAND, BAN_COMMAND, UNBAN_COMMAND)