# Core Layer (Domain Layer)

## Architectural Intent

The Core Layer contains the **domain models and business entities** that represent the core concepts of the application. This is the heart of the application - the business domain expressed in code.

## Core Responsibilities

1. **Domain Model Definition** - Define business entities and their structure
2. **Type Safety** - Provide compile-time type checking via Pydantic
3. **Validation** - Enforce basic data constraints
4. **Business Vocabulary** - Establish ubiquitous language
5. **Value Objects** - Define immutable value types
6. **Domain Events** (if needed) - Model state changes

## Architectural Patterns Applied

### 1. **Domain Model Pattern** (Fowler - P of EAA)

**Intent:** An object model of the domain that incorporates both behavior and data.

**Fowler's Definition:**
> "A Domain Model creates a web of interconnected objects, where each object represents some meaningful individual, whether as large as a corporation or as small as a single line on an order form."

**Current Implementation Style:**
This project uses an **Anemic Domain Model** - domain objects are primarily data containers with minimal behavior. This is a pragmatic choice for CRUD-heavy applications.

```python
# assessment.py
class Assessment(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    name: str
    deadline: datetime | None = Field(default=None)
    max_attempts: int | None = Field(default=None)
    tasks: list[Primer | Exercise] = Field(default_factory=list)

    # Currently: No methods, just data
    # Could have: can_accept_submission(), is_deadline_passed(), etc.
```

---

### 2. **Value Object Pattern** (Evans - DDD)

**Intent:** Small objects that are defined by their attributes rather than identity.

**Characteristics:**
- Immutable
- No identity (no ID field)
- Equality based on values, not identity
- Replaceable

**Examples in Our Domain:**

```python
# Choice is a Value Object
class Choice(BaseModel):
    id: UUID  # Technical ID for persistence, not domain identity
    text: str
    is_correct: bool
    multimedia_files: list[MultimediaFile]

    # Immutable (Pydantic frozen=True could enforce this)
    # Two choices with same text/is_correct are equivalent
```

**Contrast with Entity:**
```python
# Assessment is an Entity
class Assessment(BaseModel):
    id: UUID  # Domain identity
    name: str

    # Two assessments with same name are DIFFERENT (different IDs)
```

**Evans' Wisdom:**
> "When you care only about the attributes of an element of the model, classify it as a VALUE OBJECT. Treat the VALUE OBJECT as immutable."

---

### 3. **Entity Pattern** (Evans - DDD)

**Intent:** Objects that have identity and continuity through time.

**Characteristics:**
- Has unique identity (ID)
- Mutable (state can change over time)
- Equality based on ID, not attributes
- Tracked through lifecycle

**Entities in Our Domain:**
- `Assessment` - Has identity, can be modified
- `Exercise` - Has identity, can be modified
- `Primer` - Has identity, can be modified
- `AssessmentSubmission` - Has identity, evolves through states

```python
class Assessment(BaseModel):
    id: UUID  # Identity
    created_at: datetime
    modified_at: datetime | None  # Tracks changes over time

    # State can change
    name: str
    deadline: datetime | None
```

---

### 4. **Composite Pattern** (GoF)

**Intent:** Compose objects into tree structures to represent part-whole hierarchies.

**Implementation:**
```python
# Assessment is composite of Tasks
class Assessment(BaseModel):
    tasks: list[Primer | Exercise]  # Composite structure

# Task is abstract component
# Primer and Exercise are leaf nodes
```

**Pattern:**
```
      Assessment
         |
      [tasks]
      /     \
 Primer   Exercise
```

---

### 5. **Strategy Pattern** (Implicit in Polymorphism)

**Intent:** Define a family of algorithms, encapsulate each one, and make them interchangeable.

**Implementation:**
```python
# Union type allows different task types
tasks: list[Primer | Exercise]

# Each task type is a "strategy" for what to display
# - Primer: Show instructional content
# - Exercise: Show question with choices
```

---

## Layer Structure

### Directory Layout

