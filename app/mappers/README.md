# Mapper Layer (Transformation Layer)

## Architectural Intent

The Mapper Layer is responsible for **transforming data between domain models and database models**. It acts as a translation layer that keeps the domain logic independent from database implementation details.

## Core Responsibilities

1. **Domain ↔ Database Transformation** - Convert between domain and DB models
2. **Decoupling** - Keep domain models independent of ORM
3. **Type Handling** - Handle polymorphism and type conversions
4. **Relationship Mapping** - Transform associated objects
5. **Validation Support** - Ensure data integrity during transformation

## Architectural Patterns Applied

### 1. **Data Mapper Pattern** (Fowler - P of EAA)

**Intent:** A layer of Mappers that moves data between objects and a database while keeping them independent of each other and the mapper itself.

**Fowler's Definition:**
> "Objects and relational databases have different mechanisms for structuring data. The Data Mapper is a layer of software that separates the in-memory objects from the database. Its responsibility is to transfer data between the two and also to isolate them from each other."

**Key Insight:**
The domain model and database schema can **evolve independently**. Changes to one don't require changes to the other.

**Implementation:**
```python
# assessment_mapper.py
def assessment_to_domain(db_assessment: DbAssessment) -> Assessment:
    """Database → Domain"""
    tasks = []
    for task in db_assessment.tasks:
        if isinstance(task, DbPrimer):
            tasks.append(primer_to_domain(task))
        elif isinstance(task, DbExercise):
            tasks.append(exercise_to_domain(task))

    return Assessment(
        id=db_assessment.id,
        name=db_assessment.name,
        tasks=tasks
    )


def assessment_to_db(assessment: Assessment) -> DbAssessment:
    """Domain → Database"""
    assessment_tasks = []
    for position, task in enumerate(assessment.tasks, start=1):
        if isinstance(task, Primer):
            db_task = primer_to_db(task)
        else:
            db_task = exercise_to_db(task)
        assessment_tasks.append(
            DbAssessmentsTasks(position=position, task=db_task)
        )

    return DbAssessment(
        id=assessment.id,
        name=assessment.name,
        tasks_link=assessment_tasks
    )
```

**Benefits:**
- Domain model can focus on behavior
- Database schema can be optimized for queries
- Easy to test transformations in isolation
- Supports multiple persistence strategies

---

### 2. **Adapter Pattern** (GoF)

**Intent:** Convert the interface of a class into another interface clients expect.

**Application:**
Mappers adapt the ORM interface (SQLAlchemy models) to the domain interface (Pydantic models):

```
Domain Layer (Pydantic)
        ↕ Adapter/Mapper
Database Layer (SQLAlchemy)
```

**GoF Insight:**
> "An adapter makes things work after they're designed; a good mapper makes them work before."

---

### 3. **Two-Way Transformation**

**Pattern:** Bidirectional mapping between models

Every mapper provides two functions:
1. **`{entity}_to_domain(db_model)`** - Database → Domain
2. **`{entity}_to_db(domain_model)`** - Domain → Database

**Symmetry:**
```python
# Round-trip should preserve data
original_domain = Assessment(...)
db_model = assessment_to_db(original_domain)
reconstructed_domain = assessment_to_domain(db_model)

assert original_domain == reconstructed_domain
```

---

## Layer Rules & Constraints

### ✅ ALLOWED Dependencies

Mappers MAY depend on:
- **Domain Models** (`app.core.models.*`) - Input/output types
- **Database Tables** (`app.database.tables.*`) - ORM models
- **Other Mappers** (`app.mappers.*`) - For nested transformations

### ❌ FORBIDDEN Dependencies

Mappers MUST NOT:
- **Depend on Services** - Would create circular dependency
- **Depend on Repositories** - Mappers are called BY repositories
- **Depend on REST Layer** - Wrong direction
- **Contain Business Logic** - Pure transformation only
- **Perform Database Operations** - No session access

### Dependency Flow

