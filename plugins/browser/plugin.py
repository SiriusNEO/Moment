IMPORT_FLAG = True
try:
    from playwright.async_api import async_playwright
except:
    IMPORT_FLAG = False

from plugins.browser.plugin_doc import PLUGIN_DOC
from plugins.browser.plugin_config import *
from plugins.browser.basic_browser import BrowserManager

from core.plugin import *
from core.bot import Bot

from utils.log import Log

from core.image import *

class Browser_Plugin(Plugin):

    def __init__(self):
        super().__init__(
                name = "Browser",
                requirements = [], 
                info = "简单的浏览器功能",
                doc = PLUGIN_DOC
            )
    

    def setup(self, bot: Bot):
        if not IMPORT_FLAG:
            raise Exception("浏览器插件缺少关键库: playwright")
        super().setup(bot)

        self.task_queue = []
        self.task_lock = False
        self.task_cnt = 0
    

    async def handle_message(self, message: Message) -> Union[Message, List[Message], Error]:
        assert self._setup_flag

        if message.text is not None:
            cmd_args = message.text.split(" ")

            if cmd_args[0] == BROWSER_COMMAND:
                if len(cmd_args) != 2:
                    return Error("参数个数不对!")
                
                try:
                    async with async_playwright() as pw:
                        async with BrowserManager(pw, 1080, 720) as page:
                            await page.goto(cmd_args[1])
                            screenshot = await page.screenshot(timeout=1000)
                except:
                    return Error("奇怪的浏览错误发生了...", urge=self.get_name())

                if isinstance(screenshot, bytes):
                    screenshot_path = save_image(screenshot, file_name=TMP_FILENAME)
                    reply = Message()
                    reply.pic = Picture(LOCAL_FILE_URL, pic_path=screenshot_path)
                    return reply
                else:
                    return Error("哦哟，崩溃啦", urge=self.get_name())
        
        return Error("命令格式不符此插件!")

                
    

