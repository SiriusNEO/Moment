from plugins.pixiv.plugin import *

PLUGIN_DOC = """Pixiv 图片插件. 使用第三方API, 目前只支持来一张.

命令:
    - {} <tag> (来一张图. tag 可省略.)

API 地址: {}
为了防爆, 目前的SAN设定是: {}
""".format(FETCH_COMMAND, API_URL, SAN)