# Assignment 5: Full Django + Tests

## **West Texas A&M University**

- **Semester:** Spring 2025
- **Course:** CIDM-6330-70 Software Engineering
- **Student:**

---

**Git repo link:** [CIDM6330-Spring2025/Assignment04](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment04)

- [ERD for assignment04](/docs/edr.PNG)
- [Class Diagram](/docs/Class%20Diagram.png)

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Objectives](#objectives)
- [Project Folder Directory](#project-folder-directory)
- [Installation & Setup](#installation--setup)
- [Docker, Redis, and Celery Configuration](#docker-redis-and-celery-configuration)
- [Django Ninja API Setup](#django-ninja-api-setup)
- [Event-Driven Architecture](#event-driven-architecture)
- [Code Files & Explanation](#code-files--explanation)
- [API Endpoints](#api-endpoints)
- [Using the Django Admin](#using-the-django-admin)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Verification and Results](#verification-and-results)
- [References](#references)
- [Conclusion](#conclusion)

---

## 🩹 Overview

This is a Django-based API designed to manage patients, devices, and providers in a healthcare system. The project was migrated from a FastAPI-based architecture and continues to follow a clean, modular, and scalable structure.

### ✅ Features

- Django Ninja for modern API development
- Celery/Redis for background task processing
- PostgreSQL with Docker Compose integration
- Clean repository-style structure
- Unit tests with Pytest
- Admin UI with inlines for relationship assignment

### 🔌 Tech Stack

| Component                  | Purpose                        |
| -------------------------- | ------------------------------ |
| `django`, `django-ninja`   | Core web framework and routing |
| `celery`, `redis`          | Background tasks (MQ)          |
| `pytest`, `pytest-django`  | Testing                        |
| `docker`, `docker-compose` | Containerization               |

---

## 🚀 Django Ninja API Setup

### Installation

```bash
pip install django-ninja
```

Register the API:

```python
from ninja import NinjaAPI
api = NinjaAPI()
```

Then add routes and include them in `urls.py`:

```python
from mainapp.api import api
urlpatterns = [
    path("api/", api.urls),
]
```

---

## 📁 Installation & Setup

1. Clone and navigate to the project directory:

```bash
git clone <REPO_URL>
cd Assignment05
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

3. Install requirements:

```bash
pip install -r requirements.txt
```

4. Run migrations and start server:

```bash
python manage.py migrate
python manage.py runserver
```

---

## 🐋 Docker, Redis, and Celery Configuration

### 📆 Docker Setup

Ensure you have Docker and Docker Compose installed.

**Build Docker containers:**

```bash
docker compose build
```

**Start containers:**

```bash
docker compose up -d
```

**Stop containers:**

```bash
docker compose down
```

**View logs:**

```bash
docker compose logs -f
```

**Check container status:**

```bash
docker compose ps
```

---

### ♻️ Redis & Celery Integration

#### Redis Configuration

Redis is used as the message broker and task result backend for Celery.

Redis runs in a Docker container defined in `docker-compose.yml`:

```yaml
redis_broker:
  image: redis:7
  ports:
    - "6379:6379"
```

No additional config is needed for Redis; it is ready to accept connections at `redis://redis:6379` within Docker's network.

#### 📌 Celery Configuration Settings in `settings.py`

```python
CELERY_BROKER_URL = "redis://redis:6379/0"  # where tasks are queued
CELERY_RESULT_BACKEND = "redis://redis:6379/1"  # where task results are stored
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
```

#### 🔍 Explanation:

- `CELERY_BROKER_URL`: Redis DB 0 stores task queue.
- `CELERY_RESULT_BACKEND`: Redis DB 1 stores task results.
- `CELERY_ACCEPT_CONTENT`: Restricts accepted task content types to `json`.
- `CELERY_TASK_SERIALIZER`: Uses JSON for serialization.

#### Celery Configuration - `djconfig/celery.py`

```python
from celery import Celery

app = Celery("djconfig")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.broker_connection_retry_on_startup = True
```

**`djconfig/__init__.py`**

```python
from .celery import app as celery_app
__all__ = ("celery_app",)
```

#### Sample Celery Task - `mainapp/tasks.py`

This file defines asynchronous tasks that can be triggered by Django signals or views. These tasks are processed by Celery workers outside the main request-response cycle.

```python
from celery import shared_task

@shared_task
def notify_new_patient_created(name):
    print(f"New patient created: {name}")
```

#### Signal Trigger - `mainapp/signals.py`

This connects model events (e.g., `post_save`) to business logic. When a patient is created, a signal triggers a background Celery task to handle post-creation activities asynchronously.

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Patient
from .tasks import notify_new_patient_created

@receiver(post_save, sender=Patient)
def patient_created(sender, instance, created, **kwargs):
    if created:
        notify_new_patient_created.delay(instance.name)
```

---

## 🔔 Event-Driven Architecture

This project uses **event-driven messaging** between Django, Celery, and Redis.

### 💡 Workflow Summary

| Step | Action                                                   | File(s) Involved                             |
|------|----------------------------------------------------------|----------------------------------------------|
| 1️⃣   | User sends API request to create a patient              | `api_patient.py`, `patient_schema.py`        |
| 2️⃣   | Django ORM saves the patient                            | `models.py`                                  |
| 3️⃣   | `post_save` signal detects creation                     | `signals.py`                                 |
| 4️⃣   | Signal triggers a Celery task using `.delay()`          | `signals.py`, `tasks.py`                     |
| 5️⃣   | Task is queued in Redis DB 0                            | `settings.py` → `CELERY_BROKER_URL`          |
| 6️⃣   | Celery worker picks up and runs the task asynchronously | `celery.py`, Docker container `celery_worker`|
| 7️⃣   | Task logs output or performs async job                  | `tasks.py`                                   |

### 🧽 Diagram Overview

```
+-------------+        POST /patients        +-----------------+
|  User/API   +----------------------------->|     Django      |
+-------------+                              |   (Ninja API)   |
                                             +--------+--------+
                                                      |
                                                      v
                                          +-----------+------------+
                                          |     ORM Saves Patient   |
                                          +-----------+------------+
                                                      |
                                                      v
                                   +------------------+------------------+
                                   | Django Signal (post_save) triggers   |
                                   +------------------+------------------+
                                                      |
                                                      v
                                     +----------------+----------------+
                                     | Celery Task Queued via Redis DB0 |
                                     +----------------+----------------+
                                                      |
                                                      v
                                   +------------------+------------------+
                                   | Celery Worker picks and executes it |
                                   +------------------+------------------+
                                                      |
                                                      v
                                  +-------------------------------------+
                                  | Task Logic (e.g., logging, notify) |
                                  +-------------------------------------+
```

This **message-bus architecture** improves scalability and keeps your request-response cycle fast and clean.

---

[... Existing README content continues below here ...]

