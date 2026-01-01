class BaseState:
    def __init__(self):
        self.logs = []
        self.refused = False
        self.refusal_reason = None


    def log(self, message):
        self.logs.append(message)


    def refuse(self, reason):
        self.refused = True
        self.refusal_reason = reason


    def check_invariant(self, condition, message):
        if not condition:
            self.refuse(message)