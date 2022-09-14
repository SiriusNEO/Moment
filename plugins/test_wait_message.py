from core.plugin import *
from core.bot import Bot


class Test_Plugin(Plugin):

    def __init__(self):
        super().__init__(
                name = "Test",
                requirements = [], 
                info = "仅测试用",
                doc = "没有文档"
            )

    def setup(self, bot: Bot):
        self.bot = bot
        super().setup(bot)
    

    async def handle_message(self, message: Message) -> Union[Message, List[Message], Error]:
        assert self._setup_flag

        if message.text is not None and message.text == "第一句话":
            await self.send("说第二句话")
            await self.wait_message(checker=(lambda x: x.text=="第二句话"))
            return Message("行")
        
        return Error("")
            