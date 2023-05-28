import pytest

from app.services.assessment_service import AssessmentService


def test_get_assessment_by_id(object_storage_client, repository, settings):
    assessment_service = AssessmentService(object_storage_client, repository, settings)
    assessment_id = 1

    assessment = assessment_service.get_assessment_by_id(assessment_id)

    repository.get_assessment_by_id.assert_called_once_with(assessment_id)
    assert assessment.name == "Test Assessment"
    for item in assessment.items:
        assert item.question.url == "http://some-url"
        assert all([choice.url == "http://some-url" for choice in item.choices])


def test_exception_is_thrown_if_assessment_does_not_exist(object_storage_client, repository, settings):
    assessment_service = AssessmentService(object_storage_client, repository, settings)
    repository.get_assessment_by_id.side_effect = KeyError('4711')

    with pytest.raises(KeyError, match="4711"):
        assessment_service.get_assessment_by_id(4711)


def test_score_assessment(object_storage_client, repository, settings):
    assessment_service = AssessmentService(object_storage_client, repository, settings)

    score = assessment_service.score_assessment(1, {0: [1], 1: [0]})

    assert score == {"score": 2}
