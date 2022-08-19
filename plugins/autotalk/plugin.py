from core.plugin import *

from plugins.autotalk.plugin_config import *
from plugins.autotalk.plugin_doc import PLUGIN_DOC

from plugins.db.basic_db import DataBase
from plugins.db.db_event import TagPair

import random

import time

class Autotalk_Plugin(Plugin):

    def __init__(self):
        super().__init__(
                name = "Autotalk",
                requirements = ["Database"], 
                info = "全自动发病",
                doc = PLUGIN_DOC
            )


    def setup(self):
        self.database = DataBase(AUTOTALK_DB_PATH)
        self.database.tag_type[TAG_CONTENT] = Message
        self.next_happen_time = time.time() + Autotalk_Plugin()._get_period()
        super().setup()


    def handle_message(self, message: Message) -> Union[Error, Message]:
        assert self._setup_flag

        if message.text is not None:
            if message.text == ADD_COMMAND:
                if message.quote is None:
                    return Error("没有引用的内容!", urge=self.get_name())
                self.database.new([TagPair(TAG_CONTENT, message.quote, 0)])
                self.database.write_back()
                return Message("发病数据喜加一喵")
            elif message.text == SEND_COMMAND:
                if len(self.database.storage) == 0:
                    return Error("没有数据喵", urge=self.get_name())
                return random.choice(self.database.storage)[TAG_CONTENT]

        return Error("命令不满足该插件")
    

    async def plugin_task(self, send_method):
        while True:
            await asyncio.sleep(WAIT)

            if self.banned:
                continue
            
            if len(self.database.storage) == 0:
                continue
            
            now_time = time.localtime(time.time())
            if now_time.tm_hour >= 14 and now_time.tm_hour <= 20 and now_time.tm_sec == 0:
                happen_time = time.localtime(self.next_happen_time)
                if now_time.tm_hour == happen_time.tm_hour and now_time.tm_min == happen_time.tm_min:
                    await send_method(random.choice(self.database.storage)[TAG_CONTENT])
                self.next_happen_time += Autotalk_Plugin()._get_period()
    
    @staticmethod
    def _get_period():
        return random.gauss(60, 20) * 60