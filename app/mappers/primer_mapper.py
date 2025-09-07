from app.core.models.primer import Primer
from app.database.tables.primers import DbPrimer
from app.mappers.multimedia_file_mapper import bucket_object_to_domain


def primer_to_domain(db_primer: DbPrimer) -> Primer:
    return Primer(
        id=db_primer.id,
        created_at=db_primer.created_at,
        content=bucket_object_to_domain(db_primer.bucket_object)
    )


def primer_to_db(primer: Primer) -> DbPrimer:
    return DbPrimer(
        id=primer.id,
        created_at=primer.created_at,
        bucket_object_id=primer.content.id
    )
