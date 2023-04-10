import dataclasses
import os
from dataclasses import asdict
from typing import Any

from fastapi import HTTPException
from minio import Minio

from app.core.models.assessment import Assessment
from app.core.models.minio_location import MinioLocation
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.text_choice import TextChoice
from app.core.models.video_choice import VideoChoice
from app.utils import strtobool

client = Minio(
    endpoint=os.getenv("DATA_ENDPOINT"),
    access_key=os.getenv("DATA_ROOT_USER"),
    secret_key=os.getenv("DATA_ROOT_PASSWORD"),
    secure=strtobool(os.getenv("DATA_SECURE"), default=True),
)

def get_presigned_url(location: MinioLocation) -> str:
    try:
        return client.get_presigned_url(
            method="GET",
            bucket_name=location.bucket,
            object_name=location.key
        )
    except Exception as exc:
        raise HTTPException(
            status_code=503, detail=f"Minio not reachable. {exc}"
        )

repository = {
    1: Assessment(
        name="Elefantenprüfung",
        items=(
            MultipleChoice(
                description="Was essen Elefanten?",
                choices=(
                    VideoChoice(
                        location=MinioLocation(
                            bucket="slportal",
                            key="hexen_algorithmus.mp4"
                        ),
                        is_correct=False,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket="slportal",
                            key="hexen_algorithmus.mp4"
                        ),
                        is_correct=True,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket="slportal",
                            key="hexen_algorithmus.mp4"
                        ),
                        is_correct=False,
                        type="video",
                    )
                )
            ),
            MultipleChoice(
                description="Was trinken Elefanten?",
                choices=(
                    TextChoice(
                        label="Mineralwasser",
                        is_correct=True,
                        type="text",
                    ),
                    TextChoice(
                        label="Limonade",
                        is_correct=False,
                        type="text",
                    ),
                    TextChoice(
                        label="Wasser",
                        is_correct=True,
                        type="text",
                    ),
                    TextChoice(
                        label="Hühnersuppe",
                        is_correct=False,
                        type="text",
                    )
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
