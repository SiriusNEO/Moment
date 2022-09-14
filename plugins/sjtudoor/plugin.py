from core.plugin import *
from core.bot import Bot

from plugins.sjtudoor.plugin_config import *
from plugins.sjtudoor.plugin_doc import PLUGIN_DOC

from utils.log import Log

import os
import sys
import time

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

        self.jLock_path = os.path.dirname(__file__) + "/jLock/"

        if not os.path.exists(self.jLock_path):
            Log.info(self.jLock_path)
            raise Exception("开门插件缺少放于同目录下的工具: jLock. 获取: https://github.com/cmd2001/jLock")

        super().setup(bot)

        self.last_refresh_time = time.time()
        self.cur_cwd = os.getcwd()


    async def handle_message(self, message: Message) -> Union[Message, List[Message], Error]:
        assert self._setup_flag

        if message.text is not None:
            if message.text in OPENDOOR_WORDS:
                
                if message.sender.uid not in DORMITORY_MEMBERS_MAP:
                    opener = "宿舍外人员{}".format(message.sender.name)
                else:
                    opener = DORMITORY_MEMBERS_MAP[message.sender.uid]
                
                await self.send("正在尝试开门, 别急喵")

                
                try:
                    os.system(UNSET_PROXIES)
                    self.change_cwd()
                    exit_code = os.system("python3 src/entrypoints/unlock.py")
                    self.restore_cwd()
                    if exit_code != 0:
                        raise Exception("")
                except:
                    return Message("开门失败")
                else:
                    return Message("由{}成功开门, 预计{}秒后关门".format(opener, CLOSE_DOOR_TIME))

        return Error("命令不满足该插件")
    

    async def plugin_task(self):
        assert self._setup_flag

        while True:
            await asyncio.sleep(WAIT)

            # session expire
            now_time = time.time()
            if now_time - self.last_refresh_time > EXPIRE_TIME:
                self.last_refresh_time = now_time
                # await self.send("session 过期 (有效时间{}秒), 尝试刷新".format(EXPIRE_TIME))
                try:
                    os.system(UNSET_PROXIES)
                    self.change_cwd()
                    exit_code = os.system("python3 src/entrypoints/refresh_session.py")
                    self.restore_cwd()
                    if exit_code != 0:
                        raise Exception("")
                except:
                    # await self.send("刷新失败!")
                    pass
                else:
                    # await self.send("刷新成功!")
                    pass
    

    def change_cwd(self):
        os.chdir(self.jLock_path)
    
    
    def restore_cwd(self):
        os.chdir(self.cur_cwd)
        