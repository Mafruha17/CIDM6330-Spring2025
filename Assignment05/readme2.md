# Assignment 06: Migrate API from  Django to Event driven Architecture and container  (with Repository Pattern)

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
- [Code Files & Explanation](#code-files--explanation)
- [API Endpoints](#api-endpoints)
- [Using the Django Admin](#using-the-django-admin)
- [Testing](#testing)
- [Future Improvements](#future-improvements)
- [Conclusion](#conclusion)

---

## 🪹 Overview

This is a Django REST Framework (DRF)-based API designed to manage patients, devices, and providers in a healthcare system. The project was migrated from a FastAPI-based architecture (Assignment 03) and continues to follow a clean, modular, and scalable structure. It includes JWT authentication, CRUD operations, and a repository pattern for abstraction and testability, preserving a clean, layered architecture:

Project uses:

- Django 5.1+
- Django REST Framework
- PostgreSQL
- Repository Pattern
- JWT Authentication (Simple JWT)
- Docker & Docker Compose
- Celery & Redis for asynchronous tasks

---

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
- **ModelViewSet** or custom `ViewSet` for CRUD APIs
- **One-to-Many** relationship: **Patients** ↔ **Devices**
- **Many-to-Many** relationship: **Patients** ↔ **Providers**
- **Assignment/Unassignment** logic via custom actions and Django Admin inlines
- 🧠 Repository pattern for decoupled data logic
- 🧚 Pytest support for test automation (no reliance on Django shell)

---

## **Docker, Celery, and Redis Setup**

### Dockerfile

```Dockerfile
FROM python:3.10-slim

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

Start everything:

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

## 📦 Access API

- Run the app:

```bash
docker-compose up --build
```

- Access API at: [http://localhost:8000/api/](http://localhost:8000/api/)
- Access Admin at: [http://localhost:8000/admin/](http://localhost:8000/admin/)


