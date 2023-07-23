import dataclasses
from typing import Annotated

from fastapi import Depends

from app.config import Settings
from app.core.models.assessment import Assessment
from app.core.models.assessment_summary import AssessmentSummary
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.text_choice import TextChoice
from app.core.models.text_question import TextQuestion
from app.core.models.video_choice import VideoChoice
from app.core.models.video_question import VideoQuestion
from app.rest.settings import get_settings
from app.services.assessment_repository import AssessmentRepository
from app.services.object_storage_client import ObjectStorageClient


class AssessmentService:
    def __init__(
            self,
            object_storage_client: Annotated[ObjectStorageClient, Depends()],
            repository: Annotated[AssessmentRepository, Depends()],
            settings: Annotated[Settings, Depends(get_settings)]
    ):
        self.object_storage_client = object_storage_client
        self.repository = repository
        self.settings = settings

    def get_assessment_by_id(self, assessment_id: int) -> Assessment:
        return self.resolve_assessment(self.repository.get_assessment_by_id(assessment_id))

    def list_assessments(self) -> list[AssessmentSummary]:
        return self.repository.list_assessments()

    def score_assessment(self, assessment_id: int, submission: dict[int, list[int]]) -> dict[str, int]:
        assessment = self.get_assessment_by_id(assessment_id)
        return assessment.score(submission)

    def resolve_question(self, question: VideoQuestion | TextQuestion) -> VideoQuestion | TextQuestion:
        if isinstance(question, VideoQuestion):
            return dataclasses.replace(
                question, url=self.object_storage_client.get_presigned_url(question.location)
            )
        return question

    def resolve_choice(self, choice: VideoChoice | TextChoice) -> VideoChoice | TextChoice:
        if isinstance(choice, VideoChoice):
            return dataclasses.replace(
                choice, url=self.object_storage_client.get_presigned_url(choice.location)
            )
        return choice

    def resolve_item(self, item: MultipleChoice) -> MultipleChoice:
        return dataclasses.replace(
            item,
            question=self.resolve_question(item.question),
            choices=tuple(self.resolve_choice(choice) for choice in item.choices)
        )

    def resolve_assessment(self, assessment: Assessment) -> Assessment:
        return dataclasses.replace(
            assessment, items=tuple(self.resolve_item(item) for item in assessment.items)
        )
