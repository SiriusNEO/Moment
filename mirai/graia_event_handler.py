import asyncio

from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain, At
from graia.application.group import Group, Member

from mirai.mirai_config import *

from event.msg_handler import 

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)

app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://" + HOST + ":" + PORT,  # 填入 httpapi 服务运行的地址
        authKey=AUTHKEY,  # 填入 authKey
        account=ACCOUNT,  # 你的机器人的 qq 号
        websocket=True  # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)

# listen

@bcc.receiver("GroupMessage")
async def group_message_listener(app: GraiaMiraiApplication,
                                 group: Group,
                                 member: Member,
                                 graia_chain: MessageChain):
    
    if group.id == WORKING_GROUP:
        message = await graia2moment(app, graia_chain, member.id)
        
        # handle message
        message_handle(message)

# send 

async def send_group_message(graia_chain: MessageChain):
    await app.sendGroupMessage(WORKING_GROUP, graia_chain)

app.launch_blocking()