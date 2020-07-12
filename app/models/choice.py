from pydantic import BaseModel  # pylint: disable=E0611


class Choice(BaseModel):
    label: str
    is_correct: bool
