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
Assessments: TypeAlias = list["DbAssessment"]
Bucket: TypeAlias = "DbBucket"
Buckets: TypeAlias = list["DbBucket"]
Choice: TypeAlias = "DbChoice"
Choices: TypeAlias = list["DbChoice"]
Exercise: TypeAlias = "DbExercise"
Exercises: TypeAlias = list["DbExercise"]
MultipleChoice: TypeAlias = "DbMultipleChoice"
MultipleChoices: TypeAlias = list["DbMultipleChoice"]
MulitpleChoiceSubmission: TypeAlias = "DbMultipleChoiceSubmission"
MultipleChoiceSubmissions: TypeAlias = list["DbMultipleChoiceSubmission"]
Primer: TypeAlias = "DbPrimer"
Primers: TypeAlias = list["DbPrimer"]
Submission: TypeAlias = "DbSubmission"
Submissions: TypeAlias = list["DbSubmission"]
Task: TypeAlias = "DbTask"
Tasks: TypeAlias = list["DbTask"]
TextSubmission: TypeAlias = "DbTextSubmission"
TextSubmissions: TypeAlias = list["DbTextSubmission"]
Text: TypeAlias = "DbText"
Texts: TypeAlias = list["DbText"]
