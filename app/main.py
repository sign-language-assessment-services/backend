from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

# pylint: disable=wrong-import-position
from app.rest.main import create_app

app = create_app()
