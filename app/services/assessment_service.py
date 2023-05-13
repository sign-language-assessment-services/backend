import dataclasses
from typing import Annotated

from fastapi import Depends

from app.config import Settings
from app.core.models.assessment import Assessment
from app.core.models.minio_location import MinioLocation
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.text_choice import TextChoice
from app.core.models.text_question import TextQuestion
from app.core.models.video_choice import VideoChoice
from app.core.models.video_question import VideoQuestion
from app.rest.settings2 import get_settings
from app.services.object_storage_client import ObjectStorageClient


class AssessmentService:
    def __init__(self, object_storage_client: Annotated[ObjectStorageClient, Depends()],
                 settings: Annotated[Settings, Depends(get_settings)]):
        self.settings = settings
        self.object_storage_client = object_storage_client

    def get_assessment_by_id(self, assessment_id: int) -> Assessment:
        return self.resolve_assessment(self.all_assessments()[assessment_id])

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

    def all_assessments(self):
        return {
            1: Assessment(
                name="SLAS DSGS GV",
                items=(
                    MultipleChoice(
                        question=VideoQuestion(
                            location=MinioLocation(
                                bucket=self.settings.data_bucket_name,
                                key="slas_sgs_gv/exercises/1/01_Frage.mp4",
                            ),
                        ),
                        choices=(
                            VideoChoice(
                                location=MinioLocation(
                                    bucket=self.settings.data_bucket_name,
                                    key="slas_sgs_gv/exercises/1/01a_Antwort.mp4"
                                ),
                                is_correct=False,
                                type="video",
                            ),
                            VideoChoice(
                                location=MinioLocation(
                                    bucket=self.settings.data_bucket_name,
                                    key="slas_sgs_gv/exercises/1/01b_Antwort.mp4"
                                ),
                                is_correct=True,
                                type="video",
                            ),
                            VideoChoice(
                                location=MinioLocation(
                                    bucket=self.settings.data_bucket_name,
                                    key="slas_sgs_gv/exercises/1/01c_Antwort.mp4"
                                ),
                                is_correct=False,
                                type="video",
                            ),
                        )
                    ),
                    MultipleChoice(
                        question=VideoQuestion(
                            location=MinioLocation(
                                bucket=self.settings.data_bucket_name,
                                key="slas_sgs_gv/exercises/2/02_Frage.mp4",
                            ),
                        ),
                        choices=(
                            VideoChoice(
                                location=MinioLocation(
                                    bucket=self.settings.data_bucket_name,
                                    key="slas_sgs_gv/exercises/2/02a_Antwort.mp4"
                                ),
                                is_correct=False,
                                type="video",
                            ),
                            VideoChoice(
                                location=MinioLocation(
                                    bucket=self.settings.data_bucket_name,
                                    key="slas_sgs_gv/exercises/2/02b_Antwort.mp4"
                                ),
                                is_correct=True,
                                type="video",
                            ),
                            VideoChoice(
                                location=MinioLocation(
                                    bucket=self.settings.data_bucket_name,
                                    key="slas_sgs_gv/exercises/2/02c_Antwort.mp4"
                                ),
                                is_correct=False,
                                type="video",
                            ),
                        )
                    ),
                    MultipleChoice(
                        question=VideoQuestion(
                            location=MinioLocation(
                                bucket=self.settings.data_bucket_name,
                                key="slas_sgs_gv/exercises/4/04_Frage.mp4",
                            ),
                        ),
                        choices=(
                            VideoChoice(
                                location=MinioLocation(
                                    bucket=self.settings.data_bucket_name,
                                    key="slas_sgs_gv/exercises/4/04a_Antwort.mp4"
                                ),
                                is_correct=False,
                                type="video",
                            ),
                            VideoChoice(
                                location=MinioLocation(
                                    bucket=self.settings.data_bucket_name,
                                    key="slas_sgs_gv/exercises/4/04b_Antwort.mp4"
                                ),
                                is_correct=True,
                                type="video",
                            ),
                            VideoChoice(
                                location=MinioLocation(
                                    bucket=self.settings.data_bucket_name,
                                    key="slas_sgs_gv/exercises/4/04c_Antwort.mp4"
                                ),
                                is_correct=False,
                                type="video",
                            ),
                        )
                    ),
                    MultipleChoice(
                        question=VideoQuestion(
                            location=MinioLocation(
                                bucket=self.settings.data_bucket_name,
                                key="slas_sgs_gv/exercises/5/05_Frage.mp4",
                            ),
                        ),
                        choices=(
                            VideoChoice(
                                location=MinioLocation(
                                    bucket=self.settings.data_bucket_name,
                                    key="slas_sgs_gv/exercises/5/05a_Antwort.mp4"
                                ),
                                is_correct=False,
                                type="video",
                            ),
                            VideoChoice(
                                location=MinioLocation(
                                    bucket=self.settings.data_bucket_name,
                                    key="slas_sgs_gv/exercises/5/05b_Antwort.mp4"
                                ),
                                is_correct=True,
                                type="video",
                            ),
                            VideoChoice(
                                location=MinioLocation(
                                    bucket=self.settings.data_bucket_name,
                                    key="slas_sgs_gv/exercises/5/05c_Antwort.mp4"
                                ),
                                is_correct=False,
                                type="video",
                            ),
                        )
                    ),
                    MultipleChoice(
                        question=VideoQuestion(
                            location=MinioLocation(
                                bucket=self.settings.data_bucket_name,
                                key="slas_sgs_gv/exercises/6/06_Frage.mp4",
                            ),
                        ),
                        choices=(
                            VideoChoice(
                                location=MinioLocation(
                                    bucket=self.settings.data_bucket_name,
                                    key="slas_sgs_gv/exercises/6/06a_Antwort.mp4"
                                ),
                                is_correct=False,
                                type="video",
                            ),
                            VideoChoice(
                                location=MinioLocation(
                                    bucket=self.settings.data_bucket_name,
                                    key="slas_sgs_gv/exercises/6/06b_Antwort.mp4"
                                ),
                                is_correct=True,
                                type="video",
                            ),
                            VideoChoice(
                                location=MinioLocation(
                                    bucket=self.settings.data_bucket_name,
                                    key="slas_sgs_gv/exercises/6/06c_Antwort.mp4"
                                ),
                                is_correct=False,
                                type="video",
                            ),
                        )
                    ),
                    MultipleChoice(
                        question=VideoQuestion(
                            location=MinioLocation(
                                bucket=self.settings.data_bucket_name,
                                key="slas_sgs_gv/exercises/8/08_Frage.mp4",
                            ),
                        ),
                        choices=(
                            VideoChoice(
                                location=MinioLocation(
                                    bucket=self.settings.data_bucket_name,
                                    key="slas_sgs_gv/exercises/8/08a_Antwort.mp4"
                                ),
                                is_correct=False,
                                type="video",
                            ),
                            VideoChoice(
                                location=MinioLocation(
                                    bucket=self.settings.data_bucket_name,
                                    key="slas_sgs_gv/exercises/8/08b_Antwort.mp4"
                                ),
                                is_correct=True,
                                type="video",
                            ),
                            VideoChoice(
                                location=MinioLocation(
                                    bucket=self.settings.data_bucket_name,
                                    key="slas_sgs_gv/exercises/8/08c_Antwort.mp4"
                                ),
                                is_correct=False,
                                type="video",
                            ),
                        )
                    ),
                    MultipleChoice(
                        question=VideoQuestion(
                            location=MinioLocation(
                                bucket=self.settings.data_bucket_name,
                                key="slas_sgs_gv/exercises/10/10_Frage.mp4",
                            ),
                        ),
                        choices=(
                            VideoChoice(
                                location=MinioLocation(
                                    bucket=self.settings.data_bucket_name,
                                    key="slas_sgs_gv/exercises/10/10a_Antwort.mp4"
                                ),
                                is_correct=False,
                                type="video",
                            ),
                            VideoChoice(
                                location=MinioLocation(
                                    bucket=self.settings.data_bucket_name,
                                    key="slas_sgs_gv/exercises/10/10b_Antwort.mp4"
                                ),
                                is_correct=True,
                                type="video",
                            ),
                            VideoChoice(
                                location=MinioLocation(
                                    bucket=self.settings.data_bucket_name,
                                    key="slas_sgs_gv/exercises/10/10c_Antwort.mp4"
                                ),
                                is_correct=False,
                                type="video",
                            ),
                        )
                    ),
                )
            )
        }
