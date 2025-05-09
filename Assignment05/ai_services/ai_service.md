
## 🧠 AI Services Integration (Gemini API)

This project integrates **Google Gemini AI Services** for medical text summarization and device anomaly detection using a modular Django app named `ai_services`.

### 📂 Directory Structure
```

ai\_services/
├── gemini.py                  # Initializes Gemini model
├── gemini\_services.py         # AI logic (summarization + anomaly)
├── api\_gemini.py              # Ninja API endpoints
├── schemas.py                 # Input/output schemas
└── tests/
└── test\_gemini.py         # Ninja API tests

````

---

## 🔗 API Endpoints

| Endpoint                  | Method | Description                            |
|---------------------------|--------|----------------------------------------|
| `/api/`                  | GET    | API root response (JSON)               |
| `/api/docs`              | GET    | Swagger API documentation              |
| `/api/ai/summaries`      | POST   | Summarize medical notes                |
| `/api/ai/tests`          | POST   | Detect anomalies in device data        |
| `/dashboard/`            | GET    | View patient/provider/device metrics   |
| `/admin/`                | GET    | Django admin panel                     |

---

## ⚙️ Docker Commands (Clean Build)

```bash
# Remove everything (containers, images, volumes)
docker-compose down --volumes --remove-orphans
docker image prune -a

# Rebuild fresh
docker-compose build --no-cache
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate
````

---

## 🐍 Run Locally with Python (Non-Docker)

```bash
# Set up virtual environment
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Start server
python manage.py runserver
```

---

## ⚙️ Required `settings.py` Setup

### ✅ Add to `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ...
    "dashboard",
    "ai_services",
]
```

### ✅ TEMPLATES section

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # App-discovered templates
        'APP_DIRS': True,
        ...
    }
]
```

---

## ✅ Dashboard Overview

Accessible at: [http://localhost:8000/dashboard/](http://localhost:8000/dashboard/)

Displays:

* Patient count
* Provider count
* Device count

> 📌 We will extend this to include patient growth charts, anomaly visualizations, and AI-generated insights (e.g., word clouds) in upcoming versions.

---

## 🧪 Testing with `ninja.testing.TestClient`

Test your API endpoints using:

```bash
pytest
```

Example:

```python
from ninja.testing import TestClient



from ai_services.api_gemini import ai_router

client = TestClient(ai_router)

def test_summary():
    response = client.post("/summaries", json={"text": "Patient is fatigued."})
    assert response.status_code == 200
```

---

## 🌟 Summary

This project now supports:

* 🧠 Gemini AI integration (summarization + anomaly detection)
* ⚙️ Modular Django structure
* 🐳 Docker orchestration
* 📊 Realtime dashboard
* 🧪 Fully testable API endpoints with Ninja + Pytest

Handy command to keep for docker and container.

```
# Step 1: Shut everything down and remove volumes
docker-compose down --volumes --remove-orphans

# Step 2: Remove all images (optional but thorough)
docker image prune -a

# Step 3: Rebuild everything from scratch
docker-compose build --no-cache

# Step 4: Start fresh containers
docker-compose up -d

# Step 5: Run migrations inside the container
docker-compose exec web python manage.py migrate


---

