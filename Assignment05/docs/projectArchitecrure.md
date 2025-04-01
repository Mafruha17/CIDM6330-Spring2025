# 🏗️ Project Architecture: Django Healthcare Management API

This document provides a detailed layout and explanation of the **project architecture** and how various modules and layers communicate in the Healthcare Management API built with Django and Django REST Framework (DRF). It covers how the `dgconfig`, `core` app (main app), `repositories`, `models`, `views`, `database`, and `config` files work together—from request to CRUD processing.

---

## 📦 Project Layout

```
Assignment04/
├── config/                # Django project-level configuration
│   ├── __init__.py
│   ├── settings.py        # Global settings, JWT, DB setup, apps
│   ├── urls.py            # Root URL router
│   └── wsgi.py/asgi.py    # Deployment interface
│
├── core/                 # Main app for API business logic
│   ├── database/
│   │   ├── models/        # ORM model definitions
│   │   └── connection.py  # Optional manual DB setup
│   │
│   ├── repositories/      # Repository pattern layer
│   ├── routers/           # DRF views and route handling
│   ├── schemas/           # DRF serializers (schema validation)
│   ├── tests/             # Pytest-based testing
│   └── urls.py            # App-specific URL routes
│
├── docs/                 # ERD, diagrams, external documentation
├── manage.py             # Django CLI interface
└── requirements.txt      # Dependencies
```

---

## 🔁 Request Flow (End-to-End)

```
Client → Router (URL) → View → Repository → Model → DB → Response
```

### 🔹 1. Client Request
- A client (Postman, frontend, etc.) makes a request to an API endpoint (e.g., `POST /patients/`).

### 🔹 2. URL Routing
- `config/urls.py` includes app routes from `core/urls.py`.
- `core/urls.py` maps URL paths to their respective views.

### 🔹 3. View Layer (Routers)
- Located in `core/routers/`, each view handles:
  - Authentication/authorization via DRF permissions (`IsAuthenticated` for JWT)
  - Input parsing and validation using serializers
  - Delegating DB logic to repositories

### 🔹 4. Serializers (Schemas)
- `core/schemas/` contains serializers (like `PatientSerializer`) that:
  - Validate incoming request data
  - Convert ORM objects to JSON (response)

### 🔹 5. Repository Layer
- `core/repositories/` contains decoupled data access logic.
- Each repository (e.g., `patient_repository.py`) provides functions to:
  - Create, read, update, delete database records
  - Abstract away direct ORM usage from views

### 🔹 6. Models & ORM
- Defined in `core/database/models/`.
- Models represent tables in the database with Django ORM.
- Relationships like `ForeignKey`, `ManyToManyField` manage links between Patient, Device, Provider.

### 🔹 7. Database
- SQLite or PostgreSQL, based on settings in `config/settings.py`.
- Tables created through migrations.

### 🔹 8. Response
- Once a record is created/queried/updated, the view returns a response using serializers to format it as JSON.

---

## ⚙️ How Modules Work Together

| Layer           | Location                     | Role |
|----------------|------------------------------|------|
| Config         | `config/settings.py`         | Global setup for DB, REST, JWT, apps |
| Main Router    | `config/urls.py`             | Routes root URLs to app views |
| App Router     | `core/urls.py`               | Maps endpoints to views |
| View Layer     | `core/routers/*.py`          | Authenticates, validates, delegates |
| Serializers    | `core/schemas/*.py`          | Input validation and output formatting |
| Repositories   | `core/repositories/*.py`     | Encapsulates ORM access |
| Models         | `core/database/models/*.py`  | Defines data tables and relationships |
| Database       | SQLite/PostgreSQL            | Persistent storage |

---

## 🔐 Authentication Layer
- Configured in `settings.py` using Simple JWT.
- Endpoints `/api/token/` and `/api/token/refresh/` handle login and renewal.
- Protected routes use `IsAuthenticated` to enforce token access.

---

## 🧪 Testing Layer
- All test files are in `core/tests/`.
- Uses Pytest instead of Django’s test runner.
- Tests repository logic and view endpoints (token-based auth).

---

## 🧠 Summary: CRUD Lifecycle (A to Z)

### Example: `POST /patients/`
1. Request hits `core/urls.py` → `patient_views.py`.
2. View uses `PatientSerializer` to validate input.
3. On success, view calls `create_patient()` from `patient_repository.py`.
4. Repository saves patient using ORM (`Patient.objects.create(...)`).
5. New instance returned → serialized → response sent back to client.

This same flow applies to Devices, Providers, and relationship management (assign/remove).

---

## ✅ Designed For
- Maintainability: Separation of concerns
- Flexibility: Easily extendable with new models and services
- Testability: Pytest-friendly repositories
- Security: JWT-protected routes
- Scalability: Modular, layered architecture
