from core.core_config import *
from core.message import Message

import json
import os

from utils.rand_tool import random_str

"""
    Load an image.
"""
def load_image(path: str) -> bytes:
    fp = open(path, "rb")
    return bytes(fp.read())


"""
    Save an image. Return its path.
"""
def save_image(data: bytes, file_name=TMP_FILENAME) -> str:
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
            return {MSGHEAD_SYMBOL: "", "text": msg.text, "pic_url": None, "pic_path": None}
        if msg.pic.pic_path is None:
            path = IMG_PATH + PIC_NUM_FN
        
            if not os.path.exists(path):
                with open(path, "w") as f:
                    f.write("0")
            
            with open(path, "r+") as f:
                total_pic_num = int(f.read())
                total_pic_num += 1
                pic_fn = str(total_pic_num)
                pic_path = save_image(msg.pic.pic_bytes, pic_fn)
                f.seek(0)
                f.write(str(total_pic_num))
            
            return {MSGHEAD_SYMBOL: "", "text": msg.text, "pic_url": msg.pic.pic_url, "pic_path": pic_path}
        return {MSGHEAD_SYMBOL: "", "text": msg.text, "pic_url": msg.pic.pic_url, "pic_path": msg.pic.pic_path}


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
        if MSGHEAD_SYMBOL in obj:
            return parse_from_JSONable(obj)
        return obj