```
core/
  ├── models/                    # Domain models
  │   ├── assessment.py         # Assessment entity
  │   ├── exercise.py           # Exercise entity
  │   ├── primer.py             # Primer entity
  │   ├── choice.py             # Choice value object
  │   ├── multiple_choice.py    # Multiple choice value object
  │   ├── assessment_submission.py
  │   ├── exercise_submission.py
  │   ├── multimedia_file.py
  │   ├── user.py               # User entity
  │   ├── role.py               # Role enum
  │   └── ...
  ├── exceptions.py             # Domain exceptions
  └── __init__.py
```

---

## Domain Model Design

### Entity Structure

```python
from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Assessment(BaseModel):
    """
    Assessment entity - represents a collection of tasks to be completed.

    Domain Concept:
    An assessment is a structured evaluation consisting of primers
    (instructional content) and exercises (questions). Students submit
    their answers, and the system scores their performance.

    Lifecycle:
    1. Created by teacher
    2. Published with tasks
    3. Submitted by students
    4. Scored automatically
    """

    # IDENTITY
    id: UUID = Field(default_factory=uuid4)

    # TIMESTAMPS
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    modified_at: datetime | None = Field(default=None)

    # ATTRIBUTES
    name: str
    deadline: datetime | None = Field(default=None)
    max_attempts: int | None = Field(default=None)

    # RELATIONSHIPS
    tasks: list[Primer | Exercise] = Field(default_factory=list)

    # FUTURE: Could add methods
    # def is_deadline_passed(self) -> bool:
    #     if not self.deadline:
    #         return False
    #     return datetime.now(timezone.utc) > self.deadline
    #
    # def can_accept_submission(self, existing_count: int) -> bool:
    #     if self.is_deadline_passed():
    #         return False
    #     if self.max_attempts and existing_count >= self.max_attempts:
    #         return False
    #     return True
```

---

### Value Object Structure

```python
class Choice(BaseModel):
    """
    Choice value object - represents a possible answer.

    Domain Concept:
    A choice is one possible answer in a multiple-choice exercise.
    It's defined by its content (text, multimedia) and correctness.

    Value Object Properties:
    - No meaningful identity (ID is for persistence only)
    - Immutable (should not change after creation)
    - Replaceable (can swap one choice for another)
    - Equality based on content, not identity
    """

    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    text: str
    is_correct: bool
    multimedia_files: list[MultimediaFile] = Field(default_factory=list)

    # Could make immutable:
    # model_config = ConfigDict(frozen=True)
```

---

## Domain Concepts

### Core Entities

#### 1. **Assessment**
**Business Definition:** A structured evaluation consisting of tasks.

**Attributes:**
- `name` - Human-readable identifier
- `deadline` - Optional due date
- `max_attempts` - Maximum submission attempts
- `tasks` - Ordered collection of Primers and Exercises

**Relationships:**
- Has many Tasks (composition)
- Has many AssessmentSubmissions

---

#### 2. **Task** (Abstract)
**Business Definition:** A unit of work in an assessment.

**Subtypes:**
- **Primer** - Instructional content (teach)
- **Exercise** - Question to answer (test)

**Pattern:** Strategy Pattern (different types, same interface)

---

#### 3. **Exercise**
**Business Definition:** A question that requires an answer.

**Attributes:**
- `question` - Question object containing text/multimedia
- `multiple_choice` - Answer options

**Relationships:**
- Belongs to Assessment(s)
- Has one MultipleChoice (composition)
- Has many ExerciseSubmissions

---

#### 4. **Primer**
**Business Definition:** Instructional content to teach concepts.

**Attributes:**
- `instruction` - Text instruction
- `multimedia_files` - Supporting media

**Purpose:** Prepare students before exercises

---

#### 5. **AssessmentSubmission**
**Business Definition:** A student's attempt at an assessment.

**Attributes:**
- `user_id` - Student identifier
- `assessment_id` - Assessment being submitted
- `finished` - Completion status
- `score` - Final score (when finished)

**Lifecycle:**
```
Created → In Progress → Finished → Scored
```

