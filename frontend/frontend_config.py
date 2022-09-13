SEND_WAIT = 1
TIMEOUT = 60

"""
    pass global yaml config
"""
import yaml

class YamlConfig:
    """
        yaml_dict: dict
    """

    def __init__(self):
        self.yaml_dict = {}


    def init(self, init_data):
        self.yaml_dict = yaml.load(init_data, Loader=yaml.FullLoader)


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