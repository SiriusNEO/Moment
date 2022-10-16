from plugins.alarm.plugin_doc import PLUGIN_DOC
from plugins.alarm.plugin_config import *

from core.plugin import *
from core.bot import Bot

from plugins.db.db_event import TagPair
from plugins.db.plugin_config import WORD_DEL

from utils.log import Log

import time
import random

class Alarm_Plugin(Plugin):

    def __init__(self):
        super().__init__(
                name = "Alarm",
                requirements = ["Database"], 
                info = "闹钟插件",
                doc = PLUGIN_DOC
            )
    

    def setup(self, bot: Bot):
        self.database = bot.invoke_method("Database", "register_database", "alarm", ALARM_DB_PATH)
        self.database.tag_type[TAG_AL] = Message
        self.database.tag_type[TAG_CONTENT] = Message
        super().setup(bot)


    @check_setup
    async def handle_message(self, message: Message) -> Union[Message, List[Message], Error]:
        reply = Message()

        if message.text is not None:
            if message.text == LS_ALARM:
                reply.text = "当前闹钟, 共有 {} 个：".format(len(self.database.storage))
                for line in self.database.storage:
                    reply.text += "\n" + line[TAG_AL].text + "\t" + line[TAG_CONTENT].to_readable_str()
                return reply
            
            cmd_args = message.text.split(" ")
            if cmd_args[0] == SET_ALARM or cmd_args[0] == DEL_ALARM:
                if len(cmd_args) != 2:
                    return Error("参数个数错误!", urge=self.get_name())
                try:
                    alarm_time = time.strptime(cmd_args[1], TIME_FORMAT)
                except:
                    return Error("时间格式错误!", urge=self.get_name())
                else:
                    alarm_time_str = TIME_FORMAT.replace("%H", str(alarm_time.tm_hour)).replace("%M", str(alarm_time.tm_min))
                    if cmd_args[0] == SET_ALARM:
                        if message.quote is None:
                            return Error("无引用内容!", urge=self.get_name())
                        error = self.database.new([TagPair(TAG_AL, Message(alarm_time_str), 0), TagPair(TAG_CONTENT, message.quote, 0)])
                        if isinstance(error, Error):
                            return error
                        self.database.write_back()
                        reply.text = "闹钟添加成功!"
                        return reply
                    elif cmd_args[0] == DEL_ALARM:
                        error = self.database.modify([TagPair(TAG_AL, Message(alarm_time_str), 0)], [], WORD_DEL)
                        if isinstance(error, Error):
                            return error
                        self.database.write_back()
                        reply.text = "闹钟删除成功!"
                        return reply

        return Error("命令格式不符此插件!")
    
    @check_setup
    async def plugin_task(self):
        async for _ in Ticker(self, 1):    
            # Log.info("{} Working".format(self.get_name()))
            
            now_time = time.localtime(time.time())
            if now_time.tm_sec == 0:
                query_key = TIME_FORMAT.replace("%H", str(now_time.tm_hour)).replace("%M", str(now_time.tm_min))
                lines, _ = self.database.query([TagPair(TAG_AL, Message(query_key), 0)])
                
                if isinstance(lines, list) and len(lines) > 0:
                    report_line = random.choice(lines)
                    await self.send(report_line[TAG_CONTENT])


