# Service Layer (Business Logic Layer)

## Architectural Intent

The Service Layer acts as the **orchestration and business logic layer** in our architecture. It encapsulates the application's use cases and coordinates operations across multiple repositories and domain objects.

## Core Responsibilities

1. **Business Logic Execution** - Implement application-specific business rules
2. **Orchestration** - Coordinate operations across multiple repositories
3. **Transaction Boundaries** - Define transaction scope for operations
4. **Domain Object Coordination** - Work with multiple domain entities
5. **Validation** - Enforce business rules and constraints
6. **Exception Translation** - Convert technical exceptions to domain exceptions

## Architectural Patterns Applied

### 1. **Service Layer Pattern** (Fowler - P of EAA)

**Intent:** Define an application's boundary with a layer of services that establishes a set of available operations and coordinates the application's response in each operation.

**Fowler's Definition:**
> "A Service Layer defines an application's boundary and its set of available operations from the perspective of interfacing client layers. It encapsulates the application's business logic, controlling transactions and coordinating responses in the implementation of its operations."

**Implementation:**

Services define application boundaries and coordinate operations across repositories. Each service method represents one business use case.

**Benefits:**
- Single place for business logic
- Reusable across different presentation layers (REST, GraphQL, CLI)
- Transaction control
- Testable independently

---

### 2. **Transaction Script Pattern** (Fowler - P of EAA)

**Intent:** Organizes business logic by procedures where each procedure handles a single request from the presentation.

**Current Implementation Style:**
This project uses **Transaction Script** rather than **Domain Model**. Each service method is a procedure that handles one complete business transaction.

**Fowler's Guidance:**
> "For simple problems, Transaction Script works just fine and is easier to write than Domain Model. But as business logic gets more complex, Transaction Script starts to get messy and a Domain Model approach becomes more attractive."

**Trade-offs:**
- ✅ Easy to modify
- ✅ Good for CRUD operations
- ⚠️ Can lead to duplication in complex scenarios
- ⚠️ Logic spread across multiple service methods

---

### 3. **Facade Pattern** (GoF)

**Intent:** Provide a unified interface to a set of interfaces in a subsystem.

**Implementation:**
Services act as facades over repositories, mappers, and domain logic:

```python
class AssessmentSubmissionService:
    def __init__(
        self,
        assessment_service: AssessmentService,
        exercise_service: ExerciseService,
        scoring_service: ScoringService
    ):
        # Facade over multiple services and repositories

    def create_submission(self, assessment_id: UUID, user_id: str):
        # Coordinates multiple subsystems:
        # 1. Get assessment (via assessment_service)
        # 2. Validate user can submit
        # 3. Create submission (via repository)
        # 4. Return result
```

**Benefits:**
- Simplifies complex subsystems
- Reduces coupling between layers
- Single entry point for operations

---

### 4. **Dependency Injection** (Fowler, Uncle Bob)

**Intent:** Invert control of dependency creation, making code testable and flexible.

**Implementation:**
```python
class AssessmentService:
    def __init__(self, task_service: Annotated[TaskService, Depends()]):
        self.task_service = task_service
        # Dependencies injected by framework
```

**Benefits:**
- Testable (inject mocks)
- Loose coupling
- Follows Dependency Inversion Principle

---

## Layer Rules & Constraints

### ✅ ALLOWED Dependencies

Services MAY depend on:
- **Other Services** (`app.services.*`) - For orchestration
- **Repositories** (`app.repositories.*`) - For data access
- **Mappers** (`app.mappers.*`) - For transformation
- **Domain Models** (`app.core.models.*`) - For business entities
- **Database Tables** (`app.database.tables.*`) - Via repositories (indirectly)
- **External Services** (`app.external_services.*`) - For integrations

### ❌ FORBIDDEN Dependencies

Services MUST NOT:
- **Depend on REST Layer** - Would create circular dependency
- **Depend on Presentation DTOs** - Use domain models instead
- **Directly construct SQL queries** - Use repositories

