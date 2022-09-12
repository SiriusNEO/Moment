"""
    The basic class of all plugins
"""
from core.message import Message
from core.error import Error
from typing import Union, List

from utils.log import Log

import asyncio

class Plugin:

    def __init__(self, name, requirements = [], info = "", doc = ""):
        self._name = name
        self.requirements = requirements
        self.info = info
        self.doc = doc
        self._setup_flag = False
        self.banned = False
    
    """
        Get the plugin name (class name)
    """
    def get_name(self):
        return self._name

    """
        Things that should be done when installing this plugin to bot
    """
    def setup(self, bot):
        self._setup_flag = True
        Log.info("插件 {} 已植入Bot @{} 中.".format(self.get_name(), bot.name))

    """
        Message 2 Reply
    """
    async def handle_message(self, message: Message) -> Union[Message, List[Message], Error]:
        return Error("Unimplemented")

    """
        It will be created as a task in the main loop
    """
    async def plugin_task(self, send_method):
        pass
    