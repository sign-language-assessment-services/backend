from uuid import uuid4

from app.core.models.assessment import Assessment
from tests.data.models.exercises import exercise_1, exercise_2
from tests.data.models.primers import primer_1, primer_2


assessment_1 = Assessment(
        id=uuid4(),
        name="Test Assessment 1",
        tasks=[primer_1, exercise_1]
)

assessment_2 = Assessment(
    id=uuid4(),
    name="Test Assessment 2",
    tasks=[primer_2, exercise_2]
)
