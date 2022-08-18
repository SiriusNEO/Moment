from frontend.mirai.frontend_config import IMG_PATH
from core.message import Message

import json

from utils.rand_tool import random_str

tmp_file_name = "tmp"

"""
    Load an image.
"""
def load_image(path: str) -> bytes:
    fp = open(path, "rb")
    return bytes(fp.read())


"""
    Save an image. Return its path.
"""
def save_image(data: bytes, file_name=tmp_file_name) -> str:
    path = IMG_PATH + file_name
    fp = open(path, "wb")
    fp.write(data)
    fp.close()
    return path


class Picture:
    
    """
        Three storage approach:
        - pic_url: str
        - pic_bytes: bytes
        - pic_path: str
    """
    def __init__(self, pic_url: str, pic_path = None, pic_bytes = None):
        self.pic_url = pic_url
        self.pic_path = pic_path
        self.pic_bytes = pic_bytes
    
    def __eq__(self, other: "Picture"):
        if self is None and other is None:
            return True

        if self is None or other is None:
            return False
        
        return self.pic_bytes == other.pic_bytes


def parse_to_JSONable(msg: Message):
        if msg.pic is None:
            return {"__msghead__": "", "text": msg.text, "pic_url": None, "pic_path": None}
        
        pic_fn = random_str()
        pic_path = save_image(msg.pic.pic_bytes, pic_fn)
        return {"__msghead__": "", "text": msg.text, "pic_url": msg.pic.pic_url, "pic_path": pic_path}


def parse_from_JSONable(JSONable):
    ret = Message()
    ret.text = JSONable["text"]
    if JSONable["pic_url"] is None:
        ret.pic = None
    else:
        ret.pic = Picture(JSONable["pic_url"], 
                            pic_path = JSONable["pic_path"],
                            pic_bytes = load_image(JSONable["pic_path"]))
    return ret


class MessageJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Message):
            return parse_to_JSONable(obj)
        return json.JSONEncoder.default(self, obj)


def decode_hook(obj):
    if isinstance(obj, dict):
        if "__msghead__" in obj:
            return parse_from_JSONable(obj)
        return obj
