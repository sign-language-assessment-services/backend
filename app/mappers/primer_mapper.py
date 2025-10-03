import logging

from app.core.models.primer import Primer
from app.database.tables.primers import DbPrimer
from app.mappers.multimedia_file_mapper import bucket_object_to_domain

logger = logging.getLogger(__name__)


def primer_to_domain(db_primer: DbPrimer) -> Primer:
    logger.info("Transform DbPrimer into domain model object.")
    primer = Primer(
        id=db_primer.id,
        created_at=db_primer.created_at,
        content=bucket_object_to_domain(db_primer.bucket_object)
    )
    return primer


def primer_to_db(primer: Primer) -> DbPrimer:
    logger.info("Transform primer into database object.")
    db_primer = DbPrimer(
        id=primer.id,
        created_at=primer.created_at,
        bucket_object_id=primer.content.id
    )
    logger.info(
        "Primer database object with id %(_id)s created.",
        {"_id": db_primer.id}
    )
    return db_primer
