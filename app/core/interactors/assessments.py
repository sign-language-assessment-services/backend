from dataclasses import asdict
from typing import Any

from app.core.models.assessment import Assessment
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.text_choice import TextChoice
from app.core.models.video_choice import VideoChoice

repository = {
    1: Assessment(
        name="Elefantenprüfung",
        items=(
            MultipleChoice(
                description="Was essen Elefanten?",
                choices=(
                    VideoChoice(
                        url="https://tinyurl.com/4bvyka5u",
                        is_correct=False,
                        type="video",
                    ),
                    VideoChoice(
                        url="https://tinyurl.com/4bvyka5u",
                        is_correct=True,
                        type="video",
                    ),
                    VideoChoice(
                        url="https://tinyurl.com/4bvyka5u",
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


def get_assessment_by_id(assessment_id: int) -> dict[str, Any]:
    return asdict(repository[assessment_id])


def score_assessment(assessment_id: int, submission: dict[int, list[int]]) -> dict[str, int]:
    assessment = repository[assessment_id]
    return assessment.score(submission)
