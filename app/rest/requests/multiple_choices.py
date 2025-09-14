from uuid import UUID

from pydantic import BaseModel, model_validator


class CreateMultipleChoiceRequest(BaseModel):
    choice_ids: list[UUID]
    correct_choice_ids: list[UUID]

    @model_validator(mode="after")
    def validate_correct_choices_is_subset_of_choices(self):
        choices = set(self.choice_ids)
        correct_choices = set(self.correct_choice_ids)
        if not correct_choices.issubset(choices):
            invalid_ids = [str(_id) for _id in sorted(correct_choices - choices)]
            raise ValueError(
                f"The correct choices have to be a subset of choices. "
                f"These ids are not valid: {", ".join(invalid_ids)}."
            )
        return self
