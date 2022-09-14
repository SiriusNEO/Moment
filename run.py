
import sys

from utils.log import Log
from frontend.frontend_config import CONFIG
from frontend.auto_plugin_loader import AutoPluginLoader

# command line
if len(sys.argv) <= 1:
    Log.error("缺少配置文件路径.")
    print("使用方式: python3 run.py <the path of your yaml file>")
    raise Exception("error in command line")

yaml_path = sys.argv[1]

CONFIG.init(yaml_path)

loader = AutoPluginLoader("plugins")

CONFIG.put("preloaded_plugins", loader.preloaded_plugins)

if CONFIG.get("platform") == "graia-v4":
    import frontend.graia_v4.launcher
elif CONFIG.get("platform") == "aiocqhttp":
    import frontend.aiocqhttp.launcher