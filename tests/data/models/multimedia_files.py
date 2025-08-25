from uuid import uuid4

from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia_file import MultimediaFile

multimedia_file_primer_1 = MultimediaFile(
    id=uuid4(),
    location=MinioLocation(
        bucket="testbucket",
        key="primer-1.mpg"
    ),
    media_type=MediaType.VIDEO,
    url="http://some-url/"
)

multimedia_file_primer_2 = MultimediaFile(
    id=uuid4(),
    location=MinioLocation(
        bucket="testbucket",
        key="primer-2.mpg"
    ),
    media_type=MediaType.VIDEO,
    url="http://some-url/"
)

multimedia_file_question_1 = MultimediaFile(
    id=uuid4(),
    location=MinioLocation(
        bucket="testbucket",
        key="question-1.mpg"
    ),
    media_type=MediaType.VIDEO,
    url="http://some-url/"
)

multimedia_file_question_2 = MultimediaFile(
    id=uuid4(),
    location=MinioLocation(
        bucket="testbucket",
        key="question-2.mpg"
    ),
    media_type=MediaType.VIDEO,
    url="http://some-url/"
)

multimedia_file_choice_1 = MultimediaFile(
    id=uuid4(),
    location=MinioLocation(
        bucket="testbucket",
        key="choice-1.mpg"
    ),
    media_type=MediaType.VIDEO,
    url="http://some-url/"
)

multimedia_file_choice_2 = MultimediaFile(
    id=uuid4(),
    location=MinioLocation(
        bucket="testbucket",
        key="choice-2.mpg"
    ),
    media_type=MediaType.VIDEO,
    url="http://some-url/"
)

multimedia_file_choice_3 = MultimediaFile(
    id=uuid4(),
    location=MinioLocation(
        bucket="testbucket",
        key="choice-3.mpg"
    ),
    media_type=MediaType.VIDEO,
    url="http://some-url/"
)

multimedia_file_choice_4 = MultimediaFile(
    id=uuid4(),
    location=MinioLocation(
        bucket="testbucket",
        key="choice-4.mpg"
    ),
    media_type=MediaType.VIDEO,
    url="http://some-url/"
)

multimedia_file_choice_5 = MultimediaFile(
    id=uuid4(),
    location=MinioLocation(
        bucket="testbucket",
        key="choice-5.mpg"
    ),
    media_type=MediaType.VIDEO,
    url="http://some-url/"
)

multimedia_file_choice_6 = MultimediaFile(
    id=uuid4(),
    location=MinioLocation(
        bucket="testbucket",
        key="choice-6.mpg"
    ),
    media_type=MediaType.VIDEO,
    url="http://some-url/"
)

multimedia_file_choice_7 = MultimediaFile(
    id=uuid4(),
    location=MinioLocation(
        bucket="testbucket",
        key="choice-7.mpg"
    ),
    media_type=MediaType.VIDEO,
    url="http://some-url/"
)

multimedia_file_choice_8 = MultimediaFile(
    id=uuid4(),
    location=MinioLocation(
        bucket="testbucket",
        key="choice-8.mpg"
    ),
    media_type=MediaType.VIDEO,
    url="http://some-url/"
)
