from click import Choice
from sqlalchemy.orm import Session

from app.database.tables.choices import DbChoice


def get_choice_by_id(session: Session, _id: str) -> Choice:
    result = session.get(DbChoice, {"id": _id})
    return result.to_choice()
