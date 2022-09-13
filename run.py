
import sys

from utils.log import Log
from frontend.frontend_config import CONFIG

# command line
if len(sys.argv) <= 1:
    Log.error("缺少配置文件路径.")
    print("使用方式: python3 run.py <the path of your yaml file>")
    exit(1)

yaml_path = sys.argv[1]

# support platforms
SUPPORT_PLATFORMS = ["graia-v4", "aiocqhttp"]

try:
    with open(yaml_path, 'r', encoding="utf-8") as fp:
        yaml_data = fp.read()
        
        CONFIG.init(yaml_data)

        DEFAULT_NAME = "moment"
        DEFAULT_ENV  = "unknown"

        # boring part
        if not CONFIG.is_in("name"):
            Log.warn("配置文件缺少机器人名: name, 将使用默认名: {}".format(DEFAULT_NAME))
            CONFIG.set("name", DEFAULT_NAME)
        
        if not CONFIG.is_in("env"):
            Log.warn("配置文件缺少环境名: env, 将使用默认名: {}".format(DEFAULT_ENV))
            CONFIG.set("env", DEFAULT_ENV)
        
        if not CONFIG.is_in("platform"):
            Log.error("缺少对接平台. 至少需要指定一个对接平台!")
            exit(1)
        
        if CONFIG.get("platform") not in SUPPORT_PLATFORMS:
            Log.error("未知的平台. 当前支持: {}".format(SUPPORT_PLATFORMS))
            exit(1)

        Log.info("成功加载配置文件: {}".format(yaml_path))
except Exception as e:
    Log.error("读取配置文件: {} 发生错误!".format(yaml_path))
    Log.error(e.args)
    exit(1)

# import: plugins
from plugins.help.plugin import Help_Plugin
from plugins.db.plugin import Database_Plugin
from plugins.replier.plugin import Replier_Plugin
from plugins.random.plugin import Random_Plugin
from plugins.touhou.plugin import Touhou_Plugin
from plugins.translate.plugin import Translate_Plugin
from plugins.hello.plugin import Hello_Plugin
from plugins.alarm.plugin import Alarm_Plugin
from plugins.word.plugin import Word_Plugin
from plugins.autotalk.plugin import Autotalk_Plugin
from plugins.pixiv.plugin import Pixiv_Plugin
from plugins.ps.plugin import PS_Plugin
from plugins.judge.plugin import Judge_Plugin
from plugins.browser.plugin import Browser_Plugin
from plugins.star.plugin import Star_Plugin
from plugins.sjtudoor.plugin import SJTUDoor_Plugin

CONFIG.put("prepared_plugins",
[
    Help_Plugin(), Database_Plugin(), Replier_Plugin(), Random_Plugin(),
    Touhou_Plugin(), Translate_Plugin(), Hello_Plugin(), Alarm_Plugin(),
    Word_Plugin(), Autotalk_Plugin(), Pixiv_Plugin(), PS_Plugin(), Judge_Plugin(),
    Browser_Plugin(), Star_Plugin(), SJTUDoor_Plugin()
])

if CONFIG.get("platform") == "graia-v4":
    import frontend.graia_v4.launcher
elif CONFIG.get("platform") == "aiocqhttp":
    import frontend.aiocqhttp.launcher