from pydantic import BaseModel


class ObjectStorageResponse(BaseModel):
    id: str
    url: str
    media_type: str
