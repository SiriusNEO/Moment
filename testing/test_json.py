from model.message import *


msg = Message()
msg.text = "233"
dick = {"me": msg}

"""
with open("test", "w") as fp:
    json.dump(dick, fp, cls=MessageJSONEncoder)
"""

with open("test", "r") as fp:
    dick = json.load(fp, object_hook=decode_hook)

print(dick["me"].display())