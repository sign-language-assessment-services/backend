# Repository Layer (Data Access Layer)

## Architectural Intent

The Repository Layer mediates between the domain and data mapping layers, providing a **collection-like interface** for accessing domain objects. It encapsulates all data access logic and shields the service layer from database implementation details.

## Core Responsibilities

1. **Data Access Abstraction** - Hide database implementation details
2. **CRUD Operations** - Create, Read, Update, Delete domain objects
3. **Query Construction** - Build database queries
4. **Collection Interface** - Provide collection-like methods (add, get, list, remove)
5. **Domain Object Retrieval** - Return domain objects, not database models
6. **Query Optimization** - Handle efficient data retrieval

## Architectural Patterns Applied

### 1. **Repository Pattern** (Fowler - P of EAA)

**Intent:** Mediates between the domain and data mapping layers using a collection-like interface for accessing domain objects.

**Fowler's Definition:**
> "A Repository mediates between the domain and data mapping layers, acting like an in-memory domain object collection. Client objects construct query specifications declaratively and submit them to Repository for satisfaction."

**Key Characteristics:**
- Objects can be added to and removed from the Repository
- Repository encapsulates the mechanisms for accessing data
- Provides a more object-oriented view of the persistence layer
- Minimizes duplicate query logic

**Implementation:**
```python
# assessments.py
def add_assessment(session: Session, assessment: Assessment) -> None:
    db_model = assessment_to_db(assessment)
    add_entry(session, db_model)

def get_assessment(session: Session, _id: UUID) -> Assessment | None:
    result = get_by_id(session, DbAssessment, _id)
    if result:
        return assessment_to_domain(result)
    return None

def list_assessments(session: Session) -> list[Assessment]:
    results = get_all(session, DbAssessment)
    return [assessment_to_domain(result) for result in results]
```

**Benefits:**
- Decouples business logic from data access
- Testable (can mock repositories)
- Centralized query logic
- Easy to change data source (SQL, NoSQL, API, etc.)

---

### 2. **Data Mapper Pattern** (Fowler - P of EAA)

**Intent:** A layer of mappers that moves data between objects and a database while keeping them independent of each other.

**Integration with Repository:**
```python
def get_assessment(session: Session, _id: UUID) -> Assessment | None:
    # 1. Repository retrieves DB model
    db_result = get_by_id(session, DbAssessment, _id)

    # 2. Mapper transforms to domain model
    if db_result:
        return assessment_to_domain(db_result)  # ← Mapper

    return None
```

**Why Separate?**
- Repository = "how to find data"
- Mapper = "how to transform data"
- Single Responsibility Principle

---

### 3. **Unit of Work Pattern** (Implicit via SQLAlchemy Session)

**Intent:** Maintain a list of objects affected by a business transaction and coordinates the writing out of changes.

**Implementation:**
```python
def add_entry(session: Session, db: Any) -> None:
    session.add(db)
    # Session tracks changes
    # Commit happens at transaction boundary (REST layer)
```

**Benefits:**
- Automatic change tracking
- Transaction consistency
- Batch updates

---

### 4. **Query Object Pattern** (Fowler - P of EAA)

**Intent:** Represents a database query as an object.

**Current Implementation:**
Repositories use SQLAlchemy for query construction:
```python
def get_by_id(session: Session, model: type[T], _id: UUID) -> T | None:
    return session.get(model, _id)

def get_all(session: Session, model: type[T]) -> list[T]:
    return session.query(model).all()
```

**Note:** SQLAlchemy Session/Query acts as Query Object

---

## Layer Rules & Constraints

### ✅ ALLOWED Dependencies

Repositories MAY depend on:
- **Database Tables** (`app.database.tables.*`) - ORM models
- **Mappers** (`app.mappers.*`) - For transformation
- **Domain Models** (`app.core.models.*`) - Return types
- **SQLAlchemy Session** - For database operations
- **Utility Functions** (`repositories/utils.py`) - Shared helpers

