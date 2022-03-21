from event.cmd_parser import database_cmd_parse
from model.message import Message
from db.db_scheduler import *
from model.error import Error

while True:
    test_msg = Message()
    test_msg.text = input()

    event = database_cmd_parse(test_msg)

    event.tell()

    reply = db_event_handle(event)

    if type(reply) == Error:
        print("error: ", reply.what)
    else:
        reply.display()