### Dependency Flow

```
REST Layer
    ↓
Service Layer ← YOU ARE HERE
    ↓
Repository Layer
    ↓
Mapper Layer
    ↓
Database Layer
```

---

## Current Architecture Issue: Static Methods

### ⚠️ **Anti-Pattern Detected**

**Problem:**
```python
class AssessmentService:
    def __init__(self, task_service: Annotated[TaskService, Depends()]):
        self.task_service = task_service  # Injected

    @staticmethod  # ❌ But methods are static!
    def create_assessment(session: Session, ...):
        # Cannot use self.task_service here!
```

**Issues:**
1. Constructor injection is useless if methods are static
2. Cannot use injected dependencies
3. Hard to test (cannot mock dependencies)
4. Inconsistent design

**Should Be:**
```python
class AssessmentService:
    def __init__(self, task_service: Annotated[TaskService, Depends()]):
        self.task_service = task_service

    def create_assessment(self, session: Session, ...):  # ✅ Instance method
        # Now can use self.task_service
        task = self.task_service.get_task(...)
```

---

## Current Architecture Issue: Layer Violation

### ⚠️ **Service Bypassing Repository**

**Problem:**
```python
# In assessment_service.py
def create_assessment(session: Session, ...):
    db_task = session.get(DbTask, task_id)  # ❌ Direct ORM access
```

**Why is this wrong?**
- Service should NOT directly access database
- Bypasses repository abstraction
- Mixes business logic with data access
- Hard to test
- Violates Single Responsibility Principle

**Should Be:**
```python
# Create task_repository.py
def get_task(session: Session, task_id: UUID) -> Task | None:
    db_task = session.get(DbTask, task_id)
    return task_to_domain(db_task) if db_task else None

# In service
def create_assessment(self, session: Session, ...):
    task = self.task_repository.get_task(session, task_id)  # ✅ Via repository
```

---

## Service Layer Responsibilities

### ✅ **Services SHOULD:**

1. **Orchestrate Multiple Operations**
   ```python
   def submit_assessment(self, submission_id: UUID):
       # 1. Get submission (repository)
       # 2. Calculate score (scoring service)
       # 3. Update submission (repository)
       # 4. Send notification (external service)
   ```

2. **Enforce Business Rules**
   ```python
   def create_submission(self, assessment_id: UUID, user_id: str):
       assessment = self.assessment_repo.get(assessment_id)

       # Business rule: Check max attempts
       existing = self.submission_repo.count_by_user(user_id, assessment_id)
       if assessment.max_attempts and existing >= assessment.max_attempts:
           raise MaxAttemptsExceededError()

       # Business rule: Check deadline
       if assessment.deadline and datetime.now() > assessment.deadline:
           raise DeadlinePassedError()
   ```

3. **Coordinate Multiple Repositories**
   ```python
   def create_assessment_with_tasks(self, name: str, task_ids: list[UUID]):
       # Multiple repositories involved
       tasks = [self.task_repo.get(tid) for tid in task_ids]
       assessment = Assessment(name=name, tasks=tasks)
       self.assessment_repo.add(assessment)
   ```

4. **Handle Transactions**
   - Services define transaction boundaries
   - Passed-in session ensures atomicity
   - All-or-nothing operations

### ❌ **Services SHOULD NOT:**

1. **Directly Access Database**
   ```python
   # BAD
   db_task = session.get(DbTask, task_id)

   # GOOD
   task = self.task_repository.get(session, task_id)
   ```

2. **Contain SQL or ORM Queries**
   - That's the repository's job

3. **Know About HTTP, JSON, or REST**
   - That's the presentation layer's job
   - Services work with domain objects, not DTOs

4. **Perform Complex Transformations**
   - Use mappers for that

---

## SOLID Principles in Service Layer

### Single Responsibility Principle (SRP)

