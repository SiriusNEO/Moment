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
        return self.uid == other.uid