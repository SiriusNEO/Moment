from plugins.word.plugin import Word_Plugin

from core.error import Error
from core.message import Message

word_plugin = Word_Plugin()
word_plugin.setup()

reply = word_plugin.handle_message(Message("来10个词"))

if isinstance(reply, Error):
    print(reply.what)
else:
    assert isinstance(reply, Message)
    print(reply.text)