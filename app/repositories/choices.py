from typing import Any

from click import Choice
from sqlalchemy.orm import Session

from app.database.tables.choices import DbChoice
from app.mappers.choice_mapper import ChoiceMapper


def add_choice(session: Session, choice: Choice) -> None:
    db_model = ChoiceMapper.domain_to_db(choice)
    session.add(db_model)
    session.commit()
    return None


def get_choice_by_id(session: Session, _id: str) -> Choice | None:
    result = session.get(DbChoice, {"id": _id})
    if result:
        model = ChoiceMapper.db_to_domain(result)
        return model
    return None


def list_choices(session: Session) -> list[Choice]:
    results = session.query(DbChoice).all()
    models = [ChoiceMapper.db_to_domain(result) for result in results]
    return models


def update_choice(session: Session, choice: Choice, **kwargs: dict[str, Any]) -> None:
    session.query(DbChoice).filter_by(id=choice.id).update(kwargs)
    session.commit()
    return None


def delete_choice_by_id(session: Session, _id: str) -> None:
    session.query(DbChoice).filter_by(id=_id).delete()
    session.commit()
    return None
