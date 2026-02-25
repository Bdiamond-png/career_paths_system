import pytest
from evidence_mapping import EvidenceMapping, EvidenceMappingEntry
from justification_gate import Evidence


def test_evidence_mapping_validate_success():
    mapping = EvidenceMapping([
        EvidenceMappingEntry(id="e1", evidence=Evidence(payload={"x": 1}, source="src"))
    ])
    result = mapping.validate("e1")
    assert result.trusted is True
    assert result.verified_data == {"x": 1}


def test_evidence_mapping_missing():
    mapping = EvidenceMapping([])
    result = mapping.validate("missing")
    assert result.trusted is False
    assert "Missing evidence" in result.refusal_reason


def test_evidence_mapping_payload_none():
    mapping = EvidenceMapping([
        EvidenceMappingEntry(id="e2", evidence=Evidence(payload=None, source="src"))
    ])
    result = mapping.validate("e2")
    assert result.trusted is False
    assert "payload missing" in result.refusal_reason


def test_evidence_mapping_payload_unstructured():
    mapping = EvidenceMapping([
        EvidenceMappingEntry(id="e3", evidence=Evidence(payload="not a dict", source="src"))
    ])
    result = mapping.validate("e3")
    assert result.trusted is False
    assert "unstructured" in result.refusal_reason


def test_evidence_mapping_payload_empty():
    mapping = EvidenceMapping([
        EvidenceMappingEntry(id="e4", evidence=Evidence(payload={}, source="src"))
    ])
    result = mapping.validate("e4")
    assert result.trusted is False
    assert "empty" in result.refusal_reason
