# REST Layer (Presentation Layer)

## Architectural Intent

The REST layer serves as the **Presentation Layer** in our layered architecture. It is the outermost layer responsible for handling HTTP communication with clients and translating external requests into domain operations.

## Core Responsibilities

1. **HTTP Request/Response Handling** - Accept HTTP requests, return HTTP responses
2. **Input Validation** - Validate incoming data using Pydantic models
3. **Authentication & Authorization** - Enforce security policies
4. **Serialization/Deserialization** - Convert between JSON and Python objects
5. **Error Handling** - Translate domain exceptions to HTTP status codes
6. **API Documentation** - Generate OpenAPI/Swagger documentation

## Architectural Patterns Applied

### 1. **Front Controller Pattern** (Fowler - P of EAA)

**Intent:** A single entry point handles all requests and dispatches to appropriate handlers.

**Implementation:**
- `main.py:create_app()` - Central application factory
- All routers registered in one place
- Global exception handlers
- Middleware applied uniformly

```python
def create_app() -> FastAPI:
    app = FastAPI(...)
    app.include_router(assessments.router)
    app.include_router(exercises.router)
    # ... all routers
    app.add_exception_handler(NotFoundException, handler)
    return app
```

**Benefits:**
- Single point of configuration
- Consistent error handling
- Centralized security policies

---

### 2. **Data Transfer Object (DTO)** (Fowler - P of EAA)

**Intent:** Carry data between presentation and service layers without exposing domain internals.

**Implementation:**
- `requests/` - Input DTOs (Request Models)
- `responses/` - Output DTOs (Response Models)
- Separate from domain models in `core/models/`

```python
# requests/assessments.py
class CreateAssessmentRequest(BaseModel):
    name: str
    tasks: list[UUID]

# responses/assessments.py
class GetAssessmentResponse(BaseModel):
    id: UUID
    name: str
    tasks: list[TaskResponse]
```

**Benefits:**
- API contract independent of domain model
- Can evolve separately
- Prevents over-fetching/under-fetching
- Type-safe validation (Pydantic)

**Fowler's Wisdom:**
> "The main reason you need a DTO is for assemblage—to get data from multiple sources and package it for transfer."

---

### 3. **Dependency Injection** (Fowler, Uncle Bob)

**Intent:** Invert dependencies, making code testable and decoupled.

**Implementation:**
- FastAPI's `Depends()` mechanism
- `dependencies.py` - Shared dependencies
- Services injected into route handlers

```python
async def create_assessment(
    data: CreateAssessmentRequest,
    assessment_service: Annotated[AssessmentService, Depends()],
    db_session: Annotated[Session, Depends(get_db_session)]
):
    # Dependencies injected by framework
    assessment = assessment_service.create_assessment(...)
    return assessment
```

**Benefits:**
- Testable (can inject mocks)
- Loose coupling
- Follows Dependency Inversion Principle (SOLID)

---

### 4. **Separation of Concerns** (Uncle Bob - Clean Architecture)

**Intent:** Each module has one well-defined responsibility.

**Implementation:**
```
rest/
  ├── routers/         # HTTP endpoint definitions (one per entity)
  ├── requests/        # Request validation models
  ├── responses/       # Response serialization models
  ├── dependencies.py  # Shared dependencies (auth, DB session)
  ├── filters/         # Query filtering logic
  └── main.py          # Application factory
```

**Benefits:**
- Easy to locate functionality
- Changes are localized
- Clear module boundaries

---

## Layer Rules & Constraints

### ✅ ALLOWED Dependencies

The REST layer MAY depend on:
- **Service Layer** (`app.services.*`) - To execute business logic
- **Core Models** (`app.core.models.*`) - For domain types
- **Database ORM** (`app.database.orm`) - For session management only
- **External Services** (`app.external_services.*`) - For auth, etc.

### ❌ FORBIDDEN Dependencies

The REST layer MUST NOT:
- **Directly access Repositories** - Business logic belongs in services
- **Directly access Database Tables** - Violates layering
- **Directly access Mappers** - Transformation is service responsibility
- **Contain business logic** - Keep routers thin, delegate to services

### Dependency Flow

```
REST Layer
    ↓ (depends on)
Service Layer
    ↓ (depends on)
Repository Layer
```

**Rule:** Dependencies point INWARD, never outward.

---

## Key Design Principles (SOLID)

### Single Responsibility Principle (SRP)

Each router handles ONE entity:
- `assessments.py` - Assessment operations only
- `exercises.py` - Exercise operations only
- `submissions.py` - Submission operations only

Each file in `requests/` and `responses/` represents ONE use case.

### Dependency Inversion Principle (DIP)

Routers depend on abstractions (service interfaces), not concrete implementations:
```python
# Good: Depends on abstract Session type
db_session: Annotated[Session, Depends(get_db_session)]

# Good: Framework resolves concrete service
service: Annotated[AssessmentService, Depends()]
```

### Open/Closed Principle (OCP)

- New endpoints added without modifying existing code
- New DTOs extend BaseModel without changing base
- Exception handlers can be added without changing routers

---

## Security Patterns

### Authentication via JWT Bearer Token

**Pattern:** Token-Based Authentication (Industry Standard)

```python
@router.post(
    "/assessments/",
    dependencies=[
        Depends(JWTBearer()),                      # Authentication
        Depends(require_roles([UserRole.FRONTEND]))  # Authorization
    ]
)
```

**Implementation:**
- `dependencies.py:get_current_user()` - Extracts user from JWT
- `dependencies.py:require_roles()` - Role-based access control
- Keycloak validates tokens

**Benefits:**
- Stateless (no server-side sessions)
- Scalable
- Industry standard (OAuth2/OIDC)

---

## Router Structure Template

Every router follows this pattern:

```python
import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.models.role import UserRole
from app.database.orm import get_db_session
from app.external_services.keycloak.auth_bearer import JWTBearer
from app.rest.dependencies import require_roles
from app.rest.requests.{entity} import Create{Entity}Request
from app.rest.responses.{entity} import Create{Entity}Response
from app.services.{entity}_service import {Entity}Service

logger = logging.getLogger(__name__)

# Router with security dependencies
router = APIRouter(
    dependencies=[
        Depends(JWTBearer()),
        Depends(require_roles([UserRole.FRONTEND]))
    ],
    tags=["{Entities}"]
)

# Endpoint pattern: verb + entity + optional qualifier
@router.post(
    "/{entities}/",
    response_model=Create{Entity}Response,
    status_code=status.HTTP_200_OK
)
async def create_{entity}(
    data: Create{Entity}Request,                           # Request DTO
    service: Annotated[{Entity}Service, Depends()],        # Service injection
    db_session: Annotated[Session, Depends(get_db_session)]  # DB session
):
    """
    Create a new {entity}.

    - **name**: {Entity} name (required)
    - Returns: Created {entity} with ID
    """
    entity = service.create_{entity}(
        session=db_session,
        **data.model_dump()
    )
    return entity
```

---

## Common Patterns in This Layer

### 1. **Request-Response Pattern**

```
Client Request → DTO Validation → Service Call → DTO Serialization → Client Response
```

### 2. **Transaction Boundaries**

Database sessions are managed at the REST layer:
```python
async def endpoint(
    db_session: Annotated[Session, Depends(get_db_session)]
):
    # Session auto-commits on success, rolls back on exception
    service.do_something(session=db_session)
```

**Why here?** HTTP request = transaction boundary (unit of work)

### 3. **Exception Translation**

Domain exceptions → HTTP status codes:
```python
# In main.py
app.add_exception_handler(NotFoundException, not_found_exception_handler)

async def not_found_exception_handler(_, exc: NotFoundException):
    return ORJSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )
```

---

## FastAPI-Specific Best Practices

### 1. **Use Pydantic for Validation**

```python
class CreateAssessmentRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    tasks: list[UUID] = Field(default_factory=list)

    @field_validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v
```

### 2. **Use Annotated for Dependencies**

```python
# Modern (Python 3.10+)
service: Annotated[AssessmentService, Depends()]

# Old style (avoid)
service: AssessmentService = Depends()
```

### 3. **Use Response Models**

Always specify `response_model` for type safety and OpenAPI docs:
```python
@router.get("/assessments/{id}", response_model=GetAssessmentResponse)
```

### 4. **Use Status Code Constants**

```python
status_code=status.HTTP_200_OK  # Not: status_code=200
```

---

## Anti-Patterns to Avoid

### ❌ **1. Business Logic in Routers**

```python
# BAD: Business logic in router
@router.post("/assessments/")
async def create_assessment(data, session):
    if len(data.tasks) > 50:  # ❌ Business rule in router
        raise ValueError("Too many tasks")

    assessment = DbAssessment(name=data.name)  # ❌ Direct ORM usage
    session.add(assessment)
    return assessment

# GOOD: Delegate to service
@router.post("/assessments/")
async def create_assessment(data, service, session):
    return service.create_assessment(session, data.name, data.tasks)
```

### ❌ **2. Exposing Domain Models Directly**

```python
# BAD: Return domain model as-is
@router.get("/assessments/{id}", response_model=Assessment)
                                               # ^^^ Domain model leaked

# GOOD: Use Response DTO
@router.get("/assessments/{id}", response_model=GetAssessmentResponse)
                                               # ^^^ Presentation DTO
```

### ❌ **3. Bypassing Service Layer**

```python
# BAD: Direct repository access
@router.post("/assessments/")
async def create_assessment(data, session):
    assessment = Assessment(...)
    add_assessment(session, assessment)  # ❌ Calling repository directly

# GOOD: Through service
@router.post("/assessments/")
async def create_assessment(data, service, session):
    return service.create_assessment(...)  # ✅ Service orchestrates
```

---

## Testing Strategy

### Unit Tests

Mock services, test request/response handling:
```python
def test_create_assessment_endpoint(mock_service):
    mock_service.create_assessment.return_value = Assessment(...)

    response = client.post("/assessments/", json={"name": "Test"})

    assert response.status_code == 200
    assert response.json()["name"] == "Test"
```

### Integration Tests

Test with real services, mocked database:
```python
def test_create_assessment_integration(test_db):
    response = client.post("/assessments/", json={
        "name": "Integration Test",
        "tasks": [str(uuid4())]
    })
    assert response.status_code == 200
```

---

## References

**Books:**
- Fowler, Martin. *Patterns of Enterprise Application Architecture*. 2002.
  - Front Controller (p344)
  - Data Transfer Object (p401)
  - Service Layer (p133)

- Martin, Robert C. *Clean Architecture*. 2017.
  - Dependency Rule
  - Boundaries and Interfaces

**FastAPI Documentation:**
- Dependency Injection: https://fastapi.tiangolo.com/tutorial/dependencies/
- Security: https://fastapi.tiangolo.com/tutorial/security/

**Related Patterns:**
- Model-View-Controller (MVC) - This layer is the "Controller"
- Gateway Pattern - Routers act as gateways to backend services
- Adapter Pattern - REST adapts HTTP to domain operations

---

## Summary

The REST layer is a **thin presentation layer** that:
- ✅ Handles HTTP concerns (requests, responses, status codes)
- ✅ Validates input using DTOs
- ✅ Enforces authentication and authorization
- ✅ Delegates all business logic to services
- ❌ Contains NO business logic
- ❌ Does NOT directly access repositories or database

**Keep it thin. Keep it focused. Keep it at the boundary.**
