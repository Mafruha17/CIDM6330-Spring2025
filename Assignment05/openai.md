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

### Supported Providers

* **OpenAI API** (GPT-4, GPT-3.5)
* **Azure OpenAI Service** (deployments of OpenAI models in Azure)

### Other AI API Options

#### Text‑Based

* **AWS Comprehend Medical** – Extract medical entities, PHI detection, and clinical summarization with HIPAA compliance.
* **Google Cloud Healthcare Natural Language API** – Analyze and annotate clinical notes, identify medical terminology, and sentiment analysis.
* **Hugging Face Inference API** – Use community models for summarization, translation, or fine‑tuned clinical models.

#### Vision & Imaging

* **Azure Cognitive Services: Computer Vision** – OCR, image classification, object detection, and medical image analysis via Custom Vision.
* **AWS Rekognition** – Face detection, object and scene analysis, text in image, and video surveillance capabilities.
* **Google Cloud Vision API** – Label detection, OCR, landmark detection, and AutoML Vision for custom models.
* **Hugging Face Transformers + PIL/OpenCV** – On‑device or server‑side inference with vision‑capable models (e.g., DINO, CLIP) for anomaly detection in device images.

### Advanced Predictive Health‑Analytics

Enhance proactive care by integrating predictive analytics on patient and device data:

* **Time‑Series Forecasting**: Use frameworks like **Facebook Prophet**, **TensorFlow**, or **Azure Time Series Insights** to project vital sign trends and detect deviations before they become critical.
* **Risk‑Scoring Models**: Deploy custom or AutoML‑trained models on **Azure ML**, **AWS SageMaker**, or **Google AI Platform** to compute health risk scores from EHR and sensor data.
* **Cohort Analytics**: Leverage **Azure Synapse** or **BigQuery** with integrated ML to identify at‑risk patient groups and recommend interventions.

```python
# Example: call Azure ML REST scoring endpoint
import os, requests

def predict_risk(patient_features: dict) -> float:
    endpoint = os.getenv("AZURE_ML_ENDPOINT")
    api_key = os.getenv("AZURE_ML_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {"data": [patient_features]}
    resp = requests.post(f"{endpoint}/score", json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()["predictedRiskScore"]
```

Use these analytics to trigger alerts, plan maintenance, or recommend follow‑up care.

### Quick Start for Visual AI

1. Install SDK:

   ```bash
   pip install azure-cognitiveservices-vision-computervision  # for Azure CV
   pip install boto3                                           # for AWS Rekognition
   pip install google-cloud-vision                             # for GCP Vision
   ```
2. Configure credentials in `.env`:

   ```bash
   AZURE_CV_KEY=<key>
   AZURE_CV_ENDPOINT=<endpoint>
   AWS_ACCESS_KEY_ID=<key>
   AWS_SECRET_ACCESS_KEY=<secret>
   GOOGLE_APPLICATION_CREDENTIALS=/path/to/creds.json
   ```
3. Example usage (Azure Computer Vision):

   ```python
   from azure.cognitiveservices.vision.computervision import ComputerVisionClient
   from msrest.authentication import CognitiveServicesCredentials

   cv_client = ComputerVisionClient(
       os.getenv("AZURE_CV_ENDPOINT"),
       CognitiveServicesCredentials(os.getenv("AZURE_CV_KEY"))
   )

   def analyze_image(url: str):
       features = cv_client.analyze_image(url, ["Tags", "Objects", "OCR"])
       return {"tags": [t.name for t in features.tags], "text": features.ocr.read_results}
   ```

---

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

---

### 🛠️ Quick Setup

```bash
# 1️⃣  From the Assignment05 root directory
python -m venv venv          # or poetry env use python3.11
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2️⃣  Install all project dependencies
pip install -r requirements.txt

# …or install just the OpenAI SDK individually if you’re experimenting:
pip install openai

# 3️⃣  Run the local stack
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

> **Why here?** Running `pip install …` inside the *Assignment05* directory ensures the package is installed into the same virtual environment that your Django & FastAPI apps use. Location on disk doesn’t matter as long as the venv is active, but staying at the project root keeps your dependency tree tidy and your `requirements.txt` reproducible.

Add **`openai==1.*`** to `requirements.txt`, commit, and push so CI/CD and teammates get the same environment.

---

**Suggesting PowerShell script**

It looks like the user wants to run the test in a PowerShell script, perhaps using Python code in it. I could provide an example using a here-string or OpenAI CLI, but they're asking specifically for PowerShell. So, I might suggest embedding Python code or calling it directly with `-c`. A good option is a `.ps1` script like this:

```
$env:OPENAI_API_KEY = 'sk-...'
$script = @"
import openai
from django.conf import settings
import os, django
...
"@
python - <<EOF
... EOF
```


Thought for 5 seconds


Here’s a tiny PowerShell script you can drop into your project root (e.g. call it **`test_openai.ps1`**) to smoke-test your OpenAI integration from PowerShell:

```powershell
# test_openai.ps1
# 1) Make sure you’re in Assignment05/ and your venv is active:
#    PS> .\venv\Scripts\Activate.ps1
#
# 2) Then just run:
#    PS> .\test_openai.ps1

# Build the Python snippet as a here-string
$pythonCode = @"
import os
import django
from django.conf import settings

# bootstrap Django so settings.py is loaded
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE_DIR)       # ensure manage.py is on the CWD
django.setup()

import openai
openai.api_key = settings.OPENAI_API_KEY
model = settings.OPENAI_MODEL

# fire off a quick prompt
resp = openai.ChatCompletion.create(
    model=model,
    messages=[{"role": "user", "content": "What is 2+2?"}],
    max_tokens=5,
)

print(">> LLM answer:", resp.choices[0].message.content.strip())
"@

# Pipe it into python
$pythonCode | python
```

### How it works

1. **Here-string** (`@"…@"`) holds your Python code.
2. Piping (`| python`) feeds it to Python’s STDIN.
3. Inside the snippet, we:

   * `os.chdir(BASE_DIR)` so that `django.setup()` finds your `manage.py` and `djconfig/settings.py`
   * Call the same OpenAI SDK code you’ll eventually use in `ai_services`.

#### Running it

```powershell
PS> cd Assignment05
PS> .\venv\Scripts\Activate.ps1
(venv) PS> .\test_openai.ps1
>> LLM answer: 4
```

If you see a “4” (or similar), your `.env`→`django-environ`→OpenAI pipeline is fully wired up.


---
# test_openai.ps1
# 1) Make sure you’re in Assignment05/ and your venv is active:
#    PS> .\venv\Scripts\Activate.ps1
#
# 2) Then just run:
#    PS> .\test_openai.ps1

# Build the Python snippet as a here-string
$pythonCode = @"
import os
import django
from django.conf import settings

# bootstrap Django so settings.py is loaded
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE_DIR)       # ensure manage.py is on the CWD
django.setup()

import openai
openai.api_key = settings.OPENAI_API_KEY
model = settings.OPENAI_MODEL

# fire off a quick prompt
resp = openai.ChatCompletion.create(
    model=model,
    messages=[{"role": "user", "content": "What is 2+2?"}],
    max_tokens=5,
)

print(">> LLM answer:", resp.choices[0].message.content.strip())
"@

# Pipe it into python
$pythonCode | python

---