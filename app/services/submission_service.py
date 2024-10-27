import dataclasses
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import Settings
from app.core.models.assessment import Assessment
from app.core.models.exercise import Exercise
from app.core.models.multimedia_choice import MultimediaChoice
from app.core.models.multimedia_file import MultimediaFile
from app.core.models.primer import Primer
from app.core.models.score import Score
from app.core.models.submission import Submission
from app.core.models.text_choice import TextChoice
from app.repositories.submissions import (
    add_submission, get_submission_by_id, list_submission_by_user_id,
    list_submissions
)
from app.settings import get_settings
from app.type_hints import SubmissionAnswers


class SubmissionService:
    def __init__(self, settings: Annotated[Settings, Depends(get_settings)]):
        self.settings = settings

    @staticmethod
    def get_submission_by_id(session: Session, submission_id: UUID) -> Submission:
        return get_submission_by_id(session=session, _id=str(submission_id))

    @staticmethod
    def list_submissions(session: Session) -> list[Submission]:
        return list_submissions(session)

    def score_submission(
            self,
            assessment_id: UUID,
            answers: SubmissionAnswers,
            user_id: str,
            session: Session
    ) -> Score:
        assessment = self.get_assessment_by_id(session=session, assessment_id=assessment_id)
        score = assessment.score(answers=answers)
        submission = Submission(
            user_id=user_id,
            assessment_id=assessment_id,
            answers=answers,
            points=score.points,
            maximum_points=score.maximum_points,
            percentage=score.percentage
        )
        add_submission(session=session, submission=submission)  # submission=DbSubmission.from_submission(submission))
        return score

    @staticmethod
    def list_submissions(session: Session) -> list[Submission]:
        return list_submission_by_user_id(session=session, user_id=None)

    def resolve_video(self, video: MultimediaFile) -> MultimediaFile:
        return dataclasses.replace(
            video, url=self.object_storage_client.get_presigned_url(video.location)
        )

    def resolve_choice(self, choice: MultimediaChoice | TextChoice) -> MultimediaChoice | TextChoice:
        if isinstance(choice, MultimediaChoice):
            return dataclasses.replace(
                choice, url=self.object_storage_client.get_presigned_url(choice.location)
            )
        return choice  # pragma: no cover (TextChoice yet not implemented)

    def resolve_item(self, item: Primer | Exercise) -> Primer | Exercise:
        if isinstance(item, Exercise):
            return dataclasses.replace(
                item,
                question=self.resolve_video(item.question),
                choices=tuple(self.resolve_choice(choice) for choice in item.choices)
            )
        return dataclasses.replace(item, content=self.resolve_video(item.content))

    def resolve_assessment(self, assessment: Assessment) -> Assessment:
        return dataclasses.replace(
            assessment, items=list(self.resolve_item(item) for item in assessment.items)
        )
