from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class AssessmentSummary:
    id: UUID
    name: str