```
Repository Layer
    ↓
Mapper Layer ← YOU ARE HERE
    ↕ (bidirectional transformation)
Domain Models ↔ Database Models
```

---

## Mapper Structure

### Directory Layout

```
mappers/
  ├── assessment_mapper.py
  ├── exercise_mapper.py
  ├── primer_mapper.py
  ├── submission_mapper.py
  ├── choice_mapper.py
  └── multimedia_file_mapper.py
```

Each file contains:
- `{entity}_to_domain()` - DB → Domain
- `{entity}_to_db()` - Domain → DB

---

## Transformation Patterns

### 1. **Simple Field Mapping**

```python
def choice_to_domain(db_choice: DbChoice) -> Choice:
    """Simple 1:1 field mapping."""
    return Choice(
        id=db_choice.id,
        created_at=db_choice.created_at,
        text=db_choice.text,
        is_correct=db_choice.is_correct
    )
```

**Pattern:** Direct field-to-field copy

---

### 2. **Nested Object Mapping**

```python
def assessment_to_domain(db_assessment: DbAssessment) -> Assessment:
    """Map with nested collections."""
    # Transform nested tasks
    tasks = []
    for task in db_assessment.tasks:
        if isinstance(task, DbPrimer):
            tasks.append(primer_to_domain(task))  # Recursive mapper call
        elif isinstance(task, DbExercise):
            tasks.append(exercise_to_domain(task))  # Recursive mapper call

    return Assessment(
        id=db_assessment.id,
        name=db_assessment.name,
        tasks=tasks  # Transformed collection
    )
```

**Pattern:** Recursive transformation of nested objects

---

### 3. **Polymorphic Mapping**

```python
def assessment_to_domain(db_assessment: DbAssessment) -> Assessment:
    """Handle polymorphism (Primer vs Exercise)."""
    tasks = []
    for task in db_assessment.tasks:
        # Type dispatch
        if isinstance(task, DbPrimer):
            tasks.append(primer_to_domain(task))
        elif isinstance(task, DbExercise):
            tasks.append(exercise_to_domain(task))
        # Future: elif isinstance(task, DbNewType): ...

    return Assessment(tasks=tasks)
```

**Pattern:** Type-based dispatch for inheritance hierarchies

**Open/Closed Principle:** Easy to extend with new types

---

### 4. **Association Table Mapping**

```python
def assessment_to_db(assessment: Assessment) -> DbAssessment:
    """Map with association table (many-to-many)."""
    assessment_tasks = []
    for position, task in enumerate(assessment.tasks, start=1):
        db_task = exercise_to_db(task) if isinstance(task, Exercise) else primer_to_db(task)

        # Create association object
        assessment_tasks.append(
            DbAssessmentsTasks(
                position=position,
                task=db_task
            )
        )

    return DbAssessment(
        id=assessment.id,
        name=assessment.name,
        tasks_link=assessment_tasks  # Association table
    )
```

**Pattern:** Explicit association table with metadata (position)

---

### 5. **Optional Field Handling**

```python
def assessment_to_domain(db_assessment: DbAssessment) -> Assessment:
    """Handle optional fields."""
    return Assessment(
        id=db_assessment.id,
        name=db_assessment.name,
        deadline=db_assessment.deadline,  # May be None
        max_attempts=db_assessment.max_attempts,  # May be None
        modified_at=db_assessment.modified_at  # May be None
    )
```

**Pattern:** Direct pass-through of `None` values

---

## Transformation Principles

### 1. **No Business Logic**

```python
# BAD: Business logic in mapper
def assessment_to_domain(db_assessment: DbAssessment) -> Assessment:
    tasks = [...]

    # ❌ Validation is business logic
    if len(tasks) > 50:
        raise TooManyTasksError()

    return Assessment(tasks=tasks)

# GOOD: Pure transformation
def assessment_to_domain(db_assessment: DbAssessment) -> Assessment:
    tasks = [...]
    return Assessment(tasks=tasks)  # ✅ Just transform
```

**Rule:** Mappers transform, they don't validate

---

