from pydantic import BaseModel


class User(BaseModel):
    roles: list[str]
