# Backend Architecture Documentation

## Overview

This document provides an overview of the backend architecture and points to detailed layer-specific documentation.

## Architecture Style

**Layered Architecture** with **Transaction Script** pattern for business logic.

### Architectural Influences

- **Martin Fowler** - *Patterns of Enterprise Application Architecture* (2002)
- **Eric Evans** - *Domain-Driven Design* (2003)
- **Robert C. Martin (Uncle Bob)** - *Clean Architecture* (2017)
- **Gang of Four** - *Design Patterns* (1994)

---

## Layer Structure

```
┌─────────────────────────────────────────┐
│         REST Layer                      │  ← HTTP/JSON Interface
│         (Presentation)                  │  ← app/rest/
├─────────────────────────────────────────┤
│         Service Layer                   │  ← Business Logic
│         (Transaction Scripts)           │  ← app/services/
├─────────────────────────────────────────┤
│         Repository Layer                │  ← Data Access
│         (Collection Interface)          │  ← app/repositories/
├─────────────────────────────────────────┤
│         Mapper Layer                    │  ← Transformation
│         (Data Mapper)                   │  ← app/mappers/
├─────────────────────────────────────────┤
│         Database Layer                  │  ← ORM Models
│         (Persistence)                   │  ← app/database/
└─────────────────────────────────────────┘
             ↕
┌─────────────────────────────────────────┐
│         Core Layer                      │  ← Domain Models
│         (Domain)                        │  ← app/core/
└─────────────────────────────────────────┘
```

### Dependency Rule

**Dependencies point INWARD:**
```
REST → Services → Repositories → Mappers → Database
  ↓       ↓           ↓            ↓          ↓
  └───────┴───────────┴────────────┴──────────┴→ Core
```

**Core has NO dependencies** - it's the center of the architecture.

---

## Layer Documentation

Each layer has detailed documentation in its respective directory:

### 📋 [REST Layer](app/rest/README.md)
**Responsibility:** HTTP request/response handling, API endpoints

**Patterns:**
- Front Controller Pattern
- Data Transfer Object (DTO)
- Dependency Injection

**Key Files:**
- `main.py` - Application factory
- `routers/` - API endpoints
- `requests/` - Request DTOs
- `responses/` - Response DTOs

---

### 🔧 [Service Layer](app/services/README.md)
**Responsibility:** Business logic orchestration, transaction boundaries

**Patterns:**
- Service Layer Pattern
- Transaction Script Pattern
- Facade Pattern

**Key Files:**
- `assessment_service.py` - Assessment operations
- `exercise_service.py` - Exercise operations
- `scoring_service.py` - Score calculation

**⚠️ Current Issues:**
- Static methods (should be instance methods)
- Some direct ORM access (should use repositories)

---

### 💾 [Repository Layer](app/repositories/README.md)
**Responsibility:** Data access abstraction, CRUD operations

**Patterns:**
- Repository Pattern
- Data Mapper Pattern (via mappers)
- Unit of Work Pattern (via Session)

**Key Files:**
- `assessments.py` - Assessment data access
- `exercises.py` - Exercise data access
- `utils.py` - Shared CRUD utilities

**Rules:**
- Always returns domain models, never DB models
- No business logic
- Session passed in, not managed

---

### 🔄 [Mapper Layer](app/mappers/README.md)
**Responsibility:** Transform between domain models and database models

**Patterns:**
- Data Mapper Pattern
- Adapter Pattern
- Bidirectional Transformation

**Key Files:**
- `assessment_mapper.py` - Assessment transformations
- `exercise_mapper.py` - Exercise transformations

**Functions:**
- `{entity}_to_domain()` - DB → Domain
- `{entity}_to_db()` - Domain → DB

**Rules:**
- No business logic
- No database access
- Pure transformation

---

### 🗄️ [Database Layer](app/database/README.md)
**Responsibility:** Database schema, ORM models, session management

**Patterns:**
- Object-Relational Mapping (ORM)
- Table Module Pattern
- Foreign Key Mapping
- Association Table Mapping
- Single Table Inheritance

**Key Files:**
- `orm.py` - Engine, session factory
- `tables/base.py` - Base model class
- `tables/assessments.py` - Assessment table
- `tables/tasks.py` - Task inheritance hierarchy

**Tools:**
- SQLAlchemy ORM
- Alembic migrations

---

### 🎯 [Core Layer](app/core/README.md)
**Responsibility:** Domain models, business entities

