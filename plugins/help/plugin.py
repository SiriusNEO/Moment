from core.plugin import *
from core.bot import Bot
from plugins.help.plugin_config import *
from plugins.help.plugin_doc import PLUGIN_DOC

import random

class Help_Plugin(Plugin):

    def __init__(self):
        super().__init__(
                name = "Help",
                requirements = [], 
                info = "帮助文档与插件管理",
                doc = PLUGIN_DOC
            )

    def setup(self, bot: Bot):
        self.bot = bot
        super().setup()
    

    def handle_message(self, message: Message) -> Union[Message, List[Message], Error]:
        assert self._setup_flag

        if message.text is not None:
            cmd_args = message.text.split(" ")
            
            if len(cmd_args) <= 2:
                plugin_num = len(self.bot.installed_plugins)

                if cmd_args[0] == PING_COMMAND and len(cmd_args) == 1:
                    return Message("大家好啊, 我是 {}".format(self.bot.name))
                elif cmd_args[0] == MONITER_COMMAND and len(cmd_args) == 1:
                    reply = Message("")
                    for i in range(plugin_num):
                        plugin = self.bot.installed_plugins[i]
                        status = MONITER_BANNED if self.bot.is_banned(plugin.get_name()) else MONITER_RUNNING
                        reply.text += "[{}:{}]".format(plugin.get_name(), status)
                        if i != plugin_num-1:
                            reply.text += " "
                    return reply
                        
                elif cmd_args[0] == HELP_COMMAND:
                    reply = Message()
                    if len(cmd_args) == 1:
                        reply.text = "机器人 {} 运行于 {} 中. 对接前端: {}\n".format(self.bot.name, self.bot.env, self.bot.platform)
                        reply.text += "当前已安装 {} 个插件: \n\n".format(plugin_num)

                        for i in range(plugin_num):
                            plugin = self.bot.installed_plugins[i]
                            plugin_status = "banned" if self.bot.is_banned(plugin.get_name()) else "running"
                            reply.text += "{}. {}: {}\t[{}]".format(i, plugin.get_name(), plugin.info, plugin_status)
                            if i != plugin_num-1:
                                reply.text += "\n"
                    else:
                        assert len(cmd_args) == 2
                        if str.isdigit(cmd_args[1]):
                            plugin_no = int(cmd_args[1])
                            if 0 <= plugin_no < plugin_num:
                                reply.text = self.bot.installed_plugins[plugin_no].doc
                            else:
                                return Error("没有此下标的插件!", urge=self.get_name())
                        else:
                            if cmd_args[1] not in self.bot.name_2_plugin:
                                return Error("没有名为{}的插件!".format(cmd_args[1]), urge=self.get_name())
                            else:
                                reply.text = self.bot.name_2_plugin[cmd_args[1]].doc
                    return reply
                
                elif cmd_args[0] == BAN_COMMAND or cmd_args[0] == UNBAN_COMMAND:
                    if message.sender not in self.roots:
                        return Error("权限不足!", urge=self.get_name())
                    if len(cmd_args) != 2:
                        return Error("参数个数错误!", urge=self.get_name())
                    if str.isdigit(cmd_args[1]):
                            plugin_no = int(cmd_args[1])
                            if 0 <= plugin_no < plugin_num:
                                plugin_name = self.bot.installed_plugins[plugin_no].get_name()
                                if cmd_args[0] == BAN_COMMAND:
                                    error = self.bot.ban(plugin_name)
                                    if error is not None:
                                        return Error(error.what, urge=self.get_name())
                                    return Message("{}: 禁用成功!".format(plugin_name))
                                else:
                                    assert cmd_args[0] == UNBAN_COMMAND
                                    error = self.bot.unban(plugin_name)
                                    if error is not None:
                                        return Error(error.what, urge=self.get_name())
                                    return Message("{}: 解禁成功!".format(plugin_name))
                            else:
                                return Error("没有此下标的插件!", urge=self.get_name())
                    else:
                        if cmd_args[1] == ARG_ALL:
                            name_list = list(self.bot.name_2_plugin.keys())
                            if cmd_args[0] == BAN_COMMAND:
                                for plugin_name in name_list:
                                    if plugin_name == self.get_name() or self.bot.is_banned(plugin_name):
                                        continue
                                    error = self.bot.ban(plugin_name)
                                    if error is not None:
                                        return Error(error.what, urge=self.get_name())
                                return Message("全部禁用成功! (除了本插件)")
                            else:
                                assert cmd_args[0] == UNBAN_COMMAND
                                for plugin_name in name_list:
                                    if plugin_name == self.get_name() or not self.bot.is_banned(plugin_name):
                                        continue
                                    error = self.bot.unban(plugin_name)
                                    if error is not None:
                                        return Error(error.what, urge=self.get_name())
                                return Message("全部解禁成功!")
                        
                        if cmd_args[1] == self.get_name():
                            return Error("不能对本插件进行操作", urge=self.get_name())

                        if cmd_args[0] == BAN_COMMAND:
                            error = self.bot.ban(cmd_args[1])
                            if error is None:
                                return Message("{}: 禁用成功!".format(cmd_args[1]))
                            else:
                                return Error(error.what, urge=self.get_name())
                        else:
                            assert cmd_args[0] == UNBAN_COMMAND
                            error = self.bot.unban(cmd_args[1])
                            if error is None:
                                return Message("{}: 解禁成功!".format(cmd_args[1]))
                            else:
                                return Error(error.what, urge=self.get_name())

        return Error("命令不满足该插件")