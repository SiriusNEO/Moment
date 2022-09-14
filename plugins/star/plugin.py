from plugins.star.plugin_doc import PLUGIN_DOC
from plugins.star.plugin_config import *

try:
    from playwright.async_api import async_playwright
except:
    pass

from plugins.browser.basic_browser import BrowserManager

from plugins.db.basic_db import DataBase

from core.plugin import *
from core.bot import Bot

from utils.log import Log

from core.image import *

from plugins.db.db_event import TagPair

import re
import os
import random
import datetime

class Star_Plugin(Plugin):

    def __init__(self):
        super().__init__(
                name = "Star",
                requirements = ["Database", "Browser"], 
                info = "制作精选评论",
                doc = PLUGIN_DOC
            )
    

    def setup(self, bot: Bot):
        self.database = bot.require_info(plugin_name="Database", member_name="database")
        self.database.tag_type[TAG_STAR] = Message
        super().setup(bot)
    

    async def handle_message(self, message: Message) -> Union[Message, List[Message], Error]:
        assert self._setup_flag

        if message.text is not None:
            cmd_args = message.text.split(" ")

            if cmd_args[0] == MAKESTAR_COMMAND:
                if len(cmd_args) != 2:
                    return Error("参数个数不对!", urge=self.get_name())

                if not str.isdigit(cmd_args[1]):
                    return Error("参数类型不对, 第二个参数是一个非负整数", urge=self.get_name())
                
                star_id = int(cmd_args[1])

                query_result, _ = self.database.query([TagPair(TAG_ID, star_id, 0)])

                if isinstance(query_result, Error) or len(query_result) == 0:
                    return Error("未找到 id:{} 对应的评论".format(star_id), urge=self.name())
                
                if TAG_STAR not in query_result[0]:
                    return Error("id: {} 的评论需要一个精品标记 (star字段)".format(star_id), urge=self.name())
                
                if TAG_CM not in query_result[0] or len(query_result[0][TAG_CM]) == 0:
                    return Error("id: {} 的评论需要一个评论内容 (cm字段)".format(star_id), urge=self.name())
                
                star_info = query_result[0][TAG_STAR].text
                star_msg  = query_result[0][TAG_CM][0]

                if star_info is None or re.match(STAR_REGEX, star_info) is None:
                    return Error("star字段格式错误: 应该是 <作者名>(<时间>)".format(star_id), urge=self.get_name())

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
                        async with BrowserManager(pw, 320, 10) as page:
                            abs_path = os.path.dirname(__file__) + "/" + HTML_RENDERED
                            Log.info("abs_path:", abs_path)
                            await page.goto("file://" + abs_path)
                            card = await page.query_selector("div")
                            screenshot = await card.screenshot(timeout=1000)
                except Exception as e:
                    return Error("制作精品评论发生错误... {}".format(e.args), urge=self.get_name())

                if isinstance(screenshot, bytes):
                    screenshot_path = save_image(screenshot, file_name=TMP_FILENAME)
                    reply = Message()
                    reply.pic = Picture(LOCAL_FILE_URL, pic_path=screenshot_path)
                    return reply
                else:
                    return Error("制作精品评论发生错误...", urge=self.get_name())

                # 不输出
                return Error("")
            
            elif cmd_args[0] == AVATAR_COMMAND:
                if len(cmd_args) != 2:
                    return Error("参数个数不对!", urge=self.get_name())
                
                if message.quote is None or message.quote.pic is None:
                    return Error("头像上传缺少引用的图片!", urge=self.get_name())
                
                save_image(message.quote.pic.pic_bytes, file_name=AVATAR_DIR + cmd_args[1] + AVATAR_FORMAT)
                return Message("头像上传成功!")
            
            elif cmd_args[0] == TAG_STAR:
                if len(cmd_args) < 2 or len(cmd_args) > 3:
                    return Error("参数个数不对!", urge=self.get_name())
                
                if message.quote is None:
                    return Error("制作精选评论缺少引用!", urge=self.get_name())
                
                star_author = cmd_args[1]
                if len(cmd_args) == 2:
                    star_time = datetime.datetime.now().strftime(DATE_FORMAT)
                else:
                    star_time = cmd_args[2]

                error = self.database.new([TagPair(TAG_STAR, Message("{}({})".format(star_author, star_time)), 0), TagPair(TAG_CM, message.quote, 0)])

                if isinstance(error, Error):
                    return error
                        
                return Message("设精成功!")

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
    