**Patterns:**
- Domain Model Pattern (Anemic style)
- Entity Pattern
- Value Object Pattern
- Composite Pattern

**Key Files:**
- `models/assessment.py` - Assessment entity
- `models/exercise.py` - Exercise entity
- `models/choice.py` - Choice value object
- `models/role.py` - User roles enum

**Current Style:** Anemic Domain Model (acceptable for CRUD apps)

**Rules:**
- No dependencies on other layers
- Pure domain concepts
- Type-safe via Pydantic

---

## Key Architectural Decisions

### 1. **Layered Architecture**

**Why?**
- Clear separation of concerns
- Easy to understand and navigate
- Standard pattern, well-documented
- Testable

**Trade-offs:**
- Can feel over-engineered for simple CRUD
- Multiple files for one feature
- ✅ Worth it for maintainability

---

### 2. **Transaction Script (Not Rich Domain Model)**

**Why?**
- Application is CRUD-heavy
- Simple business logic
- FastAPI/Pydantic ecosystem preference
- Team productivity

**Trade-offs:**
- Logic spread across service methods
- Potential duplication
- ✅ Acceptable for this complexity level

**Martin Fowler:**
> "For simple problems, Transaction Script works just fine and is easier to write than Domain Model."

---

### 3. **Data Mapper (Not Active Record)**

**Why?**
- Separation of domain and persistence
- Pydantic models (domain) separate from SQLAlchemy (DB)
- More testable
- Independent evolution

**Trade-offs:**
- More boilerplate (mapper functions)
- Extra transformation step
- ✅ Worth it for clean architecture

---

### 4. **Anemic Domain Model (Not Rich Domain Model)**

**Why?**
- Pydantic models are data-focused
- Simple validation rules
- Fits Transaction Script pattern

**Trade-offs:**
- No behavior in domain objects
- Business logic in services
- ⚠️ Could evolve to Rich Domain Model if complexity grows

---

## Architectural Principles Applied

### SOLID Principles

| Principle | Application | Compliance |
|-----------|-------------|------------|
| **Single Responsibility** | Each layer, class, function has one job | ⚠️ Good (some service violations) |
| **Open/Closed** | Extend via new classes/functions, not modification | ✅ Good |
| **Liskov Substitution** | Subtypes (Primer/Exercise) are substitutable | ✅ Excellent |
| **Interface Segregation** | Focused interfaces (implicit in Python) | ✅ Good |
| **Dependency Inversion** | Depend on abstractions (Session, not concrete) | ⚠️ Partial (no abstract base classes) |

### Clean Architecture Principles

| Principle | Application |
|-----------|-------------|
| **Dependency Rule** | ✅ Dependencies point inward |
| **Independent of Frameworks** | ⚠️ Partial (Pydantic, FastAPI integrated) |
| **Testable** | ✅ Each layer testable in isolation |
| **Independent of UI** | ✅ Domain independent of REST |
| **Independent of Database** | ✅ Domain independent of ORM |

---

## Common Patterns

### Creating a New Entity

When adding a new entity (e.g., `Quiz`), create files in this order:

1. **Domain Model** (`app/core/models/quiz.py`)
   ```python
   class Quiz(BaseModel):
       id: UUID
       name: str
   ```

2. **Database Table** (`app/database/tables/quizzes.py`)
   ```python
   class DbQuiz(DbBase):
       __tablename__ = "quizzes"
       name: Mapped[str]
   ```

3. **Mapper** (`app/mappers/quiz_mapper.py`)
   ```python
   def quiz_to_domain(db_quiz: DbQuiz) -> Quiz: ...
   def quiz_to_db(quiz: Quiz) -> DbQuiz: ...
   ```

4. **Repository** (`app/repositories/quizzes.py`)
   ```python
   def add_quiz(session: Session, quiz: Quiz) -> None: ...
   def get_quiz(session: Session, id: UUID) -> Quiz | None: ...
   ```

5. **Service** (`app/services/quiz_service.py`)
   ```python
   class QuizService:
       def create_quiz(self, session: Session, name: str) -> Quiz: ...
   ```

6. **DTOs** (`app/rest/requests/quizzes.py`, `app/rest/responses/quizzes.py`)
   ```python
   class CreateQuizRequest(BaseModel): ...
   class GetQuizResponse(BaseModel): ...
   ```

