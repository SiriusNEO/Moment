import random
from utils.rand_tool import *
from utils.misc import find_all

from core.plugin import *
from plugins.random.plugin_config import *
from plugins.random.plugin_doc import PLUGIN_DOC
from plugins.random.dice import build, evaluate


class Random_Plugin(Plugin):

    def __init__(self):
        super().__init__(
                name = "Random",
                requirements = [], 
                info = "随机数工具",
                doc = PLUGIN_DOC
            )


    def handle_message(self, message: Message) -> Union[Error, Message]:
        assert self._setup_flag
        
        if message.text is not None:
            reply = Message()
            
            cmd_args = message.text.split(" ")
            
            # gk part
            if cmd_args[0] == GK_COMMAND:
                reply.at = message.sender
                if len(cmd_args) > 2 or (len(cmd_args) == 2 and cmd_args[1] != "理" and cmd_args[1] != "文"):
                    return Error("高考命令格式不正确", urge=self.get_name())
                
                reply.at = message.sender
                reply.text = Random_Plugin._gk("理" if len(cmd_args) == 1 else cmd_args[1])
                return reply
            # dice part
            elif cmd_args[0] in DICE_COMMAND:
                if not 2 <= len(cmd_args) <= 3:
                    return Error("命令参数个数不正确", urge=self.get_name())
                
                if len(cmd_args) == 3:
                    reason = cmd_args[2]
                else:
                    reason = "掷骰"
                
                result = evaluate(build(cmd_args[1]))
                if isinstance(result, Error):
                    return result
                assert isinstance(result, int)
                
                reply.at = message.sender
                reply.text = reason + ": " + str(result)
                return reply
            # choose part
            elif cmd_args[0] == CHOOSE_COMMAND:
                if len(cmd_args) <= 1:
                    return Error("命令参数个数不正确", urge=self.get_name())
                reply.text = random.choice(cmd_args[1:])
                return reply
            # A不A part
            else:
                bu_pos_list = find_all(message.text, "不")
                for bu_pos in bu_pos_list:
                    for i in range(bu_pos):
                        str_len = bu_pos - i
                        if str_len*2+1 <= len(message.text) and message.text[i:bu_pos] == message.text[bu_pos+1:bu_pos+str_len+1]:
                            decision = random.randint(0, 1)
                            reply.text = ""
                            if decision == 0:
                                reply.text += "不"
                            reply.text += message.text[i:bu_pos]
                            return reply

        return Error("命令不满足该插件")
    
    @staticmethod
    def _gk(major: str) -> str:
        ret = """参加普通高等学校招生全国统一考试({})的分数是：
语文: {}/150
数学: {}/150
英语: {}/150
{}综: {}/300
总分: {}/750"""

        chinese = int(random.gauss(120, 5))
        math = int(random.gauss(125, 15))
        english = int(random.gauss(137, 6))
        if chinese > 145:
            chinese = 145
        if math > 149:
            math = 150
        if english > 149:
            english = 150

        # 采用理科数据
        if major == "理":
            zonghe = int(random.gauss(250, 25))
            if zonghe > 299:
                zonghe = 300
            
        # 采用文科数据
        else:
            zonghe = int(random.gauss(220, 20))
            if zonghe > 299:
                zonghe = 300
        
        return ret.format(major, chinese, math, english, major, zonghe, chinese+math+english+zonghe)
    