from core.message import Message
from core.bot import Bot
from core.user import User
from core.image import Picture, load_image
from core.core_config import LOCAL_FILE_URL

import asyncio
import queue
import re

from frontend.frontend_config import SEND_WAIT

from utils.log import Log

from typing import Union, List

AT_REGEX = "@(\S)+\s"
IMAGE_REGEX = "\{pic:\S+\}"  # {pic:path}
QUOTE_REGEX = "\{quote:\S+\}" # {quote:number}


"""
    talking in shell.
"""
class ChatRoom():

    def __init__(self, your_name: str, bot: Bot, input_offset: int):
        self.your_name = your_name
        self.bot = bot
        self.input_offset = input_offset
        self.message_queue = queue.Queue()
        self.message_record = []
        self.loop = asyncio.get_event_loop()
        self._increment = 0


    def __del__(self):
        self.loop.close()


    """
        run and blocking
    """
    def run(self):
        self.loop.run_until_complete(self.input_and_flush())


    async def input_and_flush(self):
        print("------------ Moment ChatRoom ------------")

        while True:
            raw_input = input(" " * self.input_offset + "({}) >>> ".format(self.your_name)).strip()
            if len(raw_input) > 0:
                user_message = Message()
                
                at_match = re.match(AT_REGEX, raw_input)
                if at_match:
                    left = at_match.span()[0]
                    right = at_match.span()[1]
                    at_literal = raw_input[left:right][1:]
                    user_message.at = User(uid=at_literal, name="")
                    raw_input = raw_input[:left] + raw_input[right:]
                
                img_match = re.match(IMAGE_REGEX, raw_input)
                if img_match:
                    left = img_match.span()[0]
                    right = img_match.span()[1]
                    img_literal = raw_input[left+5:right-1]
                    try:
                        user_message.pic = Picture(LOCAL_FILE_URL, pic_bytes=load_image(img_literal))
                    except:
                        Log.error("error in load picture from local: {}".format(img_literal))
                        user_message.pic = None
                    raw_input = raw_input[:left] + raw_input[right:]
                
                quote_match = re.match(QUOTE_REGEX, raw_input)
                if quote_match:
                    left = quote_match.span()[0]
                    right = quote_match.span()[1]
                    quote_literal = raw_input[left+7:right-1]
                    try:
                        if not str.isdigit(quote_literal):
                            Log.error("error in load quote: not a number: {}".format(quote_literal))
                            raise Exception("")
                        quote_no = int(quote_literal)
                        if quote_no < 0 or quote_no >= self._increment:
                            Log.error("error in load quote: no such message: {}".format(quote_literal))
                            raise Exception("")
                    except:
                        user_message.quote = None
                    else:
                        user_message.quote = self.message_record[quote_no].copy()

                    raw_input = raw_input[:left] + raw_input[right:]


                user_message.text = raw_input
                user_message.sender = User(uid="0", name=self.your_name)
                self.add_message(user_message)
                await self.bot.handle_message(user_message)
            
            # flush
            # Log.info(self.message_queue.qsize())
            if not self.message_queue.empty():
                message, message_id = self.message_queue.get() # eat
                print("[{}] {}: {}".format(str(message_id), message.sender.name, message.to_readable_str(limit=False)))

    """
        add new message
    """
    def add_message(self, message: Message):
        self.message_queue.put([message, self._increment])
        self.message_record.append(message)
        self._increment += 1
    

    async def send_message(self, message: Union[Message, List[Message]]):
        # Log.info("send", message.to_readable_str())

        if isinstance(message, list):
            for single_message in message:
                await self.send_message(single_message)
                await asyncio.sleep(SEND_WAIT)
            return
        
        message.sender = User(uid="1", name=self.bot.name)
        self.add_message(message)
        
