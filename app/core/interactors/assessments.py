import dataclasses
from dataclasses import asdict
from typing import Any, cast

from fastapi import HTTPException
from minio import Minio

from app import settings
from app.core.models.assessment import Assessment
from app.core.models.minio_location import MinioLocation
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.text_choice import TextChoice
from app.core.models.video_choice import VideoChoice
from app.core.models.video_question import VideoQuestion

client = Minio(
    endpoint=settings.DATA_ENDPOINT,
    access_key=settings.DATA_ROOT_USER,
    secret_key=settings.DATA_ROOT_PASSWORD,
    secure=settings.DATA_SECURE,
)

def get_presigned_url(location: MinioLocation) -> str:
    try:
        presigned_url = client.get_presigned_url(
            method="GET",
            bucket_name=location.bucket,
            object_name=location.key
        )
        return cast(str, presigned_url)
    except Exception as exc:
        raise HTTPException(
            status_code=503, detail=f"Minio not reachable. {exc}"
        ) from exc

repository = {
    1: Assessment(
        name="SLAS DSGS GV",
        items=(
            MultipleChoice(
                question=VideoQuestion(
                    location=MinioLocation(
                        bucket=settings.DATA_BUCKET_NAME,
                        key="slas_sgs_gv/exercises/1/01_Frage.mp4",
                    ),
                ),
                choices=(
                    VideoChoice(
                        location=MinioLocation(
                            bucket=settings.DATA_BUCKET_NAME,
                            key="slas_sgs_gv/exercises/1/01a_Antwort.mp4"
                        ),
                        is_correct=False,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket=settings.DATA_BUCKET_NAME,
                            key="slas_sgs_gv/exercises/1/01b_Antwort.mp4"
                        ),
                        is_correct=True,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket=settings.DATA_BUCKET_NAME,
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
                        bucket=settings.DATA_BUCKET_NAME,
                        key="slas_sgs_gv/exercises/2/02_Frage.mp4",
                    ),
                ),
                choices=(
                    VideoChoice(
                        location=MinioLocation(
                            bucket=settings.DATA_BUCKET_NAME,
                            key="slas_sgs_gv/exercises/2/02a_Antwort.mp4"
                        ),
                        is_correct=False,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket=settings.DATA_BUCKET_NAME,
                            key="slas_sgs_gv/exercises/2/02b_Antwort.mp4"
                        ),
                        is_correct=True,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket=settings.DATA_BUCKET_NAME,
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
                        bucket=settings.DATA_BUCKET_NAME,
                        key="slas_sgs_gv/exercises/4/04_Frage.mp4",
                    ),
                ),
                choices=(
                    VideoChoice(
                        location=MinioLocation(
                            bucket=settings.DATA_BUCKET_NAME,
                            key="slas_sgs_gv/exercises/4/04a_Antwort.mp4"
                        ),
                        is_correct=False,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket=settings.DATA_BUCKET_NAME,
                            key="slas_sgs_gv/exercises/4/04b_Antwort.mp4"
                        ),
                        is_correct=True,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket=settings.DATA_BUCKET_NAME,
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
                        bucket=settings.DATA_BUCKET_NAME,
                        key="slas_sgs_gv/exercises/5/05_Frage.mp4",
                    ),
                ),
                choices=(
                    VideoChoice(
                        location=MinioLocation(
                            bucket=settings.DATA_BUCKET_NAME,
                            key="slas_sgs_gv/exercises/5/05a_Antwort.mp4"
                        ),
                        is_correct=False,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket=settings.DATA_BUCKET_NAME,
                            key="slas_sgs_gv/exercises/5/05b_Antwort.mp4"
                        ),
                        is_correct=True,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket=settings.DATA_BUCKET_NAME,
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
                        bucket=settings.DATA_BUCKET_NAME,
                        key="slas_sgs_gv/exercises/6/06_Frage.mp4",
                    ),
                ),
                choices=(
                    VideoChoice(
                        location=MinioLocation(
                            bucket=settings.DATA_BUCKET_NAME,
                            key="slas_sgs_gv/exercises/6/06a_Antwort.mp4"
                        ),
                        is_correct=False,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket=settings.DATA_BUCKET_NAME,
                            key="slas_sgs_gv/exercises/6/06b_Antwort.mp4"
                        ),
                        is_correct=True,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket=settings.DATA_BUCKET_NAME,
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
                        bucket=settings.DATA_BUCKET_NAME,
                        key="slas_sgs_gv/exercises/8/08_Frage.mp4",
                    ),
                ),
                choices=(
                    VideoChoice(
                        location=MinioLocation(
                            bucket=settings.DATA_BUCKET_NAME,
                            key="slas_sgs_gv/exercises/8/08a_Antwort.mp4"
                        ),
                        is_correct=False,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket=settings.DATA_BUCKET_NAME,
                            key="slas_sgs_gv/exercises/8/08b_Antwort.mp4"
                        ),
                        is_correct=True,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket=settings.DATA_BUCKET_NAME,
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
                        bucket=settings.DATA_BUCKET_NAME,
                        key="slas_sgs_gv/exercises/10/10_Frage.mp4",
                    ),
                ),
                choices=(
                    VideoChoice(
                        location=MinioLocation(
                            bucket=settings.DATA_BUCKET_NAME,
                            key="slas_sgs_gv/exercises/10/10a_Antwort.mp4"
                        ),
                        is_correct=False,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket=settings.DATA_BUCKET_NAME,
                            key="slas_sgs_gv/exercises/10/10b_Antwort.mp4"
                        ),
                        is_correct=True,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket=settings.DATA_BUCKET_NAME,
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


def resolve_choice(choice: VideoChoice|TextChoice) -> VideoChoice|TextChoice:
    if isinstance(choice, VideoChoice):
        return dataclasses.replace(
            choice, url=get_presigned_url(choice.location)
        )
    return choice


def resolve_item(item: MultipleChoice) -> MultipleChoice:
    return dataclasses.replace(
        item, choices=tuple(resolve_choice(choice) for choice in item.choices)
    )


def resolve_assessment(assessment: Assessment) -> Assessment:
    return dataclasses.replace(
        assessment, items=tuple(resolve_item(item) for item in assessment.items)
    )


def get_assessment_by_id(assessment_id: int) -> dict[str, Any]:
    return asdict(resolve_assessment(repository[assessment_id]))


def score_assessment(assessment_id: int, submission: dict[int, list[int]]) -> dict[str, int]:
    assessment = repository[assessment_id]
    return assessment.score(submission)
