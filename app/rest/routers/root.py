from fastapi import APIRouter

router = APIRouter()


@router.get("/")
@router.get("/health")
async def read_root():
    return {"status": "ok"}
