# Assignment 04: Migrate to Django

## **West Texas A&M University**
- **Semester:** Spring 2025  
- **Course:** CIDM6330/01 Software Engineering  
- **Student:**   

---

## **Overview**
This assignment migrates the previous FastAPI project to **Django** using **Django REST Framework (DRF)**. The goal is to refactor the API and repository pattern while leveraging Django's ORM for database management.

## **Objectives**
- Convert the **FastAPI-based API** to **Django REST Framework**.
- Replace **SQLModel (FastAPI)** with **Django ORM**.
- Maintain the **Repository Pattern** for database operations.
- Implement a structured **project layout** with separate directories for repositories, routers, and schemas.

---

## **Project Folder Structure**
```
Assignment04/            # Main project directory
│── core/                # Django app
│   ├── database/        # Database models
│   │   ├── connection.py
│   │   ├── models.py
│   ├── repositories/    # Repository pattern
│   │   ├── base_repository.py
│   │   ├── patient_repository.py
│   │   ├── provider_repository.py
│   │   ├── device_repository.py
│   ├── routers/         # API Endpoints
│   │   ├── patient_router.py
│   │   ├── provider_router.py
│   │   ├── device_router.py
│   ├── schemas/         # DRF Serializers
│   │   ├── patient.py
│   │   ├── provider.py
│   │   ├── device.py
│   ├── tests/           # Unit tests
│   │   ├── test_sql_repository.py
│   │   ├── test_csv_repository.py
│   │   ├── test_in_memory_repository.py
│   │   ├── conftest.py
│── config/              # Project settings
│   ├── settings.py
│   ├── urls.py
│── docs/                # Documentation
│   ├── patient_repository.md
│   ├── provider_repository.md
│   ├── device_repository.md
│── manage.py            # Django management script
│── requirements.txt     # Dependencies
│── .gitignore
│── .env                 # Environment variables
│── README.md
```

---

## **Dependency Installation**
Before proceeding, install all necessary dependencies in a **virtual environment**.

### **1. Create & Activate Virtual Environment**
```sh
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### **2. Install Required Packages**
```sh
pip install django djangorestframework django-environ
pip install psycopg2-binary  # Only for PostgreSQL
pip install pytest pytest-django factory_boy
pip install django-filter drf-yasg djangorestframework-simplejwt
```

### **3. Save Installed Dependencies**
```sh
pip freeze > requirements.txt
```

---

## **Setting Up the Project**

### **1. Initialize Django Project**
```sh
django-admin startproject config .
```

### **2. Create Django App**
```sh
python manage.py startapp core
```

### **3. Apply Database Migrations**
```sh
python manage.py makemigrations
python manage.py migrate
```

### **4. Run Django Development Server**
```sh
python manage.py runserver
```

---

## **Next Steps**
- Implement **Django ORM Models** (`core/database/models.py`)
- Develop **Repository Pattern** (`core/repositories/`)
- Configure **API Endpoints** (`core/routers/`)
- Implement **Authentication & Permissions**

This document will be updated as the project progresses. 🚀

