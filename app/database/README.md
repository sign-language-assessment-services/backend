# Database Layer (Persistence Layer)

## Architectural Intent

The Database Layer is responsible for **data persistence and schema management**. It defines the database structure using SQLAlchemy ORM and provides the foundation for all data storage operations.

## Core Responsibilities

1. **Schema Definition** - Define database tables and relationships
2. **ORM Mapping** - Map Python classes to database tables
3. **Relationship Management** - Define foreign keys and associations
4. **Migration Support** - Enable schema evolution via Alembic
5. **Connection Management** - Manage database connections and sessions
6. **Query Foundation** - Provide base for repository queries

## Architectural Patterns Applied

### 1. **Object-Relational Mapping (ORM)** (Fowler - P of EAA)

**Intent:** Map objects to relational database tables, hiding SQL details.

**Implementation:** SQLAlchemy Declarative ORM

```python
class DbAssessment(DbBase):
    __tablename__ = "assessments"

    name: Mapped[str] = mapped_column(Unicode(100), nullable=False)
    deadline: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

    # Relationships
    tasks: Mapped[list["DbTask"]] = relationship(
        secondary="assessments_tasks",
        viewonly=True
    )
```

**Benefits:**
- Write Python instead of SQL
- Type safety
- Automatic query generation
- Database portability

**Fowler's Wisdom:**
> "An ORM is a framework that maps between object-oriented concepts and relational database concepts, allowing developers to work with objects instead of SQL."

---

### 2. **Table Module Pattern** (Fowler - P of EAA)

**Intent:** A single instance that handles the business logic for all rows in a database table.

**Implementation:**
Each table is defined as a class:
- `DbAssessment` - assessments table
- `DbExercise` - exercises table
- `DbTask` - tasks table

**Pattern Relationship:**
```
Table Module (ORM Class)
    ↓ used by
Repository (Data Access Functions)
    ↓ used by
Service (Business Logic)
```

---

### 3. **Foreign Key Mapping** (Fowler - P of EAA)

**Intent:** Map object references to foreign key relationships in the database.

**Implementation:**
```python
class DbAssessmentSubmission(DbBase):
    __tablename__ = "assessment_submissions"

    # Foreign key
    assessment_id: Mapped[UUID] = mapped_column(
        ForeignKey("assessments.id"),
        nullable=False
    )

    # Relationship (ORM navigation)
    assessment: Mapped["DbAssessment"] = relationship(
        back_populates="assessment_submissions"
    )
```

**Benefits:**
- Referential integrity enforced at database level
- Automatic JOIN generation
- Cascade operations

---

### 4. **Association Table Mapping** (Fowler - P of EAA)

**Intent:** Model many-to-many relationships using an intermediate table.

**Implementation:**
```python
# Association table with metadata
class DbAssessmentsTasks(DbBase):
    __tablename__ = "assessments_tasks"

    assessment_id: Mapped[UUID] = mapped_column(
        ForeignKey("assessments.id"),
        primary_key=True
    )
    task_id: Mapped[UUID] = mapped_column(
        ForeignKey("tasks.id"),
        primary_key=True
    )
    position: Mapped[int] = mapped_column(nullable=False)  # Extra metadata

    # Relationships
    assessment: Mapped["DbAssessment"] = relationship(...)
    task: Mapped["DbTask"] = relationship(...)
```

**Pattern:**
```
DbAssessment ←→ DbAssessmentsTasks ←→ DbTask
   (1)              (many-to-many)        (1)
```

---

### 5. **Single Table Inheritance** (Fowler - P of EAA)

**Intent:** Represent an inheritance hierarchy in one table with a type discriminator column.

**Implementation:**
```python
class DbTask(DbBase):
    __tablename__ = "tasks"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # Discriminator

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "task"
    }


class DbPrimer(DbTask):
    __tablename__ = "primers"

    id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "primer"
    }


class DbExercise(DbTask):
    __tablename__ = "exercises"

    id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "exercise"
    }
```

**Pattern:**
- Base table: `tasks` (common fields + type column)
- Child tables: `primers`, `exercises` (specific fields)

**Query Behavior:**
```python
session.query(DbTask).all()  # Returns DbPrimer and DbExercise objects
```

---

## Layer Structure

### Directory Layout

```
database/
  ├── tables/              # ORM model definitions
  │   ├── base.py         # Base class for all tables
  │   ├── assessments.py
  │   ├── exercises.py
  │   ├── primers.py
  │   ├── tasks.py        # Base for inheritance
  │   ├── assessment_submissions.py
  │   └── ...
  ├── orm.py              # Session management, engine setup
  ├── exceptions.py       # Database-specific exceptions
  └── __init__.py
```

