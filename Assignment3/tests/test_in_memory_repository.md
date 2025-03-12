# **In-Memory Repository Tests**

## **Overview**
This document outlines the test cases designed for the **In-Memory Repository** implementation. These tests ensure that the **temporary storage solution** correctly supports **CRUD operations** while ensuring consistency in a non-persistent environment.

---

## **Test Objectives**
- Validate **data persistence within runtime** (memory-based storage).
- Ensure **CRUD operations** function as expected.
- Confirm that **data is lost on restart**, simulating a transient storage mechanism.

---

## **Test Cases**
### **✅ Test Creating a Patient in Memory**
```python
def test_create_patient_memory():
    repository = InMemoryRepository()
    patient_data = PatientSchema(name="John Doe", email="johndoe@example.com", age=30, active=True)
    created_patient = repository.create(patient_data)
    assert created_patient["id"] is not None
    assert created_patient["name"] == "John Doe"
```

### **✅ Test Retrieving a Patient from Memory**
```python
def test_get_patient_memory():
    repository = InMemoryRepository()
    patient_data = PatientSchema(name="Jane Doe", email="janedoe@example.com", age=28, active=True)
    created_patient = repository.create(patient_data)
    retrieved_patient = repository.get(created_patient["id"])
    assert retrieved_patient is not None
    assert retrieved_patient["email"] == "janedoe@example.com"
```

### **✅ Test Updating a Patient in Memory**
```python
def test_update_patient_memory():
    repository = InMemoryRepository()
    patient_data = PatientSchema(name="Alice", email="alice@example.com", age=40, active=True)
    created_patient = repository.create(patient_data)
    update_data = PatientSchema(name="Alice Updated", email="alice@example.com", age=42, active=False)
    updated_patient = repository.update(created_patient["id"], update_data)
    assert updated_patient["name"] == "Alice Updated"
    assert updated_patient["age"] == 42
```

### **✅ Test Deleting a Patient in Memory**
```python
def test_delete_patient_memory():
    repository = InMemoryRepository()
    patient_data = PatientSchema(name="Bob", email="bob@example.com", age=50, active=True)
    created_patient = repository.create(patient_data)
    deleted = repository.delete(created_patient["id"])
    assert deleted is True
    assert repository.get(created_patient["id"]) is None
```

---

## **Conclusion**
These tests validate that the **In-Memory Repository correctly handles CRUD operations** while maintaining **data consistency during runtime**. Since **data is lost when the application restarts**, this repository is best suited for **unit testing and transient data storage scenarios**.

