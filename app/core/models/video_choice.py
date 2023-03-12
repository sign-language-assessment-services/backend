from dataclasses import dataclass


@dataclass(frozen=True)
class VideoChoice:
    url: str
    is_correct: bool
