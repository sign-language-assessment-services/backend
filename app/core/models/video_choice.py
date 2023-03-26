from dataclasses import dataclass, field


@dataclass(frozen=True)
class VideoChoice:
    url: str
    is_correct: bool
    type: str = field(default="video")