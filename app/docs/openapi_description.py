DESCRIPTION = """
## Domain Language

This API uses a domain-specific language for sign language assessments.

### Core Entities

**Assessment**
A structured collection of tasks presented to learners. Contains an ordered sequence of tasks (primers and exercises), optional deadline, and max_attempts limit.

**Task**
An item within an assessment. Can be either a Primer or Exercise.

**Primer**
Non-questioning content in an assessment. Used for instructions, stories, technical explanations, or conclusion videos. Contains multimedia (video/image).

**Exercise**
A question requiring answer selection. Contains a Question and Multiple Choice with 2-4 choices.

**Question**
The question content of an exercise (multimedia file).

**Multiple Choice**
Container for answer choices (2-4). Each choice has position and correctness flag.

**Choice**
One answer option with multimedia content.

**Multimedia File**
Media content (image or video). Stored in MinIO with presigned URLs. Future versions may add other content types.

### Submission Entities

**Assessment Submission**
One learner attempt at an assessment. Contains exercise submissions, finished flag, and calculated score.

**Exercise Submission**
Learner's answer to one exercise. Contains selected choice IDs and correctness flag. Immutable after creation.

**Assessment Result**
Aggregated statistics for all submissions of an assessment. Requires TEST_SCORER role.

### Roles

- **FRONTEND** - Learner (create submissions, answer exercises, view own submissions)
- **TEST_SCORER** - Teacher (all FRONTEND permissions + view all submissions/results)
- **ADMIN** - Full system access

### Entity Relationships

```
Assessment
  └─ Tasks (ordered)
      ├─ Primer (content)
      └─ Exercise
          ├─ Question (multimedia)
          └─ Multiple Choice
              └─ Choices (2-4, positioned)

Assessment Submission (per attempt)
  └─ Exercise Submissions (one per exercise)
      └─ answer (selected choice IDs)
```

### Technical

**Authentication:** JWT Bearer token (Keycloak)
**IDs:** UUID v4
**Timestamps:** ISO 8601 (UTC)
**Media URLs:** Presigned (1 hour expiry)

**Constraints:**
- Choices: 2-4 per multiple choice
- Exercise submissions: Immutable

[OpenAPI Specification][1] | [Source Code][2]

[1]: https://swagger.io/resources/open-api/
[2]: ../
"""
