import asyncio

# import: aiocqhttp
import aiocqhttp
from aiocqhttp import CQHttp, Event

# import: frontend
from frontend.frontend_config import *
from frontend.aiocqhttp.msg_parser import *

# import: core
from core.message import Message
from core.error import Error
from core.bot import Bot
from core.image import *

# import: log
from utils.log import Log

# others
from typing import Union, List
from os import path

"""
    Check Config
"""
PLATFORM = CONFIG.get("platform")

checkPassed = (CONFIG.is_in("host", prefix=PLATFORM) and
               CONFIG.is_in("port", prefix=PLATFORM) and
               CONFIG.is_in("account", prefix=PLATFORM) and
               CONFIG.is_in("root-accounts", prefix=PLATFORM) and
               CONFIG.is_in("working-group", prefix=PLATFORM))

CONFIG_TEMPLATE = """aiocqhttp:
    api-root:
        cqhttp host+port  # 若使用反向websocket, 无需此项. 否则若使用http, 填写cqhttp的host+post
    host:          # aiocqhttp server 的地址
        your-host
    port:          # aiocqhttp server 的端口号
        your-port
    account:       # 机器人qq号
        your-account
    root-accounts: #可以对机器人发送更高命令的用户的qq号
        - root1
        - root2
    working-group: # 工作的群聊
        your-working-qq-group
"""

if not checkPassed:
    Log.error("Platform {} 配置文件格式错误! 请保证配置文件中如下字段均正确填写:".format(PLATFORM))
    print(CONFIG_TEMPLATE)
    raise Exception("config check error")
else:
    Log.info("配置对接 {} 成功! 检测到机器人账号: {}".format(PLATFORM, CONFIG.get("account", prefix=PLATFORM)))


"""
    Bot initialization
"""
bot = Bot(platform=PLATFORM, config=CONFIG)

"""
    aiocqhttp initialization
"""

api_root = None
if CONFIG.is_in("api-root", prefix=PLATFORM)
    api_root = CONFIG.get("api-root", prefix=PLATFORM)
    if api_root == "":
        api_root = None

if api_root is None:
    Log.info("检测到 api-root 字段, 使用反向 websocket 与 CQHTTP 通信")
    cqhttp = CQHttp()
else:
    Log.info("检测到 api-root 字段, 使用 http 与 CQHTTP 通信")
    cqhttp = CQHttp(api_root=api_root)

"""
    send method
"""
async def send_group_message(message: Union[Message, List[Message]]):
    if isinstance(message, list):
        for single_message in message:
            await send_group_message(single_message)
            await asyncio.sleep(SEND_WAIT)
        return

    await cqhttp.call_action("send_group_msg", group_id=CONFIG.get("working-group", prefix=PLATFORM), message=await moment2cqhttp(message))

# register it
bot.register_send_method(send_group_message)

"""
    listen method
"""
@cqhttp.on('message.group')
async def group_message_listener(event: Event):
    # only work in WORKING_GROUP
    if event.group_id == CONFIG.get("working-group", prefix=PLATFORM):
        cqmessage = aiocqhttp.Message()
        cqmessage.extend(event.message)
        message = await cqhttp2moment(cqhttp, cqmessage, event.sender)
        
        # debug
        message.display()

        # handle message
        await bot.handle_message(message)

"""
    Plugin Task (注意等连接上ws再启动)
"""
@cqhttp.on_websocket_connection
async def _(event: Event):
    bot.create_plugin_task(cqhttp.loop)

Log.info("FrontEnd {} 启动完成. {}({}) 正式开始工作.".format(PLATFORM, bot.name, PLATFORM))

cqhttp.run(host=CONFIG.get("host", prefix=PLATFORM), port=str(CONFIG.get("port", prefix=PLATFORM)))