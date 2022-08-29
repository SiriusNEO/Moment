from core.plugin import *
from core.bot import Bot
from plugins.word.plugin_config import *
from plugins.word.plugin_doc import PLUGIN_DOC

import random
import re
import json

class Word_Plugin(Plugin):

    def __init__(self):
        super().__init__(
                name = "Word",
                requirements = [], 
                info = "背单词插件",
                doc = PLUGIN_DOC
            )

    def handle_message(self, message: Message) -> Union[Message, List[Message], Error]:
        assert self._setup_flag

        if message.text is not None:
            if re.match(COMMAND_PATTERN, message.text) is not None:
                ge_pos = message.text.find("个")
                word_num = int(message.text[1:ge_pos])
                if word_num > WORD_THRESHOLD:
                    return Error("太多词了!", urge=self.get_name())
                
                reply = Message()
                # reply.at = message.sender  
                # without at, you can translate the word directly by Translate Plugin
                reply.text = "给你词: \n"

                with open(WORD_PATH) as fp:
                    word_list = list(json.load(fp))

                    for i in range(word_num):
                        reply.text += random.choice(word_list)
                        if i != word_num-1:
                            reply.text += "\n"
                
                return reply

        return Error("命令不满足该插件")