from plugins.db.basic_db import DataBase
from plugins.replier.plugin_config import *
from plugins.db.db_event import TagPair

from model.plugin import *

import random

class Replier_Plugin(Plugin):

    def __init__(self):
        super().__init__(
                requirements = ["Database_Plugin"], 
                info = "Replier: 键值对回复器",
                doc = "给指定信息设定值 key (关键词回复), full (完全匹配回复), 回复内容为 cm"
            )

    def setup(self, database: DataBase):
        database.tag_type[TAG_KEY] = list
        database.tag_type[TAG_FULL] = list
        database.tag_type[TAG_CM] = list

        self.database = database

    def handle_message(self, message: Message) -> Union[Error, Message]:
        key_tp = TagPair(TAG_KEY, message, 1)
        full_tp = TagPair(TAG_FULL, message, 0)
        
        key_ret, _ = self.database.query([key_tp])

        full_ret, _ = self.database.query([full_tp])
        
        reply = Message()

        if not isinstance(key_ret, Error) and len(key_ret) > 0:
            for ret_line in key_ret:
                if TAG_CM in ret_line:
                    assert type(ret_line[TAG_CM]) == list
                    return random.choice(ret_line[TAG_CM])

        if not isinstance(full_ret, Error) and len(full_ret) > 0:
            for ret_line in full_ret:
                if TAG_CM in ret_line:
                    assert type(ret_line[TAG_CM]) == list
                    return random.choice(ret_line[TAG_CM])
        
        return Error("没有满足条件的回复")