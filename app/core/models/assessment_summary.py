from dataclasses import dataclass


@dataclass(frozen=True)
class AssessmentSummary:
    id: int
    name: str
