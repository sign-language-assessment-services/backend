from dataclasses import dataclass


@dataclass(frozen=True)
class BucketObject:
    name: str
    content_type: str
