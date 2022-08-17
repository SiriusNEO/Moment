from model.message import Message
from model.error import Error

from plugins.db.database import Database_Plugin
from plugins.replier.replier import Replier_Plugin

dp_plugin = Database_Plugin()
rep_plugin = Replier_Plugin()

dp_plugin.setup()
rep_plugin.setup(dp_plugin.database)

while True:
    test_msg = Message()
    test_msg.text = input()

    reply = dp_plugin.handle_message(test_msg)

    if type(reply) == Error:
        print("error: ", reply.what)
    else:
        reply.display()
