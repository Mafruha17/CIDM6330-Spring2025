# **CSV Repository Tests**

## **Overview**
This document outlines the test cases designed for the **CSV Repository** implementation. These tests ensure that the **CSV-based storage** correctly supports **CRUD operations** while maintaining **data integrity** in a file-based format.

---

## **Test Objectives**
- Validate **file-based persistence** for patients, providers, and devices.
- Ensure **CRUD operations** function as expected.
- Check that **CSV files are properly read and written**.

---

## **Test Cases**
### **✅ Test Creating a Patient in CSV**
```python
def test_create_patient_csv():
    repository = CSVRepository("test_patients.csv")
    patient_data = PatientSchema(name="John Doe", email="johndoe@example.com", age=30, active=True)
    created_patient = repository.create(patient_data)
    assert created_patient["id"] is not None
    assert created_patient["name"] == "John Doe"
```

### **✅ Test Retrieving a Patient from CSV**
```python
def test_get_patient_csv():
    repository = CSVRepository("test_patients.csv")
    patient_data = PatientSchema(name="Jane Doe", email="janedoe@example.com", age=28, active=True)
    created_patient = repository.create(patient_data)
    retrieved_patient = repository.get(created_patient["id"])
    assert retrieved_patient is not None
    assert retrieved_patient["email"] == "janedoe@example.com"
```

### **✅ Test Updating a Patient in CSV**
```python
def test_update_patient_csv():
    repository = CSVRepository("test_patients.csv")
    patient_data = PatientSchema(name="Alice", email="alice@example.com", age=40, active=True)
    created_patient = repository.create(patient_data)
    update_data = PatientSchema(name="Alice Updated", email="alice@example.com", age=42, active=False)
    updated_patient = repository.update(created_patient["id"], update_data)
    assert updated_patient["name"] == "Alice Updated"
    assert updated_patient["age"] == 42
```

### **✅ Test Deleting a Patient in CSV**
```python
def test_delete_patient_csv():
    repository = CSVRepository("test_patients.csv")
    patient_data = PatientSchema(name="Bob", email="bob@example.com", age=50, active=True)
    created_patient = repository.create(patient_data)
    deleted = repository.delete(created_patient["id"])
    assert deleted is True
    assert repository.get(created_patient["id"]) is None
```

---

## **Conclusion**
These tests validate that the **CSV Repository correctly handles CRUD operations** while ensuring **data persistence and correctness in file-based storage**. By testing CSV read/write operations, we can ensure that **data integrity is maintained even when stored as a CSV file**.

