from core.message import Message
from core.image import *
from graia.application.message.chain import MessageChain
from graia.application import GraiaMiraiApplication
from graia.application.message.elements.internal import Plain, Image, Quote, At, Source

"""
    graia message to moment message
"""
async def graia2moment(app: GraiaMiraiApplication,
                       graia_chain: MessageChain,
                       sender: int):
    
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
async def moment2graia(message: Message):

    chain_list = list()

    if message.text != None:
        chain_list.append(Plain(message.text))
    
    if message.pic is not None:
        if message.pic.pic_url != None:
            chain_list.append(Image.fromUnsafeAddress(message.pic.pic_url))

    return MessageChain.create(chain_list)
