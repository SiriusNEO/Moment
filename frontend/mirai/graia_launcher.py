import asyncio

# import: graia
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain, At
from graia.application.group import Group, Member

# import: frontend
from frontend.mirai.msg_parser import *
from frontend.mirai.frontend_config import *

# import: core
from core.message import Message
from core.error import Error
from core.bot import Bot

# import: plugins
from plugins.help.plugin import Help_Plugin
from plugins.db.plugin import Database_Plugin
from plugins.replier.plugin import Replier_Plugin
from plugins.random.plugin import Random_Plugin
from plugins.touhou.plugin import Touhou_Plugin
from plugins.translate.plugin import Translate_Plugin
from plugins.hello.plugin import Hello_Plugin
from plugins.alarm.plugin import Alarm_Plugin
from plugins.word.plugin import Word_Plugin
from plugins.autotalk.plugin import Autotalk_Plugin
from plugins.pixiv.plugin import Pixiv_Plugin
from plugins.ps.plugin import PS_Plugin
from plugins.judge.plugin import Judge_Plugin

# import: log
from utils.log import Log

"""
    Bot initialization
"""
bot = Bot(
            name="moment",
            account=ACCOUNT,
            roots=ROOT_ACCOUNTS,
            platform="Graia v4",
            env="CentOS"
        )

help_plugin = Help_Plugin()
database_plugin = Database_Plugin()
replier_plugin = Replier_Plugin()
random_plugin = Random_Plugin()
touhou_plugin = Touhou_Plugin()
translate_plugin = Translate_Plugin()
hello_plugin = Hello_Plugin()
alarm_plugin = Alarm_Plugin()
word_plugin = Word_Plugin()
autotalk_plugin = Autotalk_Plugin()
pixiv_plugin = Pixiv_Plugin()
ps_plugin = PS_Plugin()
judge_plugin = Judge_Plugin()

bot.install(help_plugin, bot)
bot.install(database_plugin)
bot.install(random_plugin)
bot.install(touhou_plugin)
bot.install(translate_plugin)
bot.install(hello_plugin)
bot.install(alarm_plugin)
bot.install(word_plugin)
bot.install(autotalk_plugin)
bot.install(pixiv_plugin)
bot.install(ps_plugin)
bot.install(judge_plugin)
bot.install(replier_plugin, database_plugin.database)

"""
    Graia initialization
"""
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

"""
    listen method
"""
@bcc.receiver("GroupMessage")
async def group_message_listener(app: GraiaMiraiApplication,
                                 group: Group,
                                 member: Member,
                                 graia_chain: MessageChain):
    
    if group.id == WORKING_GROUP:
        message = await graia2moment(app, graia_chain, member.id)
        
        message.display()

        # handle message
        reply = bot.handle_message(message)
        if reply is not None:
            await send_group_message(reply)
        

"""
    send method
"""
async def send_group_message(message: Message):
    graia_chain = await moment2graia(app, message)
    await app.sendGroupMessage(WORKING_GROUP, graia_chain)

"""
    Plugin Task
"""
for plugin in bot.installed_plugins:
    loop.create_task(plugin.plugin_task(send_group_message))

app.launch_blocking()

Log.info("[Moment] FrontEnd Graia started.")