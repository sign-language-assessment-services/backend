from fastapi import APIRouter, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(tags=["Health & Monitoring"])


@router.get(
    "/health",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
    description=(
        "The objective of this endpoint is to return {'status': 'ok'} if the "
        "application is running. It does not distinguish between health and "
        "readiness, i.e. does not check if underlying services are healthy. "
    )
)
@router.get(
    "/",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
    description=(
        "The objective of this endpoint is to return {'status': 'ok'} if the "
        "application is running. It does not distinguish between health and "
        "readiness, i.e. does not check if underlying services are healthy. "
    )
)
@limiter.limit(
    limit_value="30/minute",
    error_message="Too many requests: Only 30 requests per minutes are allowed."
)
async def health_check(request: Request):
    _ = request  # requests needed by the limiter to work
    return {"status": "ok"}