7. **Router** (`app/rest/routers/quizzes.py`)
   ```python
   @router.post("/quizzes/")
   async def create_quiz(...): ...
   ```

8. **Register Router** (`app/rest/main.py`)
   ```python
   app.include_router(quizzes.router)
   ```

---

## Testing Strategy

### Unit Tests

Test each layer in isolation:

```python
# Service layer (mock repository)
def test_create_assessment(mock_repo):
    service = AssessmentService(mock_repo)
    assessment = service.create_assessment(...)
    mock_repo.add.assert_called_once()

# Repository layer (mock mapper, session)
def test_add_assessment(mock_session, mock_mapper):
    add_assessment(mock_session, assessment)
    mock_session.add.assert_called_once()

# Mapper layer (no mocks)
def test_assessment_to_domain():
    db_model = DbAssessment(...)
    domain = assessment_to_domain(db_model)
    assert domain.name == db_model.name
```

### Integration Tests

Test multiple layers together:

```python
# Service + Repository + Database (testcontainers)
def test_create_and_get_assessment(test_db):
    service = AssessmentService(test_db)

    # Create
    assessment = service.create_assessment(test_db, "Test")

    # Retrieve
    result = service.get_assessment_by_id(test_db, assessment.id)

    assert result.name == "Test"
```

### End-to-End Tests

Test through REST API:

```python
def test_api_create_assessment(client):
    response = client.post("/assessments/", json={
        "name": "E2E Test",
        "tasks": []
    })

    assert response.status_code == 200
    assert response.json()["name"] == "E2E Test"
```

---

## Known Issues & Improvements

### Current Issues

1. **Static Methods in Services** ⚠️
   - Services have `@staticmethod` but also inject dependencies
   - Should use instance methods
   - **Fix:** Remove `@staticmethod`, make all methods instance methods

2. **Service Layer Violations** ⚠️
   - Some services directly access ORM (`session.get()`)
   - Should use repositories
   - **Fix:** Add repository methods, use them in services

3. **No Abstract Base Classes** ⚠️
   - Services/Repositories are concrete classes
   - Hard to swap implementations
   - **Fix:** Add `IAssessmentRepository(ABC)` interfaces

### Future Improvements

1. **Add Simple Domain Logic**
   - Add query methods to domain models
   - Example: `assessment.is_deadline_passed()`
   - Keep services thin

2. **Repository Interfaces**
   - Define abstract base classes
   - Enable better testing
   - Follow Dependency Inversion Principle

3. **Consider CQRS**
   - For read-heavy operations
   - Separate read models from write models
   - Only if needed

---

## Quick Reference

### Find a Feature

**"Where is the logic for creating an assessment?"**
1. Entry point: `app/rest/routers/assessments.py:create_assessment()`
2. Business logic: `app/services/assessment_service.py:create_assessment()`
3. Data access: `app/repositories/assessments.py:add_assessment()`

**"Where is the Assessment model defined?"**
- Domain: `app/core/models/assessment.py`
- Database: `app/database/tables/assessments.py`

**"Where is the transformation between domain and DB?"**
- `app/mappers/assessment_mapper.py`

---

## Resources

### Books

1. **Fowler, Martin.** *Patterns of Enterprise Application Architecture*. 2002.
   - Service Layer, Repository, Data Mapper, Transaction Script

2. **Evans, Eric.** *Domain-Driven Design*. 2003.
   - Entities, Value Objects, Aggregates, Ubiquitous Language

3. **Martin, Robert C.** *Clean Architecture*. 2017.
   - Dependency Rule, Boundaries, Use Cases

4. **Gamma et al.** *Design Patterns*. 1994.
   - GoF patterns: Composite, Strategy, Adapter, Factory

### Articles

- Martin Fowler's Bliki: https://martinfowler.com/bliki/
  - Anemic Domain Model
  - Repository
  - Service Layer

---

## Summary

This backend follows a **classic layered architecture** with:
- ✅ Clear separation of concerns
- ✅ Dependency rule (inward flow)
- ✅ Well-defined patterns per layer
- ✅ Testable design
- ⚠️ Some improvements possible (static methods, interfaces)

**For new developers:** Read the layer-specific README files in order:
1. Core (understand domain)
2. Database (understand persistence)
3. Mappers (understand transformations)
4. Repositories (understand data access)
5. Services (understand business logic)
6. REST (understand API)

**Overall Quality:** Professional-grade architecture, appropriate for the problem domain.
