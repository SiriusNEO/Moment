from core.plugin import *
from core.bot import Bot
from plugins.help.plugin_config import *
from plugins.help.plugin_doc import PLUGIN_DOC

import random

class Help_Plugin(Plugin):

    def __init__(self):
        super().__init__(
                requirements = [], 
                info = "Help: 帮助文档与插件管理",
                doc = PLUGIN_DOC
            )

    def setup(self, bot: Bot):
        self.bot = bot

    def handle_message(self, message: Message) -> Union[Error, Message]:
        if message.text is not None:
            cmd_args = message.text.split(" ")
            if len(cmd_args) <= 2 and cmd_args[0] == HELP_COMMAND:
                reply = Message()
                plugin_num = len(self.bot.installed_plugins)

                if len(cmd_args) == 1:
                    reply.text = "机器人 {} 运行于 {} 中. 对接前端: {}\n".format(self.bot.name, self.bot.env, self.bot.platform)
                    reply.text += "当前已安装 {} 个插件: \n".format(plugin_num)

                    for i in range(plugin_num):
                        reply.text += "{}. {}\n".format(i, self.bot.installed_plugins[i].info)
                else:
                    assert len(cmd_args) == 2
                    if str.isdigit(cmd_args[1]):
                        plugin_no = int(cmd_args[1])
                        if 0 <= plugin_no < plugin_num:
                            reply.text = self.bot.installed_plugins[plugin_no].doc
                        else:
                            return Error("没有此下标的插件!")
                    else:
                        return Error("help指令第二个参数必须是整数!")
                return reply

        return Error("命令不满足该插件")