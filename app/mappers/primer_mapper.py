import logging

from app.core.models.primer import Primer
from app.database.tables.primers import DbPrimer
from app.mappers.multimedia_file_mapper import bucket_object_to_domain

logger = logging.getLogger(__name__)


def primer_to_domain(db_primer: DbPrimer) -> Primer:
    logger.debug(
        "Mapping primer to domain model: %(db_primer)r",
        {"db_primer": db_primer}
    )
    return Primer(
        id=db_primer.id,
        created_at=db_primer.created_at,
        content=bucket_object_to_domain(db_primer.bucket_object)
    )


def primer_to_db(primer: Primer) -> DbPrimer:
    logger.debug(
        "Mapping primer to database model: %(primer)r",
        {"primer": primer}
    )
    return DbPrimer(
        id=primer.id,
        created_at=primer.created_at,
        bucket_object_id=primer.content.id
    )
