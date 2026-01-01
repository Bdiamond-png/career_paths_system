from base_state import BaseState

from datetime import datetime, timezone

class Evaluation(BaseState):
    def __init__(self):
        super().__init__()
        self.records = []

    def record(self, state_name, status, details=None):
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "state": state_name,
            "status": status,
            "details": details
        }
        self.records.append(entry)
        self.log(f"Evaluation record added: {entry}")

    def summarize(self):
        return {
            "total_events": len(self.records),
            "failures": [r for r in self.records if r["status"] == "refused"],
            "successes": [r for r in self.records if r["status"] == "passed"]
        }