### ❌ FORBIDDEN Dependencies

Repositories MUST NOT:
- **Depend on Service Layer** - Would create circular dependency
- **Depend on REST Layer** - Violates layering
- **Contain Business Logic** - Pure data access only
- **Depend on other Repositories** - Keep them independent

### Dependency Flow

```
Service Layer
    ↓
Repository Layer ← YOU ARE HERE
    ↓
Mapper Layer
    ↓
Database Layer (ORM)
```

---

## Repository Structure

### Current Implementation Pattern

Each entity has its own repository file:
```
repositories/
  ├── assessments.py        # Assessment CRUD
  ├── exercises.py          # Exercise CRUD
  ├── primers.py            # Primer CRUD
  ├── submissions.py        # Submission CRUD
  ├── choices.py            # Choice CRUD
  └── utils.py              # Shared utilities
```

### Standard Repository Functions

Every repository provides:
1. **add_{entity}(session, entity)** - Create
2. **get_{entity}(session, id)** - Read by ID
3. **list_{entities}(session)** - Read all
4. **update_{entity}(session, id, **kwargs)** - Update
5. **delete_{entity}(session, id)** - Delete

---

## Repository Method Patterns

### 1. **Add (Create)**

```python
def add_assessment(session: Session, assessment: Assessment) -> None:
    """
    Add a new assessment to the database.

    Args:
        session: Database session (transaction context)
        assessment: Domain model to persist

    Returns:
        None (object is modified in-place with DB-generated values)
    """
    # Transform domain → database
    db_model = assessment_to_db(assessment)

    # Persist
    add_entry(session, db_model)
    # Commit happens at transaction boundary
```

**Pattern:**
```
Domain Model → Mapper → DB Model → Session.add() → (Commit later)
```

### 2. **Get (Read by ID)**

```python
def get_assessment(session: Session, _id: UUID) -> Assessment | None:
    """
    Retrieve an assessment by ID.

    Args:
        session: Database session
        _id: Assessment UUID

    Returns:
        Assessment domain model or None if not found
    """
    # Fetch DB model
    db_result = get_by_id(session, DbAssessment, _id)

    # Transform database → domain
    if db_result:
        return assessment_to_domain(db_result)

    return None
```

**Pattern:**
```
Session.get() → DB Model → Mapper → Domain Model (or None)
```

### 3. **List (Read All)**

```python
def list_assessments(session: Session) -> list[Assessment]:
    """
    Retrieve all assessments.

    Args:
        session: Database session

    Returns:
        List of Assessment domain models (may be empty)
    """
    # Fetch all DB models
    db_results = get_all(session, DbAssessment)

    # Transform each database → domain
    return [assessment_to_domain(result) for result in db_results]
```

**Pattern:**
```
Session.query().all() → [DB Model] → [Mapper] → [Domain Model]
```

### 4. **Update**

```python
def update_assessment(session: Session, _id: UUID, **kwargs: Any) -> None:
    """
    Update an assessment with new values.

    Args:
        session: Database session
        _id: Assessment UUID
        **kwargs: Fields to update

    Returns:
        None

    Raises:
        NotFoundException: If assessment not found
    """
    update_entry(session, DbAssessment, _id, **kwargs)
```

**Pattern:**
```
Session.get() → Modify attributes → (Commit later via dirty tracking)
```

### 5. **Delete**

```python
def delete_assessment(session: Session, _id: UUID) -> None:
    """
    Delete an assessment.

    Args:
        session: Database session
        _id: Assessment UUID

    Returns:
        None

    Raises:
        NotFoundException: If assessment not found
    """
    delete_entry(session, DbAssessment, _id)
```

**Pattern:**
```
Session.get() → Session.delete() → (Commit later)
```

---

## Shared Utilities (utils.py)

### Generic CRUD Functions

