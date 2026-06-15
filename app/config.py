from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = str(Path(__file__).parent.parent / ".env")


class Settings(BaseSettings):
    # Keycloak authentication
    auth_enabled: bool = True

    # Keycloak config
    keycloak_server_url: str = "http://localhost:9000/auth/"
    keycloak_realm: str = "slas"
    algorithms: list[str] = Field(default_factory=lambda: ["RS256"])
    api_audience: str = "backend"
    keycloak_realm_url: str = f"{keycloak_server_url}{keycloak_realm}"
    issuer: str = f"{keycloak_realm_url}"
    keycloak_open_connect_url: str = f"{keycloak_realm_url}/protocol/openid-connect"
    jwks_url: str = f"{keycloak_open_connect_url}/certs"
    token_endpoint: str = f"{keycloak_open_connect_url}/token"

    # Keycloak credentials
    client_id: str
    client_secret: str

    # MinIO
    data_endpoint: str = "127.0.0.1:9030"
    data_bucket_name: str = "slportal"
    data_secure: bool = False
    data_sts_endpoint: str = "http://127.0.0.1:9030"

    # Database connection
    db_type: str = "postgresql"
    db_driver: str = "psycopg2"
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "backend"
    db_password: str
    db_name: str = "backend"

    # Database configuration settings
    db_pool_size: int = 5
    db_pool_timeout: int = 30
    db_pool_recycle: int = 3600
    db_pool_pre_ping: bool = True
    db_max_overflow: int = 10
    db_echo: bool = False
    db_echo_pool: bool = False

    # Database session settings
    db_expire_on_commit: bool = False
    db_autoflush: bool = False

    # Environment variables from .env file in root folder
    model_config = SettingsConfigDict(env_file=ENV_PATH)
