"""Main file for SLPortal FastAPI app"""

from fastapi import FastAPI

from .routers import root


app = FastAPI()

app.include_router(root.router)
