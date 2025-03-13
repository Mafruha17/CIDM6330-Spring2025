from sqlmodel import Session
from database.connection import get_db
from database.models import Patient

def test_patient_id_generation():
    db = next(get_db())

    new_patient = Patient(name="Test Patient", email="test@example.com", age=30, active=True)
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    print(f"Generated Patient ID: {new_patient.id}")  # Expect a non-null, auto-generated ID

if __name__ == "__main__":
    test_patient_id_generation()
