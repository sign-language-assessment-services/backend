from dataclasses import dataclass


@dataclass(frozen=True)
class MinioLocation:
    bucket: str
    key: str
