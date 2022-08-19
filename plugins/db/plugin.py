from plugins.db.plugin_config import *
from plugins.db.basic_db import DataBase
from plugins.db.db_cmd_parser import database_cmd_parse
from plugins.db.db_event import *
from plugins.db.plugin_doc import PLUGIN_DOC

from core.error import Error

from core.plugin import *

class Database_Plugin(Plugin):

    def __init__(self):
        super().__init__(
                name = "Database",
                requirements = [], 
                info = "强大的信息数据库.",
                doc = PLUGIN_DOC
            )


    def setup(self):
        self.database = DataBase(CM_PATH)
        self.database.tag_type["id"] = int
        super().setup()


    def handle_message(self, message: Message) -> Union[Message, List[Message], Error]:
        assert self._setup_flag

        if message.text == COMMIT_COMMAND or message.text == BACKUP_COMMAND:
            if message.sender not in self.roots:
                return Error("权限不够", urge=self.get_name())

        event = database_cmd_parse(message)

        if event is None:
            return Error("parse failed.")

        reply = Message()

        # 信息包装
        if hasattr(event, 'indices'):
            for index in event.indices:
                if index.tag not in self.database.tag_type:
                    return Error("标签不存在: {}".format(index.tag))
                error = self._val_resolve(index, event)
                if error != None:
                    return error
        
        if hasattr(event, 'modifies'):
            for modify in event.modifies:
                if modify.tag not in self.database.tag_type:
                    return Error("标签不存在: {}".format(modify.tag))
                error = self._val_resolve(modify, event)
                if error != None:
                    return error
        # 0 query
        if isinstance(event, QueryEvent):
            result, result_id = self.database.query(event.indices, target_tag=event.target_tag)
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
                        reply.text += self._display_line(result[i], result_id[i])
                        if i < len(result)-1:
                            reply.text += "\n"
                else:
                    reply.text = "共有 {0} 条数据:\n".format(len(result))
                    for i in range(len(result)):
                        # to do: 更好的显示方式
                        reply.text += self._display_line(result[i], result_id[i])
                        if i < len(result)-1:
                            reply.text += "\n"
        # 1 modify
        elif isinstance(event, ModifyEvent):
            result = self.database.modify(event.indices, event.modifies, event.word, target_tag=event.target_tag)
            if isinstance(result, Error):
                return Error(result.what, urge=self.get_name())
            else:
                reply.text = "修改成功!"
        # 2 new
        elif isinstance(event, NewEvent):
            result = self.database.new(event.modifies)
            if isinstance(result, Error):
                return Error(result.what, urge=self.get_name())
            else:
                reply.text = "添加成功!"
        # 3 commit
        elif isinstance(event, CommitEvent):
            self.database.write_back()
            reply.text = "写回成功!"
        # 4 backup
        elif isinstance(event, BackupEvent):
            self.database.write_back(BACKUP_PATH)
            reply.text = "备份成功!"
        else:
            return Error("未知数据库事件类型")

        return reply

    """
        info_cut: 过长信息截断，用 ... 代替
    """
    @staticmethod
    def _info_cut(text: str):
        if len(text) > MAX_INFO_LEN:
            return text[0:MAX_INFO_LEN] + "..."
        return text

    """
        display_line: 显示数据库中的一行 (line)
    """
    def _display_line(self, line: dict, id: int):
        ret = "{0}: ".format(id)
        if not line:
            # 空数据条目
            return ret + "空数据"

        for tag in line:
            if tag == SHADOW_CODE:
                continue
            if self.database.tag_type[tag] == list:
                ret += "{0}=".format(tag)

                if len(line[tag]) != 1:
                    ret += "["
                
                for val in line[tag]:
                    # 一定是 msg
                    ret += val.msg_2_str() + ", "
                
                if len(line[tag]) > 0:
                    ret = ret[0: len(ret)-2]

                if len(line[tag]) != 1:
                    ret += "]"
            else:
                ret += "{0}={1}".format(tag, info_cut(str(line[tag])))
            ret += "; "
        return ret

    """
        val_resolve: 解析 tag_pair 的 val 并赋予真实值
        真实值只能是 Message, int, float 三种类型之一
    """
    def _val_resolve(self, tag_pair: TagPair, event: BaseDatabaseEvent):
        if self.database.tag_type[tag_pair.tag] == list:
            if tag_pair.val == THIS:
                if event.quote is None:
                    return Error("无引用的内容！")
                tag_pair.val = event.quote
            else:
                text = tag_pair.val
                tag_pair.val = Message(text)
        elif self.database.tag_type[tag_pair.tag] == int:
            if not str.isdigit(tag_pair.val):
                return Error("{0} 应该是个整数！".format(tag_pair.tag))
            tag_pair.val = int(tag_pair.val)
        elif self.database.tag_type[tag_pair.tag] == float:
            if not is_float(tag_pair.val):
                return Error("{0} 应该是个浮点数！".format(tag_pair.tag))
            tag_pair.val = float(tag_pair.val)

    """
        display the database
    """
    def display():
        self.database.display()