### 2. **No Database Access**

```python
# BAD: Database access in mapper
def assessment_to_domain(db_assessment: DbAssessment) -> Assessment:
    # ❌ Querying database
    tasks = session.query(DbTask).filter(...).all()

    return Assessment(tasks=tasks)

# GOOD: Use provided data
def assessment_to_domain(db_assessment: DbAssessment) -> Assessment:
    # ✅ Use relationships already loaded
    tasks = [task_to_domain(t) for t in db_assessment.tasks]

    return Assessment(tasks=tasks)
```

**Rule:** Mappers transform existing data, don't fetch new data

---

### 3. **Preserve Identity**

```python
def assessment_to_db(assessment: Assessment) -> DbAssessment:
    """Preserve domain object IDs."""
    return DbAssessment(
        id=assessment.id,  # ✅ Same ID
        created_at=assessment.created_at,  # ✅ Preserve timestamps
        name=assessment.name
    )
```

**Rule:** IDs and timestamps flow through unchanged

---

### 4. **Handle Null Safely**

```python
def multimedia_file_to_domain(db_file: DbBucketObjects | None) -> MultimediaFile | None:
    """Handle None input."""
    if db_file is None:
        return None

    return MultimediaFile(
        id=db_file.id,
        bucket=db_file.bucket,
        object_name=db_file.object_name
    )
```

**Pattern:** Null in → Null out

---

## Mapper Responsibilities

### ✅ **Mappers SHOULD:**

1. **Transform Data Types**
   ```python
   # DateTime formatting, UUID conversion, etc.
   created_at=db_assessment.created_at  # datetime → datetime (no change)
   id=UUID(db_assessment.id)  # If conversion needed
   ```

2. **Handle Nested Objects**
   ```python
   tasks = [task_mapper(t) for t in db_assessment.tasks]
   ```

3. **Manage Associations**
   ```python
   # Create association table entries
   tasks_link = [DbAssessmentsTasks(...) for task in tasks]
   ```

4. **Dispatch Polymorphic Types**
   ```python
   if isinstance(task, DbPrimer):
       return primer_to_domain(task)
   elif isinstance(task, DbExercise):
       return exercise_to_domain(task)
   ```

### ❌ **Mappers SHOULD NOT:**

1. **Validate Business Rules**
   - Validation happens in service or domain model

2. **Query Database**
   - No session access
   - Work with provided data only

3. **Contain Control Flow Logic**
   - No complex if/else for business decisions
   - Only type-based dispatch

4. **Modify Input Objects**
   - Pure functions (input → output)

---

## Common Mapping Scenarios

### Scenario 1: Flattening Relationships

**Database:** Normalized (multiple tables)
**Domain:** Denormalized (embedded objects)

```python
# DB: Assessment ← AssessmentsTasks → Task
# Domain: Assessment with embedded tasks list

def assessment_to_domain(db_assessment: DbAssessment) -> Assessment:
    # Flatten association table
    tasks = [task_to_domain(link.task) for link in db_assessment.tasks_link]

    return Assessment(
        id=db_assessment.id,
        tasks=tasks  # Flattened
    )
```

---

### Scenario 2: Exploding Collections

**Database:** One table
**Domain:** Separate objects

```python
def multiple_choice_to_domain(db_mc: DbMultipleChoice) -> MultipleChoice:
    # Explode junction table to list of choices
    choices = [
        choice_to_domain(link.choice)
        for link in db_mc.choices_link
    ]

    return MultipleChoice(
        id=db_mc.id,
        choices=choices
    )
```

---

### Scenario 3: Handling Inheritance

**Database:** Single Table Inheritance (type column)
**Domain:** Class hierarchy

```python
def task_to_domain(db_task: DbTask) -> Primer | Exercise:
    """Dispatch based on type."""
    if db_task.type == "primer":
        return primer_to_domain(db_task)
    elif db_task.type == "exercise":
        return exercise_to_domain(db_task)
    else:
        raise ValueError(f"Unknown task type: {db_task.type}")
```

