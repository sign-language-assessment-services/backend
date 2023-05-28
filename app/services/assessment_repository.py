from app.core.models.assessment import Assessment
from app.core.models.minio_location import MinioLocation
from app.core.models.multiple_choice import MultipleChoice
from app.core.models.video_choice import VideoChoice
from app.core.models.video_question import VideoQuestion


class AssessmentRepository:
    def get_assessment_by_id(self, assessment_id: int) -> Assessment:
        return ASSESSMENTS[assessment_id]


ASSESSMENTS = {
    1: Assessment(
        name="SLAS DSGS GV",
        items=(
            MultipleChoice(
                question=VideoQuestion(
                    location=MinioLocation(
                        bucket="slportal",
                        key="slas_sgs_gv/exercises/1/01_Frage.mp4",
                    ),
                ),
                choices=(
                    VideoChoice(
                        location=MinioLocation(
                            bucket="slportal",
                            key="slas_sgs_gv/exercises/1/01a_Antwort.mp4"
                        ),
                        is_correct=False,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket="slportal",
                            key="slas_sgs_gv/exercises/1/01b_Antwort.mp4"
                        ),
                        is_correct=True,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket="slportal",
                            key="slas_sgs_gv/exercises/1/01c_Antwort.mp4"
                        ),
                        is_correct=False,
                        type="video",
                    ),
                )
            ),
            MultipleChoice(
                question=VideoQuestion(
                    location=MinioLocation(
                        bucket="slportal",
                        key="slas_sgs_gv/exercises/2/02_Frage.mp4",
                    ),
                ),
                choices=(
                    VideoChoice(
                        location=MinioLocation(
                            bucket="slportal",
                            key="slas_sgs_gv/exercises/2/02a_Antwort.mp4"
                        ),
                        is_correct=False,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket="slportal",
                            key="slas_sgs_gv/exercises/2/02b_Antwort.mp4"
                        ),
                        is_correct=True,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket="slportal",
                            key="slas_sgs_gv/exercises/2/02c_Antwort.mp4"
                        ),
                        is_correct=False,
                        type="video",
                    ),
                )
            ),
            MultipleChoice(
                question=VideoQuestion(
                    location=MinioLocation(
                        bucket="slportal",
                        key="slas_sgs_gv/exercises/4/04_Frage.mp4",
                    ),
                ),
                choices=(
                    VideoChoice(
                        location=MinioLocation(
                            bucket="slportal",
                            key="slas_sgs_gv/exercises/4/04a_Antwort.mp4"
                        ),
                        is_correct=False,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket="slportal",
                            key="slas_sgs_gv/exercises/4/04b_Antwort.mp4"
                        ),
                        is_correct=True,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket="slportal",
                            key="slas_sgs_gv/exercises/4/04c_Antwort.mp4"
                        ),
                        is_correct=False,
                        type="video",
                    ),
                )
            ),
            MultipleChoice(
                question=VideoQuestion(
                    location=MinioLocation(
                        bucket="slportal",
                        key="slas_sgs_gv/exercises/5/05_Frage.mp4",
                    ),
                ),
                choices=(
                    VideoChoice(
                        location=MinioLocation(
                            bucket="slportal",
                            key="slas_sgs_gv/exercises/5/05a_Antwort.mp4"
                        ),
                        is_correct=False,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket="slportal",
                            key="slas_sgs_gv/exercises/5/05b_Antwort.mp4"
                        ),
                        is_correct=True,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket="slportal",
                            key="slas_sgs_gv/exercises/5/05c_Antwort.mp4"
                        ),
                        is_correct=False,
                        type="video",
                    ),
                )
            ),
            MultipleChoice(
                question=VideoQuestion(
                    location=MinioLocation(
                        bucket="slportal",
                        key="slas_sgs_gv/exercises/6/06_Frage.mp4",
                    ),
                ),
                choices=(
                    VideoChoice(
                        location=MinioLocation(
                            bucket="slportal",
                            key="slas_sgs_gv/exercises/6/06a_Antwort.mp4"
                        ),
                        is_correct=False,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket="slportal",
                            key="slas_sgs_gv/exercises/6/06b_Antwort.mp4"
                        ),
                        is_correct=True,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket="slportal",
                            key="slas_sgs_gv/exercises/6/06c_Antwort.mp4"
                        ),
                        is_correct=False,
                        type="video",
                    ),
                )
            ),
            MultipleChoice(
                question=VideoQuestion(
                    location=MinioLocation(
                        bucket="slportal",
                        key="slas_sgs_gv/exercises/8/08_Frage.mp4",
                    ),
                ),
                choices=(
                    VideoChoice(
                        location=MinioLocation(
                            bucket="slportal",
                            key="slas_sgs_gv/exercises/8/08a_Antwort.mp4"
                        ),
                        is_correct=False,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket="slportal",
                            key="slas_sgs_gv/exercises/8/08b_Antwort.mp4"
                        ),
                        is_correct=True,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket="slportal",
                            key="slas_sgs_gv/exercises/8/08c_Antwort.mp4"
                        ),
                        is_correct=False,
                        type="video",
                    ),
                )
            ),
            MultipleChoice(
                question=VideoQuestion(
                    location=MinioLocation(
                        bucket="slportal",
                        key="slas_sgs_gv/exercises/10/10_Frage.mp4",
                    ),
                ),
                choices=(
                    VideoChoice(
                        location=MinioLocation(
                            bucket="slportal",
                            key="slas_sgs_gv/exercises/10/10a_Antwort.mp4"
                        ),
                        is_correct=False,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket="slportal",
                            key="slas_sgs_gv/exercises/10/10b_Antwort.mp4"
                        ),
                        is_correct=True,
                        type="video",
                    ),
                    VideoChoice(
                        location=MinioLocation(
                            bucket="slportal",
                            key="slas_sgs_gv/exercises/10/10c_Antwort.mp4"
                        ),
                        is_correct=False,
                        type="video",
                    ),
                )
            ),
        )
    )
}
