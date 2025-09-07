from pydantic import BaseModel, Field


class MinioLocation(BaseModel):
    bucket: str = Field(max_length=63)
    key: str = Field(max_length=1024)
