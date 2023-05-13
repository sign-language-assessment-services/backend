from typing import Annotated

from fastapi import FastAPI, Depends, Request, Header, HTTPException

from app.authorization.token_verifier import TokenVerifier
from app.rest.routers import assessments, root


async def verify_token(authorization: Annotated[str, Header()], token_verifier: Annotated[TokenVerifier, Depends()]):
    scopes, user = token_verifier.verify_authorization_header(authorization)
    print(scopes)
    print(user)
    # if authorization != "fake-super-secret-token":
    #     raise HTTPException(status_code=400, detail="X-Token header invalid")


def create_app() -> FastAPI:
    app = FastAPI(dependencies=[Depends(verify_token)])

    # @app.middleware("http")
    # async def add_process_time_header(request: Request, call_next, token_verifier: Annotated[TokenVerifier, Depends()]):
    #     token_verifier.verify_authorization_header(request.headers)
    #     response = await call_next(request)
    #     return response

    app.include_router(root.router)
    app.include_router(assessments.router)

    # app.add_middleware(AuthMiddleware, verify_header=verify_authorization_header)


    return app
