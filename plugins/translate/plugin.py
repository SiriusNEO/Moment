IMPORT_FLAG = True
try:
    from googletrans import Translator
except:
    IMPORT_FLAG = False

from plugins.translate.plugin_doc import PLUGIN_DOC
from plugins.translate.plugin_config import *

from core.plugin import *

class Translate_Plugin(Plugin):

    def __init__(self):
        super().__init__(
                name = "Translate",
                requirements = [], 
                info = "翻译器",
                doc = PLUGIN_DOC
            )
    
    def setup(self):
        if not IMPORT_FLAG:
            raise Exception("翻译插件缺少关键库: googletrans")
        super().setup()
    

    def handle_message(self, message: Message) -> Union[Message, List[Message], Error]:
        assert self._setup_flag

        if message.quote is None or message.quote.text is None:
            return Error("缺少引用的内容")

        if message.text is not None:
            reply = Message()

            if len(message.text) == 3 and message.text[1] == TRANS_COMMAND:
                if not message.text[0] in LANG:
                    return Error("未知语种: {}".format(message.text[0]), urge=self.get_name())
                elif not message.text[2] in LANG:
                    return Error("未知语种: {}".format(message.text[2]), urge=self.get_name())
                
                src_text = message.quote.text
                src_lang = LANG_MAP[message.text[0]]
                dest_lang = LANG_MAP[message.text[2]]
                translater = Translator()
                reply.text = translater.translate(src_text, src=src_lang, dest=dest_lang).text
                return reply

        return Error("命令不满足该插件")