from plugins.db.plugin_config import *
from plugins.db.basic_db import DataBase
from plugins.db.db_cmd_parser import database_cmd_parse
from plugins.db.db_event import *
from plugins.db.plugin_doc import PLUGIN_DOC

from core.error import Error
from core.user import User
from core.plugin import *
from core.bot import Bot

import time
from utils.log import Log

class Database_Plugin(Plugin):

    def __init__(self):
        super().__init__(
                name = "Database",
                requirements = [], 
                info = "强大的信息数据库.",
                doc = PLUGIN_DOC
            )


    def setup(self, bot: Bot):
        # 记录所有数据库, 方便切换
        self.database_table = dict()

        # 默认数据库: cm数据库
        # self.cur_database = DataBase(CM_PATH)
        self.cur_database = self.register_database("comment", CM_PATH)
        self.cur_database.tag_type["info"] = Message

        super().setup(bot)

        # 实现 record
        # TODO: 其实可以用 wait_message 实现
        self.record_flag = False
        self.record_list = []

    """
        register a database (internal usage or external plugins)
    """
    def register_database(self, database_name, database_path):
        database = DataBase(database_path)
        # table: name, path, db
        if database_name in self.database_table:
            raise Exception("register database error: 数据库名 {} 已被注册".format(database_name))
        self.database_table[database_name] = database
        return database

    
    @check_setup
    async def handle_message(self, message: Message) -> Union[Message, List[Message], Error]:
        if message.text == RECORD_COMMAND:
            if self.record_flag:
                self.record_flag = False
                return Message("接收到第二次命令, Moment 已放弃记录")
            else:
                self.record_flag = True    
                self.record_list = []
                return Message("得得")
        
        if message.text == SHOWDB_COMMAND:
            reply = Message("当前所有插件共注册{}个数据库: \n".format(len(self.database_table)))
            database_id = 0
            for db_name in self.database_table:
                now_db = self.database_table[db_name]
                reply.text += "{}: {}  ({})".format(database_id, db_name, now_db.path)
                if now_db == self.cur_database:
                    reply.text += " (*now)"
                if database_id != len(self.database_table)-1:
                    reply.text += "\n"
                database_id += 1
            return reply

        if message.text == COMMIT_COMMAND or message.text == BACKUP_COMMAND or message.text == RELOAD_COMMAND or message.text == ROLLBACK_COMMAND:
            if not self.check_privilege(message.sender):
                return Error("权限不够", urge=self.get_name())

        cmd_args = message.text.split(" ")
        if cmd_args[0] == USEDB_COMMAND:
            if len(cmd_args) != 2:
                return Error("参数个数错误")
            if str.isdigit(cmd_args[1]) and 0 <= int(cmd_args[1]) < len(self.database_table):
                db_name, self.cur_database = list(self.database_table.items())[int(cmd_args[1])]
                return Message("数据库切换为: {}".format(db_name))
            if cmd_args[1] not in self.database_table:
                return Error("未知的数据库名: {}".format(cmd_args[1]), urge=self.get_name())
            self.cur_database = self.database_table[cmd_args[1]]
            return Message("数据库切换为: {}".format(cmd_args[1]))
            
        event = database_cmd_parse(message)

        if event is None:
            if self.record_flag:
                if len(self.record_list) >= RECORD_MAX_NUM:
                    self.record_list = []
                    self.record_flag = False
                    return Message(" 消息太多了, Moment 已自动放弃记录")
                
                self.record_list.append(message)
                # 正常收集, 用一个占位 Error 返回
                return Error("")
            return Error("parse failed.")

        reply = Message()

        # 信息包装
        if hasattr(event, 'indices'):
            for index in event.indices:
                if index.tag not in self.cur_database.tag_type:
                    return Error("未被允许的 tag: {}".format(index.tag), urge=self.get_name())
                error = await self._val_resolve(index, event, message.sender)
                if error != None:
                    return error
        
        if hasattr(event, 'modifies'):
            for modify in event.modifies:
                if modify.tag not in self.cur_database.tag_type:
                    return Error("未被允许的 tag: {}".format(modify.tag), urge=self.get_name())
                error = await self._val_resolve(modify, event, message.sender)
                if error != None:
                    return error
        # 0 query
        if isinstance(event, QueryEvent):
            result, result_id = self.cur_database.query(event.indices, target_tag=event.target_tag)
            if isinstance(result, Error):
                return Error(result.what, urge=self.get_name())
            elif event.target_tag is not None:
                ret = []
                if len(result) == 0:
                    return Message("很遗憾, 查询结果为空")
                if len(result) > SEND_THRESHOLD:
                    ret.append(Message("元素太多了噢, 只发前{}条噢".format(SEND_THRESHOLD)))
                    send_len = SEND_THRESHOLD
                else:
                    send_len = len(result)
                for i in range(send_len):
                    # forced: to Message
                    if not isinstance(result[i], Message):
                        ret.append(Message(str(result[i])))
                    else:
                        ret.append(result[i])
                return ret
            else:
                if len(result) == 0:
                    reply.text = "很遗憾, 查询结果为空"
                elif len(result) > QUERY_DISPLAY_THRESHOLD:
                    reply.text = "共有 {0} 条数据, 仅显示最新 {1} 条:\n".format(len(result), QUERY_DISPLAY_THRESHOLD)
                    for i in range(len(result)-QUERY_DISPLAY_THRESHOLD, len(result)):
                        reply.text += self.cur_database.display_line(result[i], result_id[i])
                        if i < len(result)-1:
                            reply.text += "\n"
                else:
                    reply.text = "共有 {0} 条数据:\n".format(len(result))
                    for i in range(len(result)):
                        # to do: 更好的显示方式
                        if len(result) == 1:
                            reply.text += self.cur_database.display_line(result[i], result_id[i], False)
                        else:
                            reply.text += self.cur_database.display_line(result[i], result_id[i])
                        if i < len(result)-1:
                            reply.text += "\n"
        # 1 modify
        elif isinstance(event, ModifyEvent):
            result = self.cur_database.modify(event.indices, event.modifies, event.word, target_tag=event.target_tag)
            if isinstance(result, Error):
                return Error(result.what, urge=self.get_name())
            else:
                reply.text = "修改成功!"
        # 2 new
        elif isinstance(event, NewEvent):
            result = self.cur_database.new(event.modifies)
            if isinstance(result, Error):
                return Error(result.what, urge=self.get_name())
            else:
                reply.text = "添加成功!"
        # 3 commit
        elif isinstance(event, CommitEvent):
            self.cur_database.write_back()
            reply.text = "数据写回成功!"
        # 4 backup
        elif isinstance(event, BackupEvent):
            self.cur_database.write_back(backup=True)
            reply.text = "数据备份成功!"
        # 5. reload
        elif isinstance(event, ReloadEvent):
            self.cur_database.load_from()
            reply.text = "数据刷新成功!"
        # 6. rollback
        elif isinstance(event, RollbackEvent):
            self.cur_database.load_from(backup=True)
            self.cur_database.write_back()
            reply.text = "数据回滚成功!"
        else:
            return Error("未知数据库事件类型")

        return reply

    @check_setup
    async def plugin_task(self):
        async for _ in Ticker(self, 60):
            now_time_local = time.localtime(time.time())

            # Log.info("{} Working".format(self.get_name()))

            # 自动保存
            if now_time_local.tm_hour in AUTO_SAVE_TIME and now_time_local.tm_min == 42:
                self.cur_database.write_back()
                await self.send("[{}]({}) 自动存档完成, 数据与云端同步.".format(self.get_name(), Log.show_time()))


    """
        val_resolve: 解析 tag_pair 的 val 并赋予真实值
        真实值只能是 Message, int, float 三种类型之一
    """
    async def _val_resolve(self, tag_pair: TagPair, event: BaseDatabaseEvent, sender: User):
        if self.cur_database.tag_type[tag_pair.tag] == list or self.cur_database.tag_type[tag_pair.tag] == Message:
            if tag_pair.val == THIS:
                if event.quote is None:
                    return Error("无引用的内容！", urge=self.get_name())
                tag_pair.val = event.quote
            elif tag_pair.val == SPLIT_THIS:
                if event.quote is None:
                    return Error("无引用的内容！", urge=self.get_name())
                tag_pair.val = []
                raw = event.quote.text
                if raw is not None:
                    raw_split = raw.split(" ")
                    for raw_split_single in raw_split:
                        tag_pair.val.append(Message(raw_split_single))

            elif tag_pair.val == ABOVE:
                if self.cur_database.tag_type[tag_pair.tag] != list:
                    return Error("字段 {} 类型不是 List[Message]".format(tag_pair.tag), urge=self.get_name())
                
                tag_pair.val = self.record_list[:]

                self.record_list = []
                self.record_flag = False
            elif tag_pair.val == NEXT:
                await self.send("请输入{}的对应信息: ".format(NEXT))
                tag_pair.val = await self.wait_message(for_sender=sender)
            else:
                text = tag_pair.val
                tag_pair.val = Message(text)
        elif self.cur_database.tag_type[tag_pair.tag] == int:
            if not str.isdigit(tag_pair.val):
                return Error("{0} 应该是个整数！".format(tag_pair.tag), urge=self.get_name())
            tag_pair.val = int(tag_pair.val)
        elif self.cur_database.tag_type[tag_pair.tag] == float:
            if not is_float(tag_pair.val):
                return Error("{0} 应该是个浮点数！".format(tag_pair.tag), urge=self.get_name())
            tag_pair.val = float(tag_pair.val)

    """
        display the database
    """
    def display():
        self.cur_database.display()