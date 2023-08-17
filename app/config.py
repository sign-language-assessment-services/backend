from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Keycloak
    algorithms: list[str] = ["RS256"]
    api_audience: str = "backend"
    auth_enabled: bool = True
    issuer: str = "http://localhost:9000/auth/realms/slas"
    jwks_url: str = "http://localhost:9000/auth/realms/slas/protocol/openid-connect/certs"

    # MinIO
    data_endpoint: str = "127.0.0.1:9030"
    data_bucket_name: str = "slportal"
    data_root_user: str = "minioadmin"
    data_root_password: str = "minioadmin"
    data_secure: bool = False
