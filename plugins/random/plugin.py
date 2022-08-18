import random

from core.plugin import *


class Random_Plugin(Plugin):

    def __init__(self):
        super().__init__(
                requirements = [], 
                info = "Random: 随机数工具",
                doc = "随机数库大全！"
            )
    
    