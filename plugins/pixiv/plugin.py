from core.plugin import *
from core.bot import Bot

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

    @check_setup
    async def handle_message(self, message: Message) -> Union[Message, List[Message], Error]:
        if message.text is not None:
            cmd_args = message.text.split(" ")
            
            if len(cmd_args) > 2:
                return Error("参数个数错误")
            
            if cmd_args[0] in FETCH_COMMAND:
                if len(cmd_args) == 1:
                    url = API_URL + "/?san={}".format(SAN)
                else:
                    url = API_URL + "/get/tags/{}?san={}".format(cmd_args[1], SAN)
                
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
                                return reply
                            else:
                               return Error("pixiv 服务获取图片时失败...", urge=self.get_name())
                        else:
                            return Error("pixiv 服务连接失败...", urge=self.get_name())
                    except Exception as e:
                        return Error("唔 发生奇怪错误: {}".format(e.args), urge=self.get_name())

        return Error("命令不满足该插件")
                    