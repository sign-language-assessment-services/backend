from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.exercise_submission import ExerciseSubmission
from app.database.tables.exercise_submissions import DbExerciseSubmission
from app.mappers.exercise_submission_mapper import (
    exercise_submission_to_db, exercise_submission_to_domain
)
from app.repositories.utils import (
    add_entry, delete_entry, get_all, get_by_id, update_entry, upsert_entry
)


def add_exercise_submission(session: Session, submission: ExerciseSubmission) -> None:
    db_model = exercise_submission_to_db(submission)
    add_entry(session, db_model)


def get_exercise_submission(session: Session, _id: UUID) -> ExerciseSubmission | None:
    result = get_by_id(session, DbExerciseSubmission, _id)
    if result:
        return exercise_submission_to_domain(result)
    return None


def get_exercise_submissions_for_assessment_submission(
        session: Session,
        assessment_submission_id: UUID
) -> list[ExerciseSubmission]:
    filter_conditions = {DbExerciseSubmission.assessment_submission_id: assessment_submission_id}
    result = get_all(session, DbExerciseSubmission, filter_by=filter_conditions)
    return [exercise_submission_to_domain(r) for r in result]


def list_exercise_submissions(session: Session) -> list[ExerciseSubmission]:
    result = get_all(session, DbExerciseSubmission)
    return [exercise_submission_to_domain(r) for r in result]


def update_exercise_submission(session: Session, _id: UUID, **kwargs: Any) -> None:
    update_entry(session, DbExerciseSubmission, _id, **kwargs)


def upsert_exercise_submission(session: Session, submission: ExerciseSubmission) -> None:
    db_model = exercise_submission_to_db(submission)
    upsert_entry(
        session=session,
        db=db_model,
        on_constraint="exercise_submissions_assessment_submission_id_exercise_id_key",
        fields_to_update={
            DbExerciseSubmission.choices: db_model.choices,
            DbExerciseSubmission.score: db_model.score
        }
    )


def delete_exercise_submission(session: Session, _id: UUID) -> None:
    delete_entry(session, DbExerciseSubmission, _id)
