from typing import Annotated

from fastapi import APIRouter, Depends

from app.config import Settings
from app.rest.settings import get_settings

router = APIRouter()


@router.get("/")
@router.get("/health")
async def read_root() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/settings")
async def settings(settings: Annotated[Settings, Depends(get_settings)]) -> Settings:
    return settings

