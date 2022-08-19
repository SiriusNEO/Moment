from core.plugin import *

from plugins.pixiv.plugin_config import *
from plugins.pixiv.plugin_doc import PLUGIN_DOC

from core.image import *

import aiohttp

class Pixiv_Plugin(Plugin):

    def __init__(self):
        super().__init__(
                name = "Pixiv",
                requirements = [], 
                info = "P站图片搬运",
                doc = PLUGIN_DOC
            )

    def setup(self):
        self.task_queue = []
        self.task_lock = False
        self.task_cnt = 0
        super().setup()

    def handle_message(self, message: Message) -> Union[Message, List[Message], Error]:
        assert self._setup_flag

        if message.text is not None:
            cmd_args = message.text.split(" ")
            
            if len(cmd_args) > 2:
                return Error("参数个数错误")
            
            if cmd_args[0] in FETCH_COMMAND:
                # query with tag
                self.task_lock = True
                if len(cmd_args) == 2:
                    self.task_queue.append([self.task_cnt, cmd_args[1]])
                # no tag
                else:
                    self.task_queue.append([self.task_cnt])
                self.task_lock = False
                return Message("正在获取ing, 别急")

        return Error("命令不满足该插件")
    

    async def plugin_task(self, send_method):

        while True:
            await asyncio.sleep(WAIT)

            if self.banned:
                continue
            
            if not self.task_lock and len(self.task_queue) > 0:
                task = self.task_queue[0]
                self.task_queue.remove(task)

                if len(task) == 1:
                    url = API_URL + "/?san={}".format(SAN)
                else:
                    url = API_URL + "/get/tags/{}?san={}".format(task[1], SAN)
                
                timeout = aiohttp.ClientTimeout(total=TIMEOUT)
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    try:
                        res = await session.get(url)
                        content = eval(await res.text())
                        
                        if "code" in content and content["code"] == 200:
                            pic_id = content["data"]['imgs'][0]["id"]
                            author = [content["data"]['imgs'][0]["userid"], content["data"]['imgs'][0]["username"]]
                            pic_url = content["data"]['imgs'][0]["url"]
                            tags = content["data"]['imgs'][0]["tags"]
                            
                            res = await session.get(pic_url)
                            img = await res.read()
                            if isinstance(img, bytes):
                                pic_path = save_image(img, file_name=TMP_FILENAME)
                                reply = Message()
                                reply.text = "[Moment Pixiv 图片服务]\nid: {}\n作者: {}({})\nurl: {}\ntags: {}\n\n".format(pic_id, author[1], author[0], pic_url, tags)
                                reply.pic = Picture(pic_url, pic_path=pic_path)
                                await send_method(reply)
                            else:
                                await send_method(Message("pixiv 服务获取图片时失败..."))
                        else:
                            await send_method(Message("pixiv 服务连接失败..."))
                    except asyncio.TimeoutError:
                        await send_method(Message("唔 网络连接挂掉啦, 连接超时"))
                    