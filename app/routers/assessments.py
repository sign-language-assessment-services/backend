from fastapi import APIRouter

from app.models.assessment import Assessment
from app.models.multiple_choice import MultipleChoice
from app.models.choice import Choice


router = APIRouter()


@router.get("/assessments/{assessment_id}", response_model=Assessment)
async def read_assessment(assessment_id: int):  # pylint: disable=W0613
    assessment = Assessment(
        name="Elefantenprüfung",
        items=(
            MultipleChoice(
                description="Was essen Elefanten?",
                choices=(
                    Choice(
                        label="Spaghetti Bolognese",
                        is_correct=False
                    ),
                    Choice(
                        label="Nüsse",
                        is_correct=True
                    ),
                    Choice(
                        label="Menschen",
                        is_correct=False
                    )
                )
            ),
            MultipleChoice(
                description="Was trinken Elefanten?",
                choices=(
                    Choice(
                        label="Mineralwasser",
                        is_correct=True
                    ),
                    Choice(
                        label="Limonade",
                        is_correct=False
                    ),
                    Choice(
                        label="Wasser",
                        is_correct=True
                    ),
                    Choice(
                        label="Hühnersuppe",
                        is_correct=False
                    )
                )
            ),
        )
    )
    return assessment
