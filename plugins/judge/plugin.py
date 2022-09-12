from core.plugin import *
from core.bot import Bot

from plugins.judge.plugin_config import *
from plugins.judge.plugin_doc import PLUGIN_DOC

from plugins.db.basic_db import DataBase
from plugins.db.db_event import TagPair

import random

class Judge_Plugin(Plugin):

    def __init__(self):
        super().__init__(
                name = "Judge",
                requirements = ["Database"], 
                info = "锐评插件",
                doc = PLUGIN_DOC
            )

    def setup(self, bot: Bot):
        self.database = DataBase(JUDGE_DB_PATH)
        self.database.tag_type[TAG_CONTENT] = Message

        self.start_flag = False
        self.judge_time = 0
        
        super().setup(bot)

    async def handle_message(self, message: Message) -> Union[Message, List[Message], Error]:
        assert self._setup_flag

        if message.text is not None:
            if message.text == ADD_COMMAND:
                if message.quote is None:
                    return Error("找不到引用内容!", urge=self.get_name())
                self.database.new([TagPair(TAG_CONTENT, message.quote, 0)])
                self.database.write_back()
                return Message("锐评数据++")
            elif message.text == START_COMMAND:
                if self.start_flag:
                    return Message("我已经准备好了, 别再喊了")
                else:
                    self.start_flag = True
                    self.judge_time = 0
                    return Message("来")
            elif message.text == END_COMMAND:
                if not self.start_flag:
                    return Message("早就歇了")
                else:
                    self.start_flag = False
                    self.judge_time = 0
                    return Message("歇了")
        
        if message.pic is not None and self.start_flag:
            if len(self.database.storage) == 0:
                return Error("没有数据喵", urge=self.get_name())
            self.judge_time += 1
            if self.judge_time < MAX_JUDGE_TIME:
                judge_msg = random.choice(self.database.storage)[TAG_CONTENT]
                judge_msg.at = message.sender
                return judge_msg
            else:
                self.start_flag = False
                self.judge_time = 0
                return Message("歇了, 评太多了")

        return Error("命令不满足该插件")