```python
def add_entry(session: Session, db: Any) -> None:
    """Generic add for any DB model."""
    session.add(db)

def get_by_id(session: Session, model: type[T], _id: UUID) -> T | None:
    """Generic get by ID for any model."""
    return session.get(model, _id)

def get_all(session: Session, model: type[T]) -> list[T]:
    """Generic get all for any model."""
    return session.query(model).all()

def update_entry(session: Session, model: type[T], _id: UUID, **kwargs) -> None:
    """Generic update for any model."""
    entry = session.get(model, _id)
    if not entry:
        raise NotFoundException(f"{model.__name__} with id {_id} not found")
    for key, value in kwargs.items():
        setattr(entry, key, value)

def delete_entry(session: Session, model: type[T], _id: UUID) -> None:
    """Generic delete for any model."""
    entry = session.get(model, _id)
    if not entry:
        raise NotFoundException(f"{model.__name__} with id {_id} not found")
    session.delete(entry)
```

**Benefits:**
- DRY (Don't Repeat Yourself)
- Consistent error handling
- Easier to maintain

---

## Query Patterns

### Simple Queries

```python
# Get by ID
def get_assessment(session: Session, id: UUID) -> Assessment | None:
    result = session.get(DbAssessment, id)
    return assessment_to_domain(result) if result else None

# Get all
def list_assessments(session: Session) -> list[Assessment]:
    results = session.query(DbAssessment).all()
    return [assessment_to_domain(r) for r in results]
```

### Filtered Queries

```python
def get_assessments_by_user(
    session: Session,
    user_id: str
) -> list[Assessment]:
    """Get all assessments created by a user."""
    results = session.query(DbAssessment).filter(
        DbAssessment.created_by == user_id
    ).all()
    return [assessment_to_domain(r) for r in results]
```

### Complex Queries with Joins

```python
def get_assessment_with_tasks(
    session: Session,
    id: UUID
) -> Assessment | None:
    """Get assessment with eagerly loaded tasks."""
    result = session.query(DbAssessment).options(
        joinedload(DbAssessment.tasks)
    ).filter(
        DbAssessment.id == id
    ).first()

    return assessment_to_domain(result) if result else None
```

---

## Repository vs. DAO (Data Access Object)

### Repository (What We Use)

- **Domain-centric** - Returns domain objects
- **Collection-like** - add(), get(), list(), remove()
- **Object-oriented** - Hides database details
- **Rich interface** - Can have domain-specific queries

```python
def get_active_assessments(session: Session) -> list[Assessment]:
    # Domain language: "active assessments"
    pass
```

### DAO (Alternative Pattern)

- **Data-centric** - Returns database records
- **CRUD-focused** - insert(), select(), update(), delete()
- **Database-aware** - Closer to SQL
- **Generic interface** - Often one DAO per table

**We use Repository because:**
- Better fits Domain-Driven Design
- More testable
- Language closer to business domain

---

## SOLID Principles in Repository Layer

### Single Responsibility Principle (SRP)

Each repository handles ONE entity:
- `assessments.py` - Assessment data access only
- `exercises.py` - Exercise data access only
- `submissions.py` - Submission data access only

**Each function has ONE responsibility:**
- `add_assessment()` - Only adds
- `get_assessment()` - Only retrieves
- No mixed concerns

### Open/Closed Principle (OCP)

Repositories can be extended without modification:
```python
# Base implementation
def list_assessments(session: Session) -> list[Assessment]:
    return [assessment_to_domain(r) for r in session.query(DbAssessment).all()]

# Extended (new function, no modification)
def list_active_assessments(session: Session) -> list[Assessment]:
    results = session.query(DbAssessment).filter(
        DbAssessment.deadline > datetime.now()
    ).all()
    return [assessment_to_domain(r) for r in results]
```

### Dependency Inversion Principle (DIP)

**Current State:** Functions depend on concrete Session type

**Improvement Opportunity:**
```python
# Define interface
class IAssessmentRepository(ABC):
    @abstractmethod
    def add(self, session: Session, assessment: Assessment) -> None:
        pass

    @abstractmethod
    def get_by_id(self, session: Session, id: UUID) -> Assessment | None:
        pass

# Service depends on abstraction
class AssessmentService:
    def __init__(self, repository: IAssessmentRepository):
        self.repository = repository
```

---

## Anti-Patterns to Avoid

### ❌ **1. Business Logic in Repository**

```python
# BAD: Business logic in repository
def add_assessment(session: Session, assessment: Assessment) -> None:
    # ❌ Validation is business logic
    if len(assessment.tasks) > 50:
        raise TooManyTasksError()

    db_model = assessment_to_db(assessment)
    add_entry(session, db_model)

# GOOD: Pure data access
def add_assessment(session: Session, assessment: Assessment) -> None:
    # Assumes validation already done in service
    db_model = assessment_to_db(assessment)
    add_entry(session, db_model)
```

**Rule:** Repositories should be "dumb" - no business rules.

---

### ❌ **2. Leaking Database Models**

```python
# BAD: Returning DB model
def get_assessment(session: Session, id: UUID) -> DbAssessment:
    return session.get(DbAssessment, id)  # ❌ Leaks DB model

# GOOD: Returning domain model
def get_assessment(session: Session, id: UUID) -> Assessment | None:
    db_result = session.get(DbAssessment, id)
    return assessment_to_domain(db_result) if db_result else None
```

**Rule:** Always transform to domain models before returning.

---

### ❌ **3. Multiple Entities in One Repository**

```python
# BAD: God repository
def add_assessment(session, assessment):
    pass

def add_exercise(session, exercise):  # ❌ Different entity
    pass

def add_submission(session, submission):  # ❌ Different entity
    pass
```

**Rule:** One repository per aggregate root.

---

### ❌ **4. Query Logic Duplication**

```python
# BAD: Same query in multiple places
# In assessments.py
def get_active_assessments(session):
    return session.query(DbAssessment).filter(
        DbAssessment.deadline > datetime.now()
    ).all()

# In reports.py (different module)
def get_active_assessments(session):  # ❌ Duplicated
    return session.query(DbAssessment).filter(
        DbAssessment.deadline > datetime.now()
    ).all()
```

**Solution:** Centralize in repository.

---

## Testing Strategy

### Unit Tests

Mock database session:
```python
def test_add_assessment(mock_session, mock_mapper):
    assessment = Assessment(name="Test")
    mock_mapper.return_value = DbAssessment(name="Test")

    add_assessment(mock_session, assessment)

    mock_session.add.assert_called_once()
```

### Integration Tests

Use real database (testcontainers):
```python
def test_add_and_get_assessment(test_db_session):
    # Add
    assessment = Assessment(name="Integration Test")
    add_assessment(test_db_session, assessment)
    test_db_session.commit()

    # Get
    result = get_assessment(test_db_session, assessment.id)

    assert result.name == "Integration Test"
```

---

## Fowler's Repository vs. Our Implementation

### Fowler's Ideal Repository

```python
class AssessmentRepository:
    """Collection-like interface."""

    def add(self, assessment: Assessment) -> None:
        """Add to collection."""

    def remove(self, assessment: Assessment) -> None:
        """Remove from collection."""

    def find_by_id(self, id: UUID) -> Assessment | None:
        """Find in collection."""

    def find_all(self) -> list[Assessment]:
        """Get all from collection."""

    def find_by_criteria(self, criteria: Specification) -> list[Assessment]:
        """Query collection."""
```

### Our Implementation (Function-Based)

```python
def add_assessment(session: Session, assessment: Assessment) -> None:
    """Function instead of class method."""

def get_assessment(session: Session, id: UUID) -> Assessment | None:
    """Explicit session passing."""

def list_assessments(session: Session) -> list[Assessment]:
    """Simple function."""
```

**Why Functions Instead of Classes?**
- ✅ Simpler (no class overhead)
- ✅ Easier to test (no mocking required)
- ✅ FastAPI friendly (functions as dependencies)
- ⚠️ Less encapsulation
- ⚠️ Session must be passed everywhere

**Trade-off:** Pragmatic Python style vs. pure OOP

---

## Session Management

### Repositories DON'T Manage Sessions

```python
# Good: Session passed in
def add_assessment(session: Session, assessment: Assessment):
    # Use session, don't create/close it
    add_entry(session, assessment)
    # No commit here!

# Bad: Repository manages session
def add_assessment(assessment: Assessment):
    session = create_session()  # ❌ Don't do this
    add_entry(session, assessment)
    session.commit()  # ❌ Don't do this
    session.close()  # ❌ Don't do this
```

**Why?**
- Transaction boundary is at service/REST layer
- Multiple repository calls should be in ONE transaction
- Let caller control commit/rollback

---

## Repository Template

```python
import logging
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.{entity} import {Entity}
from app.database.tables.{entities} import Db{Entity}
from app.mappers.{entity}_mapper import {entity}_to_db, {entity}_to_domain
from app.repositories.utils import add_entry, delete_entry, get_all, get_by_id, update_entry

logger = logging.getLogger(__name__)


def add_{entity}(session: Session, {entity}: {Entity}) -> None:
    """
    Add a new {entity} to the database.

    Args:
        session: Database session
        {entity}: Domain model to persist
    """
    db_model = {entity}_to_db({entity})
    logger.debug("Adding {entity} %s", db_model.id)
    add_entry(session, db_model)


def get_{entity}(session: Session, _id: UUID) -> {Entity} | None:
    """
    Retrieve {entity} by ID.

    Args:
        session: Database session
        _id: {Entity} UUID

    Returns:
        {Entity} domain model or None if not found
    """
    logger.debug("Getting {entity} %s", _id)
    result = get_by_id(session, Db{Entity}, _id)
    if result:
        return {entity}_to_domain(result)
    return None


def list_{entities}(session: Session) -> list[{Entity}]:
    """
    Retrieve all {entities}.

    Args:
        session: Database session

    Returns:
        List of {Entity} domain models
    """
    logger.debug("Listing all {entities}")
    results = get_all(session, Db{Entity})
    return [{entity}_to_domain(result) for result in results]


def update_{entity}(session: Session, _id: UUID, **kwargs) -> None:
    """
    Update {entity} fields.

    Args:
        session: Database session
        _id: {Entity} UUID
        **kwargs: Fields to update
    """
    logger.debug("Updating {entity} %s", _id)
    update_entry(session, Db{Entity}, _id, **kwargs)


def delete_{entity}(session: Session, _id: UUID) -> None:
    """
    Delete {entity}.

    Args:
        session: Database session
        _id: {Entity} UUID
    """
    logger.debug("Deleting {entity} %s", _id)
    delete_entry(session, Db{Entity}, _id)
```

---

## References

**Books:**
- Fowler, Martin. *Patterns of Enterprise Application Architecture*. 2002.
  - Repository (p322-326)
  - Data Mapper (p165-169)
  - Unit of Work (p184-188)
  - Query Object (p316-321)

- Evans, Eric. *Domain-Driven Design*. 2003.
  - Repositories (Chapter 6)
  - Aggregate Roots

**Key Quotes:**

**Fowler on Repository:**
> "A Repository mediates between the domain and data mapping layers, acting like an in-memory domain object collection."

**Fowler on Repository Benefits:**
> "You'll find that you have a simple conceptual interface to your data layer. Code that asks for data simply asks for what it wants, and doesn't need to know how the repository gets that data."

---

## Summary

The Repository Layer is a **data access abstraction** that:
- ✅ Provides collection-like interface to domain objects
- ✅ Encapsulates query logic
- ✅ Always transforms DB models → Domain models
- ✅ Returns domain objects, never database models
- ❌ Contains NO business logic
- ❌ Does NOT manage transactions (receives session)
- ❌ Does NOT leak database implementation details

**Keep repositories pure data access. No business rules. No validation. Just CRUD.**
