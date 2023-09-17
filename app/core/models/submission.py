from dataclasses import dataclass


@dataclass
class Submission:
    id: str
    user_id: str
    assessment_id: str
    answers: dict
    score: int
