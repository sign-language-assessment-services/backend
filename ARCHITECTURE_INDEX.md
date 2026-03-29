# Architecture Documentation Index

This document serves as the entry point for all architectural documentation.

## Quick Links

### High-Level Overview
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Complete backend architecture overview
- **[SEQUENCE_DIAGRAMS.md](SEQUENCE_DIAGRAMS.md)** - 🔍 **Use case flows & debugging guide** (30+ sequence diagrams)
- **[../ARCHITECTURE_ANALYSIS.md](../ARCHITECTURE_ANALYSIS.md)** - Detailed analysis with diagrams

### Layer-Specific Documentation

Navigate to specific layers for detailed patterns and principles:

1. **[REST Layer](app/rest/README.md)** - Presentation layer (HTTP/JSON)
2. **[Service Layer](app/services/README.md)** - Business logic orchestration
3. **[Repository Layer](app/repositories/README.md)** - Data access abstraction
4. **[Mapper Layer](app/mappers/README.md)** - Domain ↔ Database transformation
5. **[Database Layer](app/database/README.md)** - ORM models & persistence
6. **[Core Layer](app/core/README.md)** - Domain models & entities

## Purpose of These Documents

These README files were created to:

1. **Preserve Architectural Intent** - Document WHY decisions were made
2. **Establish Patterns** - Define how each layer should be implemented
3. **Guide Development** - Provide templates and examples
4. **Reference Authority** - Cite Martin Fowler, Gang of Four, Eric Evans
5. **Enable Context Restoration** - Allow AI assistants to understand architecture without repeated explanations

## For AI Assistants

When working on this codebase:

1. **Read ARCHITECTURE.md first** - Get the big picture
2. **Check SEQUENCE_DIAGRAMS.md** - Understand request flows for the use case
3. **Read layer-specific README.md** - Understand the layer you're working in
4. **Follow the patterns** - Don't deviate without discussion
5. **Reference the authorities** - Fowler, Evans, Martin, GoF

**For debugging:** Always start with SEQUENCE_DIAGRAMS.md to trace the error!

## For Human Developers

### New to the Project?

Read in this order:
1. [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture overview
2. [app/core/README.md](app/core/README.md) - Domain models
3. Layer where you'll work most

### Adding a New Feature?

Follow the pattern in [ARCHITECTURE.md](ARCHITECTURE.md) under "Creating a New Entity"

### Debugging an Issue?

**FIRST:** Check [SEQUENCE_DIAGRAMS.md](SEQUENCE_DIAGRAMS.md) to trace the request flow!

Then find the specific layer:
- REST issue? → [app/rest/README.md](app/rest/README.md)
- Business logic? → [app/services/README.md](app/services/README.md)
- Data access? → [app/repositories/README.md](app/repositories/README.md)
- Transformation? → [app/mappers/README.md](app/mappers/README.md)
- Database? → [app/database/README.md](app/database/README.md)

**Example:** Getting 404 on creating assessment?
1. Open [SEQUENCE_DIAGRAMS.md](SEQUENCE_DIAGRAMS.md)
2. Find "UC-A1: Create Assessment"
3. Follow the sequence diagram to see where 404 can occur
4. Check error scenarios table for solution

## Document Maintenance

These documents should be updated when:
- Architecture changes significantly
- New patterns are adopted
- Anti-patterns are discovered
- Layer responsibilities shift

**Owner:** Development Team
**Last Updated:** 2026-03-28
**Version:** 1.0

## Feedback

If you find these documents unclear or outdated, please update them!
