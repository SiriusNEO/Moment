SEND_WAIT = 1

TIMEOUT = 60

# support platforms
SUPPORT_PLATFORMS = ["graia-v4", "aiocqhttp"]

DEFAULT_NAME = "moment"
DEFAULT_ENV  = "unknown"

"""
    pass global yaml config
"""
import yaml

from utils.log import Log

class YamlConfig:
    """
        yaml_dict: dict
    """

    def __init__(self):
        self.yaml_dict = {}


    def init(self, yaml_path: str):
        try:
            with open(yaml_path, 'r', encoding="utf-8") as fp:
                yaml_data = fp.read()
                
                self.yaml_dict = yaml.load(yaml_data, Loader=yaml.FullLoader)

                # boring part
                if not CONFIG.is_in("name"):
                    Log.warn("配置文件缺少机器人名: name, 将使用默认名: {}".format(DEFAULT_NAME))
                    CONFIG.set("name", DEFAULT_NAME)
                
                if not CONFIG.is_in("env"):
                    Log.warn("配置文件缺少环境名: env, 将使用默认名: {}".format(DEFAULT_ENV))
                    CONFIG.set("env", DEFAULT_ENV)
                
                if not CONFIG.is_in("platform"):
                    Log.error("缺少对接平台. 至少需要指定一个对接平台!")
                    raise Exception()
                
                if CONFIG.get("platform") not in SUPPORT_PLATFORMS:
                    Log.error("未知的平台. 当前支持: {}".format(SUPPORT_PLATFORMS))
                    raise Exception()

                Log.info("成功加载配置文件: {}".format(yaml_path))
        
        except Exception as e:
            Log.error("读取配置文件: {} 发生错误!".format(yaml_path))
            Log.error(e.args)
            raise Exception("error in yaml config")


    def is_in(self, key, prefix=None):
        if prefix is None:
            return key in self.yaml_dict
        return prefix in self.yaml_dict and key in self.yaml_dict[prefix]


    def put(self, key, value):
        self.yaml_dict[key] = value


    def get(self, key, prefix=None):
        if prefix is None:
            if key not in self.yaml_dict:
                return None
            return self.yaml_dict[key]
        else:
            if prefix not in self.yaml_dict:
                return None
            if key not in self.yaml_dict[prefix]:
                return None
            return self.yaml_dict[prefix][key]


CONFIG = YamlConfig()