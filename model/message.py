"""
    Message For Moment
"""

import json

class Picture:
    pic_url: str
    pic_path: str
    pic_bytes: bytes

    def __init__(self, pic_url: str, pic_path = None, pic_bytes = None):
        self.pic_url = pic_url
        self.pic_path = pic_path
        self.pic_bytes = pic_bytes
    
    def __eq__(self, other: "Picture"):
        if self is None and other is None:
            return True

        if self is None or other is None:
            return False
        
        # use url now
        return self.pic_bytes == other.pic_bytes
        

class Message:
    text:       str
    pic:        "Picture"
    quote:      "Message"
    at:         int
    sender:     int

    def __init__(self):
        
        # set None now
        self.text = None
        self.pic = None
        self.quote = None
        self.at = None
        self.sender = None

    def __eq__(self, other: "Message"):
        if self is None or other is None:
            return False

        if self.text != other.text:
            return False
        
        if self.pic != other.pic:
            return False

        if self.quote != other.quote:
            return False
        
        if self.at != other.at:
            return False

        return True
    
    def msg_2_str(self):
        ret = str()
        if self.text != None:
            ret += self.text
        
        if self.pic != None:
            if len(ret) > 0:
                ret += "|"
            ret += "图"
        
        if self.quote != None:
            if len(ret) > 0:
                ret += "|"
            ret += "引"
        
        if self.at != None:
            if len(ret) > 0:
                ret += "|"
            ret += "@"
            
        return ret
    
    def display(self):
        print("[moment message] ", self)

        if self.text != None:
            print("   > it has text = ", self.text)

        if self.pic != None:
            print("   > it has pic, url = ", self.pic.pic_url)

        if self.quote != None:
            print("   > it has quote. show its quote now.\n")
            self.quote.display()
    
    def parse_to_JSONable(self):
        if self.pic is None:
            return {"__msghead__": "", "text": self.text, "pic": None}
        return {"__msghead__": "", "text": self.text, "pic": self.pic.pic_url}
    
    @staticmethod
    def parse_from_JSONable(JSONable):
        ret = Message()
        ret.text = JSONable["text"]
        if JSONable["pic"] is None:
            ret.pic = None
        else:
            ret.pic = Picture(JSONable["pic"])
        return ret

class MessageJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Message):
            return obj.parse_to_JSONable()
        return json.JSONEncoder.default(self, obj)

def decode_hook(obj):
    if isinstance(obj, dict):
        if "__msghead__" in obj:
            return Message.parse_from_JSONable(obj)
        return obj