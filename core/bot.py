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
        if isinstance(self.account, int):
            self.account = str(self.account)

        self.roots = config.get("root-accounts", prefix=platform)
        if self.roots is None:
            self.roots = []
        
        # use str
        for i in range(len(self.roots)):
            if isinstance(self.roots[i], int):
                self.roots[i] = str(self.roots[i])

        self.platform = platform
        self.env = config.get("env")

        self.installed_plugins = []
        self.installed_plugins_name = []
        self.name_2_plugin = {}
        
        self._ban_list = []
        self._send_method = None

        if config.is_in("preloaded_plugins"):
            preloaded_plugins = config.get("preloaded_plugins")
            if preloaded_plugins is None:
                preloaded_plugins = []
        else:
            preloaded_plugins = []

        if config.is_in("plugins") and len(preloaded_plugins) > 0:
            name_2_preloaded_plugin = {}

            for i in range(len(preloaded_plugins)):
                name_2_preloaded_plugin[preloaded_plugins[i].get_name()] = preloaded_plugins[i]

            install_list = config.get("plugins")
            for i in range(len(install_list)):
                if install_list[i] not in name_2_preloaded_plugin:
                    raise Exception("未知的插件名: {}".format(install_list[i]))
                
                if install_list[i] in self.installed_plugins_name:
                    Log.warn("检测到重复插件, 将忽略第二次安装: {}".format(install_list[i]))
                    continue
                
                self.install(name_2_preloaded_plugin[install_list[i]])
        else:
            Log.warn("缺少 preloaded_plugins, 将不会按配置载入 plugin")
    
    
    def register_send_method(self, send_method):
        if not callable(send_method):
            raise Exception("send_method 必须是一个 callable 对象")
        Log.info("Method \"{}\" 成功被注册为 Moment 的发送方法 (It must be async)".format(send_method.__name__))
        self._send_method = send_method
        for plugin in self.installed_plugins:
            plugin._send_method = send_method
    

    """
        插件依赖. 
        有时 B 插件需要 A 插件的信息, 在 setup 时由 B 插件向 A 插件发起一个 require_info
    """
    def require_info(self, plugin_name: str, member_name: str):
        if plugin_name not in self.name_2_plugin:
            raise Exception("require info error: 未预先被安装的目标插件: {}".format(plugin_name))
        plugin = self.name_2_plugin[plugin_name]

        if not hasattr(plugin, member_name):
            raise Exception("require info error: 插件{}不含该数据成员: {}".format(plugin_name, member_name))

        return getattr(plugin, member_name)
    
    """
        插件依赖. 
        有时 B 插件需要调用 A 插件的方法, 在 setup 时由 B 插件向 A 插件发起一个 invoke_method
    """
    def invoke_method(self, plugin_name: str, method_name: str, *args):
        plugin_method = self.require_info(plugin_name, method_name)
        return plugin_method(*args)


    def install(self, plugin: Plugin):
        plugin_name = plugin.get_name()

        for requirement in plugin.requirements:
            if requirement not in self.installed_plugins_name:
                raise Exception("Requirements of Plugin {} not installed, need: {}".format(plugin_name, requirement))
        
        plugin.setup(self)
        plugin._roots = self.roots
        plugin._send_method = self._send_method

        self.installed_plugins.append(plugin)
        self.installed_plugins_name.append(plugin_name)
        self.name_2_plugin[plugin_name] = plugin


    async def handle_message(self, message: Message):
        for plugin in self.installed_plugins:
            if plugin.wait_msg_flag:
                plugin.received_queue.put(message)

        # plugin.handle_message for not-wait plugin
        # if a plugin is triggered, interrupt.
        for plugin in self.installed_plugins:
            if plugin in self._ban_list:
                Log.info("{}: banned".format(plugin.get_name()))
                continue

            if not plugin.wait_msg_flag:
                reply = await plugin.handle_message(message)
            
                if isinstance(reply, Message) or isinstance(reply, list):
                    await self._send_method(reply)
                    return
                elif isinstance(reply, Error):
                    if reply.urge is not None:
                        reply_error = Message()
                        reply_error.text = "{}: {}".format(reply.urge, reply.what)
                        await self._send_method(reply_error)
                        return
                    else:
                        Log.info("<{}>: ".format(plugin.get_name()), reply.what)
                else:
                    # probably None
                    Log.info("<{}>: ".format(plugin.get_name()), reply)


    def create_plugin_task(self, loop):
        for plugin in self.installed_plugins:
            loop.create_task(plugin.plugin_task())
        
        Log.info("成功在事件循环中启动所有插件的 plugin_task")


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

