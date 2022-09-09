"""
    Message For Moment
"""

class Message:
    
    """

        text:       str
        pic:        Picture
        quote:      Message
        at:         int
        sender:     int
    """
    def __init__(self, text = None):
        
        # set None now
        self.text = text
        self.pic = None
        self.quote = None
        self.at = None
        self.sender = None

    def __eq__(self, other: "Message"):
        if self is None or other is None:
            return False

        if self.text != other.text:
            return False
        
        if not self.pic == other.pic:
            return False

        if not self.quote == other.quote:
            return False
        
        if self.at != other.at:
            return False

        return True
    
    def __str__(self):
        return self.to_readable_str()

    def to_hash_str(self):
        if self.pic is None:
            return self.text + "|"
        return self.text + "|" + str(self.pic.pic_bytes)
    
    def to_readable_str(self):
        ret = str()

        if self.text != None:
            if len(self.text) > 8:
                ret += self.text[:8] + "..."
            else:
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
        
        if ret == "":
            return "空"

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
    
    def copy(self):
        ret = Message()
        ret.text = self.text
        
        if self.pic is not None:
            ret.pic = self.pic.copy()
        else:
            ret.pic = None

        ret.quote = self.quote
        ret.at = self.at
        ret.sender = self.sender
        return ret