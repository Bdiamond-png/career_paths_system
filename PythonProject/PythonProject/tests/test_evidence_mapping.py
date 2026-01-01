import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from evidence_mapping import EvidenceMapping

def test_confidence_score_with_evidence():
    claims = [
        {"text": "Built API", "evidence": ["github"]},
        {"text": "Knows ML", "evidence": []}
    ]

    mapper = EvidenceMapping(claims)
    score, evidence = mapper.generate_confidence_score()

    assert score == 0.5
    assert len(evidence) == 1