import dataclasses
from typing import Annotated

from fastapi import Depends

from app.config import Settings
from app.core.models.assessment import Assessment
from app.core.models.assessment_summary import AssessmentSummary
from app.core.models.minio_location import MinioLocation
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.static_item import StaticItem
from app.core.models.text_choice import TextChoice
from app.core.models.video import Video
from app.core.models.video_choice import VideoChoice
from app.rest.settings import get_settings
from app.services.object_storage_client import ObjectStorageClient


class AssessmentService:
    def __init__(
            self,
            object_storage_client: Annotated[ObjectStorageClient, Depends()],
            settings: Annotated[Settings, Depends(get_settings)]
    ):
        self.object_storage_client = object_storage_client
        self.settings = settings

    def get_assessment_by_id(self, assessment_id: str) -> Assessment:
        folders = self.object_storage_client.list_folders(
            bucket_name=self.settings.data_bucket_name,
            folder=assessment_id
        )

        items: list[MultipleChoice | StaticItem] = []
        for folder in folders:
            files = self.object_storage_client.list_files(
                bucket_name=self.settings.data_bucket_name,
                folder=folder
            )
            choices = []
            question = None
            for filename in files:
                if "frage" in filename.lower():
                    question = Video(
                        location=MinioLocation(
                            bucket=self.settings.data_bucket_name,
                            key=filename
                        )
                    )
                elif "antwort" in filename.lower():
                    choices.append(
                        VideoChoice(
                            location=MinioLocation(
                                bucket=self.settings.data_bucket_name,
                                key=filename
                            ),
                            is_correct="richtig" in filename,
                            type="video"
                        )
                    )
            if question:
                items.append(MultipleChoice(question=question, choices=choices))
            else:
                items.append(
                    StaticItem(
                        Video(location=MinioLocation(bucket=self.settings.data_bucket_name, key=files[0]))
                    )
                )

        assessment = Assessment(name=assessment_id, items=items)
        return self.resolve_assessment(assessment)

    def list_assessments(self) -> list[AssessmentSummary]:
        return [
            AssessmentSummary(id=assessment, name=assessment)
            for assessment in self.object_storage_client.list_folders(bucket_name=self.settings.data_bucket_name)
        ]

    def score_assessment(self, assessment_id: str, submission: dict[int, list[int]]) -> dict[str, int]:
        assessment = self.get_assessment_by_id(assessment_id)
        return assessment.score(submission)

    def resolve_video(self, video: Video) -> Video:
        return dataclasses.replace(
            video, url=self.object_storage_client.get_presigned_url(video.location)
        )

    def resolve_choice(self, choice: VideoChoice | TextChoice) -> VideoChoice | TextChoice:
        if isinstance(choice, VideoChoice):
            return dataclasses.replace(
                choice, url=self.object_storage_client.get_presigned_url(choice.location)
            )
        return choice

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
