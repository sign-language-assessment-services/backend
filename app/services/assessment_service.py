import dataclasses
import datetime
import uuid
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import Settings
from app.core.models.assessment import Assessment
from app.core.models.assessment_summary import AssessmentSummary
from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia import Multimedia
from app.core.models.multimedia_choice import MultimediaChoice
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.static_item import StaticItem
from app.core.models.submission import Submission
from app.core.models.text_choice import TextChoice
from app.rest.settings import get_settings
from app.services.object_storage_client import ObjectStorageClient


class AssessmentService:
    def __init__(
            self,
            object_storage_client: Annotated[ObjectStorageClient, Depends()],
            settings: Annotated[Settings, Depends(get_settings)],
    ):
        self.object_storage_client = object_storage_client
        self.settings = settings

    def get_assessment_by_id(self, assessment_id: str) -> Assessment:
        folders = self.object_storage_client.list_folders(
            bucket_name=self.settings.data_bucket_name,
            folder=assessment_id
        )

        items: list[MultipleChoice | StaticItem] = []
        for position, folder in enumerate(folders):
            bucket_objects = self.object_storage_client.list_files(
                bucket_name=self.settings.data_bucket_name,
                folder=folder
            )
            choices = []
            question = None
            for bucket_object in bucket_objects:
                if "frage" in bucket_object.name.lower():
                    question = Multimedia(
                        location=MinioLocation(
                            bucket=self.settings.data_bucket_name,
                            key=bucket_object.name
                        ),
                        type=MediaType.from_content_type(bucket_object.content_type)
                    )
                elif "antwort" in bucket_object.name.lower():
                    choices.append(
                        MultimediaChoice(
                            location=MinioLocation(
                                bucket=self.settings.data_bucket_name,
                                key=bucket_object.name
                            ),
                            is_correct="richtig" in bucket_object.name,
                            type=MediaType.from_content_type(bucket_object.content_type)
                        )
                    )
            if question:
                items.append(
                    MultipleChoice(
                        question=question,
                        choices=choices,
                        position=position
                    )
                )
            else:
                items.append(
                    StaticItem(
                        content=Multimedia(
                            location=MinioLocation(
                                bucket=self.settings.data_bucket_name,
                                key=bucket_objects[0].name
                            ),
                            type=MediaType.from_content_type(bucket_objects[0].content_type)
                        ),
                        position=position
                    )

                )

        assessment = Assessment(name=assessment_id, items=items)
        return self.resolve_assessment(assessment)

    def list_assessments(self) -> list[AssessmentSummary]:
        return [
            AssessmentSummary(id=assessment, name=assessment)
            for assessment in self.object_storage_client.list_folders(bucket_name=self.settings.data_bucket_name)
        ]

    def score_assessment(
            self,
            assessment_id: str,
            answers: dict[str|int, list[str|int]],
            user_id: str, db: Session
    ) -> dict[str, int]:
        assessment = self.get_assessment_by_id(assessment_id)
        score = assessment.score(answers)
        submission = Submission(
            id=str(uuid.uuid4()),
            user_id=user_id,
            assessment_id=assessment_id,
            answers=answers,
            score=score["score"]
        )
        db.add(submission)
        db.commit()
        return score

    def resolve_video(self, video: Multimedia) -> Multimedia:
        return dataclasses.replace(
            video, url=self.object_storage_client.get_presigned_url(video.location)
        )

    def resolve_choice(self, choice: MultimediaChoice | TextChoice) -> MultimediaChoice | TextChoice:
        if isinstance(choice, MultimediaChoice):
            return dataclasses.replace(
                choice, url=self.object_storage_client.get_presigned_url(choice.location)
            )
        return choice  # pragma: no cover (TextChoice yet not implemented)

    def resolve_item(self, item: MultipleChoice | StaticItem) -> MultipleChoice | StaticItem:
        if isinstance(item, MultipleChoice):
            return dataclasses.replace(
                item,
                question=self.resolve_video(item.question),
                choices=tuple(self.resolve_choice(choice) for choice in item.choices)
            )
        return dataclasses.replace(item, content=self.resolve_video(item.content))

    def resolve_assessment(self, assessment: Assessment) -> Assessment:
        return dataclasses.replace(
            assessment, items=tuple(self.resolve_item(item) for item in assessment.items)
        )
