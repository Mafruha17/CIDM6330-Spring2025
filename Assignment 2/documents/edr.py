import os

# PlantUML ERD definition
plantuml_code = """@startuml
title Entity Relationship Diagram (ERD) - Patient & Device

entity Patient {
    *id : Integer [PK]
    --
    name : String
    email : String
    age : Integer
    active : Boolean
}

entity Device {
    *id : Integer [PK]@startuml
title Patient, Device, and Provider Entity Relationship Diagram

entity "Patient" {
    *id : int <<PK>>
    --
    name : varchar
    email : varchar
    age : int
    active : boolean
}

entity "Device" {
    *id : int <<PK>>
    --
    serial_number : varchar
    active : boolean
    patient_id : int <<FK>>
}

entity "Provider" {
    *id : int <<PK>>
    --
    name : varchar
    email : varchar
    specialty : varchar
}

entity "Patient_Provider" {
    *patient_id : int <<FK>>
    *provider_id : int <<FK>>
}

' Relationships
Patient ||--o{ Device : "1:N"
Patient ||--o{ Patient_Provider : "1:N"
Provider ||--o{ Patient_Provider : "1:N"
@enduml

    --
    serial_number : String
    patient_id : Integer [FK]
    active : Boolean
}

Patient ||--|{ Device : "has"
@enduml
"""

# Save the PlantUML code to a file
puml_file = "patient_device_erd.puml"
with open(puml_file, "w") as file:
    file.write(plantuml_code)

# Generate the ERD using PlantUML
os.system(f"plantuml {puml_file}")

print("ERD diagram generated successfully!")
