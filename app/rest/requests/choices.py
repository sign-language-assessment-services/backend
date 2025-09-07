from uuid import UUID

from pydantic import BaseModel


class CreateChoiceRequest(BaseModel):
    multimedia_file_id: UUID
