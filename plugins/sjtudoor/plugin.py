from core.plugin import *
from core.bot import Bot

from plugins.sjtudoor.plugin_config import *
from plugins.sjtudoor.plugin_doc import PLUGIN_DOC

from utils.log import Log

import os

IMPORT_FLAG = True
try:
    import pysjtu
except:
    IMPORT_FLAG = False

class SJTUDoor_Plugin(Plugin):

    def __init__(self):
        super().__init__(
                name = "SJTUDoor",
                requirements = [], 
                info = "帮你自动开门",
                doc = PLUGIN_DOC
            )
    
    def setup(self, bot: Bot):
        if not IMPORT_FLAG:
            raise Exception("开门插件缺少关键库: pysjtu")

        self.jLock_mainfile_path = os.path.dirname(__file__) + "/jLock/main.py"

        if not os.path.exists(self.jLock_mainfile_path):
            Log.info(self.jLock_mainfile_path)
            raise Exception("开门插件缺少放于同目录下的工具: jLock. 获取: https://github.com/cmd2001/jLock")

        super().setup(bot)

    async def handle_message(self, message: Message) -> Union[Message, List[Message], Error]:
        assert self._setup_flag

        if message.text is not None:
            if message.text in OPENDOOR_WORDS:
                ret_code = os.system("python3 {}".format(self.jLock_mainfile_path))
                if ret_code == 0:
                    return Message("开门成功!")
                else:
                    return Error("开门失败QAQ", urge=self.get_name())

        return Error("命令不满足该插件")