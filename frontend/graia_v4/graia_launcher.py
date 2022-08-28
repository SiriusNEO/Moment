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
    exit(1)
else:
    Log.info("配置对接 {} 成功! 检测到机器人账号: {}".format(PLATFORM, CONFIG.get("account", prefix=PLATFORM)))


"""
    Bot initialization
"""
bot = Bot(
            name=CONFIG.get("name"),
            account=CONFIG.get("account", prefix=PLATFORM),
            roots=CONFIG.get("root-accounts", prefix=PLATFORM),
            platform=PLATFORM,
            env=CONFIG.get("env")
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
    await app.sendGroupMessage(CONFIG.get("working-group", prefix="graia-v4"), graia_chain)

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
    if group.id == CONFIG.get("working-group", prefix="graia-v4"):
        message = await graia2moment(app, graia_chain, member.id)
        
        # debug
        message.display()

        # handle message
        await bot.handle_message(message)

"""
    Plugin Task
"""
bot.create_plugin_task(loop)

Log.info("FrontEnd {} started.".format(PLATFORM))

app.launch_blocking()