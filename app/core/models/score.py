from dataclasses import dataclass, field


@dataclass(slots=True)
class Score:
    points: int
    maximum_points: int
    percentage: float = field(init=False)

    def __post_init__(self) -> None:
        self.percentage = self.points / self.maximum_points * 100
