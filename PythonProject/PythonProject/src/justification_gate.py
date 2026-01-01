from base_state import BaseState


class JustificationGate(BaseState):

    def __init__(self, confidence_score, evidence):
        super().__init__()
        self.confidence_score = confidence_score
        self.evidence = evidence


    def verify_justification(self):
        if not self.evidence:
            self.check_invariant(False, "no evidence found")
            self.refuse('confidence score cannot be justified')
            return False

        if not (0.0 <= self.confidence_score <= 1.0):
            self.check_invariant(False, "confidence score out of bounds")
            self.refuse('confidence score is invalid')
            return False
        self.log('confidence score verified')
        return True