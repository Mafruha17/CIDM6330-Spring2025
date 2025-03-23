
# Assignment 04: Migrate API from FastAPI to Django (with Repository Pattern)

## **West Texas A&M University**
- **Semester:** Spring 2025  
- **Course:** CIDM-6330-70 Software Engineering  
- **Student:** Mafruha Chowdhury

---
Git repo link 
---
[https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment04](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment04)

[EDR for assignment04 ](/docs/edr.PNG)


[EDR](/docs/Class%20Diagram.png)


## **Table of Contents**
1. [Overview](#overview)  
2. [Objectives](#objectives)  
3. [Project Folder Directory](#project-folder-directory)  
4. [Installation & Setup](#installation--setup)  
5. [Code Files & Explanation](#code-files--explanation)  
6. [API Endpoints](#api-endpoints)  
7. [Using the Django Admin](#using-the-django-admin)  
8. [Testing](#testing)  
9. [Future Improvements](#future-improvements)  
10. [Conclusion](#conclusion)

---

## **Overview**
This assignment migrates our prior FastAPI application to **Django** with the **Django REST Framework**, preserving a clean, layered architecture:

- **Repository Pattern** for data access  
- **ModelViewSet** or custom `ViewSet` for CRUD APIs  
- **One-to-Many** relationship: **Patients** ↔ **Devices**  
- **Many-to-Many** relationship: **Patients** ↔ **Providers**  
- **Assignment/Unassignment** logic via custom actions and Django Admin inlines  
- **PostgreSql** data storage

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
│   ├── serializers.py             # DRF serializers (PatientSerializer, etc.)
│   ├── tests/                     # Pytest tests for models, views, assignments
│   │   ├── __init__.py
│   │   ├── test_device.py
│   │   ├── test_patient.py
│   │   └── test_provider.py
│   └── views/                     # Modular ViewSets (ModelViewSet or custom)
│       ├── __init__.py
│       ├── patient_views.py
│       ├── device_views.py
│       └── provider_views.py
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

## **Code Files & Explanation**

1. **`mainapp/models.py`**  
   - Defines **Patient**, **Provider**, **Device**, and **PatientProvider** models.  
   - **PatientProvider** is a join model for many-to-many (patients ↔ providers).  
   - **Device** uses a `ForeignKey` to `Patient`, representing one-to-many.

2. **`mainapp/serializers.py`**  
   - Houses this project **DRF serializers** (e.g., `PatientSerializer`, `ProviderSerializer`, `DeviceSerializer`).  
   - These manage input/output validation and handle nested relationships if needed.

3. **`mainapp/repositories/`**  
   - **`base_repository.py`**: Abstract base class using `abc` for CRUD methods.  
   - **`patient_repository.py`, `provider_repository.py`, `device_repository.py`**: Concrete repository classes that inherit from `BaseRepository`.

4. **`mainapp/views/`**  
   - **`patient_views.py`, `device_views.py`, `provider_views.py`**: Defined Django REST Framework ViewSets (either `ModelViewSet` or `ViewSet`) for CRUD and custom assignment actions.

5. **`mainapp/admin.py`**  
   - Registers models in the Django admin site.  
   - Adds **inlines** for `PatientProvider` (to manage providers for patients) and `Device` (to manage devices assigned to a patient).

6. **`djconfig/urls.py`**  
   - Root URL configuration, includes `mainapp.urls` under `/api/`.  

7. **`mainapp/urls.py`**  
   - Uses `DefaultRouter()` to register routes for `PatientViewSet`, `ProviderViewSet`, and `DeviceViewSet`.  

8. **Tests (`mainapp/tests/*.py`)**  
   - **`test_patient.py`, `test_device.py`, `test_provider.py`**: Pytest test files verifying CRUD, assignment endpoints, and repository logic.

---

## **API Endpoints**

| **Resource** | **Method** | **Path**                              | **Description**                    |
|--------------|------------|---------------------------------------|------------------------------------|
| **Patients** | GET, POST  | `/api/patients/`                      | List or Create new Patient         |
|              | GET, PUT, PATCH, DELETE | `/api/patients/{id}/`           | Retrieve, Update, or Delete Patient|
| **Providers**| GET, POST  | `/api/providers/`                     | List or Create new Provider        |
|              | GET, PUT, PATCH, DELETE | `/api/providers/{id}/`          | Retrieve, Update, or Delete Provider|
| **Devices**  | GET, POST  | `/api/devices/`                       | List or Create new Device          |
|              | GET, PUT, PATCH, DELETE | `/api/devices/{id}/`            | Retrieve, Update, or Delete Device |
| **Assign**   | POST       | `/api/providers/{id}/assign_patient/` | Assign a patient to a provider     |
|              | POST       | `/api/providers/{id}/remove_patient/` | Remove a patient from a provider   |
|              | POST       | `/api/devices/{id}/assign/`           | Assign device to a patient         |
|              | POST       | `/api/devices/{id}/unassign/`         | Unassign device from a patient     |

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

## **Testing**

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

---

## **Future Improvements would be nice in real world project **

- **Authentication & Authorization**: Add token-based or JWT auth, will get it done when assignment is  
- **Filtering & Pagination**: Let users filter or paginate results (e.g. `/api/patients/?active=true`).  
- **Docker & Deployment**: Containerize the Django app for consistent deployments.  
- **Swagger/OpenAPI**: Auto-document endpoints with DRF or third-party packages.  
- **Custom Frontend**: Build a React/Vue/Angular UI to handle assignment/unassignment visually without the DRF browsable UI.

---

## **Conclusion**
This Django project exemplifies a thorough migration from FastAPI to Django REST Framework while preserving **clean architecture** and **repository-driven** data access. Admin inlines make it easier to assign/unassign relationships without deleting objects, and robust tests ensure API reliability. It’s a strong foundation for further enhancements and real-world deployment.
