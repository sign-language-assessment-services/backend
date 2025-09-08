from uuid import UUID

from pydantic import BaseModel, Field, computed_field, field_validator

from app.core.models.choice import AssociatedChoice, Choice


class CreateMultipleChoiceResponse(BaseModel):
    id: UUID


class GetMultipleChoiceResponse(BaseModel):
    id: UUID
    choices: list[AssociatedChoice]

    @field_validator("choices", mode="before")
    @classmethod
    def compute_choices(cls, value) -> list[dict[str, UUID | int | bool]]:
        return [
            {
                "id": choice.id,
                "position": choice.position,
                "is_correct": choice.is_correct
            }
            for choice in value
        ]


class ListMultipleChoiceResponse(BaseModel):
    id: UUID
    choices: list[Choice] = Field(exclude=True)

    @computed_field(
        description="Number of choices",
        json_schema_extra={
            "example": 2
        }
    )
    @property
    def number_of_choices(self) -> int:
        return len(self.choices)
