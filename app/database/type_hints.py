from typing import TypeAlias, TYPE_CHECKING

if TYPE_CHECKING:
    from app.database.tables.assessments import DbAssessment
    from app.database.tables.buckets import DbBucket
    from app.database.tables.choices import DbChoice
    from app.database.tables.exercises import DbExercise
    from app.database.tables.multiple_choice_submissions import DbMultipleChoiceSubmission
    from app.database.tables.multiple_choices import DbMultipleChoice
    from app.database.tables.primers import DbPrimer
    from app.database.tables.submissions import DbSubmission
    from app.database.tables.tasks import DbTask
    from app.database.tables.text_submissions import DbTextSubmission
    from app.database.tables.texts import DbText

Assessment: TypeAlias = "DbAssessment"
Assessments: TypeAlias = "[DbAssessment]"
Bucket: TypeAlias = "DbBucket"
Buckets: TypeAlias = "[DbBucket]"
Choice: TypeAlias = "DbChoice"
Choices: TypeAlias = "[DbChoice]"
Exercise: TypeAlias = "DbExercise"
Exercises: TypeAlias = "[DbExercise]"
MultipleChoice: TypeAlias = "DbMultipleChoice"
MultipleChoices: TypeAlias = "[DbMultipleChoice]"
MulitpleChoiceSubmission: TypeAlias = "DbMultipleChoiceSubmission"
MulitpleChoiceSubmissions: TypeAlias = "[DbMultipleChoiceSubmission]"
Primer: TypeAlias = "DbPrimer"
Primers: TypeAlias = "[DbPrimer]"
Submission: TypeAlias = "DbSubmission"
Submissions: TypeAlias = "[DbSubmission]"
Task: TypeAlias = "DbTask"
Tasks: TypeAlias = "[DbTask]"
TextSubmission: TypeAlias = "DbTextSubmission"
TextSubmissions: TypeAlias = "[DbTextSubmission]"
Text: TypeAlias = "DbText"
Texts: TypeAlias = "[DbText]"
