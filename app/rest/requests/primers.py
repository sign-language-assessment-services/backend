from uuid import UUID

from pydantic import BaseModel


class CreatePrimerRequest(BaseModel):
    multimedia_file_id: UUID
