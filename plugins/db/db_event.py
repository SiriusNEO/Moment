from core.message import Message

class TagPair:

    tag: str
    val: object

    # 使用 ASSIGN (see plugin_config) 的下标代表不同类型
    typ: int

    def __init__(self, tag, val, typ):
        self.tag = tag
        self.val = val
        self.typ = typ

    def __repr__(self):
        return "<tag: {0}, val: {1}, typ: {2}>".format(self.tag, self.val, self.typ)

"""
    The basic class of event
"""
class BaseDatabaseEvent:

    quote: "Message"
    ...

"""
    New event
"""
class NewEvent(BaseDatabaseEvent):
    """
        modifies: list (a list of TagPair)
    """

    def __init__(self):
        super()
        self.modifies = list()

    def tell(self):
        print("new event")
        print("modifies list: ", self.modifies)

"""
    Query event
"""
class QueryEvent(BaseDatabaseEvent):
    """
        indices: list (a list of TagPair)
        target_tag: str (get the content of the target tag)
    """

    def __init__(self):
        super()
        self.indices = list()
        self.target_tag = None
    
    def tell(self):
        print("query event")
        print("indices list: ", self.indices)
        print("target_tag: ", self.target_tag)

"""
    Modify event
"""
class ModifyEvent(BaseDatabaseEvent):

    """
        indices: list (a list of TagPair)
        modifies: list (a list of TagPair)
        target_tag: str (modify the tag. Only support word modify)
        word: str (special modifty word)
    """

    def __init__(self):
        super()
        self.indices = list()
        self.modifies = list()
        self.target_tag = None
        self.word = None

    def tell(self):
        print("modifies event")
        print("indices list: ", self.indices)
        print("modifies list: ", self.modifies)
        print("target_tag: ", self.target_tag)
        print("word: ", self.word)

"""
    Commit Event
"""
class CommitEvent(BaseDatabaseEvent):
    ...

"""
    Backup Event
"""
class BackupEvent(BaseDatabaseEvent):
    ...