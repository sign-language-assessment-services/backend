from unittest import mock
from unittest.mock import Mock

import pytest
from freezegun import freeze_time
from sqlalchemy.orm import Session

from app.core.models.assessment_summary import AssessmentSummary
from app.core.models.exceptions import UnexpectedItemType
from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia import Multimedia
from app.core.models.multimedia_choice import MultimediaChoice
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.score import Score
from app.core.models.static_item import StaticItem
from app.core.models.submission import Submission
from app.services.assessment_service import AssessmentService


def test_get_assessment_by_id(assessment_service: AssessmentService) -> None:
    assessment_id = "Test Assessment"

    assessment = assessment_service.get_assessment_by_id(assessment_id)

    assert assessment.name == assessment_id
    assert assessment.items == [
        MultipleChoice(
            position=0,
            question=Multimedia(
                location=MinioLocation(
                    bucket="testbucket",
                    key="frage"
                ),
                url="http://some-url",
                type=MediaType.VIDEO
            ),
            choices=(
                MultimediaChoice(
                    location=MinioLocation(
                        bucket="testbucket",
                        key="video_antwort_richtig"
                    ),
                    is_correct=True,
                    url="http://some-url",
                    type=MediaType.VIDEO
                ),
                MultimediaChoice(
                    location=MinioLocation(
                        bucket="testbucket",
                        key="bild_antwort"
                    ),
                    is_correct=False,
                    type=MediaType.IMAGE,
                    url="http://some-url"
                )
            ),
        ),
        StaticItem(
            position=1,
            content=Multimedia(
                location=MinioLocation(
                    bucket="testbucket",
                    key="video"
                ),
                url="http://some-url",
                type=MediaType.VIDEO
            ),
        )
    ]


def test_list_assessments(assessment_service: AssessmentService) -> None:
    assessments = assessment_service.list_assessments()

    assert assessments == [
        AssessmentSummary(id="00", name="00"),
        AssessmentSummary(id="01", name="01")
    ]


@freeze_time("2000-01-01")
@mock.patch("uuid.uuid4", return_value="uuid4-value")
def test_score_assessment(_: str, assessment_service_multiple_choice_only: AssessmentService) -> None:
    session_spy = Mock(Session)

    score = assessment_service_multiple_choice_only.score_assessment(
        "1", {0: [0], 1: [1]},
        user_id="testuser_id",
        session=session_spy
    )

    assert score == Score(points=1, maximum_points=2)
    session_spy.add.assert_called_once_with(
        Submission(
            id="uuid4-value",
            user_id='testuser_id',
            assessment_id='1',
            answers={0: [0], 1: [1]},
            points=1,
            maximum_points=2,
            percentage=0.5
        )
    )


def test_score_assessment_raises_exception_on_static_item(assessment_service: AssessmentService) -> None:
    with pytest.raises(UnexpectedItemType):
        assessment_service.score_assessment("1", {0: [0], 1: [1]}, mock.ANY, mock.ANY)
