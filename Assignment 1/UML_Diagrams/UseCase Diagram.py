from plantuml import PlantUML

uml_code = """
@startuml

!define USECASE_COLOR LightGray

left to right direction

actor "Healthcare Organization" as HO
actor "Healthcare Provider" as HP
actor "Patient" as P
actor "Device Manufacturer" as DM

rectangle "Healthcare Platform" {
    usecase "Monitor System Uptime & Security" as MSUS
    usecase "Monitor Health Condition" as MHC
    usecase "Receive Alert for Abnormal Vital Signs" as RAAVS
    usecase "Device-to-Device Synchronization" as DDS
}

HO --> MSUS : "Scalability and Security"
HP --> RAAVS : "Educational Resources"
HP --> DDS : "Distributed Data Management"
HP --> MHC : "Provider Dashboard"
P --> MHC : "Patient Dashboard"
P --> RAAVS : "Two-Way Communication"
P --> MHC : "Device Data Integration"
DM --> DDS : "Device-to-Device Communication"

@enduml
"""

# Save the UML diagram to a file
with open("use_case_diagram.puml", "w") as file:
    file.write(uml_code)

# Render the UML diagram using PlantUML server
server = PlantUML(url="http://www.plantuml.com/plantuml/img/")
image = server.processes_file("use_case_diagram.puml")

print("Use Case Diagram generated successfully!")
