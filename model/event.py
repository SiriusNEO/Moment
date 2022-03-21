from model.message import Message

class TagPair:

    tag: str
    val: object

    # 使用 ASSIGN (see event_config) 的下标代表不同类型
    typ: int

    def __init__(self, tag, val, typ):
        self.tag = tag
        self.val = val
        self.typ = typ

    def __repr__(self):
        return "<tag: {0}, val: {1}, typ: {2}>".format(self.tag, self.val, self.typ)

class BaseEvent:

    quote: "Message"

    def __init__(self):
        pass
    
    def tell(self):
        pass

class NewEvent(BaseEvent):

    target_db: str

    # a list of TagPair
    modifies: list

    def __init__(self):
        super()
        self.target_db = None
        self.modifies = list()

    def tell(self):
        print("new event")
        print("modifies list: ", self.modifies)

class QueryEvent(BaseEvent):

    target_db: str
    
    # a list of TagPair
    indices: list

    def __init__(self):
        super()
        self.target_db = None
        self.indices = list()
    
    def tell(self):
        print("query event")
        print("indices list: ", self.indices)

class ModifyEvent(BaseEvent):

    target_db: str

    # a list of TagPair
    indices: list
    
    # a list of TagPair
    modifies: list 

    # special modifty word
    word: str

    def __init__(self):
        super()
        self.target_db = None
        self.indices = list()
        self.modifies = list()
        self.word = None

    def tell(self):
        print("modifies event")
        print("indices list: ", self.indices)
        print("modifies list: ", self.modifies)
        print("word: ", self.word)