Each service handles ONE entity or bounded context:
- `AssessmentService` - Assessment operations
- `ExerciseService` - Exercise operations
- `ScoringService` - Scoring calculations

**Violation to Fix:**
Current services have multiple responsibilities:
- Business logic ✅
- Data access ❌ (should be in repository)

### Open/Closed Principle (OCP)

Services should be open for extension, closed for modification:
```python
# Extensible through strategy pattern
class ScoringService:
    def __init__(self, strategy: ScoringStrategy):
        self.strategy = strategy

    def calculate_score(self, submission):
        return self.strategy.score(submission)
```

### Dependency Inversion Principle (DIP)

**Current Issue:** Services depend on concrete implementations

**Should Be:**
```python
# Define interface
class IAssessmentRepository(ABC):
    @abstractmethod
    def get_by_id(self, session: Session, id: UUID) -> Assessment | None:
        pass

# Service depends on abstraction
class AssessmentService:
    def __init__(self, repository: IAssessmentRepository):
        self.repository = repository
```

---

## Service Structure Template

```python
import logging
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.models.{entity} import {Entity}
from app.repositories.{entity} import (
    add_{entity}, get_{entity}, list_{entities}
)
from app.services.exceptions.not_found import {Entity}NotFoundException

logger = logging.getLogger(__name__)


class {Entity}Service:
    """
    Service for {Entity} business logic.

    Responsibilities:
    - Orchestrate {entity} operations
    - Enforce business rules
    - Coordinate with other services/repositories
    """

    def __init__(
        self,
        related_service: Annotated[RelatedService, Depends()]
    ) -> None:
        self.related_service = related_service

    def create_{entity}(
        self,
        session: Session,
        **kwargs
    ) -> {Entity}:
        """
        Create a new {entity}.

        Business Rules:
        - Rule 1: Description
        - Rule 2: Description

        Args:
            session: Database session
            **kwargs: Entity attributes

        Returns:
            Created {entity}

        Raises:
            ValidationError: If business rules violated
        """
        # 1. Validate business rules
        self._validate_creation(**kwargs)

        # 2. Create domain object
        entity = {Entity}(**kwargs)

        # 3. Persist via repository
        add_{entity}(session, entity)

        # 4. Return
        return entity

    def _validate_creation(self, **kwargs) -> None:
        """Private method for business rule validation."""
        pass
```

---

## Exception Handling

### Domain Exceptions

Services should raise **domain-specific exceptions**:

```python
# In services/exceptions/
class AssessmentNotFoundException(Exception):
    pass

class MaxAttemptsExceededError(Exception):
    pass

class DeadlinePassedError(Exception):
    pass

# In service
def get_assessment(self, session: Session, id: UUID) -> Assessment:
    assessment = self.repository.get(session, id)
    if not assessment:
        raise AssessmentNotFoundException(f"Assessment {id} not found")
    return assessment
```

**Benefits:**
- Clear error semantics
- Easy to handle at REST layer
- Testable
- Self-documenting

---

## Testing Strategy

### Unit Tests

Mock repositories, test business logic:
```python
def test_create_submission_enforces_max_attempts(mock_repo):
    service = AssessmentSubmissionService(mock_repo)

    assessment = Assessment(max_attempts=3)
    mock_repo.get.return_value = assessment
    mock_repo.count_by_user.return_value = 3

    with pytest.raises(MaxAttemptsExceededError):
        service.create_submission(assessment_id, user_id)
```

### Integration Tests

Test with real repositories, test database:
```python
def test_create_assessment_with_tasks(test_db):
    service = AssessmentService(TaskService(test_db))

    assessment = service.create_assessment(
        session=test_db,
        name="Integration Test",
        task_ids=[task1.id, task2.id]
    )

    assert len(assessment.tasks) == 2
```

---

## Common Patterns

### 1. **Validation Before Action**

