## 📘 README.md — Assignment 05: Full Django + Tests (with Optional AI Services)

### **West Texas A\&M University**

* **Semester:** Spring 2025
* **Course:** CIDM‑6330‑70 Software Engineering
* **Student:** Mafruha Chowdhury

---

### 🔗 GitHub Repository

**Repository Link:** [CIDM6330‑Spring2025/Assignment05](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment05)

* [ERD Diagram](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/docs/edr.PNG)
* [Class Diagram](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment05/docs/Class%20Diagram.png/edr.PNG)

---

## 📋 Table of Contents

1. [Overview & Objectives](#-overview--objectives)
2. [Tech Stack](#-tech-stack)
3. [Architecture & Patterns](#-architecture--patterns)
4. [Installation & Setup](#️-installation--setup)
5. [Docker, Redis, Celery](#-docker-redis-celery)
6. [API Design](#-api-design)
7. [API Endpoints (Ninja Routers)](#-api-endpoints-ninja-routers)
8. [Event‑Driven Processing](#-event-driven-processing)
9. [Testing](#-testing)
10. [Behavior‑Driven Development (BDD)](#-behavior-driven-development-bdd-with-gherkin)
11. [Admin Panel Usage](#-admin-panel-usage)
12. [Troubleshooting](#️-troubleshooting)
13. [Verification](#-verification)
14. [AI Services (Optional)](#-ai-services-optional)
15. [References](#-references)
16. [Conclusion](#-conclusion)
17. [Additional Code Files](#additional-code-files)

> *Sections after 14 were renumbered to accommodate the new optional AI component.*

---

## 🩺 Overview & Objectives

*Unchanged from previous version.*

---

## 🔌 Tech Stack

| Component             | Purpose                          |
| --------------------- | -------------------------------- |
| `Django 5.1.7`        | Core framework                   |
| `django‑ninja`        | Modern API interface             |
| `celery + redis`      | Background task queue            |
| `PostgreSQL`          | Persistent DB (via Docker)       |
| `OpenAI/Azure OpenAI` | External AI inference (optional) |
| `pytest/unittest`     | Testing & verification           |
| `Docker Compose`      | Deployment                       |

---

## 🧱 Architecture & Patterns

*Unchanged, plus AI diagram reference added in [AI Services](#-ai-services-optional).*

---

## ⚙️ Installation & Setup

```bash
# Clone the project
 git clone <REPO_URL>
 cd Assignment05

# Create a virtual environment
 python -m venv venv
 source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies (includes optional AI libs)
 pip install -r requirements.txt

# Run migrations
 python manage.py migrate

# Start server
 python manage.py runserver
```

> **AI keys** – if you enable the AI component, create a `.env` file with:
>
> ```bash
> OPENAI_API_KEY=sk-...
> OPENAI_MODEL=gpt-4o-mini  # or Azure deployment name
> ```

---

## 🐳 Docker, Redis, Celery

*Unchanged.*
Add `ai_services` environment variables to `django_app` section if the AI component is enabled.

---

## ⚡ API Design

*Unchanged; see new AI endpoints below.*

---

## 🔀 API Endpoints (Ninja Routers)

*Existing routers unchanged.*

**AI Router (optional)** — added if `ai_services` app is installed:

| Method | URL                     | Description                               |
| ------ | ----------------------- | ----------------------------------------- |
| `POST` | `/ai/summaries/`        | Summarize or translate clinical note text |
| `POST` | `/ai/device‑anomalies/` | Detect anomalies in device telemetry      |

---

## 📡 Event‑Driven Processing

*Unchanged.*
Optionally dispatch Celery tasks that call AI endpoints for heavy workloads.

---

## 🧪 Testing

Add `tests/test_ai.py` covering summary and anomaly endpoints using mocked OpenAI responses.

---

## 🧪 Behavior‑Driven Development (BDD) with Gherkin

*Unchanged.*
Include a new scenario for AI summary generation if desired.

---

## 🧑‍💼 Admin Panel Usage

*Unchanged.*

---

## 🛠️ Troubleshooting

| Issue                              | Fix                                                                |
| ---------------------------------- | ------------------------------------------------------------------ |
| `openai.error.AuthenticationError` | Verify `OPENAI_API_KEY` in env or secret store                     |
| High token cost                    | Set `temperature=0.2` and shorter prompts; monitor usage dashboard |

---

## ✅ Verification

1. **Core API** – unchanged steps.
2. **AI Demo (optional)**

   ```bash
   curl -X POST http://localhost:8000/ai/summaries/ \
        -H "Content-Type: application/json" \
        -d '{"text": "Patient presents with ...", "language": "en"}'
   ```
3. Observe summarized output; check logs for token usage.

---

## 🤖 AI Services (Optional)

### Why add AI?

* Provide concise, patient‑friendly summaries of clinical notes
* Flag anomalous vitals from wearables before provider review
* Demonstrate modern LLM integration for course extra credit

### Quick Start

1. `pip install openai` (already in requirements)
2. Export `OPENAI_API_KEY`.
3. Add `"ai_services"` to `INSTALLED_APPS`.
4. Include router in `mainapp/api/__init__.py`:

   ```python
   from ai_services.api_ai import router as ai_router
   api.add_router("/ai/", ai_router, tags=["AI"])
   ```

### Minimal Service Implementation

```python
# ai_services/services.py
import openai
from django.conf import settings
openai.api_key = settings.OPENAI_API_KEY


def summarize_note(text: str, lang: str = "en") -> str:
    prompt = (f"Summarize the clinical note below in plain {lang}, 3 sentences, no jargon:\n\n{text}")
    resp = openai.ChatCompletion.create(
        model=settings.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=200,
    )
    return resp.choices[0].message.content.strip()
```

### Security & Compliance

* **De‑identify** PHI before outbound requests.
* Use Azure OpenAI with HIPAA eligibility or sign BAA with provider.
* Log `user_id`, endpoint, prompt tokens, and response IDs for auditing.

---

## 📙 References

*Added*

* OpenAI Python SDK [https://github.com/openai/openai-python](https://github.com/openai/openai-python)
* Azure OpenAI Service HIPAA Overview

---

## 🌟 Conclusion

This project demonstrates a robust Django backend with optional AI enhancement, showcasing:

* Clean API design (Django Ninja)
* Message‑driven architecture (Celery + Redis)
* PostgreSQL persistence
* Modular Repository Pattern
* **AI Services for clinical summarization & device anomaly detection**
* Fully tested backend with zero UI

Ready for further expansion into billing, appointment scheduling, or advanced predictive health‑analytics.

---

## Additional Code Files

See full structure and links in [📁 View Project Files](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment05)
