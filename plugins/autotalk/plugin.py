from core.plugin import *
from core.bot import Bot

from plugins.autotalk.plugin_config import *
from plugins.autotalk.plugin_doc import PLUGIN_DOC

from plugins.db.basic_db import DataBase
from plugins.db.db_event import TagPair

from utils.log import Log

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


    def setup(self, bot: Bot):
        self.database = DataBase(AUTOTALK_DB_PATH)
        self.database.tag_type[TAG_CONTENT] = Message
        self.next_happen_time = Autotalk_Plugin()._get_next()
        super().setup(bot)

    @check_setup
    async def handle_message(self, message: Message) -> Union[Message, List[Message], Error]:
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
    
    @check_setup
    async def plugin_task(self):
        while True:
            await asyncio.sleep(60)

            if self.banned:
                continue
            
            Log.info("{} Working. time: ".format(self.get_name()), time.localtime(self.next_happen_time))
            
            if len(self.database.storage) == 0:
                continue
            
            now_time = time.time()
            now_time_local = time.localtime(now_time)

            if now_time_local.tm_hour == 12 and now_time_local.tm_min == 0:
                # 启动时间, roll 一次
                self.next_happen_time = Autotalk_Plugin()._get_next()
            if now_time_local.tm_hour >= 12 and now_time_local.tm_hour <= 24:
                if self.next_happen_time <= now_time:
                    try:
                        await self.send(random.choice(self.database.storage)[TAG_CONTENT])
                    except:
                        pass
                    self.next_happen_time = Autotalk_Plugin()._get_next()
    
    @staticmethod
    def _get_next():
        return time.time() + max(int(random.gauss(30, 5)), 1) * 60