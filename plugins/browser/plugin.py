IMPORT_FLAG = True
try:
    from playwright.async_api import async_playwright
except:
    IMPORT_FLAG = False

from plugins.browser.plugin_doc import PLUGIN_DOC
from plugins.browser.plugin_config import *
from plugins.browser.basic_browser import BrowserManager

from core.plugin import *
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
    

    def setup(self):
        if not IMPORT_FLAG:
            raise Exception("浏览器插件缺少关键库: playwright")
        super().setup()

        self.task_queue = []
        self.task_lock = False
        self.task_cnt = 0
    

    def handle_message(self, message: Message) -> Union[Message, List[Message], Error]:
        assert self._setup_flag

        if message.text is not None:
            cmd_args = message.text.split(" ")

            if cmd_args[0] == BROWSER_COMMAND:
                if len(cmd_args) != 2:
                    return Error("参数个数不对!")
                
                self.task_lock = True
                self.task_queue.append(cmd_args[1])
                self.task_lock = False

                return Message("正在浏览中, 别急喵")
        
        return Error("命令格式不符此插件!")
    

    async def plugin_task(self, send_method):

        while True:
            await asyncio.sleep(WAIT)

            if self.banned:
                self.task_queue = []
                continue
            
            if not self.task_lock and len(self.task_queue) > 0:
                task = self.task_queue[0]
                self.task_queue.remove(task)

                Log.info("browser task:", task)

                try:
                    async with async_playwright() as pw:
                        async with BrowserManager(pw, 1080, 720) as page:
                            await page.goto(task)
                            screenshot = await page.screenshot(timeout=1000)
                except:
                    await send_method(Message("奇怪的浏览错误发生了..."))
                    continue

                if isinstance(screenshot, bytes):
                    screenshot_path = save_image(screenshot, file_name=TMP_FILENAME)
                    reply = Message()
                    reply.pic = Picture(LOCAL_FILE_URL, pic_path=screenshot_path)
                    await send_method(reply)
                else:
                    await send_method(Message("哦哟，崩溃啦"))
    

