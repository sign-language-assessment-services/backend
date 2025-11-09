from unittest.mock import ANY

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.rest.requests.assessment_submissions import AssessmentSubmissionScope
from tests.data.models.assessment_submissions import (
    assessment_submission_1, assessment_submission_2
)
from tests.data.models.users import test_scorer_1, test_taker_1


def test_create_assessment_submission(test_client: TestClient) -> None:
    assessment_id = str(assessment_submission_1.assessment_id)

    response = test_client.post(f"/assessments/{assessment_id}/submissions/").json()

    assert response == {"id": ANY}
    assert isinstance(response["id"], str)


def test_get_assessment_submission(test_client: TestClient) -> None:
    submission_id = assessment_submission_1.id

    response = test_client.get(f"/assessment_submissions/{submission_id}").json()

    assert response == {
        "id": str(submission_id),
        "user_id": str(test_taker_1.id),
        "assessment_id": str(assessment_submission_1.assessment_id),
        "score": None,
        "finished": False,
        "finished_at": None
    }


def test_list_assessment_submissions(test_client: TestClient) -> None:
    response = test_client.get("/assessment_submissions/").json()

    assert response == [
        {
            "id": str(assessment_submission_1.id),
            "assessment_id": str(assessment_submission_1.assessment_id),
            "user_id": str(test_taker_1.id)
        },
        {
            "id": str(assessment_submission_2.id),
            "assessment_id": str(assessment_submission_2.assessment_id),
            "user_id": str(test_taker_1.id)
        }
    ]


@pytest.mark.parametrize(
    "scope, response_status_code", [
        (AssessmentSubmissionScope.ALL, status.HTTP_200_OK),
        (AssessmentSubmissionScope.MINE, status.HTTP_400_BAD_REQUEST)
    ]
)
def test_list_assessment_submissions_user_id_filter_uses_scope_all(
        test_client_with_scorer_role: TestClient,
        scope: AssessmentSubmissionScope,
        response_status_code: int
) -> None:
    query_params = {"user_id": str(test_scorer_1.id), "scope": scope.value}

    response = test_client_with_scorer_role.get("/assessment_submissions/", params=query_params)

    assert response.status_code == response_status_code


def test_list_assessment_submissions_scope_all_test_taker(test_client: TestClient) -> None:
    query_params = {"scope": AssessmentSubmissionScope.ALL.value}

    response = test_client.get("/assessment_submissions/", params=query_params)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_list_assessment_submissions_scope_all_test_scorer(test_client_with_scorer_role: TestClient) -> None:
    query_params = {"scope": AssessmentSubmissionScope.ALL.value}

    response = test_client_with_scorer_role.get("/assessment_submissions/", params=query_params)

    assert response.status_code == status.HTTP_200_OK


def test_update_assessment_submission_finished(test_client: TestClient) -> None:
    response = test_client.put(
        f"/assessment_submissions/{assessment_submission_1.id}",
        json={"finished": True}
    ).json()

    assert response["id"] == str(assessment_submission_1.id)
    assert response["finished"] is True
    assert response["score"] == 42
    assert response["finished_at"] is not None