---

## Testing Mappers

### Unit Tests (Isolated)

```python
def test_assessment_to_domain():
    # Arrange
    db_assessment = DbAssessment(
        id=uuid4(),
        name="Test Assessment",
        created_at=datetime.now(),
        tasks=[]
    )

    # Act
    domain_assessment = assessment_to_domain(db_assessment)

    # Assert
    assert domain_assessment.id == db_assessment.id
    assert domain_assessment.name == db_assessment.name
    assert isinstance(domain_assessment, Assessment)


def test_assessment_to_db():
    # Arrange
    domain_assessment = Assessment(
        id=uuid4(),
        name="Test Assessment",
        tasks=[]
    )

    # Act
    db_assessment = assessment_to_db(domain_assessment)

    # Assert
    assert db_assessment.id == domain_assessment.id
    assert db_assessment.name == domain_assessment.name
    assert isinstance(db_assessment, DbAssessment)
```

### Round-Trip Tests

```python
def test_assessment_roundtrip():
    """Test Domain → DB → Domain preserves data."""
    # Arrange
    original = Assessment(
        id=uuid4(),
        name="Test",
        tasks=[Exercise(...), Primer(...)]
    )

    # Act
    db_model = assessment_to_db(original)
    reconstructed = assessment_to_domain(db_model)

    # Assert
    assert original.id == reconstructed.id
    assert original.name == reconstructed.name
    assert len(original.tasks) == len(reconstructed.tasks)
```

---

## Mapper Template

```python
import logging

from app.core.models.{entity} import {Entity}
from app.database.tables.{entities} import Db{Entity}

logger = logging.getLogger(__name__)


def {entity}_to_domain(db_{entity}: Db{Entity}) -> {Entity}:
    """
    Transform database model to domain model.

    Args:
        db_{entity}: SQLAlchemy ORM model

    Returns:
        Pydantic domain model
    """
    logger.debug("Transforming Db{Entity} to {Entity} (id=%s)", db_{entity}.id)

    return {Entity}(
        id=db_{entity}.id,
        created_at=db_{entity}.created_at,
        modified_at=db_{entity}.modified_at,
        # ... map all fields
    )


def {entity}_to_db({entity}: {Entity}) -> Db{Entity}:
    """
    Transform domain model to database model.

    Args:
        {entity}: Pydantic domain model

    Returns:
        SQLAlchemy ORM model
    """
    logger.debug("Transforming {Entity} to Db{Entity} (id=%s)", {entity}.id)

    return Db{Entity}(
        id={entity}.id,
        created_at={entity}.created_at,
        modified_at={entity}.modified_at,
        # ... map all fields
    )
```

---

## Data Mapper vs. Active Record

### Data Mapper (What We Use)

**Characteristics:**
- Domain objects are POPOs (Plain Old Python Objects)
- No knowledge of database
- Separate mapper handles persistence
- Pydantic models (domain) ↔ SQLAlchemy models (DB)

```python
# Domain model knows nothing about DB
class Assessment(BaseModel):
    id: UUID
    name: str

# Mapper handles transformation
assessment = assessment_to_domain(db_assessment)
```

**Benefits:**
- ✅ Clean domain model
- ✅ Easy to test
- ✅ Independent evolution

---

### Active Record (Alternative)

**Characteristics:**
- Domain objects are database-aware
- Objects have save(), load(), delete() methods
- Django-style, Rails-style

```python
# Not our style (but common in Django)
class Assessment(models.Model):
    name = models.CharField(max_length=100)

    def save(self):  # DB-aware method
        # ...
```

**We don't use this because:**
- ❌ Tight coupling to database
- ❌ Hard to test
- ❌ Can't change persistence layer

**Fowler's Guidance:**
> "Use Data Mapper when you need to keep domain logic separate from database logic, especially in complex domains."

---

## Fowler's Data Mapper Advice

### When to Use Data Mapper

**From P of EAA:**
> "If your object model is simple—essentially getters, setters, and no real business logic—then an Active Record approach is fine. But as soon as you have real business logic, you need to separate it from the database, and that's where Data Mapper comes in."

