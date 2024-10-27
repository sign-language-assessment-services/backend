from datetime import UTC, datetime

from sqlalchemy import text

ASSESSMENT_ID = "00000000-0000-0000-0000-000000000000"
MULTIMEDIA_FILE_ID = "00000000-0000-0000-0000-000000000001"
EXERCISE_ID = "00000000-0000-0000-0000-000000000002"
PRIMER_ID = "00000000-0000-0000-0000-000000000003"
SUBMISSION_ID = "00000000-0000-0000-0000-000000000004"
CHOICE_ID = "00000000-0000-0000-0000-000000000005"


def add_assessment(session) -> None:
    assessment = {
        "id": ASSESSMENT_ID,
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "name": "Test Assessment"
    }
    assessment_statement = text(
        """
        INSERT INTO assessments(id, created_at, name)
        VALUES (:id, :created_at, :name)
        """
    )
    session.execute(assessment_statement, assessment)


def add_multimedia_file(session, _id: str | None = None) -> None:
    multimedia_file = {
        "id": MULTIMEDIA_FILE_ID if _id is None else _id,
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "bucket": "testportal",
        "key": "test.mpeg",
        "content_type": "VIDEO"
    }
    multimedia_file_statement = text(
        """
        INSERT INTO multimedia_files(id, created_at, bucket, key, content_type)
        VALUES (:id, :created_at, :bucket, :key, :content_type)
        """
    )
    session.execute(multimedia_file_statement, multimedia_file)


def add_exercise(session, with_dependencies=True) -> None:
    if with_dependencies:
        add_assessment(session)
        add_multimedia_file(session)

    exercise = {
        "id": EXERCISE_ID,
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "position": 1,
        "assessment_id": ASSESSMENT_ID,
        "multimedia_file_id": MULTIMEDIA_FILE_ID
    }
    exercise_statement = text(
        """
        INSERT INTO exercises(id, created_at, position, assessment_id, multimedia_file_id)
        VALUES (:id, :created_at, :position, :assessment_id, :multimedia_file_id)
        """
    )
    session.execute(exercise_statement, exercise)


def add_primer(session, with_dependencies=True) -> None:
    if with_dependencies:
        add_assessment(session)
        add_multimedia_file(session)

    primer = {
        "id": PRIMER_ID,
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "position": 1,
        "assessment_id": ASSESSMENT_ID,
        "multimedia_file_id": MULTIMEDIA_FILE_ID
    }
    primer_statement = text(
        """
        INSERT INTO primers(id, created_at, position, assessment_id, multimedia_file_id)
        VALUES (:id, :created_at, :position, :assessment_id, :multimedia_file_id)
        """
    )
    session.execute(primer_statement, primer)


def add_submission(session, with_dependencies=True) -> None:
    if with_dependencies:
        add_assessment(session)

    submission = {
        "id": SUBMISSION_ID,
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "user_id": "testuser-001",
        "points": 90,
        "maximum_points": 100,
        "percentage": 90.0,
        "assessment_id": ASSESSMENT_ID
    }
    submission_statement = text(
        """
        INSERT INTO submissions(id, created_at, user_id, points, maximum_points, percentage, assessment_id)
        VALUES (:id, :created_at, :user_id, :points, :maximum_points, :percentage, :assessment_id)
        """
    )
    session.execute(submission_statement, submission)


def add_choice(session, with_dependencies=True) -> None:
    choice_multimedia_file_id = "00000000-0000-0000-aaaa-000000000000"
    if with_dependencies:
        add_exercise(session)
        add_multimedia_file(session, _id=choice_multimedia_file_id)

    choice = {
        "id": CHOICE_ID,
        "created_at": datetime(2000, 1, 1, 12, tzinfo=UTC),
        "is_correct": True,
        "exercise_id": EXERCISE_ID,
        "multimedia_file_id": choice_multimedia_file_id
    }
    choice_statement = text(
        """
        INSERT INTO choices(id, created_at, is_correct, exercise_id, multimedia_file_id)
        VALUES (:id, :created_at, :is_correct, :exercise_id, :multimedia_file_id)
        """
    )
    session.execute(choice_statement, choice)
