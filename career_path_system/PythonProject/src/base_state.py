class BaseState:
    def __init__(self):
        self.logs = []
        self.refused = False
        self.refusal_reason = None


    def log(self, message):
        self.logs.append(message)


    def refuse(self, reason, reference=None):
        self.refused = True
        self.refusal_reason = reason
        self.log(f'Refused: {reason}')
        if reference:
            self.log(f"Refusal reference: {reference}")


    def check_invariant(self, condition, message, reference=None):
        if not condition:
            self.refuse(message,reference)

    def assert_trust(self):
        if self.refused:
            raise RuntimeError(f"Refusal reason: {self.refusal_reason} ")

    def require_trust(func):
        def wrapper(self, *args, **kwargs):
            self.assert_trust()
            return func(self, *args, **kwargs)
        return wrapper