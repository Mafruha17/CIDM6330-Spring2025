
# Assignment 04: Migrate API from FastAPI to Django (with Repository Pattern)

## **West Texas A&M University**
- **Semester:** Spring 2025  
- **Course:** CIDM-6330-70 Software Engineering  
- **Student:** Mafruha Chowdhury

---

**Git repo link:** [CIDM6330-Spring2025/Assignment04](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment04)

- [ERD for assignment04](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment04/docs/edr.PNG)
- [Class Diagram](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment04/docs/Class%20Diagram.png)
- [Code Files & Explanation](#code-files--explanation)

---


## 📌 Table of Contents

- [Overview](#-overview)
- [Objectives](#objectives)
- [Project Folder Directory](#project-folder-directory)
- [Installation & Setup](#installation--setup)
- [Code Files & Explanation](#code-files--explanation)
- [API Endpoints](#-api-endpoints-sample)
- [Using the Django Admin](#using-the-django-admin)
- [Testing](#-testing)
- [Conclusion](#conclusion)

---

## 🧹 Overview
This is a Django REST Framework (DRF)-based API designed to manage patients, devices, and providers in a healthcare system. The project was migrated from a FastAPI-based architecture (Assignment 03) and continues to follow a clean, modular, and scalable structure. It includes JWT authentication, CRUD operations, and a repository pattern for abstraction and testability, preserving a clean, layered architecture:

project uses:
- Django 5.1+
- Django REST Framework
- PostgreSQL
- Repository Pattern
- JWT Authentication (Simple JWT)
------
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
- **ModelViewSet** or custom `ViewSet` for CRUD APIs  
- **One-to-Many** relationship: **Patients** ↔ **Devices**  
- **Many-to-Many** relationship: **Patients** ↔ **Providers**  
- **Assignment/Unassignment** logic via custom actions and Django Admin inlines 
- 🧠 Repository pattern for decoupled data logic
- 🧪 Pytest support for test automation (no reliance on Django shell)
---


## **Objectives**
1. Transition core API logic from FastAPI to Django REST Framework  
2. Maintain the **Repository Pattern** for data abstraction  
3. Provide test coverage with `pytest` and `pytest-django`  
4. Utilize Django Admin inlines for assigning/unassigning entities without deleting them  

---

## **Project Folder Directory**

```
Assignment04/                      # Project Root
├── djconfig/                      # Django "project" folder (settings, urls, wsgi, etc.)
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                # Main Django settings (DB config, INSTALLED_APPS, etc.)
│   ├── urls.py                    # Root URL patterns (includes mainapp.urls)
│   └── wsgi.py
├── mainapp/                       # Primary Django "app" with models, views, etc.
│   ├── __init__.py
│   ├── admin.py                   # Django Admin config (inlines, registrations)
│   ├── models.py                  # Database schema (Patient, Provider, Device, PatientProvider)
│   ├── repositories/              # Repository Pattern classes
│   │   ├── __init__.py
│   │   ├── base_repository.py     # Abstract base repository
│   │   ├── patient_repository.py
│   │   ├── provider_repository.py
│   │   └── device_repository.py
│   ├── serializers.py             # DRF serializers (PatientSerializer, etc.) |schemas validation
│   |
│   ├── views/                     # Modular ViewSets (ModelViewSet or custom)
│   |__init__.py
│   ├── patient_views.py
│   ├── device_views.py
│   └── provider_views.py
|   ├── tests/                     # Pytest tests for models, views, assignments
│   │   ├── __init__.py
│   │   ├── test_device.py
│   │   ├── test_patient.py
│   │   └── test_provider.py
├── docs/                     # ERD, design documentation
├── manage.py                      # Django management commands (runserver, migrate, etc.)
├── requirements.txt               # Installed dependencies
└── README.md                      # Project documentation
```

### **Significance of Key Directories**

- **djconfig/**: The core Django “project” module created by `startproject`. Holds `settings.py`, `urls.py`, etc.  
- **mainapp/**: Custom Django “app” for business logic, REST views, models, etc.  
- **repositories/**: Contains classes that encapsulate data access, implementing the Repository Pattern.  
- **views/**: Houses ViewSets or API views for each entity (patient, provider, device).  
- **tests/**: Organized tests covering both unit (repositories) and integration (API endpoints).

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

1. **[`models.py`](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment04/mainapp/models.py)**  : Defines data models.
   - Defines **Patient**, **Provider**, **Device**, and **PatientProvider** models.  
   - **PatientProvider** is a join model for many-to-many (patients ↔ providers).  
   - **Device** uses a `ForeignKey` to `Patient`, representing one-to-many.

2. **[`serializers.py`](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment04/mainapp/serializers.py)**  :Input/output validation.
   - Houses this project **DRF serializers** (e.g., `PatientSerializer`, `ProviderSerializer`, `DeviceSerializer`).  
   - These manage input/output validation and handle nested relationships if needed.

3. **[`repositories/`](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment04/mainapp/repositories)** : Data abstraction.
   - **`base_repository.py`**: Abstract base class using `abc` for CRUD methods.  
   - **`patient_repository.py`, `provider_repository.py`, `device_repository.py`**: Concrete repository classes that inherit from `BaseRepository`.

4. **[`views/`](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment04/mainapp/views)**: API endpoints.
   - **`patient_views.py`, `device_views.py`, `provider_views.py`**: Defined Django REST Framework ViewSets (either `ModelViewSet` or `ViewSet`) for CRUD and custom assignment actions.

5. **[`admin.py`](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment04/mainapp/admin.py)**  Django Admin configurations.

   - Registers models in the Django admin site.  
   - Adds **inlines** for `PatientProvider` (to manage providers for patients) and `Device` (to manage devices assigned to a patient).

6. **[`urls.py`](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment04/djconfig/urls.py)**  
   - Root URL configuration, includes `mainapp.urls` under `/api/`.  

7. **[`urls.py`](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment04/mainapp/urls.py)**  
   - Uses `DefaultRouter()` to register routes for `PatientViewSet`, `ProviderViewSet`, and `DeviceViewSet`.  

8. **[`Test`](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment04/mainapp/tests)**  

   - **[`tests_patient.py`](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment04/mainapp/tests/test_patient.py)**, **[`test_device.py`](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment04/mainapp/tests/test_device.py)**, **[`test_provider.py`](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment04/mainapp/tests/test_provider.py)**: Pytest test files verifying CRUD, assignment endpoints, and repository logic.

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

## 📚 References

- [Django REST Framework](https://www.django-rest-framework.org/)
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Pytest](https://docs.pytest.org/en/stable/)
- [PostgreSQL](https://www.postgresql.org/)


---




## **Conclusion**
This Django project exemplifies a thorough migration from FastAPI to Django REST Framework while preserving **clean architecture** and **repository-driven** data access. Admin inlines make it easier to assign/unassign relationships without deleting objects, and robust tests ensure API reliability. It’s a strong foundation for further enhancements and real-world deployment.