---

## ORM Model Structure

### Base Model

```python
# tables/base.py
from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class DbBase(DeclarativeBase):
    """Base class for all database models."""

    # Common columns for all tables
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    modified_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=True
    )
```

**Pattern:** Template Method (GoF)
- Base class defines structure
- Subclasses add specific columns

---

### Entity Table

```python
# tables/assessments.py
class DbAssessment(DbBase):
    __tablename__ = "assessments"

    # COLUMNS
    name: Mapped[str] = mapped_column(Unicode(100), nullable=False)
    deadline: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    max_attempts: Mapped[int | None] = mapped_column(nullable=True)

    # RELATIONSHIPS
    assessment_submissions: Mapped[list["DbAssessmentSubmission"]] = relationship(
        back_populates="assessment",
        lazy="selectin"  # Eager loading strategy
    )

    tasks: Mapped[list["DbTask"]] = relationship(
        secondary="assessments_tasks",
        viewonly=True  # Read-only view
    )

    tasks_link: Mapped[list["DbAssessmentsTasks"]] = relationship(
        back_populates="assessment",
        cascade="all, delete-orphan"  # Cascade deletes
    )
```

**Sections:**
1. **Columns** - Table fields
2. **Relationships** - Foreign key navigation

---

## Relationship Patterns

### 1. **One-to-Many**

```python
# Parent
class DbAssessment(DbBase):
    assessment_submissions: Mapped[list["DbAssessmentSubmission"]] = relationship(
        back_populates="assessment"
    )

# Child
class DbAssessmentSubmission(DbBase):
    assessment_id: Mapped[UUID] = mapped_column(ForeignKey("assessments.id"))
    assessment: Mapped["DbAssessment"] = relationship(
        back_populates="assessment_submissions"
    )
```

**Pattern:**
```
DbAssessment (1) ←→ (many) DbAssessmentSubmission
```

---

### 2. **Many-to-Many (via Association Table)**

```python
# Side 1
class DbAssessment(DbBase):
    tasks_link: Mapped[list["DbAssessmentsTasks"]] = relationship(...)

# Association
class DbAssessmentsTasks(DbBase):
    assessment_id: Mapped[UUID] = mapped_column(ForeignKey("assessments.id"), primary_key=True)
    task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id"), primary_key=True)
    position: Mapped[int]  # Extra metadata

# Side 2
class DbTask(DbBase):
    assessments_link: Mapped[list["DbAssessmentsTasks"]] = relationship(...)
```

**Pattern:**
```
DbAssessment ←→ DbAssessmentsTasks ←→ DbTask
```

---

### 3. **Polymorphic (Inheritance)**

```python
# Base
class DbTask(DbBase):
    __mapper_args__ = {"polymorphic_on": "type"}

# Child 1
class DbPrimer(DbTask):
    __mapper_args__ = {"polymorphic_identity": "primer"}

# Child 2
class DbExercise(DbTask):
    __mapper_args__ = {"polymorphic_identity": "exercise"}
```

**Pattern:**
```
       DbTask
         / \
        /   \
  DbPrimer  DbExercise
```

---

## Session Management

### Engine & Session Factory

```python
# orm.py
@cache
def get_db_engine() -> Engine:
    """Create database engine (singleton)."""
    settings = get_settings()
    connection_url = URL.create(
        drivername=f"{settings.db_type}+{settings.db_driver}",
        username=settings.db_user,
        password=settings.db_password,
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_name,
    )
    return create_engine(connection_url, ...)


@cache
def get_sessionmaker() -> sessionmaker:
    """Create session factory (singleton)."""
    return sessionmaker(class_=Session, ...)


def get_db_session(...) -> Generator[Session, None, None]:
    """
    FastAPI dependency for database sessions.

    Provides:
    - Session creation
    - Automatic commit/rollback
    - Session cleanup
    """
    session = session_factory(bind=get_db_engine())
    try:
        yield session  # Used in request
    except Exception:
        session.rollback()  # Rollback on error
        raise
    finally:
        session.close()  # Always cleanup
```

**Pattern:** Factory Method (GoF) + Dependency Injection

---

## Database Migrations

### Alembic Integration

```python
def run_migrations():
    """Run Alembic database migrations."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
```

**Migration Files:**
```
db_migrations/
  └── versions/
      ├── 001_initial_schema.py
      ├── 002_add_max_attempts.py
      └── ...
```

**Usage:**
```bash
# Generate migration
alembic revision --autogenerate -m "Add new field"

# Apply migrations
alembic upgrade head

# Or programmatically
python -c "from app.database.orm import run_migrations; run_migrations()"
```

