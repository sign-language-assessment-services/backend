from pathlib import Path

import alembic.command
import alembic.config
from alembic import script
from alembic.runtime.migration import MigrationContext
from dotenv import load_dotenv

from app.database.orm import get_db_engine
from app.settings import get_settings


def test_database_has_the_latest_migration_applied():
    """Test if the database has the latest migration applied

    The database under test is not a temporary test db in this case.
    This test ensures that the running application is using the latest
    changes in the database structure.
    """
    root_path = Path(__file__).parent.parent.parent.parent
    alembic_config = alembic.config.Config(str(root_path / "alembic.ini"))
    alembic_config.set_main_option("script_location", str(root_path / "db_migrations"))
    migrations_folder = script.ScriptDirectory.from_config(alembic_config)
    load_dotenv(dotenv_path=root_path / ".env")
    engine = get_db_engine(settings=get_settings())

    with engine.connect() as connection:
        db_migrations_context = MigrationContext.configure(connection=connection)
        current_revision = db_migrations_context.get_current_revision()

    assert current_revision == migrations_folder.get_current_head()
