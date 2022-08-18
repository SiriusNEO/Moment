# 基础错误

class Error:
    
    """
        # Error info
        what: str

        # if urge is a plugin name, reply with this Error
        urge: str
    """
    def __init__(self, what, urge=None):
        self.what = what
        self.urge = urge