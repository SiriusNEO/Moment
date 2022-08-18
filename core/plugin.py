"""
    The basic class of all plugins
"""
from core.message import Message
from core.error import Error
from typing import Union

class Plugin:

    def __init__(self, requirements = [], info = "", doc = ""):
        self.requirements = requirements
        self.info = info
        self.doc = doc

    """
        Things that should be done when installing this plugin to bot
    """
    def setup(self):
        pass


    """
        Message 2 Reply
    """
    def handle_message(self, message: Message) -> Union[Message, Error]:
        pass


    """
        The unique method of this plugin. It will be created as a task in the main loop
    """
    async def plugin_task(self) -> Message:
        pass
    