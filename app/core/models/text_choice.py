from dataclasses import dataclass, field


@dataclass(frozen=True)
class TextChoice:
    text: str
    is_correct: bool
    type: str = field(default="text")
