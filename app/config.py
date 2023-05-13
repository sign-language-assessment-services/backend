from pydantic import BaseSettings


class Settings(BaseSettings):
    # Keycloak
    algorithms: list = ["RS256"]
    api_audience: str = "backend"
    auth_enabled: bool = True
    issuer: str = "http://localhost:9000/auth/realms/slas"
    jwks_url: str = "http://localhost:9000/auth/realms/slas/protocol/openid-connect/certs"

    # MinIO
    data_endpoint: str = "data.localhost:9000"
    data_bucket_name: str = "slportal"
    data_root_user: str = "DATA_ROOT_USER"
    data_root_password: str = "DATA_ROOT_PASSWORD"
    data_secure: bool = "false"
