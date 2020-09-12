from ..models.assessment import Assessment
from ..models.choice import Choice
from ..models.multiple_choice import MultipleChoice


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

repository = {1: assessment}


def get_assessment_by_id(assessment_id: int) -> Assessment:
    return repository.get(assessment_id, None)


def score_assessment(assessment_id: int, submission) -> int:
    assessment = repository.get(assessment_id)
    return assessment.score(submission)
