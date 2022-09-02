from plugins.touhou.plugin_config import *

PLUGIN_DOC = """东方插件. 抽东方人物/符卡.

命令:
    - {} <作品名> <个数> (抽若干个人物. 个数和作品名可省略)
    - {} <人物名> <个数> (抽若干符卡. 个数和符卡名可省略)
    - <作品名>{} (列出该作品所有人物)
    - <人物名>{} (列出该人物所有符卡)

注: 个数默认1个, 最多10个.""".format(RO_COMMAND, SC_COMMAND, LS_RO, LS_SC)