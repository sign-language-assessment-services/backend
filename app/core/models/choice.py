from dataclasses import dataclass


@dataclass(frozen=True)
class Choice:
    label: str
    is_correct: bool
