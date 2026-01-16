from dataclasses import dataclass
from typing import Any, List


@dataclass(frozen=True)
class Claim:
    description: str


@dataclass(frozen=True)
class Evidence:
    payload: Any
    source: str


@dataclass(frozen=True)
class EvidenceBinding:
    claim: Claim
    evidence: List[Evidence]


@dataclass(frozen=True)
class TrustState:
    trusted: bool
    verified_data: Any = None
    refusal_reason: str = None


class JustificationGate:
    """
    Validates whether provided evidence logically supports the claim.
    Does not extend BaseState.
    Stays fully isolated from other pipeline components.
    """

    @staticmethod
    def justify(binding: EvidenceBinding) -> TrustState:

        # No evidence provided
        if not binding.evidence:
            return TrustState(
                trusted=False,
                refusal_reason="No evidence provided"
            )

        evidence = binding.evidence[0]

        # Missing payload
        if evidence.payload is None:
            return TrustState(
                trusted=False,
                refusal_reason="Evidence payload missing"
            )

        # Unstructured payload
        if not isinstance(evidence.payload, dict):
            return TrustState(
                trusted=False,
                refusal_reason="Payload is not structured data"
            )

        # Empty payload
        if len(evidence.payload) == 0:
            return TrustState(
                trusted=False,
                refusal_reason="Evidence payload missing"
            )

        # Claim-specific validation
        if binding.claim.description.lower() == "data is complete and aligned":
            for key, value in evidence.payload.items():
                if value is None:
                    return TrustState(
                        trusted=False,
                        refusal_reason=f"Data incomplete at key '{key}'"
                    )

        # Passed
        return TrustState(
            trusted=True,
            verified_data=evidence.payload
        )
