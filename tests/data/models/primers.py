from uuid import uuid4

from app.core.models.primer import Primer
from tests.data.models.multimedia_files import multimedia_file_primer_1, multimedia_file_primer_2

primer_1 = Primer(
    id=uuid4(),
    content=multimedia_file_primer_1
)

primer_2 = Primer(
    id=uuid4(),
    content=multimedia_file_primer_2
)
