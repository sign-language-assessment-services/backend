class NotFoundException(Exception):
    """Base class for all "NotFound"-exceptions."""
    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or "Resource not found.")


class AssessmentSubmissionNotFoundException(NotFoundException):
    pass


class AssessmentNotFoundException(NotFoundException):
    pass


class ChoiceNotFoundException(NotFoundException):
    pass


class ExerciseSubmissionNotFoundException(NotFoundException):
    pass


class ExerciseNotFoundException(NotFoundException):
    pass


class MultimediaFileNotFoundException(NotFoundException):
    pass


class MultipleChoiceNotFoundException(NotFoundException):
    pass


class PrimerNotFoundException(NotFoundException):
    pass


class TaskNotFoundException(NotFoundException):
    pass
