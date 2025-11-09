from enum import Enum


class UserRole(Enum):
    FRONTEND_ACCESS = "slas-frontend-user"
    TEST_SCORER = "test-scorer"
    TEST_TAKER = "test-taker"
    MINIO_READWRITE = "readwrite-slportal"
    MINIO_ADMIN = "admin"
    GRAFANA_ADMIN = "admin"
