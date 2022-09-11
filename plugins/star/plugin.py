from plugins.star.plugin_doc import PLUGIN_DOC
from plugins.star.plugin_config import *

try:
    from playwright.async_api import async_playwright
except:
    pass

from plugins.browser.basic_browser import BrowserManager

from plugins.db.basic_db import DataBase

from core.plugin import *
from utils.log import Log

from core.image import *

from plugins.db.db_event import TagPair

import re
import os
import random

class Star_Plugin(Plugin):

    def __init__(self):
        super().__init__(
                name = "Star",
                requirements = ["Database", "Browser"], 
                info = "制作精选评论",
                doc = PLUGIN_DOC
            )
    

    def setup(self, database: DataBase):
        database.tag_type[TAG_STAR] = Message
        self.database = database

        super().setup()

        self.task_queue = []
        self.task_lock = False
    

    def handle_message(self, message: Message) -> Union[Message, List[Message], Error]:
        assert self._setup_flag

        if message.text is not None:
            cmd_args = message.text.split(" ")

            if cmd_args[0] == MAKESTAR_COMMAND:
                if len(cmd_args) != 2:
                    return Error("参数个数不对!", urge=self.get_name())

                if not str.isdigit(cmd_args[1]):
                    return Error("参数类型不对, 第二个参数是一个非负整数", urge=self.get_name())
                
                self.task_lock = True
                self.task_queue.append(int(cmd_args[1]))
                self.task_lock = False

                # 不输出
                return Error("")
            
            elif cmd_args[0] == AVATAR_COMMAND:
                if len(cmd_args) != 2:
                    return Error("参数个数不对!", urge=self.get_name())
                
                if message.quote is None or message.quote.pic is None:
                    return Error("头像上传缺少引用的图片!", urge=self.get_name())
                
                save_image(message.quote.pic.pic_bytes, file_name=AVATAR_DIR + cmd_args[1] + AVATAR_FORMAT)
                return Message("头像上传成功!")
        
        return Error("命令格式不符此插件!")
    
    @staticmethod
    def render_html(**kwargs):
        with open(PLUGIN_PATH + HTML_TEMPLATE) as html_fp:
            template = html_fp.read()

            if kwargs["pic_path"].find("no_pic") != -1:
                template = template.replace('<br><br><img id="pic" src="[pic_path]" style="width:297px; border-radius:5% 5% 5% 5%">', '')
            
            background_color = random.choice(STAR_BACKGROUND_COLORS)
            template = template.replace('{background_color}', background_color)

            template = template.replace('{', '(')
            template = template.replace('}', ')')
            template = template.replace('[', '{')
            template = template.replace(']', '}')
            
            rendered = template.format(**kwargs)

            rendered = rendered.replace('(', '{')
            rendered = rendered.replace(')', '}')

        with open(PLUGIN_PATH + HTML_RENDERED, 'w') as rendered_fp:
            rendered_fp.write(rendered)
    

    async def plugin_task(self, send_method):

        while True:
            await asyncio.sleep(WAIT)

            if self.banned:
                self.task_queue = []
                continue
            
            if not self.task_lock and len(self.task_queue) > 0:
                task = self.task_queue[0]
                self.task_queue.remove(task)

                # Log.info("star task:", task)

                query_result, _ = self.database.query([TagPair(TAG_ID, task, 0)])

                if isinstance(query_result, Error) or len(query_result) == 0:
                    await send_method(Message("未找到 id:{} 对应的评论".format(task)))
                    continue
                
                if TAG_STAR not in query_result[0]:
                    await send_method(Message("id: {} 的评论需要一个精品标记 (star字段)".format(task)))
                    continue
                
                if TAG_CM not in query_result[0] or len(query_result[0][TAG_CM]) == 0:
                    await send_method(Message("id: {} 的评论需要一个评论内容 (cm字段)".format(task)))
                    continue
                
                star_info = query_result[0][TAG_STAR].text
                star_msg  = query_result[0][TAG_CM][0]

                if star_info is None or re.match(STAR_REGEX, star_info) is None:
                    await send_method(Message("star字段格式错误: 应该是 <作者名>(<时间>)".format(task)))
                    continue

                left_bra_pos = star_info.find("(")
                star_author = star_info[:left_bra_pos]
                star_time   = star_info[left_bra_pos+1:len(star_info)-1]

                pic_path = "no_pic" if star_msg.pic is None else star_msg.pic.pic_path

                self.render_html(
                    username=star_author, 
                    sendtime=star_time, 
                    avatar_path="../../" + IMG_PATH + AVATAR_DIR + star_author + AVATAR_FORMAT, 
                    text=star_msg.text, 
                    pic_path="../../" + pic_path
                )

                try:
                    async with async_playwright() as pw:
                        async with BrowserManager(pw, 330, 10) as page:
                            abs_path = os.path.dirname(__file__) + "/" + HTML_RENDERED
                            Log.info("abs_path:", abs_path)
                            await page.goto("file://" + abs_path)
                            card = await page.query_selector("div")
                            screenshot = await card.screenshot(timeout=1000)
                except Exception as e:
                    await send_method(Message("制作精品评论发生错误... {}".format(e.args)))
                    continue

                if isinstance(screenshot, bytes):
                    screenshot_path = save_image(screenshot, file_name=TMP_FILENAME)
                    reply = Message()
                    reply.pic = Picture(LOCAL_FILE_URL, pic_path=screenshot_path)
                    await send_method(reply)
                else:
                    await send_method(Message("制作精品评论发生错误..."))
    

