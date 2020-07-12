"""Main file for SLPortal FastAPI app"""

from fastapi import FastAPI

from .routers import assessments, root


app = FastAPI()

app.include_router(root.router)
app.include_router(assessments.router)