---

#### 6. **ExerciseSubmission**
**Business Definition:** A student's answer to a specific exercise.

**Attributes:**
- `assessment_submission_id` - Parent submission
- `exercise_id` - Exercise being answered
- `answer` - Selected choice(s)
- `is_correct` - Whether answer was correct

---

### Value Objects

#### 1. **Choice**
**Definition:** One possible answer in a multiple-choice question.

**Why Value Object?**
- Identity doesn't matter (content does)
- Immutable once created
- Equality based on content

---

#### 2. **MultipleChoice**
**Definition:** Collection of choices for an exercise.

**Attributes:**
- `type` - SINGLE or MULTIPLE selection
- `choices` - List of Choice objects

---

#### 3. **Question**
**Definition:** The question content (text + multimedia).

**Attributes:**
- `question_text` - Text of the question
- `multimedia_files` - Supporting media

---

#### 4. **MultimediaFile**
**Definition:** Reference to a file in object storage.

**Attributes:**
- `bucket` - MinIO bucket
- `object_name` - File path
- `media_type` - VIDEO, IMAGE, etc.

---

## Enums and Constants

### QuestionType

```python
from enum import Enum

class QuestionType(str, Enum):
    """Multiple choice selection type."""
    SINGLE = "single"
    MULTIPLE = "multiple"
```

### MediaType

```python
class MediaType(str, Enum):
    """Supported multimedia types."""
    VIDEO = "video"
    IMAGE = "image"
```

### UserRole

```python
class UserRole(str, Enum):
    """User roles for authorization."""
    FRONTEND = "frontend"
    TEACHER = "teacher"
    ADMIN = "admin"
```

---

## Layer Rules & Constraints

### ✅ ALLOWED Dependencies

Core Layer MAY depend on:
- **Standard Library** - datetime, uuid, enum, etc.
- **Pydantic** - For model definition and validation
- **Type Hints** - For type safety

### ❌ FORBIDDEN Dependencies

Core Layer MUST NOT depend on:
- **Service Layer** - Would create circular dependency
- **Repository Layer** - Domain is persistence-ignorant
- **Database Layer** - No SQLAlchemy imports
- **REST Layer** - No FastAPI or HTTP concepts
- **External Services** - No Keycloak, MinIO, etc.

### Dependency Flow

```
ALL LAYERS
    ↓
Core Layer ← YOU ARE HERE (Everyone depends on core)
    ↓
(No dependencies - Core is the center)
```

**Key Principle:** Core is at the center. All other layers depend on it, but it depends on nothing.

---

## Pydantic Benefits

### 1. **Automatic Validation**

```python
class Assessment(BaseModel):
    name: str  # Must be string
    max_attempts: int | None = Field(default=None, ge=1)  # If set, must be >= 1
    deadline: datetime | None  # Must be valid datetime

# Invalid data raises ValidationError
try:
    Assessment(name=123, max_attempts=-5)  # ❌ Fails
except ValidationError as e:
    print(e)
```

### 2. **Type Safety**

```python
def process_assessment(assessment: Assessment) -> None:
    # IDE knows assessment.name is str
    # Type checker validates at compile time
    print(assessment.name.upper())
```

### 3. **JSON Serialization**

```python
assessment = Assessment(name="Test", tasks=[])

# To JSON
json_str = assessment.model_dump_json()

# From JSON
reconstructed = Assessment.model_validate_json(json_str)
```

### 4. **Immutability (Optional)**

```python
class Choice(BaseModel):
    model_config = ConfigDict(frozen=True)  # Make immutable

choice = Choice(text="A", is_correct=True)
choice.text = "B"  # ❌ Raises error
```

---

## Current Architecture: Anemic Domain Model

### What It Means

**Anemic Domain Model:**
- Domain objects are data structures
- No business logic in domain objects
- All behavior in service layer

