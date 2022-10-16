"""
    The basic class of all plugins
"""
from core.message import Message
from core.error import Error
from core.user import User
from typing import Union, List

from utils.log import Log

import asyncio

from core.core_config import MSG_WAIT_GAP

import queue
import functools


"""
    Ticker
    定时触发, 常用于 plugin_task
"""
class Ticker:
    
    def __init__(self, plugin, time_delta):
        self.plugin = plugin
        self.time_delta = time_delta
        self.total_time = 0
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        await asyncio.sleep(self.time_delta)
        self.total_time += self.time_delta

        # ban block
        while self.plugin.banned:
            await asyncio.sleep(1)

        return self.total_time

"""
    check_setup decorator
    为一个 method 做一个查看其是否 setup 的 check
"""
def check_setup(method):
    @functools.wraps(method)
    async def wrapper(self, *args, **kwargs):
        if not self._setup_flag:
            raise Exception("执行了未安装的插件: {}".format(self.get_name()))
        return await method(self, *args, **kwargs)
    return wrapper


class Plugin:

    def __init__(self, name, requirements = [], info = "", doc = ""):
        self._name = name
        self.requirements = requirements
        self.info = info
        self.doc = doc
        
        self._setup_flag = False
        self.banned = False
        self._roots = []
        self._send_method = None

        # used in wait_message
        self.received_queue = queue.Queue()
        self.wait_msg_flag = False
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
    

    def check_privilege(self, sender: User) -> bool:
        return sender.uid in self._roots or sender.name in self._roots

    """
        wait for a message.
        for_sender: wait the message for specific sender
        checker: wait the message which is checked by checker
    """
    async def wait_message(self, for_sender = None, checker = None):
        self.received_message = queue.Queue()
        self.wait_msg_flag = True
        
        check_pass = False

        while not check_pass:
            await asyncio.sleep(MSG_WAIT_GAP)
            if not self.received_queue.empty():
                check_pass = True
                received_message = self.received_queue.get()
                if for_sender is not None:
                    check_pass = check_pass and (received_message.sender == for_sender)
                if checker is not None:
                    if not callable(checker):
                        raise Exception("error in wait_message: checker {} not callable".format(checker))
                    check_pass = check_pass and checker(received_message)
        
        self.wait_msg_flag = False
        return received_message

    """
        send by a plugin
    """
    async def send(self, message: Union[str, Message]):
        if isinstance(message, str):
            message = Message(message)
        await self._send_method(message)

    """
        Message 2 Reply
    """
    async def handle_message(self, message: Message) -> Union[Message, List[Message], Error]:
        return Error("Unimplemented")

    """
        It will be created as a task in the main loop
    """
    async def plugin_task(self):
        pass