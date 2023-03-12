from dataclasses import asdict

from ..models.assessment import Assessment
from ..models.text_choice import TextChoice
from ..models.multiple_choice import MultipleChoice
from ..models.video_choice import VideoChoice

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


def get_assessment_by_id(assessment_id: int) -> Assessment:
    return asdict(repository.get(assessment_id))


def score_assessment(assessment_id: int, submission) -> int:
    assessment = repository.get(assessment_id)
    return assessment.score(submission)