```python
def create_submission(self, assessment_id: UUID, user_id: str):
    # Get data
    assessment = self._get_assessment_or_fail(assessment_id)

    # Validate business rules
    self._validate_can_submit(assessment, user_id)

    # Execute action
    submission = AssessmentSubmission(...)
    self.repository.add(submission)
    return submission
```

### 2. **Orchestration Across Services**

```python
def submit_and_score_assessment(self, submission_id: UUID):
    # Get submission
    submission = self.submission_service.get(submission_id)

    # Calculate score
    score = self.scoring_service.calculate(submission)

    # Update submission
    submission.score = score
    submission.finished = True
    self.repository.update(submission)

    # Notify user (external service)
    self.notification_service.send_completion_email(submission)
```

### 3. **Get-or-Fail Pattern**

```python
def _get_assessment_or_fail(self, id: UUID) -> Assessment:
    assessment = self.repository.get(id)
    if not assessment:
        raise AssessmentNotFoundException(f"Assessment {id} not found")
    return assessment
```

---

## Transaction Management

### Service as Transaction Boundary

Services define the transaction scope:
```python
# REST layer passes session
@router.post("/assessments/")
async def create_assessment(
    data: CreateAssessmentRequest,
    service: Annotated[AssessmentService, Depends()],
    session: Annotated[Session, Depends(get_db_session)]
):
    # Session commits on success, rolls back on exception
    assessment = service.create_assessment(session, ...)
    return assessment
```

**Why?**
- HTTP request = unit of work
- All service operations in one transaction
- Automatic rollback on error

---

## Anti-Patterns to Avoid

### ❌ **1. Anemic Service (Just CRUD)**

```python
# BAD: No business logic, just passes to repository
class AssessmentService:
    def create(self, session, assessment):
        return self.repository.add(session, assessment)

    def get(self, session, id):
        return self.repository.get(session, id)
```

**Problem:** No value added, just delegation
**Solution:** Either add business logic or remove service layer

### ❌ **2. God Service**

```python
# BAD: One service does everything
class ApplicationService:
    def create_assessment(...):
    def create_exercise(...):
    def create_submission(...):
    def calculate_score(...):
    def send_email(...):
    # 50 more methods...
```

**Problem:** Violates SRP
**Solution:** Split into focused services

### ❌ **3. Logic Duplication**

```python
# BAD: Same validation in multiple methods
def create_assessment(self, ...):
    if not name or len(name) < 3:
        raise ValueError()

def update_assessment(self, ...):
    if not name or len(name) < 3:  # Duplicated!
        raise ValueError()
```

**Solution:** Extract to private method or move to domain model

---

## References

**Books:**
- Fowler, Martin. *Patterns of Enterprise Application Architecture*. 2002.
  - Service Layer (p133-141)
  - Transaction Script (p110-119)
  - Domain Model (p116-145)

- Evans, Eric. *Domain-Driven Design*. 2003.
  - Application Services
  - Domain Services
  - Layered Architecture

- Martin, Robert C. *Clean Architecture*. 2017.
  - Use Cases / Interactors
  - Business Rules

**Key Quotes:**

**Fowler on Service Layer:**
> "A Service Layer is a layer that establishes a set of available operations and coordinates the application's response in each operation."

**Fowler on when to use Transaction Script:**
> "The glory of Transaction Script is its simplicity. Organizing logic this way is natural for applications with only a small amount of logic, and it involves very little overhead either in performance or in understanding."

---

## Summary

The Service Layer is the **orchestration and business logic layer** that:
- ✅ Implements business rules and workflows
- ✅ Orchestrates operations across repositories
- ✅ Defines transaction boundaries
- ✅ Throws domain-specific exceptions
- ❌ Should NOT directly access database (use repositories)
- ❌ Should NOT be static (use instance methods for DI)
- ❌ Should NOT contain presentation logic

**Current Style:** Transaction Script (acceptable for CRUD-heavy applications)
**Improvement Opportunities:** Remove static methods, enforce repository usage

**Keep services focused on "what" to do, not "how" to persist.**
