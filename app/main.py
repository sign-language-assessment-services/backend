from app.database.orm import get_db_engine, init_db
from app.rest.main import create_app
from app.settings import get_settings


init_db(engine=get_db_engine(settings=get_settings()))
app = create_app()
