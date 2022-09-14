import asyncio

# import: frontend
from frontend.frontend_config import *
from frontend.shell.chatroom import ChatRoom

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

checkPassed = (CONFIG.is_in("username", prefix=PLATFORM) and
               CONFIG.is_in("root-accounts", prefix=PLATFORM))

CONFIG_TEMPLATE = """shell:
    username:      # 你的名字
        your-name
    input-offset:  # 用于将聊天框右置的参数, 可省略
        - a number
    root-accounts: # 可以对机器人发送更高命令的用户
        - root1
"""

if not checkPassed:
    Log.error("Platform {} 配置文件格式错误! 请保证配置文件中如下字段均正确填写:".format(PLATFORM))
    print(CONFIG_TEMPLATE)
    raise Exception("config check error")
else:
    Log.info("配置对接 {} 成功!".format(PLATFORM))

"""
    input offset
"""
DEFAULT_OFFSET = 70

input_offset = None # default
if CONFIG.is_in("input-offset", prefix=PLATFORM):
    config_offset = CONFIG.get("input-offset", prefix=PLATFORM)
    if isinstance(config_offset, int) or str.isdigit(config_offset):
        input_offset = int(config_offset)

if input_offset is None:
    Log.warn("未找到 input-offset 字段, 将使用默认值: {}".format(str(DEFAULT_OFFSET)))
    input_offset = DEFAULT_OFFSET


"""
    Bot initialization
"""
bot = Bot(platform=PLATFORM, config=CONFIG)

"""
    ChatRoom initialization
"""
chatroom = ChatRoom(your_name=CONFIG.get("username", prefix=PLATFORM), bot=bot, input_offset=input_offset)

# register it
bot.register_send_method(chatroom.send_message)

"""
    Plugin Task
"""
bot.create_plugin_task(chatroom.loop)
Log.info("FrontEnd {} 启动完成. {}({}) 正式开始工作.".format(PLATFORM, bot.name, PLATFORM))

chatroom.run()