### Our Application

- ✅ Domain models are simple (Anemic Domain Model)
- ✅ But we still use Data Mapper
- **Why?** Future-proofing, testability, and FastAPI/Pydantic integration

---

## SOLID Principles

### Single Responsibility Principle (SRP)

Each mapper handles ONE entity type:
- `assessment_mapper.py` - Assessment transformations only
- `exercise_mapper.py` - Exercise transformations only

Each function has ONE responsibility:
- `{entity}_to_domain()` - Only DB → Domain
- `{entity}_to_db()` - Only Domain → DB

### Open/Closed Principle (OCP)

Easy to extend for new types:
```python
# Add new task type without modifying existing mappers
def new_task_to_domain(db_task: DbNewTask) -> NewTask:
    return NewTask(...)

# Update polymorphic dispatcher
def task_to_domain(db_task: DbTask):
    if isinstance(db_task, DbPrimer):
        return primer_to_domain(db_task)
    elif isinstance(db_task, DbExercise):
        return exercise_to_domain(db_task)
    elif isinstance(db_task, DbNewTask):  # New type added
        return new_task_to_domain(db_task)
```

---

## Anti-Patterns to Avoid

### ❌ **1. Business Logic in Mapper**

```python
# BAD
def assessment_to_domain(db_assessment: DbAssessment) -> Assessment:
    tasks = [...]

    # ❌ Business rule
    if len(tasks) > 50:
        raise TooManyTasksError()

    return Assessment(tasks=tasks)
```

### ❌ **2. Database Access in Mapper**

```python
# BAD
def assessment_to_domain(db_assessment: DbAssessment) -> Assessment:
    # ❌ Querying database
    tasks = session.query(DbTask).filter(...).all()

    return Assessment(tasks=tasks)
```

### ❌ **3. Mixing Transformation and Persistence**

```python
# BAD
def save_assessment(assessment: Assessment, session: Session):
    db_model = assessment_to_db(assessment)
    session.add(db_model)  # ❌ Mapper doing repository work
    session.commit()
```

**Separation:**
- Mapper: Transform
- Repository: Persist

---

## Performance Considerations

### Eager vs. Lazy Loading

```python
# Mapper assumes relationships are loaded
def assessment_to_domain(db_assessment: DbAssessment) -> Assessment:
    # Accessing db_assessment.tasks should NOT trigger lazy load
    tasks = [task_to_domain(t) for t in db_assessment.tasks]
```

**Repository's responsibility:**
```python
# Repository ensures eager loading
def get_assessment(session: Session, id: UUID):
    result = session.query(DbAssessment).options(
        selectinload(DbAssessment.tasks)  # Eager load
    ).filter(DbAssessment.id == id).first()

    return assessment_to_domain(result)  # Mapper won't trigger N+1
```

---

## References

**Books:**
- Fowler, Martin. *Patterns of Enterprise Application Architecture*. 2002.
  - Data Mapper (p165-169)
  - Active Record (p160-164)
  - Identity Map (p195-200)

- Gamma et al. *Design Patterns: Elements of Reusable Object-Oriented Software*. 1994.
  - Adapter Pattern (p139-150)

**Key Quotes:**

**Fowler on Data Mapper:**
> "A Data Mapper is a software layer that separates the in-memory objects from the database. Its responsibility is to transfer data between the two and also to isolate them from each other."

**Fowler on Separation:**
> "With Data Mapper the domain objects need to have no knowledge of the database, and there's no database code in the domain objects."

---

## Summary

The Mapper Layer is a **pure transformation layer** that:
- ✅ Converts between domain models and database models
- ✅ Handles polymorphism and nested objects
- ✅ Keeps domain and database independent
- ✅ Enables independent evolution of both sides
- ❌ Contains NO business logic
- ❌ Does NOT access database
- ❌ Does NOT validate or enforce rules

**Keep mappers simple, pure, and focused on transformation.**
