from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def read_root():
    return {"msg": "Hello World!"}
