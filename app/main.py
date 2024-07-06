import os

from app.database.orm import get_db_engine, init_db
from app.rest.main import create_app
from app.settings import get_settings


if os.environ.get("SLPORTAL_ENV").upper() != "TESTING":
    init_db(engine=get_db_engine(settings=get_settings()))

app = create_app()
