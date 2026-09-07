class FleshError(Exception):
    def __init__(self):
        pass


class FleshSyntaxError(FleshError):
    def __init__(self, text: str, at: int, msg: str):
        self.text = text
        self.at = at
        self.msg = msg
