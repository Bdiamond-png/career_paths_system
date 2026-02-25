from justification_gate import (
    JustificationGate,
    EvidenceBinding,
    Evidence,
    Claim,
    TrustState
)


class TestJustificationGate:

    def test_justification_success(self):
        binding = EvidenceBinding(
            claim=Claim(description="Data is complete and aligned"),
            evidence=[Evidence(payload={"a": 1, "b": 2}, source="src")]
        )

        result = JustificationGate.justify(binding)

        assert result.trusted is True
        assert result.refusal_reason is None
        assert result.verified_data == {"a": 1, "b": 2}

    def test_no_evidence(self):
        binding = EvidenceBinding(
            claim=Claim(description="anything"),
            evidence=[]
        )

        result = JustificationGate.justify(binding)

        assert result.trusted is False
        assert result.refusal_reason == "No evidence provided"

    def test_missing_payload(self):
        binding = EvidenceBinding(
            claim=Claim(description="anything"),
            evidence=[Evidence(payload=None, source="src")]
        )

        result = JustificationGate.justify(binding)

        assert result.trusted is False
        assert result.refusal_reason == "Evidence payload missing"

    def test_unstructured_payload(self):
        binding = EvidenceBinding(
            claim=Claim(description="anything"),
            evidence=[Evidence(payload="not a dict", source="src")]
        )

        result = JustificationGate.justify(binding)

        assert result.trusted is False
        assert result.refusal_reason == "Payload is not structured data"

    def test_empty_payload(self):
        binding = EvidenceBinding(
            claim=Claim(description="anything"),
            evidence=[Evidence(payload={}, source="src")]
        )

        result = JustificationGate.justify(binding)

        assert result.trusted is False
        assert result.refusal_reason == "Evidence payload missing"

    def test_incomplete_data_in_claim(self):
        binding = EvidenceBinding(
            claim=Claim(description="Data is complete and aligned"),
            evidence=[Evidence(payload={"x": None, "y": 5}, source="src")]
        )

        result = JustificationGate.justify(binding)

        assert result.trusted is False
        assert result.refusal_reason == "Data incomplete at key 'x'"
