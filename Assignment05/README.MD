# Assignment 5: Full Django + Tests

## **West Texas A&M University**
- **Semester:** Spring 2025  
- **Course:** CIDM-6330-70 Software Engineering  
- **Student:** 

---

**Git repo link:** [CIDM6330-Spring2025/Assignment04](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment04)

- [ERD for assignment04](/docs/edr.PNG)
- [Class Diagram](/docs/Class%20Diagram.png)
- [Code Files & Explanation](#code-files--explanation)

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Objectives](#objectives)
- [Project Folder Directory](#project-folder-directory)
- [Installation & Setup](#installation--setup)
- [Docker, Celery, and Redis Setup](#docker-celery-and-redis-setup)
- [Django Ninja API Setup](#django-ninja-api-setup)
- [Code Files & Explanation](#code-files--explanation)
- [API Endpoints](#api-endpoints)
- [Using the Django Admin](#using-the-django-admin)
- [Testing](#testing)
- [Future Improvements](#future-improvements)
- [Conclusion](#conclusion)

---

## 🪹 Overview
This is a Django-based API designed to manage patients, devices, and providers in a healthcare system. The project was migrated from a FastAPI-based architecture (Assignment 03) and continues to follow a clean, modular, and scalable structure. Assignment 05 focuses on integrating:

- Django Ninja for modern, type-safe API development
- Celery/Redis for message queuing (MQ)
- Django’s built-in `unittest` framework for testing

### ✅ Installed and Ready

| Library                           | Status       | Purpose                                |
|-----------------------------------|--------------|----------------------------------------|
| `django 5.1.7`                    | ✅           | Core framework                         |
| `django-ninja 1.4.0`              | ✅           | Ninja API routing                      |
| `pydantic 2.11.1`                 | ✅           | Schema validation                      |
| `celery 5.3.1`                    | ✅           | Async task queue                       |
| `redis 4.5.5`                     | ✅           | Message broker backend                 |
| `psycopg2-binary 2.9.10`          | ✅           | PostgreSQL driver                      |
| `pytest`, `pytest-django`         | ✅           | Unit testing framework                 |
| `djangorestframework`             | ✅           | Optional (OK to keep for admin/debug)  |
| `djangorestframework-simplejwt`   | ✅ (but unused) | Can be uninstalled for now          |


------
- 🔐 JWT Authentication using Simple JWT (access & refresh tokens)
- 📁 Modular architecture inspired by the FastAPI project
- 🔄 Full CRUD support for:
  - Patients
  - Devices
  - Providers
- 📌 Relationship management:
  - A **patient** can have multiple **devices**
  - A **provider** can have multiple **patients**
  - A **patient** can have multiple **providers**
- **Django Ninja** routes for modern API handling
- **One-to-Many** relationship: **Patients** ↔ **Devices**  
- **Many-to-Many** relationship: **Patients** ↔ **Providers**  
- **Assignment/Unassignment** logic via custom actions and Django Admin inlines 
- 🧠 Repository pattern for decoupled data logic
- 🔢 Unittest framework used for testing

---

## 🚀 Django Ninja API Setup

### Installation
```bash
pip install django-ninja
```
Add to `requirements.txt`:
```text
django-ninja>=0.22.2
```

### Register the API
In `mainapp/api/api_patient.py | api_device.py | api_patient.py`:
```python
from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/patient")
def ping(request):
    return {"message": "outputpataient "}
```
__
### 🌟 Benefits

| Advantage         | Why it matters                                          |
|-------------------|---------------------------------------------------------|
| ✅ Clean separation | Easier to maintain, debug, and extend per entity        |
| ✅ Scalable         | Add more APIs (e.g., billing, appointments) without clutter |
| ✅ Readable         | Logical flow for reviewing and testing specific logic  |
__

In `djconfig/urls.py`:
```python
from django.contrib import admin
from django.urls import path
from mainapp.api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

Now, the API is accessible at `http://localhost:8000/api/ping`.

Use `Schema` classes for request/response typing:
---
### 🔁 Recap of Schema Naming Convention

| Purpose        | Class Name |
|----------------|------------|
| Input (POST)   | `XxxIn`    |
| Output (GET)   | `XxxOut`   |
| Shared Fields  | Inherited from `XxxIn` |

This setup improves:

- ✅ **Clarity** between request and response types  
- ✅ **Validation** for incoming data  
- ✅ **Control** over exposed fields  
---

```python
from ninja import Schema

class PatientSchema(Schema):
    name: str
    age: int
    email: str

@api.post("/patients/")
def create_patient(request, data: PatientSchema):
    # Save to DB...
    return {"message": "Patient created"}
```

---

(Sections such as Docker, Celery, Redis setup and remaining content follow here as previously structured.)


-----
## **Docker, Celery, and Redis Setup**

### 📌 1. Install Prerequisites

Ensure the following are installed on your system:

- [Python 3.10+](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Docker Compose](https://docs.docker.com/compose/install/)

To verify:
```bash
python --version
docker --version
docker-compose --version


WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
```

### docker-compose.yml

```yaml
version: '3.9'

services:
  postgres_db:
    image: postgres:15
    environment:
      POSTGRES_DB: assignment04
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: your_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis_broker:
    image: redis:7
    ports:
      - "6379:6379"

  django_app:
    build: .
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - postgres_db
      - redis_broker
    command: sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"

  celery_worker:
    build: .
    command: celery -A djconfig worker --loglevel=info
    depends_on:
      - django_app
      - redis_broker

volumes:
  postgres_data:
```

### Celery Configuration

In `djconfig/celery.py`:

```python
from celery import Celery

app = Celery("djconfig")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.broker_connection_retry_on_startup = True
```

In `djconfig/__init__.py`:

```python
from .celery import app as celery_app

__all__ = ("celery_app",)
```

In `settings.py`:

```python
CELERY_BROKER_URL = "redis://redis_broker:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
```

Start everything:n


```bash
docker-compose up --build
```

Run migrations:

```bash
docker-compose exec django_app python manage.py migrate
```

---

## ✅ Sample Celery Task

In `mainapp/tasks.py`:

```python
from celery import shared_task

@shared_task
def notify_new_patient_created(name):
    print(f"New patient created: {name}")
```

In `signals.py` (if you use signals):

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Patient
from mainapp.tasks import notify_new_patient_created

@receiver(post_save, sender=Patient)
def patient_created(sender, instance, created, **kwargs):
    if created:
        notify_new_patient_created.delay(instance.name)
```

---
## Troubleshooting some issues 

### Database Container Not Actually Running

Ensure that your Postgres container is up and running before Django attempts to connect:

- Run the command below to verify the container status:
  ```bash
  docker compose ps
  ```
- Check that the service named `db` (or the equivalent defined in your `docker-compose.yml`) is in the **Up** state.
- If your compose file doesn’t define a `db` service, Django won’t be able to connect to `db:5432`. Make sure to add a Postgres service to your Docker Compose configuration.



## 📦 Access API

- Run the app:
---

## **Installation & Setup**
Follow setup instructions provided in [Installation & Setup](#installation--setup) section.

---

1. **Clone the Repository**
   ```bash
   git clone <REPO_URL>
   cd Assignment04
   ```

2. **Create & Activate a Virtual Environment**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Make sure `django`, `djangorestframework`, `pytest`, `pytest-django`, and `psycopg2` are included.

4. **Configure Database**  
   Edit `djconfig/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'assignment04',
           'USER': 'postgres',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a Superuser** (for Admin)
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Server**
   ```bash
   python manage.py runserver
   ```
   Access the API at [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/) and Admin at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

---

---

## 🔐 JWT Authentication

This API uses [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) for authentication.

Use Simple JWT endpoints (`/api/token/` and `/api/token/refresh/`) for authentication. See JWT Authentication above.

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
## **Code Files & Explanation**

1. **[`models.py`](/mainapp/models.py)**  : Defines data models.
   - Defines **Patient**, **Provider**, **Device**, and **PatientProvider** models.  
   - **PatientProvider** is a join model for many-to-many (patients ↔ providers).  
   - **Device** uses a `ForeignKey` to `Patient`, representing one-to-many.

2. **[`serializers.py`](mainapp/serializers.py)**  :Input/output validation.
   - Houses this project **DRF serializers** (e.g., `PatientSerializer`, `ProviderSerializer`, `DeviceSerializer`).  
   - These manage input/output validation and handle nested relationships if needed.

3. **[`repositories/`](mainapp/repositories)** : Data abstraction.
   - **`base_repository.py`**: Abstract base class using `abc` for CRUD methods.  
   - **`patient_repository.py`, `provider_repository.py`, `device_repository.py`**: Concrete repository classes that inherit from `BaseRepository`.

4. **[`views/`](mainapp/views)**: API endpoints.
   - **`patient_views.py`, `device_views.py`, `provider_views.py`**: Defined Django REST Framework ViewSets (either `ModelViewSet` or `ViewSet`) for CRUD and custom assignment actions.

5. **[`admin.py`](mainapp/admin.py)**  Django Admin configurations.

   - Registers models in the Django admin site.  
   - Adds **inlines** for `PatientProvider` (to manage providers for patients) and `Device` (to manage devices assigned to a patient).

6. **[`urls.py`](djconfig/urls.py)**  
   - Root URL configuration, includes `mainapp.urls` under `/api/`.  

7. **[`urls.py`](mainapp/urls.py)**  
   - Uses `DefaultRouter()` to register routes for `PatientViewSet`, `ProviderViewSet`, and `DeviceViewSet`.  

8. **`Test`**  
   - **[`tests`](test_patient.py)**, **[`test_device.py`](test_device.py)**, **[`test_provider.py`](test_provider.py)**: Pytest test files verifying CRUD, assignment endpoints, and repository logic.

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

## **Using the Django Admin**

1. **Go to** `/admin/` and log in with your superuser account.
2. **Manage Patients**:  
   - **Provider** assignment is shown via `PatientProviderInline`. Add or remove rows to assign/unassign providers.  
   - **Device** assignment is shown via `DeviceInline`. You can create new devices or set an existing device’s `patient` to `None` to unassign.
3. **Manage Providers**:  
   - Optionally add a `PatientProviderInline` in `ProviderAdmin` if you want to manage patient assignments from the provider side as well.
4. **No Deletion** of the main objects by unassigning:  
   - Removing a row in `PatientProviderInline` only deletes the **join record**, not the `Provider` or `Patient`.
   - Changing the `Device`’s `patient` field to `None` unassigns the device without deleting it.

**Note**: For existing devices with unique `serial_number`, do not create a new row with the same serial number (that triggers a uniqueness error). Instead, edit the existing device and reassign the `patient`.

---

## 🧪 Testing


1. **Install** `pytest` and `pytest-django`:  
   ```bash
   pip install pytest pytest-django
   ```
2. **Create** `pytest.ini` in the project root:
   ```ini
   [pytest]
   DJANGO_SETTINGS_MODULE = djconfig.settings
   python_files = tests.py test_*.py *_tests.py
   ```
3. **Run** all tests:
   ```bash
   pytest
   ```
4. **Run** a single file:
   ```bash
   pytest mainapp/tests/test_provider.py
   ```
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
- API protected using JWT tokens | Secure API endpoints
- Use Postman or Curl for testing authentication and API routes
 

---
Below is an example section you can add to your README.md to verify your configuration and results:

---

## Verification and Results

After you’ve built and started your Docker services, follow these steps to confirm that everything is working as expected:

### 1. Check Container Status

Ensure that all your containers are up and running by executing:
```bash
docker compose ps
```
You should see entries for your Django app (e.g., `web` or `django_app`), Postgres (e.g., `db` or `postgres_db`), Redis (e.g., `redis_broker`), and Celery Worker (e.g., `celery_worker`) with the **State** set to "Up".

### 2. Verify Django API and Migrations

- **Check Logs:**  
  Review the Django service logs to ensure migrations have been applied and there are no startup errors:
  ```bash
  docker compose logs web
  ```
  (Use your actual service name if different, e.g., `django_app`.)

- **Access the API:**  
  Open your browser and navigate to:
  - **API Endpoints:** [http://localhost:8000](http://localhost:8000)
  - **Django Admin:** [http://localhost:8000/admin/](http://localhost:8000/admin/)  
  Log in with your superuser credentials to verify admin functionality.

### 3. Verify Celery Worker

Check that your Celery worker has connected to Redis and is ready to process tasks:
```bash
docker compose logs celery_worker
```
Look for log entries indicating a successful connection (e.g., “Connected to redis://redis:6379/0”) and readiness to process tasks.

### 4. Verify Postgres

Make sure your Postgres container is functioning correctly:
```bash
docker compose logs db
```
Confirm that there are no error messages and that the database is running normally.

### 5. Test a Celery Task (Optional)

If you have configured a Celery task (such as sending a notification when a new patient is created):
- **Trigger the Task:**  
  Create a new patient via the API or Django Admin.
- **Check Celery Logs:**  
  Run:
  ```bash
  docker compose logs celery_worker
  ```
  You should see a log entry indicating that the task (e.g., `notify_new_patient_created`) was received and is being processed.

---

By following these steps, you can verify that your Dockerized environment—comprising Django, Postgres, Redis, and Celery—is properly configured and operational. If any issues arise, refer to the logs as described above for troubleshooting.

___

## 📚 References

- [Django REST Framework](https://www.django-rest-framework.org/)
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Pytest](https://docs.pytest.org/en/stable/)
- [PostgreSQL](https://www.postgresql.org/)


---




## **Conclusion**
This Django project exemplifies a thorough migration from FastAPI to Django REST Framework while preserving **clean architecture** and **repository-driven** data access. Admin inlines make it easier to assign/unassign relationships without deleting objects, and robust tests ensure API reliability. It’s a strong foundation for further enhancements and real-world deployment.

