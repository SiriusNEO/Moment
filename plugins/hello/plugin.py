from plugins.hello.plugin_doc import PLUGIN_DOC
from plugins.hello.plugin_config import *

from core.plugin import *

class Hello_Plugin(Plugin):

    def __init__(self):
        super().__init__(
                requirements = [], 
                info = "Hello: 开机问候",
                doc = PLUGIN_DOC
            )
    
    async def plugin_task(self, send_method):
        await send_method(Message(HELLO_WORD))