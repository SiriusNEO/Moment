"""
    The class of the bot, containing necessary information for creating the bot
"""

from core.plugin import Plugin
from core.message import Message
from core.error import Error
from utils.log import Log
from typing import Optional, List

from frontend.frontend_config import YamlConfig

class Bot:

    def __init__(self, platform: str, config: YamlConfig):
        self.name = config.get("name")
        self.account = config.get("account", prefix=platform)
        self.roots = config.get("root-accounts", prefix=platform)
        self.platform = platform

        self.env = config.get("env")
        self.installed_plugins = []
        self.installed_plugins_name = []
        
        self.name_2_plugin = {}

        self._ban_list = []
        self._send_method = None

        prepared_plugins = config.get("prepared_plugins")

        if config.is_in("plugins"):
            name_2_plugin = {}

            for i in range(len(prepared_plugins)):
                name_2_plugin[prepared_plugins[i].get_name()] = prepared_plugins[i]

            install_list = config.get("plugins")
            for i in range(len(install_list)):
                if install_list[i] not in name_2_plugin:
                    raise Exception("未知的插件名: {}".format(install_list[i]))
                
                plugin = name_2_plugin[install_list[i]]

                if plugin.get_name() == "Help":
                    self.install(plugin, self)
                elif plugin.get_name() == "Database":
                    self.install(plugin)
                    database = plugin.database
                elif plugin.get_name() == "Replier" or plugin.get_name() == "Star":
                    self.install(plugin, database)
                else:
                    self.install(plugin)
    
    
    def register_send_method(self, send_method):
        if not callable(send_method):
            raise Exception("register a not callable send_method")
        Log.info("Method {} has been registered. It must be async.".format(send_method.__name__))
        self._send_method = send_method


    def install(self, plugin: Plugin, *arg):
        plugin_name = plugin.get_name()

        for requirement in plugin.requirements:
            if requirement not in self.installed_plugins_name:
                raise Exception("Requirements of Plugin {} not installed, need: {}".format(plugin_name, requirement))
        
        plugin.setup(*arg)
        plugin.roots = self.roots

        self.installed_plugins.append(plugin)
        self.installed_plugins_name.append(plugin_name)
        self.name_2_plugin[plugin_name] = plugin


    async def handle_message(self, message: Message):
        for plugin in self.installed_plugins:
            if plugin in self._ban_list:
                Log.info("{}: banned".format(plugin.get_name()))
                continue

            reply = plugin.handle_message(message)
            
            if isinstance(reply, Message) or isinstance(reply, list):
                await self._send_method(reply)
                return
            else:
                assert isinstance(reply, Error)
                if reply.urge is not None:
                    reply_error = Message()
                    reply_error.text = "{}: {}".format(reply.urge, reply.what)
                    await self._send_method(reply_error)
                    return
                else:
                    Log.info("<{}>: ".format(plugin.get_name()), reply.what)


    def create_plugin_task(self, loop):
        Log.info("Starting Plugin tasks.")

        for plugin in self.installed_plugins:
            loop.create_task(plugin.plugin_task(self._send_method))


    def is_banned(self, plugin_name: str) -> Optional[Error]:
        if plugin_name not in self.name_2_plugin:
            return Error("插件名不存在!")
        
        return self.name_2_plugin[plugin_name] in self._ban_list


    def ban(self, plugin_name: str) -> Optional[Error]:
        if plugin_name not in self.name_2_plugin:
            return Error("插件名不存在: {}".format(plugin_name))
        
        plugin = self.name_2_plugin[plugin_name]

        if plugin in self._ban_list:
            return Error("插件已被禁用，无需重复操作: {}".format(plugin_name))

        self._ban_list.append(plugin)

        # 递归 ban
        for other_plugin in self.installed_plugins:
            if plugin.get_name() in other_plugin.requirements and other_plugin not in self._ban_list:
                error = self.ban(other_plugin.get_name())
                if error is not None:
                    return error

        plugin.banned = True
        return None


    def unban(self, plugin_name: str) -> Optional[Error]:
        if plugin_name not in self.name_2_plugin:
            return Error("插件名不存在: {}".format(plugin_name))
        
        plugin = self.name_2_plugin[plugin_name]

        if plugin not in self._ban_list:
            return Error("插件未被禁用，无法解禁: {}".format(plugin_name))
        
        # 递归 unban
        for requirement in plugin.requirements:
            if self.is_banned(requirement): # 一定非 error, 因为 requirement 一定安装了
                error = self.unban(requirement)
                if error is not None:
                    return error

        self._ban_list.remove(plugin)
        plugin.banned = False
        return None

