from plugins.alarm.plugin_config import *

PLUGIN_DOC = """闹钟插件. 闹钟提醒功能.

命令:
    - {} <时间> (设定闹钟. 需要引用一个消息表示闹钟内容.)
    - {} <时间> (删除指定时间的闹钟.)
    - {}        (查看所有闹钟)

注意: 时间格式为 小时-分钟, 且不含前导0! (不然报不出来)
""".format(SET_ALARM, DEL_ALARM, LS_ALARM)