---

## Layer Rules & Constraints

### ✅ ALLOWED Dependencies

Database Layer MAY depend on:
- **SQLAlchemy** - ORM framework
- **Alembic** - Migration tool
- **Settings** (`app.settings`) - Configuration

### ❌ FORBIDDEN Dependencies

Database Layer MUST NOT:
- **Depend on Domain Models** - ORM models are independent
- **Depend on Services** - Wrong direction
- **Depend on Repositories** - Repositories use database, not vice versa
- **Depend on REST Layer** - Violates layering

### Dependency Flow

```
Repository Layer
    ↓ (uses)
Database Layer ← YOU ARE HERE
    ↓ (persisted to)
PostgreSQL Database
```

---

## Column Type Patterns

### UUIDs (Primary Keys)

```python
id: Mapped[UUID] = mapped_column(
    primary_key=True,
    default=uuid4  # Auto-generate
)
```

### Timestamps

```python
created_at: Mapped[datetime] = mapped_column(
    TIMESTAMP(timezone=True),
    default=lambda: datetime.now(timezone.utc)
)

modified_at: Mapped[datetime | None] = mapped_column(
    TIMESTAMP(timezone=True),
    onupdate=lambda: datetime.now(timezone.utc),  # Auto-update
    nullable=True
)
```

### Strings

```python
name: Mapped[str] = mapped_column(
    Unicode(100),  # Max 100 characters, Unicode support
    nullable=False
)
```

### Optional Fields

```python
deadline: Mapped[datetime | None] = mapped_column(
    TIMESTAMP(timezone=True),
    nullable=True,
    default=None
)
```

### Booleans

```python
finished: Mapped[bool] = mapped_column(
    default=False,
    nullable=False
)
```

---

## Relationship Configuration

### Lazy Loading Strategies

```python
# Select IN loading (fewer queries, good default)
tasks: Mapped[list["DbTask"]] = relationship(
    lazy="selectin"
)

# Joined loading (single query with JOIN)
tasks: Mapped[list["DbTask"]] = relationship(
    lazy="joined"
)

# Lazy loading (query on access, N+1 risk)
tasks: Mapped[list["DbTask"]] = relationship(
    lazy="select"  # Default
)
```

**Best Practice:** Use `lazy="selectin"` for most relationships

### Cascade Operations

```python
tasks_link: Mapped[list["DbAssessmentsTasks"]] = relationship(
    cascade="all, delete-orphan"
)
```

**Cascade Options:**
- `all` - Propagate all operations
- `delete` - Delete children when parent deleted
- `delete-orphan` - Delete children when removed from collection
- `save-update` - Persist changes to children

### Bidirectional Relationships

```python
# Parent
class DbAssessment(DbBase):
    submissions: Mapped[list["DbAssessmentSubmission"]] = relationship(
        back_populates="assessment"  # Points to child attribute
    )

# Child
class DbAssessmentSubmission(DbBase):
    assessment: Mapped["DbAssessment"] = relationship(
        back_populates="submissions"  # Points to parent attribute
    )
```

**Pattern:** Mirror relationships with `back_populates`

---

## Query Optimization

### Eager Loading (Avoid N+1)

```python
# BAD: N+1 queries
assessment = session.get(DbAssessment, id)
for task in assessment.tasks:  # Each iteration = 1 query
    print(task.name)

# GOOD: Single query with eager loading
assessment = session.query(DbAssessment).options(
    selectinload(DbAssessment.tasks)
).filter(DbAssessment.id == id).first()

for task in assessment.tasks:  # No additional queries
    print(task.name)
```

### Relationship Loading

```python
from sqlalchemy.orm import joinedload, selectinload, subqueryload

# Joined load (single query, JOIN)
session.query(DbAssessment).options(
    joinedload(DbAssessment.tasks)
)

# Select IN load (2 queries: parent + IN clause for children)
session.query(DbAssessment).options(
    selectinload(DbAssessment.tasks)
)

# Subquery load (2 queries: parent + subquery for children)
session.query(DbAssessment).options(
    subqueryload(DbAssessment.tasks)
)
```

---

## Testing Database Layer

### Unit Tests (Schema Validation)

```python
def test_db_assessment_columns():
    """Test table has expected columns."""
    assert hasattr(DbAssessment, 'name')
    assert hasattr(DbAssessment, 'deadline')
    assert hasattr(DbAssessment, 'max_attempts')


def test_db_assessment_relationships():
    """Test relationships are defined."""
    assert hasattr(DbAssessment, 'tasks')
    assert hasattr(DbAssessment, 'assessment_submissions')
```

