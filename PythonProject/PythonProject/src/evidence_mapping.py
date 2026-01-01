from base_state import BaseState

class EvidenceMapping(BaseState):
    def __init__(self, claims):
        super().__init__()
        self.raw_claims = claims
        self.verified_evidence = []
        self.confidence_score = 0.0


    def verify_claim(self, claim):
        return bool(claim.get("evidence"))

    def generate_confidence_score(self):
        self.verified_evidence = [
            claim for claim in self.raw_claims
            if self.verify_claim(claim)
        ]

        if not self.verified_evidence:
            self.check_invariant(False, "No evidence found")
            return None
        total_claims = len(self.raw_claims)
        verified_count = len(self.verified_evidence)
        self.confidence_score = verified_count / total_claims

        self.log(f"confidence score calculated: {self.confidence_score:.2f}")
        return self.confidence_score, self.verified_evidence
