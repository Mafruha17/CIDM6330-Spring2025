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
- [Code Files & Explanation](#code-files--explanation)
- [API Endpoints](#api-endpoints)
- [Using the Django Admin](#using-the-django-admin)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Verification and Results](#verification-and-results)
- [References](#references)
- [Conclusion](#conclusion)

---

## 🪹 Overview

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

### 📦 Docker Setup

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

### 🔄 Redis & Celery Integration

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

#### 🔍 Explanation

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

**`djconfig/__init__.py`****\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*:**

```python
from .celery import app as celery_app
__all__ = ("celery_app",)
```

#### Sample Celery Task - `mainapp/tasks.py`

```python
from celery import shared_task

@shared_task
def notify_new_patient_created(name):
    print(f"New patient created: {name}")
```

#### Signal Trigger - `mainapp/signals.py`

🔄 signals.py — Automatic Triggers on Model Events

This file listens for Django signals, such as when a model instance is created, updated, or deleted. It connects backend logic (like calling a Celery task) to these events.



Example use:

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

This setup forms an **event-driven architecture** using Redis as a **message bus**.

✅ So when a new Patient is saved to the database, this signal:

Detects the event

Sends the patient's name to the notify\_new\_patient\_created Celery task

When a `Patient` is created → `post_save` signal triggers → Celery task runs asynchronously.



⚙️ tasks.py — Asynchronous Job Definitions

This file holds Celery tasks: background functions that run separately from the main request-response cycle.

Why it’s helpful:

Prevents API lag from slow tasks (like sending emails, logging, or notifications)

Allows scalable job processing

✅ This task can be triggered directly from your code or by a signal (like in signals.py).

---

## 🧠 Code Files & Explanation

| File/Folder    | Purpose                               |
| -------------- | ------------------------------------- |
| `models.py`    | Models for Patient, Provider, Device  |
| `api/api_*.py` | Modular Ninja routers for each entity |
| `schemas/*.py` | Pydantic-style input/output schemas   |
| `tests/`       | Test files for each entity            |
| `tasks.py`     | Defines Celery async background jobs  |
| `signals.py`   | Connects model events to task queue   |
| `settings.py`  | Config for Celery, DB, static, etc.   |

...

