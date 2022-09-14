from plugins.alarm.plugin import Alarm_Plugin
from core.message import Message
import asyncio

pl = Alarm_Plugin()
pl._setup_flag = True

loop = asyncio.get_event_loop()
loop.create_task(pl.handle_message(Message("删除 23-53")))
loop.run_forever()