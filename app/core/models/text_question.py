from dataclasses import dataclass, field


@dataclass(frozen=True)
class TextQuestion:
    text: str
    type: str = field(default="text")
