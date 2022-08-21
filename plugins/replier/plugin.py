from plugins.db.basic_db import DataBase
from plugins.replier.plugin_config import *
from plugins.replier.plugin_doc import PLUGIN_DOC
from plugins.db.db_event import TagPair

from core.plugin import *

from plugins.db.plugin_config import *

import time

class Replier_Plugin(Plugin):

    def __init__(self):
        super().__init__(
                name = "Replier",
                requirements = ["Database"], 
                info = "键值对回复器",
                doc = PLUGIN_DOC
            )

    def setup(self, database: DataBase):
        database.tag_type[TAG_KEY] = list
        database.tag_type[TAG_FULL] = list
        database.tag_type[TAG_CM] = list
        self.database = database
        self.next_available_time = time.time()
        super().setup()

    def handle_message(self, message: Message) -> Union[Message, List[Message], Error]:
        assert self._setup_flag

        reply = Message()

        # replier command
        if message.text is not None:
            cmd_args = message.text.split(" ")

            if cmd_args[0] in OLD_CM_COMMAND:
                if len(cmd_args) < 2 or len(cmd_args) > 3:
                    return Error("命令参数个数错误", urge=self.get_name())
                
                # cm del
                if cmd_args[1] == OLD_DEL_COMMAND:
                    if len(cmd_args) != 3:
                        return Error("命令参数个数错误", urge=self.get_name())
                    key_tp = TagPair(TAG_KEY, Message(cmd_args[2]), 0)
                    full_tp = TagPair(TAG_FULL, Message(cmd_args[2]), 0)
                    self.database.modify([key_tp], [], WORD_DEL)
                    self.database.modify([full_tp], [], WORD_DEL)
                    self.database.write_back()
                    reply.text = "删除成功!"
                    return reply
                else:
                    if len(cmd_args) == 3:
                        if cmd_args[2] not in [TAG_KEY, TAG_FULL]:
                            return Error("属性只能是key或者full", urge=self.get_name())
                        tag = cmd_args[2]
                    else:
                        tag = TAG_FULL
                    
                    if message.quote is None:
                        return Error("无引用内容!", urge=self.get_name())
                    else:
                        error = self.database.new([TagPair(tag, Message(cmd_args[1]), 0), TagPair(TAG_CM, message.quote, 0)])
                        if isinstance(error, Error):
                            return error
                        self.database.write_back()
                        reply.text = "添加成功!"
                        return reply
        
        if time.time() < self.next_available_time:
            return Error("不应期")

        # reply
        key_tp = TagPair(TAG_KEY, message, 4)
        full_tp = TagPair(TAG_FULL, message, 0)
        
        key_ret, _ = self.database.query([key_tp])

        full_ret, _ = self.database.query([full_tp])

        if not isinstance(key_ret, Error) and len(key_ret) > 0:
            for ret_line in key_ret:
                if TAG_CM in ret_line:
                    assert type(ret_line[TAG_CM]) == list
                    self.next_available_time = self._get_next()
                    return ret_line[TAG_CM]

        if not isinstance(full_ret, Error) and len(full_ret) > 0:
            for ret_line in full_ret:
                if TAG_CM in ret_line:
                    assert type(ret_line[TAG_CM]) == list
                    self.next_available_time = self._get_next()
                    return ret_line[TAG_CM]
        
        return Error("没有满足条件的回复")

    
    @staticmethod
    def _get_next():
        return time.time() + 10