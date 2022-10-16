from core.plugin import *
from core.bot import Bot
from plugins.curriculum_reporter.plugin_config import *
from plugins.curriculum_reporter.plugin_doc import PLUGIN_DOC
import yaml
import time
import datetime
from utils.log import Log

class Curriculum_Reporter_Plugin(Plugin):

    def __init__(self):
        super().__init__(
                name = "Curriculum_Reporter",
                requirements = [], 
                info = "自动提醒上课的qq机器人插件",
                doc = PLUGIN_DOC
            )
    

    def setup(self, bot: Bot):
        try:
            with open(CURRICULUM_PATH, "r", encoding="utf-8") as fp:
                self.curriculum = yaml.load(fp.read(), Loader=yaml.FullLoader)
        except:
            raise Exception("找不到课表文件: {}".format(CURRICULUM_PATH))

        super().setup(bot)
    

    @check_setup
    async def handle_message(self, message: Message) -> Union[Message, List[Message], Error]:
        if message.text is not None:
            cmd_args = message.text.split(" ")

            if cmd_args[0] == SHOW_COMMAND:
                if len(cmd_args) > 2:
                    return Error("参数个数不对!", urge=self.get_name())
            
                try:
                    total_info = ""
                    for course in self.curriculum['courses']:
                        if len(cmd_args) == 2:
                            if course['name'] == cmd_args[1]:
                                course_info = "课程名: {}\n会议号: {}\n密码: {}\n时间: ".format(course['name'], str(course['meeting']), str(course['passwd']))
                                for one_time in course['time']:
                                    course_info += WEEKNAME[int(one_time['weekday'])] + one_time['clock'] + ", "
                                course_info = course_info[:-2]
                                return Message(course_info)
                        else:
                            total_info += "课程名: {}\t会议号: {}\t密码: {}".format(course['name'], str(course['meeting']), str(course['passwd']))
                            if self.curriculum['courses'].index(course) != len(self.curriculum['courses'])-1:
                                total_info += "\n"
                    if len(cmd_args) == 2:
                        raise Exception("无此课程")
                    else:
                        return Message(total_info)
                except Exception as e:
                    return Error("发生错误: {}".format(e.args), urge=self.get_name())

    
    @check_setup
    async def plugin_task(self):
        async for _ in Ticker(self, 60):
            next_datetime = datetime.datetime.now() + datetime.timedelta(minutes=5)
            # Log.info(next_datetime)
            try:
                for course in self.curriculum['courses']:
                    for one_time in course['time']:
                        one_clock = time.strptime(one_time['clock'], TIME_FORMAT)
                        # Log.info(one_clock)
                        if next_datetime.weekday() == one_time['weekday'] and next_datetime.hour == one_clock.tm_hour and next_datetime.minute == one_clock.tm_min:
                            await self.send("课程【{}】还有五分钟就要开始啦~\n会议号: {}\n会议密码: {}".format(course['name'], str(course['meeting']), str(course['passwd'])))
            except Exception as e:
                Log.error(e)
            