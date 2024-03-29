from plugins.hello.plugin_doc import PLUGIN_DOC
from plugins.hello.plugin_config import *

from core.plugin import *
from utils.log import Log

import datetime

class Hello_Plugin(Plugin):

    def __init__(self):
        super().__init__(
                name = "Hello",
                requirements = [], 
                info = "开机问候与报时",
                doc = PLUGIN_DOC
            )
    
    @check_setup
    async def plugin_task(self):
        # start wait
        await asyncio.sleep(10)
        await self.send(HELLO_WORD)

        async for _ in Ticker(self, 1):
            # Log.info("{} Working".format(self.get_name()))

            now_datetime = datetime.datetime.now()
            await self._report_time(now_datetime)
    
    
    async def _report_time(self, now_datetime):
        if now_datetime.minute != 0 or now_datetime.second != 0 or (3 <= now_datetime.hour <= 6):
            return

        reply = Message()
        reply.text = "整点报时！现在是：" + str(datetime.datetime.now().hour) + "点整~"

        if now_datetime.hour == 2:
            # 晚安
            reply.text += "\n" + GOOD_NIGHT

        if now_datetime.hour == 7:
            # 早安
            reply.text += "\n" + GOOD_MORNING + str(now_datetime.month) + "月" + str(now_datetime.day) + "号，" + WEEKDAY_NAME[now_datetime.weekday()] + "~"

        await self.send(reply)
