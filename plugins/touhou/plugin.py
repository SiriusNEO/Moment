import random

from core.plugin import *
from plugins.touhou.plugin_config import *
from plugins.touhou.plugin_doc import PLUGIN_DOC
from plugins.touhou.touhou_func import *

class Touhou_Plugin(Plugin):

    def __init__(self):
        super().__init__(
                name = "Touhou",
                requirements = [], 
                info = "抽车万人工具",
                doc = PLUGIN_DOC
            )


    def handle_message(self, message: Message) -> Union[Error, Message]:
        assert self._setup_flag

        if message.text is not None:
            reply = Message()

            # list part
            ls_cmd_pos = message.text.find(LS_RO)
            if ls_cmd_pos != -1:
                game_name = message.text[:ls_cmd_pos]
                role_list = list_role(game_name)
                if len(role_list) == 0:
                    return Error("未知的作品名: {}".format(game_name), urge=self.get_name())
                else:
                    reply.text = "[Moment Touhou Role] 作品 [" + game_name + "]："
                    for role in role_list:
                        reply.text += "\n" + role
                    return reply    
            
            ls_cmd_pos = message.text.find(LS_SC)
            if ls_cmd_pos != -1:
                role_name = message.text[:ls_cmd_pos]
                sc_list = list_sc(role_name)
                if len(sc_list) == 0:
                    return Error("未知的角色名: {}".format(role_name), urge=self.get_name())
                else:
                    reply.text = "[Moment Touhou Spellcard] 角色 [" + role_name + "]："
                    for sc in sc_list:
                        reply.text += "\n" + sc
                    return reply
            
            # random part
            cmd_args = message.text.split(" ")
            
            from_what = ""
            times_arg = "1"

            if len(cmd_args) > 3:
                return Error("命令参数个数不正确!")
            elif len(cmd_args) == 3:
                from_what = cmd_args[1]
                times_arg = cmd_args[2]
            elif len(cmd_args) == 2:
                if str.isdigit(cmd_args[1]):
                    times_arg = cmd_args[1]
                else:
                    from_what = cmd_args[1]
            
            if not str.isdigit(times_arg):
                return Error("抽取次数必须是正整数!")
            
            times = int(times_arg)
            if times > NUM_THRESHOLD:
                return Error("抽太多啦...", urge=self.get_name())
            
            reply.text = ""
            reply.at = message.sender 

            for i in range(times):
                if i >= 1:
                    reply.text += "\n"
                if cmd_args[0] == RO_COMMAND:
                    result = get_role(from_what)
                    if result[0] == "":
                        return Error("未知的作品名: {}".format(from_what), urge=self.get_name())
                    reply.text += "[Touhou Role] 您抽到了："
                    reply.text += "\n" + result[0]
                    reply.text += "\n来自：" + result[1]
                elif cmd_args[0] == SC_COMMAND:
                    result = get_sc(from_what)
                    if result[0] == "":
                        return Error("未知的角色名: {}".format(from_what), urge=self.get_name())
                    reply.text += "[Touhou Spellcard] 您抽到了："
                    reply.text += "\n" + result[0]
                    reply.text += "\n使用者：" + result[1]
                else:
                    return Error("未知的命令头")
            return reply

        return Error("命令不满足该插件")