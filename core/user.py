"""
    Refering to a "User" in a chatting platform.
"""


class User:

    """
        uid: str    (some platform may not be pure number)
        name: str
    """

    def __init__(self, uid = "", name = ""):
        self.uid = uid
        self.name = name

    
    def __eq__(self, other: "User"):
        if self is None and other is None:
            return True

        if self is None or other is None:
            return False
        
        return self.uid == other.uid