**Our Implementation:**
```python
# Domain model: Just data
class Assessment(BaseModel):
    name: str
    max_attempts: int | None
    tasks: list[Primer | Exercise]

# Service: All the logic
class AssessmentService:
    def can_user_submit(self, assessment: Assessment, user_submissions: int) -> bool:
        if assessment.max_attempts and user_submissions >= assessment.max_attempts:
            return False
        return True
```

---

### Rich Domain Model Alternative

**Rich Domain Model:**
- Domain objects contain behavior
- Business logic lives in domain
- Services are thin orchestrators

**How It Could Look:**
```python
# Domain model: Data + Behavior
class Assessment(BaseModel):
    name: str
    max_attempts: int | None
    deadline: datetime | None
    tasks: list[Primer | Exercise]

    # Business logic in domain
    def can_accept_submission(self, existing_count: int) -> tuple[bool, str | None]:
        """Check if a new submission is allowed."""
        if self.deadline and datetime.now(timezone.utc) > self.deadline:
            return False, "Deadline has passed"

        if self.max_attempts and existing_count >= self.max_attempts:
            return False, f"Maximum {self.max_attempts} attempts reached"

        return True, None

    def is_deadline_passed(self) -> bool:
        """Check if deadline has passed."""
        if not self.deadline:
            return False
        return datetime.now(timezone.utc) > self.deadline

    def get_exercise_count(self) -> int:
        """Count exercises in assessment."""
        return len([t for t in self.tasks if isinstance(t, Exercise)])

# Service: Thin orchestrator
class AssessmentService:
    def create_submission(self, assessment_id: UUID, user_id: str):
        assessment = self.repository.get(assessment_id)
        existing = self.repository.count_submissions(assessment_id, user_id)

        # Domain makes decision
        can_submit, reason = assessment.can_accept_submission(existing)
        if not can_submit:
            raise ValidationError(reason)

        # Service just orchestrates
        submission = AssessmentSubmission(...)
        self.repository.add(submission)
        return submission
```

---

## Why Anemic Is OK Here

### Fowler's Guidance

**When Anemic Is Acceptable:**
1. Simple CRUD operations
2. Minimal business logic
3. Data-centric application
4. Framework constraints (Pydantic)

**Our Application:**
- ✅ Mostly CRUD
- ✅ Simple validation rules
- ✅ Pydantic-based (validation framework)
- ✅ Team is productive

**Fowler:**
> "For simple problems, Transaction Script (with anemic models) works just fine and is easier to write than Domain Model."

---

## SOLID Principles

### Single Responsibility Principle (SRP)

Each model represents ONE concept:
- `Assessment` - Assessment only
- `Exercise` - Exercise only
- `Choice` - Choice only

### Open/Closed Principle (OCP)

Easy to extend:
```python
# Add new task type without modifying Assessment
class Quiz(BaseModel):  # New task type
    pass

# Assessment already supports it
tasks: list[Primer | Exercise | Quiz]  # Just add to union
```

### Liskov Substitution Principle (LSP)

Subtypes are substitutable:
```python
tasks: list[Primer | Exercise]

# Both Primer and Exercise can be used wherever Task is expected
for task in tasks:
    # Both types work
    print(task.id)
```

---

## Domain-Driven Design Concepts

### Ubiquitous Language

**Terms from Domain:**
- **Assessment** - Not "test" or "quiz"
- **Task** - Not "item" or "question"
- **Primer** - Instructional content
- **Exercise** - Question to answer
- **Submission** - Student's attempt
- **Choice** - Possible answer

**Consistency:** Same terms in code, docs, and conversations

---

### Bounded Context

**Sign Language Assessment Context:**
- Assessments, Exercises, Submissions
- Bounded by sign language education domain

**External Contexts:**
- Authentication (Keycloak)
- Storage (MinIO)
- Not part of core domain

---

### Aggregates (Potential Future)

**Aggregate Pattern:**
- Group related entities
- One aggregate root
- Enforce invariants

