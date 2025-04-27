## 📘 README.md — Assignment 05: Full Django + Tests

### **West Texas A&M University**

- **Semester:** Spring 2025
- **Course:** CIDM-6330-70 Software Engineering
- **Student:** Mafruha Chowdhury

---

### 🔗 GitHub Repository

**Repository Link:** [CIDM6330-Spring2025/Assignment05](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment05)

- [ERD Diagram](/docs/edr.PNG)
- [Class Diagram](/docs/Class%20Diagram.png)

---

## 📋 Table of Contents

1. [Overview & Objectives](#-overview--objectives)
2. [Tech Stack](#-tech-stack)
3. [Architecture & Patterns](#-architecture--patterns)
4. [Installation & Setup](#-installation--setup)
5. [Docker, Redis, Celery](#-docker-redis-celery)
6. [API Design](#-api-design)
7. [API Endpoints (Ninja Routers)](#-api-endpoints-ninja-routers)
8. [Event-Driven Processing](#-event-driven-processing)
9. [Testing](#-testing)
10. [Behavior-Driven Development (BDD) with Gherkin](#-behavior-driven-development-bdd-with-gherkin)
11. [Admin Panel Usage](#-admin-panel-usage)
12. [Troubleshooting](#-troubleshooting)
13. [Verification](#-verification)
14. [References](#-references)
15. [Conclusion](#-conclusion)
16. [Additional Code Files](#editional-code-files)

---

## 🩺 Overview & Objectives

This Django-based healthcare API application manages **Patients**, **Providers**, and **Devices** in a medical context. Initially developed in FastAPI (Assignment 03), it is now implemented in Django for Assignment 04 and enhanced in Assignment 05.

### ✅ Objectives

- Migrate FastAPI logic to Django with clean modular architecture
- Implement Django Ninja API for type-safe, modern endpoints
- Integrate Celery and Redis for asynchronous, event-driven task processing
- Use PostgreSQL as the database via Docker
- Apply the Repository Pattern with abstract class inheritance
- Validate the complete backend logic using `unittest` and `pytest`
- Deliver the complete system using containerization (Docker)
- Document all features with code-level clarity — no UI elements

---

## 🔌 Tech Stack

| Component         | Purpose                    |
| ----------------- | -------------------------- |
| `Django 5.1.7`    | Core framework             |
| `django-ninja`    | Modern API interface       |
| `celery + redis`  | Background task queue      |
| `PostgreSQL`      | Persistent DB (via Docker) |
| `pytest/unittest` | Testing & verification     |
| `Docker Compose`  | Deployment                 |

### 🧪 `requirements.txt`

```txt
asgiref==3.8.1
colorama==0.4.6
Django==5.1.7
django-ninja==1.1.0
iniconfig==2.1.0
packaging==24.2
pluggy==1.5.0
psycopg2-binary==2.9.10
pytest==8.3.5
pytest-django==4.10.0
sqlparse==0.5.3
tzdata==2025.1
celery==5.3.1
redis==4.5.5
email-validator==2.1.1
```

---

## 📂 Code Files

Below is a list of key files and their purposes. You may expand this section as your implementation grows:

| File / Directory        | Purpose                                                              |
| ----------------------- | -------------------------------------------------------------------- |
| [`mainapp/models.py`](/mainapp/models.py)     | Django ORM models: Patient, Device, Provider, PatientProvider        |
| [`mainapp/api/`](mainapp/api/)          | API logic using Django Ninja (patient\_api.py, device\_api.py, etc.) |
| [`mainapp/repositories/`](mainapp/repositories/) | Abstract and concrete repository classes                             |
| [`mainapp/tasks.py`](mainapp/tasks.py)      | Celery tasks                                                         |
| [`mainapp/signals.py`](mainapp/signals.py)    | Signal handlers triggering async jobs                                |
| [`mainapp/tests/`](/mainapp/tests/)           | Unit tests for all endpoints and services                            |
| [`djconfig/celery.py`](djconfig/celery.py)    | Celery configuration entrypoint                                      |
| [`docker-compose.yml`](docker-compose.yml)    | Container service configuration      
| [`docker-compose.yml`](docker-compose.yml)    | Container service configuration                                      |
| [`requirements.txt`](requirements.txt)      | Python package dependencies                                          |

---

## 🔀 API Endpoints (Ninja Routers)

The project uses `django-ninja` with modular routers defined per domain:

### 🔗 Mounted Routers
```python
# __init__.py
api.add_router("/patients/", patient_router, tags=["Patients"])
api.add_router("/providers/", provider_router, tags=["Providers"])
api.add_router("/devices/", device_router, tags=["Devices"])
```

### 🧪 Patient API
- `GET /patients/` — List all patients
- `GET /patients/{id}` — Retrieve patient
- `POST /patients/` — Create patient
- `PUT /patients/{id}` — Update patient
- `DELETE /patients/{id}` — Delete patient

### 🧪 Provider API
- `GET /providers/` — List all providers
- `GET /providers/{id}` — Retrieve provider
- `POST /providers/` — Create provider
- `PUT /providers/{id}` — Update provider
- `DELETE /providers/{id}` — Delete provider

### 🧪 Device API
- `GET /devices/` — List devices
- `GET /devices/{id}` — Retrieve device
- `POST /devices/` — Create device (with optional patient ID)
- `PUT /devices/{id}` — Update device
- `DELETE /devices/{id}` — Delete device
- `POST /devices/{id}/assign/` — Assign device to patient
- `POST /devices/{id}/unassign/` — Unassign device from patient

All endpoints follow RESTful conventions and are tested using `ninja.testing.TestClient`.

(Everything else continues below unchanged)



## 🧱 Architecture & Patterns

### ✔️ Core Models
- **Patient**: Has multiple devices and providers
- **Device**: Linked to a single patient
- **Provider**: Can have many patients
- **PatientProvider**: Join table for many-to-many

### 🧹 Design Patterns
- **Repository Pattern**:
  - `AbstractRepository` (abstract base class)
  - `PatientRepository`, `DeviceRepository`, `ProviderRepository` (implementations)
- **Separation of Concerns**:
  - Models, Schemas, Repositories, Tasks, API Routes, Tests are modularized
- **Signal-based Eventing**:
  - Uses `post_save` + Celery to handle async workflows

---

## ⚙️ Installation & Setup

```bash
# Clone the project
git clone <REPO_URL>
cd Assignment05

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

---

## 🐳 Docker, Redis, Celery

### Docker Commands

```bash
# Build containers
docker-compose build

# Start containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

### Sample `docker-compose.yml` Services
- `postgres_db` (PostgreSQL)
- `redis_broker`
- `django_app`
- `celery_worker`

---

## ⚡ API Design

### Framework: **Django Ninja**

```python
from ninja import NinjaAPI, Schema

api = NinjaAPI()

class PatientSchema(Schema):
    name: str
    age: int

@api.post("/patients/")
def create_patient(request, data: PatientSchema):
    ...
```
---
🔐 Note on Authentication
Although JWT (JSON Web Token) authentication was briefly explored during development, it has been removed from the project as it was not part of the original assignment requirements. All API endpoints are accessible without authentication to align strictly with the provided specifications and evaluation criteria.


### Route Examples

| Method | URL | Action |
|--------|-----|--------|
| `POST` | `/patients/` | Create new patient |
| `GET` | `/patients/{id}/` | Retrieve patient |
| `PUT` | `/patients/{id}/assign_provider/` | Assign provider |
| `DELETE` | `/patients/{id}/remove_device/` | Unassign device |

> Accessible at: `http://localhost:8000/api/`

---

## 📡 Event-Driven Processing

### Trigger Flow
1. API creates a new patient
2. Django ORM saves it
3. `post_save` signal fires
4. Signal invokes Celery task via `.delay()`
5. Task is queued in Redis
6. Celery Worker picks it up

```python
# signals.py
@receiver(post_save, sender=Patient)
def patient_created(sender, instance, created, **kwargs):
    if created:
        notify_new_patient_created.delay(instance.name)

# tasks.py
@shared_task
def notify_new_patient_created(name):
    print(f"New patient created: {name}")
```

---

## 🧪 Testing

---

## 🧪 Behavior-Driven Development (BDD) with Gherkin

In addition to unit testing with `pytest` and Django's `unittest`, key system behaviors were modeled using Behavior-Driven Development (BDD) practices.  
Gherkin syntax was used to define expected user interactions with the system, ensuring that API behaviors align with business requirements.

### 📋 Sample Gherkin Scenario — Patient Creation
```gherkin
Feature: Patient Management

Scenario: Successfully Create a New Patient
  Given the user provides valid patient information
  When the user submits a create patient request
  Then the system should store the patient and return a success response


### Setup
```bash
pip install pytest pytest-django
```

### Configure `pytest.ini`
```ini
[pytest]
DJANGO_SETTINGS_MODULE = djconfig.settings
python_files = tests.py test_*.py *_tests.py
```

### Run All Tests
```bash
pytest
```

### Sample Ninja API Test
```python
from ninja.testing import TestClient
from mainapp.api import api

client = TestClient(api)

def test_create_patient():
    payload = {"name": "Alice", "age": 32}
    response = client.post("/patients/", json=payload)
    assert response.status_code == 201
```

> Tests cover repository CRUD, assignments, and API endpoint responses.

---

## 🧑‍💼 Admin Panel Usage

```bash
# Create superuser
python manage.py createsuperuser
```

Visit: `http://localhost:8000/admin/`

### Assign/Unassign Logic
- Providers can be assigned to patients using **PatientProviderInline**
- Devices assigned through the `DeviceInline` on the Patient admin
- Unassigning does **not delete** entities

---



## 🛠️ Troubleshooting

| Issue | Fix |
|-------|-----|
| Docker fails | Restart Docker Desktop |
| DB connection error | Ensure Postgres container is running |
| Signal not firing | Ensure Celery Worker is active |
| Redis error | `docker-compose ps` to verify container |

---

## ✅ Verification

1. Confirm containers with `docker-compose ps`
2. Access:
   - API: `http://localhost:8000/api/`
   - Admin: `http://localhost:8000/admin/`
3. Create a new patient and check Celery logs:
   ```bash
   docker-compose logs celery_worker
   ```

---

## 📙 References

- [Django Ninja Docs](https://django-ninja.dev/)
- [Celery Docs](https://docs.celeryq.dev/)
- [Docker Docs](https://docs.docker.com/)
- [Pytest Docs](https://docs.pytest.org/)
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)

---

## 🌟 Conclusion

This project illustrates a robust and scalable Django-based system integrating:
- Clean API design (Django Ninja)
- Message-driven architecture (Celery + Redis)
- PostgreSQL persistence
- Modular code structure with the **Repository Pattern**
- Fully tested backend with zero UI

Ready for real-world expansion into additional modules like billing, appointments, or remote monitoring.


## Editional Code files 

## 📁 Full Project Structure with Direct GitHub Links

Assignment05/  
├── [core/](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment05/core)  
│   ├── [admin.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/core/admin.py)  
│   ├── [apps.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/core/apps.py)  
│   ├── [admin.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/core/admin.py)  
│  
├── [djconfig/](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment05/djconfig)  
│   ├── [__init__.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/djconfig/__init__.py)  
│   ├── [settings.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/djconfig/settings.py) — *Django settings*  
│   ├── [urls.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/djconfig/urls.py) — *URL routing*  
│   └── [celery.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/djconfig/celery.py) — *Celery configuration*  
│  
├── [mainapp/](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment05/mainapp)  
│   ├── [__init__.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/mainapp/__init__.py)  
│   ├── [models.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/mainapp/models.py) — *Django ORM models*  
│   ├── [tasks.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/mainapp/tasks.py) — *Celery tasks*  
│   ├── [signals.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/mainapp/signals.py) — *Django signals*  
│   ├── [repositories/](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment05/mainapp/repositories)  
│   │   ├── [base.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/mainapp/repositories/base.py) — *AbstractRepository*  
│   │   ├── [patient_repository.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/mainapp/repositories/patient_repository.py)  
│   │   ├── [provider_repository.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/mainapp/repositories/provider_repository.py)  
│   │   └── [device_repository.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/mainapp/repositories/device_repository.py)  
│   ├── [schemas/](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment05/mainapp/schemas)  
│   │   ├── [patient_schema.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/mainapp/schemas/patient_schema.py)  
│   │   ├── [provider_schema.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/mainapp/schemas/provider_schema.py)  
│   │   └── [device_schema.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/mainapp/schemas/device_schema.py)  
│   ├── [api/](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment05/mainapp/api)  
│   │   ├── [__init__.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/mainapp/api/__init__.py) — *Registers routers*  
│   │   ├── [api_patient.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/mainapp/api/api_patient.py) — *Patient endpoints*  
│   │   ├── [api_provider.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/mainapp/api/api_provider.py) — *Provider endpoints*  
│   │   └── [api_device.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/mainapp/api/api_device.py) — *Device endpoints*  
│   ├── [tests/](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment05/mainapp/tests)  
│   │   ├── [__init__.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/mainapp/tests/__init__.py)  
│   │   ├── [test_api.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/mainapp/tests/test_api.py) — *API test (Django/Ninja)*  
│   │   ├── [test_patient.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/mainapp/tests/test_patient.py) — *Patient test (Django/Ninja)*  
│   │   ├── [test_provider.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/mainapp/tests/test_provider.py) — *Provider test (Django/Ninja)*  
│   │   └── [test_device.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/mainapp/tests/test_device.py) — *Device test (Django/Ninja)*  
│  
├── [docker-compose.yml](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/docker-compose.yml) — *Container configuration*  
├── [requirements.txt](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/requirements.txt) — *Dependencies*  
├── [README.md](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/README.md) — *Project documentation*  
└── [manage.py](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/manage.py) — *Django management script*  




## Editional Code files 



Navigate the full project on GitHub: [📂 View Project Files](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment05)

---


