from fastapi import FastAPI

from app.rest.main import setup_openapi_security_scheme


def test_setup_openapi_security_scheme_modifies_custom_openapi_function() -> None:
    app = FastAPI()
    original_openapi = app.openapi

    setup_openapi_security_scheme(app)

    assert app.openapi != original_openapi
    assert callable(app.openapi)


def test_setup_openapi_security_scheme_adds_bearer_to_components() -> None:
    app = FastAPI()

    @app.get("/test")
    async def test_route():
        return {"message": "test"}

    setup_openapi_security_scheme(app)
    openapi_schema = app.openapi()

    assert openapi_schema is not None
    assert "components" in openapi_schema
    assert "securitySchemes" in openapi_schema["components"]
    assert "Bearer" in openapi_schema["components"]["securitySchemes"]


def test_setup_openapi_security_scheme_bearer_config_is_correct() -> None:
    app = FastAPI()

    @app.get("/test")
    async def test_route():
        return {"message": "test"}

    setup_openapi_security_scheme(app)
    openapi_schema = app.openapi()

    assert openapi_schema is not None
    bearer_config = openapi_schema["components"]["securitySchemes"]["Bearer"]
    assert bearer_config["type"] == "http"
    assert bearer_config["scheme"] == "bearer"
    assert bearer_config["bearerFormat"] == "JWT"
    assert "description" in bearer_config


def test_setup_openapi_security_scheme_applies_security_to_all_routes() -> None:
    app = FastAPI()

    @app.get("/test")
    async def test_route():
        return {"message": "test"}

    setup_openapi_security_scheme(app)
    openapi_schema = app.openapi()

    assert openapi_schema is not None
    assert "security" in openapi_schema
    assert openapi_schema["security"] == [{"Bearer": []}]


def test_setup_openapi_security_scheme_caches_schema() -> None:
    app = FastAPI()

    @app.get("/test")
    async def test_route():
        return {"message": "test"}

    setup_openapi_security_scheme(app)
    schema1 = app.openapi()
    schema2 = app.openapi()

    assert schema1 is not None
    assert schema2 is not None
    assert schema1 is schema2


def test_setup_openapi_security_scheme_preserves_app_metadata() -> None:
    app = FastAPI(
        title="Test API",
        version="1.0.0",
        description="Test Description"
    )

    @app.get("/test")
    async def test_route():
        return {"message": "test"}

    setup_openapi_security_scheme(app)
    openapi_schema = app.openapi()

    assert openapi_schema is not None
    assert openapi_schema["info"]["title"] == "Test API"
    assert openapi_schema["info"]["version"] == "1.0.0"
    assert openapi_schema["info"]["description"] == "Test Description"
