# 基础错误

class Error:
    what: str

    def __init__(self, what):
        self.what = what