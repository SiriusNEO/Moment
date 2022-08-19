from plugins.ps.plugin import *

PLUGIN_DOC = """图片处理插件. 可以对图片做一些简单变换.

命令:
    - {} <变换> (进行对应变换)

目前支持的变换有:
    - 转n       (0 <= n < 360)
    - {}
    - {}
    - {}""".format(PS_COMMAND, ARG_BW, ARG_LR, ARG_UD)