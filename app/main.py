from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from app.rest.main import create_app

app = create_app()
