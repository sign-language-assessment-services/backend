from decouple import Csv, config

# Keycloak
# ----------------------------------------------------------------------------
ALGORITHMS = config(
    "ALGORITHMS",
    default="RS256",
    cast=Csv(str),
)
API_AUDIENCE = config(
    "API_AUDIENCE",
    default="backend",
    cast=str,
)
AUTH_ENABLED = config(
    "AUTH_ENABLED",
    default=True,
    cast=bool,
)
ISSUER = config(
    "ISSUER",
    default="http://localhost:8080/realms/slas",
    cast=str,
)
JWKS_URL = config(
    "JWKS_URL",
    default="http://localhost:8080/realms/slas/protocol/openid-connect/certs",
    cast=str,
)

# MinIO
# ----------------------------------------------------------------------------
DATA_ENDPOINT = config(
    "DATA_ENDPOINT",
    default="data.localhost:9000",
    cast=str,
)
DATA_BUCKET_NAME = config(
    "DATA_BUCKET_NAME",
    default="slportal",
    cast=str,
)
DATA_ROOT_USER = config(
    "DATA_ROOT_USER",
    cast=str,
)
DATA_ROOT_PASSWORD = config(
    "DATA_ROOT_PASSWORD",
    cast=str,
)
DATA_SECURE = config(
    "DATA_SECURE",
    default=True,
    cast=bool,
)
