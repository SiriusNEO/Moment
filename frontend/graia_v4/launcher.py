import asyncio

# import: graia
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain, At
from graia.application.group import Group, Member

# import: frontend
from frontend.frontend_config import *
from frontend.graia_v4.msg_parser import *

# import: core
from core.message import Message
from core.error import Error
from core.bot import Bot

# import: log
from utils.log import Log

# others
from typing import Union, List

"""
    Check Config
"""
PLATFORM = CONFIG.get("platform")

checkPassed = (CONFIG.is_in("host", prefix=PLATFORM) and
               CONFIG.is_in("port", prefix=PLATFORM) and
               CONFIG.is_in("author-key", prefix=PLATFORM) and 
               CONFIG.is_in("account", prefix=PLATFORM) and
               CONFIG.is_in("root-accounts", prefix=PLATFORM) and
               CONFIG.is_in("working-group", prefix=PLATFORM))

CONFIG_TEMPLATE = """graia-v4:
    host:          # mirai 的地址
        your-host
    port:          # mirai 的端口号
        your-port
    author-key:    # mah 的 author key
        your-author-key
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
    Graia initialization
"""
loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://" + CONFIG.get("host", prefix=PLATFORM) + ":" + str(CONFIG.get("port", prefix=PLATFORM)),
        authKey=CONFIG.get("author-key", prefix=PLATFORM),
        account=CONFIG.get("account", prefix=PLATFORM),
        websocket=True
    )
)

"""
    send method
"""
async def send_group_message(message: Union[Message, List[Message]]):
    if isinstance(message, list):
        for single_message in message:
            await send_group_message(single_message)
            await asyncio.sleep(SEND_WAIT)
        return
    
    graia_chain = await moment2graia(app, message)
    await app.sendGroupMessage(CONFIG.get("working-group", prefix=PLATFORM), graia_chain)

# register it
bot.register_send_method(send_group_message)

"""
    listen method
"""
@bcc.receiver("GroupMessage")
async def group_message_listener(app: GraiaMiraiApplication,
                                 group: Group,
                                 member: Member,
                                 graia_chain: MessageChain):
    # only work in WORKING_GROUP
    if group.id == CONFIG.get("working-group", prefix=PLATFORM):
        message = await graia2moment(app, graia_chain, member.id)
        
        # debug
        message.display()

        # handle message
        await bot.handle_message(message)

"""
    Plugin Task
"""
bot.create_plugin_task(loop)

Log.info("FrontEnd {} 启动完成. {}({}) 正式开始工作.".format(PLATFORM, bot.name, PLATFORM))

app.launch_blocking()