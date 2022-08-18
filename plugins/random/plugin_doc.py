from plugins.random.plugin_config import *

PLUGIN_DOC = """随机插件. 来玩各种随机游戏吧.

命令:
    - {} <掷骰子表达式> <掷骰子原因> (参考 Dice! 的掷骰子. 原因可略.)
    - {} <事物1> <事物2> ... <事物n> (随机选择)
    - <动作>不<动作> (决定要不要, 注意这个命令判定很严)
    - {} 理/文 (进行一次高考模拟. 默认为理.)
""".format(DICE_COMMAND, CHOOSE_COMMAND, GK_COMMAND)