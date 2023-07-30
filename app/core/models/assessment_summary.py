from dataclasses import dataclass


@dataclass(frozen=True)
class AssessmentSummary:
    id: str  # temporary use name as id
    name: str
