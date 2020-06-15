"""Routes for the SLPortal FastAPI app"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def read_root():
    """Read access to endpoint '/'"""
    return {"msg": "Hello World!"}
