from core.message import Message
from core.image import *
from core.user import User
from core.core_config import LOCAL_FILE_URL

from utils.log import Log

import aiocqhttp

from frontend.frontend_config import CONFIG, TIMEOUT

import aiohttp

"""
    cqhttp message to moment message
"""
async def cqhttp2moment(cqhttp: aiocqhttp.CQHttp, cqmessage: aiocqhttp.Message, sender) -> Message:
    message = Message()

    message.sender = User(str(sender['user_id']), sender['nickname'])

    for message_seg in cqmessage:
        if message_seg.type == "text" and message.text is None:
            message.text = message_seg.data["text"].strip()
        
        if message_seg.type == "image" and message.pic is None:
            url = message_seg.data["url"]
            timeout = aiohttp.ClientTimeout(total=TIMEOUT)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                try:
                    res = await session.get(url)
                    pic_bytes = await res.read()
                except:
                    pic_bytes = None
                
            message.pic = Picture(url, pic_bytes=pic_bytes)
        
        if message_seg.type == "reply" and message.quote is None:
            reply_id = message_seg.data["id"]
            try:
                reply = await cqhttp.call_action("get_msg", message_id=reply_id)
                cq_reply_msg = aiocqhttp.Message()
                cq_reply_msg.extend(reply["message"])
            except:
                Log.error("cq get reply error")
                pass
            else:
                message.quote = await cqhttp2moment(cqhttp, cq_reply_msg, reply["sender"])
        
        if message_seg.type == "at" and message.at is None:
            message.at = User(str(message_seg.data["qq"]), "")
    
    return message


"""
    moment message to cqhttp message
"""
async def moment2cqhttp(message: Message) -> aiocqhttp.Message:
    cqmessage = aiocqhttp.Message()

    if message.at is not None:
        cqmessage.append(aiocqhttp.MessageSegment.at(message.at.uid))

    if message.text is not None:
        cqmessage.append(aiocqhttp.MessageSegment.text(message.text))
    
    if message.pic is not None:
        if message.pic.pic_url != None and message.pic.pic_url != LOCAL_FILE_URL:
            cqmessage.append(aiocqhttp.MessageSegment.image(message.pic.pic_url))
        else:
            abs_path = path.dirname(__file__) + "/../../" + message.pic.pic_path
            cqmessage.append(aiocqhttp.MessageSegment.image("file://" + abs_path))
    
    return cqmessage