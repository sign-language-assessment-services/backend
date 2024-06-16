import datetime
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
from app.database.tables.submissions import DbSubmission
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


@mock.patch.object(
    AssessmentService, AssessmentService.list_assessments.__name__,
    return_value=[
        AssessmentSummary(id="00", name="00"),
        AssessmentSummary(id="01", name="01")
    ]
)
def test_list_assessments(mocked_get_assessment, assessment_service: AssessmentService) -> None:
    mocked_session = Mock()
    assessments = assessment_service.list_assessments(mocked_session)
    assert assessments == [
        AssessmentSummary(id="00", name="00"),
        AssessmentSummary(id="01", name="01")
    ]
    mocked_get_assessment.assert_called_once_with(mocked_session)


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

    session_spy.add.assert_called_once()
    call_object: DbSubmission = session_spy.add.call_args[0][0]
    assert call_object.id == "uuid4-value"
    assert call_object.created_at == datetime.datetime(2000, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)
    assert call_object.user_id == "testuser_id"
    assert call_object.points == 1
    assert call_object.maximum_points == 2
    assert call_object.percentage == 0.5
    assert call_object.assessment_id == "1"


def test_score_assessment_raises_exception_on_static_item(assessment_service: AssessmentService) -> None:
    with pytest.raises(UnexpectedItemType):
        assessment_service.score_assessment("1", {0: [0], 1: [1]}, mock.ANY, mock.ANY)
