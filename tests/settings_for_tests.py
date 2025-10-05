from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    __test__ = False  # Prevent pytest from collecting this class as a test

    # Keycloak authentication
    auth_enabled: bool = True

    # Keycloak config
    algorithms: list[str] = Field(default_factory=lambda: ["RS256"])
    api_audience: str = "backend"
    issuer: str = "http://localhost:9000/auth/realms/slas"
    jwks_url: str = "http://localhost:9000/auth/realms/slas/protocol/openid-connect/certs"
    token_endpoint: str = "http://localhost:9000/auth/realms/slas/protocol/openid-connect/token"

    # Keycloak credentials
    client_id: str = "client_id"
    client_secret: str = "client_secret"

    # MinIO
    data_endpoint: str = "127.0.0.1:9030"
    data_bucket_name: str = "slportal"
    data_secure: bool = False
    data_sts_endpoint: str = "http://127.0.0.1:9030"

    # Database connection
    db_type: str = "postgresql"
    db_driver: str = "psycopg2"
    db_host: str = "localhost"
    db_port: int = 32800
    db_user: str = "testuser"
    db_password: str = "testpassword"
    db_name: str = "test"

    # Database configuration settings
    db_pool_size: int = 5
    db_pool_timeout: int = 5
    db_pool_recycle: int = 60
    db_pool_pre_ping: bool = True
    db_max_overflow: int = 0
    db_echo: bool = False  # True
    db_echo_pool: bool = False  # True

    # Database session settings
    db_expire_on_commit: bool = False
    db_autoflush: bool = False

    # Overwrite test settings with .testenv file in root folder
    model_config = SettingsConfigDict(env_file=".testenv")
