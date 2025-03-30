from uuid import uuid4

from app.core.models.assessment_submission import AssessmentSubmission
from tests.data.models.assessments import assessment_1, assessment_2
from tests.data.models.users import test_taker_1

assessment_submission_1 = AssessmentSubmission(
    id=uuid4(),
    assessment_id=assessment_1.id,
    user_id=test_taker_1.id,
    score=None
)

assessment_submission_2 = AssessmentSubmission(
    id=uuid4(),
    assessment_id=assessment_2.id,
    user_id=test_taker_1.id,
    score=None
)
