from uuid import UUID

from pydantic import BaseModel


class CreateExerciseRequest(BaseModel):
    multimedia_file_id: UUID  # question
    multiple_choice_id: UUID
