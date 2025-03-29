
# 🩺 HealthCare Management API (Assignment 04)

## 📌 Overview

This is a Django REST Framework (DRF)-based API designed to manage patients, devices, and providers in a healthcare system. The project was migrated from a FastAPI-based architecture (Assignment 03) and continues to follow a clean, modular, and scalable structure. It includes JWT authentication, CRUD operations, and a repository pattern for abstraction and testability.

---

## 🚀 Features

- 🔐 JWT Authentication using Simple JWT (access & refresh tokens)
- 📁 Modular architecture inspired by the FastAPI project
- 🔄 Full CRUD support for:
  - Patients
  - Devices
  - Providers
- 📎 Relationship management:
  - A **patient** can have multiple **devices**
  - A **provider** can have multiple **patients**
  - A **patient** can have multiple **providers**
- 🧠 Repository pattern for decoupled data logic
- 🧪 Pytest support for test automation (no reliance on Django shell)
- 🗃️ SQLite/PostgreSQL support

---


## 📚 Table of Contents

- [📌 Overview](#-overview)
- [🚀 Features](#-features)
- [🏗️ Project Structure](#️-project-structure)
- [📂 Code File Overview](#-code-file-overview)
- [⚙️ Installation](#️-installation)
- [🧱 Setup & Configuration](#️-setup--configuration)
- [🔐 JWT Authentication](#-jwt-authentication)
- [📬 API Endpoints (Sample)](#-api-endpoints-sample)
- [🧪 Running Tests](#-running-tests)
- [📎 Notes](#-notes)
- [📚 References](#-references)
- [🏷️ Badges (Optional)](#-badges-optional)
- [✅ Status](#-status)

---

## 🏗️ Project Structure

```
Assignment04/
├── config/                   
│   └── settings.py
│
├── core/
│   ├── database/
│   │   ├── models/           # Django ORM models
│   │   └── connection.py     # Database connection setup (if needed)
│   │
│   ├── repositories/         # Custom repository classes
│   │   ├── patient_repository.py
│   │   ├── provider_repository.py
│   │   └── device_repository.py
│   │
│   ├── routers/              # DRF API views and endpoints
│   │   ├── patient_views.py
│   │   ├── provider_views.py
│   │   └── device_views.py
│   │
│   ├── schemas/              # DRF Serializers
│   │   ├── patient_serializer.py
│   │   ├── provider_serializer.py
│   │   └── device_serializer.py
│   │
│   ├── tests/                # Pytest-based unit tests
│   │   ├── test_patient_repository.py
│   │   ├── test_provider_repository.py
│   │   └── test_device_repository.py
│
├── docs/                     # ERD, design documentation
├── manage.py
├── requirements.txt
└── README.md
```

---

## 📂 Code File Overview

| File / Folder                      | Purpose |
|-----------------------------------|---------|
| `core/database/models/`           | Contains Django ORM models for `Patient`, `Device`, and `Provider`. Defines fields and relationships like `ForeignKey` and `ManyToManyField`. |
| `core/repositories/`              | Repository Pattern implementations. Each repository file encapsulates business logic for querying, creating, updating, and deleting entities. |
| `core/schemas/`                   | DRF serializers used to validate input data and serialize/deserialize model instances. |
| `core/routers/`                   | DRF API views handle business logic, map HTTP methods to repository functions, and enforce permissions. |
| `core/tests/`                     | Pytest unit tests to validate the correctness of each repository class. Helps ensure code works without using Django shell. |
| `core/urls.py`                    | Main router that includes app-level view routes and authentication endpoints. |
| `config/settings.py`              | Project settings including installed apps, REST framework, database settings, and JWT configuration. |
| `config/urls.py`                  | Root URL configuration that includes `core.urls` and admin routes. |
| `manage.py`                       | Django's CLI for managing the project. Use to run migrations, launch server, and create superusers. |

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/your-username/Assignment04.git
cd Assignment04

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🧱 Setup & Configuration

1. **Database**
   - Default: SQLite (pre-configured)
   - PostgreSQL: Update `DATABASES` in `config/settings.py`

2. **Migrate the database**

```bash
python manage.py makemigrations
python manage.py migrate
```

3. **Create a superuser (optional)**

```bash
python manage.py createsuperuser
```

4. **Run the development server**

```bash
python manage.py runserver
```

---

## 🔐 JWT Authentication

This API uses [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) for authentication.

- **Get Token**
  ```http
  POST /api/token/
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```

- **Refresh Token**
  ```http
  POST /api/token/refresh/
  {
    "refresh": "<your_refresh_token>"
  }
  ```

- **Authorization Header**
  ```
  Authorization: Bearer <access_token>
  ```

---

## 📬 API Endpoints (Sample)

| Method | Endpoint                           | Description                         |
|--------|------------------------------------|-------------------------------------|
| POST   | `/patients/`                       | Create a new patient                |
| GET    | `/patients/{id}/`                  | Retrieve a patient                  |
| PUT    | `/patients/{id}/assign_provider/`  | Assign a provider to a patient      |
| DELETE | `/patients/{id}/remove_device/`    | Remove a device from a patient      |
| POST   | `/devices/`                        | Create a new device                 |
| POST   | `/providers/`                      | Create a new provider               |
| GET    | `/providers/{id}/patients/`        | List all patients for a provider    |

> Full endpoint list is available in `core/urls.py` or through Django DRF’s browsable API.

---

## 🧪 Running Tests

Ensure your virtual environment is active and run:

```bash
pytest
```

- All test files are located in `core/tests/`
- Test coverage includes repositories and database logic

---

## 📎 Notes

- Ensure each module has `__init__.py` files to avoid import issues
- DRF Browsable API is enabled for ease of testing
- Django Admin is accessible at `/admin/`
- API protected using JWT tokens
- Use Postman or Curl for testing authentication and API routes

---

## 📚 References

- Django REST Framework: https://www.django-rest-framework.org/
- Simple JWT: https://django-rest-framework-simplejwt.readthedocs.io/
- Pytest: https://docs.pytest.org/en/stable/
- PostgreSQL: https://www.postgresql.org/
- FastAPI (Reference from Assignment 03)

---

## 🏷️ Badges (Optional)

You can add these later:

- ![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
- ![DRF](https://img.shields.io/badge/Django%20REST-Framework-green)
- ![JWT](https://img.shields.io/badge/Auth-JWT-lightgrey)
- ![License](https://img.shields.io/badge/license-MIT-blue)

---

## ✅ Status

> Project is under active development as part of **Assignment 04**.  
> Core features and authentication are implemented. Testing and endpoint expansion in progress.

