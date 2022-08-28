from core.message import Message
from core.image import *
from core.core_config import LOCAL_FILE_URL
from graia.application.message.chain import MessageChain
from graia.application import GraiaMiraiApplication
from graia.application.message.elements.internal import Plain, Image, Quote, At, Source

from frontend.frontend_config import CONFIG

"""
    graia message to moment message
"""
async def graia2moment(app: GraiaMiraiApplication,
                       graia_chain: MessageChain,
                       sender: int) -> Message:
    
    message = Message()

    message.sender = sender

    if graia_chain.has(Plain):
        message.text = graia_chain.get(Plain)[0].asDisplay().strip(' ')
    else:
        message.text = ""

    if graia_chain.has(Image):
        image = graia_chain.get(Image)[0]
        
        pic_bytes = await Image.http_to_bytes(Image(), image.url)
        message.pic = Picture(image.url, pic_bytes = pic_bytes)

    if graia_chain.has(Quote):
        quote_id = graia_chain.get(Quote)[0].origin.get(Source)[0].id
        try:
            quote_message = await app.messageFromId(quote_id)
        except:
            pass
        else:
            message.quote = await graia2moment(app, quote_message.messageChain, quote_message.sender)
    
    if graia_chain.has(At):
        message.at = graia_chain.get(At)[0].target
    
    return message

"""
    moment message to graia message
"""
async def moment2graia(app: GraiaMiraiApplication, message: Message) -> MessageChain:    
    chain_list = []

    if message.at is not None:
        # At fails in this version
        # chain_list.append(At(message.at)) 
        member_info = await app.getMemberInfo(message.at, CONFIG.get("working-group", prefix="graia-v4"))
        chain_list.append(Plain("@" + member_info.name + " "))

    if message.text != None:
        chain_list.append(Plain(message.text))
    
    if message.pic is not None:
        if message.pic.pic_url != None and message.pic.pic_url != LOCAL_FILE_URL:
            chain_list.append(Image.fromUnsafeAddress(message.pic.pic_url))
        else:
            chain_list.append(Image.fromLocalFile(message.pic.pic_path))

    return MessageChain.create(chain_list)
