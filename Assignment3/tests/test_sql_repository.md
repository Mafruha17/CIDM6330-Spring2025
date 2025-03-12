# **SQL Repository Tests**

## **Overview**
This document outlines the test cases designed for the **SQL Repository** implementation. These tests ensure that the **SQLModel-based repository** correctly supports **CRUD operations** while maintaining **data integrity** in a relational database.

---

## **Test Objectives**
- Validate **database persistence** for patients, providers, and devices.
- Ensure **CRUD operations** function as expected.
- Use **SQLite (in-memory) for isolated testing**.

---

## **Test Cases**
### **✅ Test Creating a Patient**
```python
def test_create_patient(session):
    repository = SQLPatientRepository(session)
    patient_data = PatientSchema(name="John Doe", email="johndoe@example.com", age=30, active=True)
    created_patient = repository.create(patient_data)
    assert created_patient.id is not None
    assert created_patient.name == "John Doe"
```

### **✅ Test Retrieving a Patient**
```python
def test_get_patient(session):
    repository = SQLPatientRepository(session)
    patient_data = PatientSchema(name="Jane Doe", email="janedoe@example.com", age=28, active=True)
    created_patient = repository.create(patient_data)
    retrieved_patient = repository.get(created_patient.id)
    assert retrieved_patient is not None
    assert retrieved_patient.email == "janedoe@example.com"
```

### **✅ Test Updating a Patient**
```python
def test_update_patient(session):
    repository = SQLPatientRepository(session)
    patient_data = PatientSchema(name="Alice", email="alice@example.com", age=40, active=True)
    created_patient = repository.create(patient_data)
    update_data = PatientSchema(name="Alice Updated", email="alice@example.com", age=42, active=False)
    updated_patient = repository.update(created_patient.id, update_data)
    assert updated_patient.name == "Alice Updated"
    assert updated_patient.age == 42
```

### **✅ Test Deleting a Patient**
```python
def test_delete_patient(session):
    repository = SQLPatientRepository(session)
    patient_data = PatientSchema(name="Bob", email="bob@example.com", age=50, active=True)
    created_patient = repository.create(patient_data)
    deleted = repository.delete(created_patient.id)
    assert deleted is True
    assert repository.get(created_patient.id) is None
```

---

## **Conclusion**
These tests validate that the **SQL Repository correctly handles CRUD operations** while ensuring **data persistence and consistency**. By using **in-memory SQLite**, we can run tests efficiently without affecting a production database.

