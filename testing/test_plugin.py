from core.message import Message
from core.error import Error

from plugins.db.plugin import Database_Plugin
from plugins.replier.plugin import Replier_Plugin
from plugins.help.plugin import Help_Plugin

dp_plugin = Database_Plugin()
rep_plugin = Replier_Plugin()

dp_plugin.setup()
rep_plugin.setup(dp_plugin.database)

installed_plugins = [dp_plugin, rep_plugin]

while True:
    test_msg = Message()
    test_msg.text = input()

    for plugin in installed_plugins:
        reply = plugin.handle_message(test_msg)

        if isinstance(reply, Error):
            print("error: ", reply.what)
        elif isinstance(reply, list):
            print("list: ", reply)
        else:
            reply.display()
