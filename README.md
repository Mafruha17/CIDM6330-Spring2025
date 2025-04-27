# Final Project Submission 

**Title:** Distributed Healthcare Communication Platform\
**Domain:** Healthcare Device Communication and Chronic Disease Management\
**Author:** Mafruha Chowdhury\
**University:** West Texas A&M University — Spring 2025\
**Course:** CIDM-6330-70 Software Engineering

##

## 📚 Project Overview

**GitHub Repository:** [CIDM6330-Spring2025 - Assignment05](https://github.com/Mafruha17/CIDM6330-Spring2025)


This project provides a scalable, secure, and distributed healthcare communication system, integrating devices, patients, and providers. Built with Django, Django Ninja, Celery, Redis, Docker, and PostgreSQL.


## 📋 Table of Contents

- [📚 Project Overview](#-project-overview)
- [🔄 Evolutions Alignment Summary](#-evolutions-alignment-summary)
- [🧠 Final Project Alignment Overview](#-final-project-alignment-overview)
- [📖 Evolution 0: Domain Specification and UML Modeling](#-evolution-0-domain-specification-and-uml-modeling)
- [📖 Evolution 1: Requirements Specification Summary](#-evolution-1-requirements-specification-summary)
- [📖 Evolution 2: API Development (FastAPI)](#-evolution-2-api-development-fastapi)
- [📖 Evolution 3: Repository Pattern (FastAPI)](#-evolution-3-repository-pattern-fastapi)
- [📖 Evolution 4: Migration to Django](#-evolution-4-migration-to-django)
- [📖 Evolution 5: Full Django + Tests](#-evolution-5-full-django--tests)
- [📕 Updated Architecture Overview](#-updated-architecture-overview)
- [📖 Domain-Driven Design (DDD) Ubiquitous Language Glossary](#-domain-driven-design-ddd-ubiquitous-language-glossary)
- [📘 Gherkin BDD Scenarios](#-gherkin-bdd-scenarios)
- [🔢 TDD Mapping: Unit Tests Correspondence](#-tdd-mapping-unit-tests-correspondence)
- [🛠️ Running the System](#-running-the-system)
- [📝 Notes](#-notes)
- [🌟 Conclusion](#-conclusion)

---

## 🔄 Evolutions Alignment Summary

## 🧠 Final Project Alignment Overview

This final project integrates all required evolutions, progressively evolving from domain specification through full system deployment. Each phase demonstrates mastery over key software engineering concepts:

- **Domain Specification and Modeling:** Defined a real-world healthcare problem domain supported by detailed UML diagrams.
- **Requirements and API Specification:** Developed clear user stories, use cases, features, and initial Gherkin BDD scenarios.
- **API Development and Persistence:** Built robust RESTful APIs with FastAPI, demonstrating clear entity relationships and CRUD operations.
- **Architectural Patterns:** Applied Repository Pattern for clean separation of concerns.
- **Framework Migration:** Seamlessly migrated to Django and Django Ninja, adopting modern API development standards.
- **System Orchestration and Testing:** Integrated Celery, Redis, PostgreSQL with Docker for scalable deployment, and validated the system with comprehensive pytest and unittest coverage.

This structure fully aligns with the final project goals, delivering a modular, tested, scalable, and professional-grade backend system.

---

| Evolution | Contribution | Final Status | Link to Repo |
|:---------|:-------------|:------------|:------------|
| Evolution 0 | Domain selection and UML modeling | Completed & updated | [Evolution 0 Repo](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment0) |
| Evolution 1 | Requirements Specification with Gherkin Scenarios | Completed & enhanced | [Evolution 1 Repo](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment1) |
| Evolution 2 | API Development (FastAPI) | Completed and transitioned to Django Ninja | [Evolution 2 Repo](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment2) |
| Evolution 3 | Repository Pattern (FastAPI) | Completed (not reimplemented post-Django) | [Evolution 3 Repo](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment3) |
| Evolution 4 | Migration to Django (DRF initially) | Completed with Ninja upgrade | [Evolution 4 Repo](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment4) |
| Evolution 5 | Full Django Ninja, Docker, Celery, Redis, Testing | Fully implemented | [Evolution 5 Repo](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment5) |

---

## 📖 Evolution 0: Domain Specification and UML Modeling
- ✅ Completed and Done
- Selected Healthcare Device Communication domain
- Defined comprehensive problem statement and domain relevance
- Designed full UML suite:
  - Activity Diagram
  - Class Diagram
  - Component Diagram
  - Sequence Diagram
  - State Machine Diagram
  - Use Case Diagram

---

## 📖 Evolution 1: Requirements Specification Summary
- ✅ Completed and Done
- Full Requirements Specification:
  - User Stories
  - Use Cases (UC1–UC4)
  - Features list (Device Data Integration, Two-Way Communication, etc.)
- Gherkin Scenarios (BDD style):
  - 5 initial Gherkin scenarios written and validated
- UX Notes, Interface Requirements, and Behaviors clearly defined
- UML Diagrams:
  - Class, Component, Deployment, Package Diagrams (Structural)
  - Use Case, Sequence, State, Activity, Interaction Overview (Behavioral)

---

## 📖 Evolution 2: API Development (FastAPI)
- ✅ Completed and Done
- Built REST API with FastAPI
- Developed CRUD operations for Patient, Device, and Provider
- Designed ERD to model entity relationships
- Implemented entity validation using Pydantic
- Project folder organized with `schemas/`, `routers/`, `crud/`, and `models/`

---

## 📖 Evolution 3: Repository Pattern (FastAPI)
- ✅ Completed and Done
- Implemented Repository Pattern abstraction for:
  - SQLModel Repository
  - CSV Repository
  - In-Memory Repository
- Dynamic repository selection using environment variables
- Unit tests and API tests completed for each storage method
- Final project migrated to Django ORM, Repository Pattern kept conceptually

---

## 📖 Evolution 4: Migration to Django
- ✅ Completed and Done
- Full migration from FastAPI to Django REST Framework initially
- Adopted Django Ninja for lighter, faster APIs
- Maintained clean architecture:
  - Separate models, views, serializers, and repositories
- Implemented JWT Authentication initially (removed later per scope)
- Developed CRUD operations and relationship management
- Setup Docker, PostgreSQL, Celery, and Redis

---

## 📖 Evolution 5: Full Django + Tests
- ✅ Completed and Done
- Integrated Django Ninja for type-safe APIs
- Developed Dockerized deployment for Django, Celery, PostgreSQL, and Redis
- Implemented Event-Driven Architecture using Django signals + Celery Tasks
- Added full unit tests and integration tests (pytest, ninja TestClient)
- Documented DDD Glossary, BDD Gherkin Scenarios, and TDD mappings
- Final architecture production-ready and extensible

---

## 📕 Updated Architecture Overview

- **Framework:** Django 5.1 + Django Ninja
- **Asynchronous Tasks:** Celery + Redis
- **Database:** PostgreSQL (Dockerized)
- **Authentication:** Open APIs (JWT optional; omitted by scope)
- **Testing:** pytest, unittest
- **Deployment:** Docker Compose orchestration

---

## 📖 Domain-Driven Design (DDD) Ubiquitous Language Glossary

| Term | Definition |
|:-----|:-----------|
| Patient | A healthcare system user who owns health-related data and devices. |
| Provider | A healthcare professional managing one or more patients. |
| Device | A healthcare monitoring tool associated with a patient. |
| PatientProvider | Relationship entity linking Patients and Providers. |
| Repository | Abstraction layer for model persistence. |
| API Endpoint | URL routes for managing CRUD operations. |
| Ninja Router | Django Ninja modular route groupings. |
| Celery Task | Background job triggered asynchronously. |
| Redis Queue | Message broker for Celery. |
| Signal Handler | Django event listener (e.g., post_save). |
| Assignment Action | Linking a Provider or Device to a Patient. |
| Unassignment Action | Unlinking without deleting objects. |
| Docker Service | Containerized app environment. |
| Schema | API data validation models. |
| TestClient | Django Ninja testing tool. |
| Unit Test | Test specific functions or components. |
| Integration Test | Test full workflows across layers. |
| Admin Inline | Django Admin relationship management tool. |

---

## 📘 Gherkin BDD Scenarios

### Feature: Patient Management

**Scenario: Successfully Create a New Patient**
```gherkin
Given the user provides valid patient information
When the user submits a create patient request
Then the system should store the patient and return a success response
```

**Scenario: Update an Existing Patient's Information**
```gherkin
Given a patient already exists in the system
When the user updates the patient's details
Then the system should reflect the updated information
```

### Feature: Provider Management

**Scenario: Assign a Provider to a Patient**
```gherkin
Given both a patient and a provider exist
When the user assigns the provider to the patient
Then the system should link the provider to the patient without creating duplicates
```

**Scenario: List All Patients Under a Provider**
```gherkin
Given a provider has multiple patients assigned
When the user requests the list of patients for that provider
Then the system should return all linked patients
```

### Feature: Device Management

**Scenario: Assign a Device to a Patient**
```gherkin
Given a device exists and a patient exists
When the user assigns the device to the patient
Then the system should update the device to reference the correct patient
```

**Scenario: Unassign a Device from a Patient**
```gherkin
Given a device is currently assigned to a patient
When the user unassigns the device
Then the system should remove the patient reference but retain the device
```

### Feature: Event Notification

**Scenario: Trigger a Notification on New Patient Creation**
```gherkin
Given a new patient is successfully created
When the patient is saved in the database
Then the system should asynchronously trigger a notification task using Celery
```

---

## 🔢 TDD Mapping: Unit Tests Correspondence

| Gherkin Scenario | Unit Test File | Test Method |
|:-----------------|:--------------|:------------|
| Create Patient | test_patient.py | `test_create_patient` |
| Update Patient | test_patient.py | `test_update_patient` |
| Assign Provider | test_provider.py | `test_assign_provider` |
| List Patients for Provider | test_provider.py | `test_list_patients_for_provider` |
| Assign/Unassign Device | test_device.py | `test_assign_and_unassign_device` |
| Trigger Notification | test_api.py | `test_patient_creation_triggers_task` |

Each Gherkin BDD feature is backed by corresponding Django unittest methods in the `mainapp/tests/` directory.

---

## 🛠️ Running the System

1. **Clone the Repository:**
   ```bash
   git clone <REPO_URL>
   cd Assignment05
   ```

2. **Setup Virtual Environment & Install Dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Docker Setup:**
   ```bash
   docker-compose up -d
   ```

4. **Run Django Migrations:**
   ```bash
   docker-compose exec django_app python manage.py migrate
   ```

5. **Access Services:**
   - API: [http://localhost:8000/api/](http://localhost:8000/api/)
   - Admin Panel: [http://localhost:8000/admin/](http://localhost:8000/admin/)

6. **Run Tests:**
   ```bash
   pytest
   ```

---

## 📝 Notes

- APIs are open (no JWT enforced).
- No front-end UI (API-focused backend).
- Event-driven tasks demonstrated via Celery worker logs.
- Docker environment ensures portability and consistency.

---
## 📄 License
This project was developed as part of the CIDM-6330 Software Engineering course at West Texas A&M University.
The domain of Distributed Healthcare Communication was selected to demonstrate the application of software engineering principles to a real-world problem.
This project is intended solely for academic purposes

##  Acknowledgment
Special thanks to Professor Dr.Babb for guidance, instruction, and support throughout the course.

## 🌟 Conclusion

This project demonstrates a full-stack, real-world backend system using Django, Ninja, Celery, Docker, and PostgreSQL. It integrates all software engineering principles covered across Evolutions 0–5, meeting and exceeding final project expectations.

Ready for professional deployment or expansion.

---

> For full project files and documentation, refer to the repository: [GitHub Repository](https://github.com/Mafruha17/CIDM6330-Spring2025)

