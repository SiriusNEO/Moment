from plugins.db.basic_db import DataBase
from plugins.replier.plugin_config import *
from plugins.replier.plugin_doc import PLUGIN_DOC
from plugins.replier.template_render import *

from plugins.db.db_event import TagPair

from core.plugin import *
from core.bot import Bot

from plugins.db.plugin_config import *

from utils.log import Log

import time
import random


class Replier_Plugin(Plugin):

    def __init__(self):
        super().__init__(
                name = "Replier",
                requirements = ["Database"], 
                info = "键值对回复器",
                doc = PLUGIN_DOC
            )

    def setup(self, bot: Bot):
        self.database = bot.require_info(plugin_name="Database", member_name="cur_database")

        self.database.tag_type[TAG_KEY] = list
        self.database.tag_type[TAG_FULL] = list
        self.database.tag_type[TAG_CM] = list
        self.database.tag_type[TAG_ARGMAP] = dict
        self.database.tag_type[TAG_POOL] = Message
        self.database.tag_type[TAG_ACTIVE] = int

        self._timelock_dict = {}
        
        super().setup(bot)
    
    # this will do some replace...
    def pool_pass(self, message_list: list):
        ret = []

        for message in message_list:
            new_msg = message.copy()
            
            if new_msg.text is not None:
                modify_flag = True

                while modify_flag:
                    last_left_pos = -1
                    modify_flag = False

                    for i in range(len(new_msg.text)):
                        if new_msg.text[i] == POOL_BRACKET[0]:
                            last_left_pos = i
                        elif new_msg.text[i] == POOL_BRACKET[1] and last_left_pos != -1:
                            pool_name = new_msg.text[last_left_pos+1:i]
                            pool_ret, _ = self.database.query([TagPair(TAG_POOL, Message(pool_name), 0)])

                            pool_replace = ""
                            random.seed()
                            if len(pool_ret) > 0:
                                chosen_line = random.choice(pool_ret)
                                if TAG_CM in chosen_line and len(chosen_line[TAG_CM]) > 0:
                                    chosen_msg = random.choice(chosen_line[TAG_CM])
                                    if chosen_msg.text is not None:
                                        pool_replace = chosen_msg.text

                            new_msg.text = new_msg.text.replace(POOL_BRACKET[0] + pool_name + POOL_BRACKET[1], pool_replace, 1)
                            modify_flag = True
                            break
            ret.append(new_msg)
        
        return ret

    @check_setup
    async def handle_message(self, message: Message) -> Union[Message, List[Message], Error]:
        # template detect
        template_detect = message.text is not None and message.text.find(TEMPLATE_BRACKET[0]) != -1
        if template_detect:
            argmap = {}
        

        # replier command
        if message.text is not None:
            if message.text == REFLESH_COMMAND:
                self._timelock_dict = {}
                return Message("不应期清除！")

            cmd_args = message.text.split(" ")

            if cmd_args[0] == SEARCH_COMMAND:
                if len(cmd_args) != 2:
                    return Error("命令参数个数错误", urge=self.get_name())
                
                key_ret, key_id = self.database.query([TagPair(TAG_KEY, Message(cmd_args[1]), 1)])
                full_ret, full_id = self.database.query([TagPair(TAG_FULL, Message(cmd_args[1]), 1)])
                
                result = []
                result_id = []

                if not isinstance(key_ret, Error):
                    result += key_ret
                    result_id += key_id
                if not isinstance(full_ret, Error):
                    result += full_ret
                    result_id += full_id

                reply = Message("key/full查询: ")
                if len(result) == 0:
                    reply.text += "很遗憾, 查询结果为空"
                else:
                    reply.text += "共有 {0} 条数据:\n".format(len(result))
                    # copy from database plugin
                    for i in range(len(result)):
                        if len(result) == 1:
                            reply.text += self.database.display_line(result[i], result_id[i], False)
                        else:
                            reply.text += self.database.display_line(result[i], result_id[i])
                        if i < len(result)-1:
                            reply.text += "\n"
                return reply

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
                    return Message("删除成功!")
                else:
                    if len(cmd_args) == 3:
                        if cmd_args[2] not in [TAG_KEY, TAG_FULL]:
                            # return Error("属性只能是key或者full", urge=self.get_name())
                            error = self.database.new([TagPair(TAG_FULL, Message(cmd_args[1]), 0), TagPair(TAG_CM, Message(cmd_args[2]), 0)])
                            if isinstance(error, Error):
                                return error
                            return Message("添加成功!")
                        tag = cmd_args[2]
                    else:
                        tag = TAG_FULL
                    
                    if message.quote is None:
                        # return Error("无引用内容!", urge=self.get_name())
                        key_result, _ = self.database.query([TagPair(TAG_KEY, Message(cmd_args[1]), 0)])
                        full_result, _ = self.database.query([TagPair(TAG_FULL, Message(cmd_args[1]), 0)])
                        if not isinstance(key_result, Error) and len(key_result) > 0:
                            return key_result[0][TAG_CM]
                        elif not isinstance(full_result, Error) and len(full_result) > 0:
                            return full_result[0][TAG_CM]
                    else:
                        if template_detect:
                            if tag == TAG_KEY:
                                return Error("模板不可以存成key类型", urge=self.get_name())
                            template = extract_argmap(cmd_args[1], argmap)
                            if isinstance(template, Error):
                                return Error(template.what, urge=self.get_name())
                            error = self.database.new([TagPair(TAG_FULL, Message(template), 0), TagPair(TAG_CM, message.quote, 0), TagPair(TAG_ARGMAP, argmap, 0)])
                        else:
                            error = self.database.new([TagPair(tag, Message(cmd_args[1]), 0), TagPair(TAG_CM, message.quote, 0)])
                        
                        if isinstance(error, Error):
                            return error
                        
                        return Message("添加成功!")
                        
        # reply
        key_tp = TagPair(TAG_KEY, message, 4)
        full_tp = TagPair(TAG_FULL, message, 0)
        
        key_ret, key_ret_id = self.database.query([key_tp])

        full_ret, full_ret_id = self.database.query([full_tp])

        if not isinstance(key_ret, Error) and len(key_ret) > 0:
            ret_line = random.choice(key_ret)
            if TAG_CM in ret_line:
                hash_key = key_ret_id[key_ret.index(ret_line)]
                if hash_key in self._timelock_dict:
                    if self._timelock_dict[hash_key] <= time.time():
                        self._timelock_dict.pop(hash_key)
                    else:
                        return Error("不应期")

                assert type(ret_line[TAG_CM]) == list
                if not TAG_ACTIVE in ret_line:
                    self._timelock_dict[hash_key] = self._get_next()
                return self.pool_pass(ret_line[TAG_CM])
            else:
                return Error("回复中无cm词条")

        if not isinstance(full_ret, Error) and len(full_ret) > 0:
            ret_line =  random.choice(full_ret)
            if TAG_CM in ret_line:
                hash_key = full_ret_id[full_ret.index(ret_line)]
                # Log.info(hash_key)
                if hash_key in self._timelock_dict:
                    if self._timelock_dict[hash_key] <= time.time():
                        self._timelock_dict.pop(hash_key)
                    else:
                        return Error("不应期")
                
                assert type(ret_line[TAG_CM]) == list
                if not TAG_ACTIVE in ret_line:
                    self._timelock_dict[hash_key] = self._get_next()
                return self.pool_pass(ret_line[TAG_CM])
            else:
                return Error("回复中无cm词条")

        # 模板
        for line in self.database.storage:
            if TAG_ARGMAP in line and TAG_FULL in line and TAG_CM in line:
                for full_msg in line[TAG_FULL]:
                    if full_msg.text is not None and template_match(message.text, full_msg.text):
                        collected_map = collect(message.text, full_msg.text, line[TAG_ARGMAP])
                        # Log.info(collected_map)
                        if isinstance(collected_map, Error):
                            return Error(collected_map.what, urge=self.get_name())

                        ret = self.pool_pass(line[TAG_CM])

                        for every in ret:
                            if every.text is not None:
                                every.text = render(every.text, collected_map)
                        
                        return ret
        
        return Error("没有满足条件的回复")

    
    @staticmethod
    def _get_next():
        # 10 min
        return time.time() + 10 * 60