### Integration Tests (with TestContainers)

```python
def test_create_assessment(test_db):
    """Test can persist and retrieve assessment."""
    # Create
    assessment = DbAssessment(name="Test")
    test_db.add(assessment)
    test_db.commit()

    # Retrieve
    result = test_db.get(DbAssessment, assessment.id)

    assert result.name == "Test"
```

---

## Anti-Patterns to Avoid

### ❌ **1. Business Logic in ORM Models**

```python
# BAD: Business logic in database model
class DbAssessment(DbBase):
    def can_user_submit(self, user_id):  # ❌ Business logic
        submissions = self.get_user_submissions(user_id)
        return len(submissions) < self.max_attempts

# GOOD: ORM model is just structure
class DbAssessment(DbBase):
    __tablename__ = "assessments"
    name: Mapped[str]
    max_attempts: Mapped[int | None]
    # No methods
```

**Rule:** ORM models define structure, not behavior

---

### ❌ **2. Circular Imports**

```python
# BAD: Importing domain models
from app.core.models.assessment import Assessment  # ❌

class DbAssessment(DbBase):
    pass

# GOOD: Database layer is independent
class DbAssessment(DbBase):
    pass  # No imports from domain
```

---

### ❌ **3. Missing Relationships**

```python
# BAD: Only foreign key, no relationship
class DbAssessmentSubmission(DbBase):
    assessment_id: Mapped[UUID] = mapped_column(ForeignKey("assessments.id"))
    # ❌ No relationship defined

# GOOD: Foreign key + relationship
class DbAssessmentSubmission(DbBase):
    assessment_id: Mapped[UUID] = mapped_column(ForeignKey("assessments.id"))
    assessment: Mapped["DbAssessment"] = relationship(...)  # ✅ ORM navigation
```

---

## SOLID Principles

### Single Responsibility Principle (SRP)

Each table model represents ONE entity:
- `DbAssessment` - assessments table only
- `DbExercise` - exercises table only

Each file contains ONE table definition.

### Open/Closed Principle (OCP)

Schema can be extended without modification:
```python
# Base schema defined
class DbAssessment(DbBase):
    name: Mapped[str]

# Extended via migration (not code change)
# Migration adds new column
```

---

## Database Design Principles

### 1. **Normalization**

Tables are normalized to 3NF:
- 1NF: Atomic values (no arrays in columns)
- 2NF: No partial dependencies
- 3NF: No transitive dependencies

**Example:**
```
assessments (id, name, deadline)
tasks (id, type, ...)
assessments_tasks (assessment_id, task_id, position)
```

### 2. **Referential Integrity**

All relationships use foreign keys:
```python
assessment_id: Mapped[UUID] = mapped_column(
    ForeignKey("assessments.id"),  # References parent
    nullable=False
)
```

### 3. **Cascading**

Deletes cascade appropriately:
```python
tasks_link: Mapped[list["DbAssessmentsTasks"]] = relationship(
    cascade="all, delete-orphan"  # Delete association when assessment deleted
)
```

---

## PostgreSQL Specific Features

### JSON Columns

```python
from sqlalchemy.dialects.postgresql import JSON

metadata: Mapped[dict] = mapped_column(JSON, nullable=True)
```

### Arrays

```python
from sqlalchemy.dialects.postgresql import ARRAY

tags: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
```

### UUIDs

```python
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
```

---

## References

**Books:**
- Fowler, Martin. *Patterns of Enterprise Application Architecture*. 2002.
  - Object-Relational Behavioral Patterns (Chapter 12)
  - Object-Relational Structural Patterns (Chapter 13)
  - Foreign Key Mapping (p236)
  - Association Table Mapping (p248)
  - Single Table Inheritance (p278)

**Documentation:**
- SQLAlchemy ORM: https://docs.sqlalchemy.org/en/20/orm/
- Alembic Migrations: https://alembic.sqlalchemy.org/

**Key Quotes:**

**Fowler on ORM:**
> "Object-relational mapping is a technique for managing the differences between object-oriented and relational worlds."

**Fowler on Single Table Inheritance:**
> "Single Table Inheritance maps all fields of all classes of an inheritance hierarchy into a single table."

---

## Summary

The Database Layer is a **schema definition and persistence foundation** that:
- ✅ Defines database structure using ORM
- ✅ Manages relationships and foreign keys
- ✅ Provides migration support (Alembic)
- ✅ Handles session/connection management
- ❌ Contains NO business logic
- ❌ Does NOT depend on domain models
- ❌ Does NOT perform queries (repositories do that)

**Keep database models simple, structural, and focused on persistence.**
