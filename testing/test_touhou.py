from plugins.touhou.plugin import Touhou_Plugin
from core.message import Message
from core.error import Error

plugin = Touhou_Plugin()
plugin.setup()

while True:
    test_msg = Message()
    test_msg.text = input()

    reply = plugin.handle_message(test_msg)

    if type(reply) == Error:
        print("error: ", reply.what)
    else:
        reply.display()