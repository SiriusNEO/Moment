from core.plugin import *
from core.bot import Bot

from core.image import save_image, Picture
from core.core_config import LOCAL_FILE_URL

from plugins.ps.plugin_config import *
from plugins.ps.plugin_doc import PLUGIN_DOC

import re

IMPORT_FLAG = True
try:
    from PIL import Image as PIL_IM
except:
    IMPORT_FLAG = False

class PS_Plugin(Plugin):

    def __init__(self):
        super().__init__(
                name = "PS",
                requirements = [], 
                info = "云图片处理插件",
                doc = PLUGIN_DOC
            )

    def setup(self, bot: Bot):
        if not IMPORT_FLAG:
            raise Exception("ps插件缺少关键库: Pillow")
        super().setup(bot)

    async def handle_message(self, message: Message) -> Union[Message, List[Message], Error]:
        assert self._setup_flag

        if message.text is not None:
            cmd_args = message.text.split(" ")
            
            if len(cmd_args) == 2 and cmd_args[0] == PS_COMMAND:
                reply = Message()
                if message.quote is None or message.quote.pic is None:
                    return Error("找不到引用的图片", urge=self.get_name())
                if message.quote.pic.pic_bytes is None:
                    return Error("图片损坏", urge=self.get_name())

                pic_path = save_image(message.quote.pic.pic_bytes, file_name=TMP_FILENAME)
                print(pic_path)
                pil_img = PIL_IM.open(pic_path)
                
                if re.match(ROTATE_PATTERN, cmd_args[1]) is not None:
                    angle = int(cmd_args[1][1:])
                    if angle < 0 or angle >= 360:  
                        return Error("角度请在[0, 360)内", urge=self.get_name())
                    pil_img = pil_img.rotate(angle)
                elif cmd_args[1] == ARG_BW:
                    pil_img = pil_img.convert("L")
                elif cmd_args[1] == ARG_UD:
                    pil_img = pil_img.transpose(PIL_IM.FLIP_TOP_BOTTOM)
                elif cmd_args[1] == ARG_LR:
                    pil_img = pil_img.transpose(PIL_IM.FLIP_LEFT_RIGHT)
                else:
                    return Error("未知的变换", urge=self.get_name())
                
                pil_img.save(pic_path)
                
                reply = Message()
                reply.pic = Picture(LOCAL_FILE_URL, pic_path=pic_path)
                return reply

        return Error("命令不满足该插件")