**Could Be:**
```python
class AssessmentAggregate:
    """
    Aggregate Root: Assessment

    Ensures:
    - Tasks are valid
    - Submissions respect max_attempts
    - Deadline enforced
    """

    def __init__(self, assessment: Assessment):
        self._assessment = assessment
        self._submissions: list[AssessmentSubmission] = []

    def create_submission(self, user_id: str) -> AssessmentSubmission:
        # Aggregate enforces rules
        if len(self._submissions) >= self._assessment.max_attempts:
            raise MaxAttemptsError()

        submission = AssessmentSubmission(...)
        self._submissions.append(submission)
        return submission
```

---

## Testing Domain Models

### Validation Tests

```python
def test_assessment_requires_name():
    with pytest.raises(ValidationError):
        Assessment(name="")  # Empty name

def test_assessment_max_attempts_must_be_positive():
    with pytest.raises(ValidationError):
        Assessment(name="Test", max_attempts=-1)
```

### Business Logic Tests (If Rich Domain)

```python
def test_assessment_deadline_passed():
    past = datetime.now(timezone.utc) - timedelta(days=1)
    assessment = Assessment(name="Test", deadline=past)

    assert assessment.is_deadline_passed() is True

def test_assessment_can_accept_submission():
    assessment = Assessment(name="Test", max_attempts=3)

    can_submit, _ = assessment.can_accept_submission(existing_count=2)
    assert can_submit is True

    can_submit, reason = assessment.can_accept_submission(existing_count=3)
    assert can_submit is False
    assert "maximum" in reason.lower()
```

---

## Future Evolution: Rich Domain Model

### When to Evolve

**Consider Rich Domain Model when:**
1. Business logic becomes complex
2. Same logic duplicated across services
3. Domain rules are hard to enforce
4. Need better testability

### Migration Path

```python
# Phase 1: Add query methods (read-only)
class Assessment(BaseModel):
    def get_exercise_count(self) -> int:
        return len([t for t in self.tasks if isinstance(t, Exercise)])

# Phase 2: Add validation methods
class Assessment(BaseModel):
    def validate_can_submit(self, existing: int) -> None:
        if self.max_attempts and existing >= self.max_attempts:
            raise ValidationError(...)

# Phase 3: Add command methods
class Assessment(BaseModel):
    def create_submission(self, user_id: str) -> AssessmentSubmission:
        self.validate_can_submit(...)
        return AssessmentSubmission(...)

# Phase 4: Full rich domain model
```

---

## References

**Books:**
- Fowler, Martin. *Patterns of Enterprise Application Architecture*. 2002.
  - Domain Model (p116-145)
  - Anemic Domain Model (bliki article, 2003)

- Evans, Eric. *Domain-Driven Design: Tackling Complexity in the Heart of Software*. 2003.
  - Entities (Chapter 5)
  - Value Objects (Chapter 5)
  - Aggregates (Chapter 6)
  - Ubiquitous Language (Chapter 2)

- Gamma et al. *Design Patterns*. 1994.
  - Composite (p163)
  - Strategy (p315)

**Key Quotes:**

**Evans on Entities:**
> "Some objects are not defined primarily by their attributes. They represent a thread of identity that runs through time and often across distinct representations."

**Evans on Value Objects:**
> "When you care only about the attributes of an element of the model, classify it as a VALUE OBJECT."

**Fowler on Domain Model:**
> "An object model of the domain that incorporates both behavior and data."

---

## Summary

The Core Layer is the **heart of the application** that:
- ✅ Defines business entities and concepts
- ✅ Provides type safety via Pydantic
- ✅ Establishes ubiquitous language
- ✅ Is independent of all other layers
- ⚠️ Currently anemic (acceptable for this use case)
- 🚀 Could evolve to rich domain model if complexity grows

**This layer is the foundation. All other layers exist to support it.**

---

## Current State Assessment

**Architecture Style:** Anemic Domain Model + Transaction Script
**Appropriateness:** ✅ Good fit for CRUD-heavy application
**Recommendation:** Keep current style, optionally add simple query methods

**If complexity grows:** Gradually migrate to Rich Domain Model by adding behavior to domain objects.
