from plantuml import PlantUML

uml_code = """
@startuml
title Sequence Diagram - Healthcare Device Pairing and Data Transmission

actor Patient
actor "Healthcare Provider" as Provider
participant "Healthcare Platform" as Platform
participant "Device Frontend" as Frontend
participant "Device" as Device
participant "Database" as Database

activate Platform
activate Frontend
activate Device
activate Database

Patient -> Provider: Connect and Authenticate()
Provider -> Platform: Forward Connection Request()
Platform -> Frontend: Authenticate Device()
Frontend -> Device: Device Connected
Device -> Database: Store Device Info()

== Device Pairing Process ==
loop "Retry Pairing If Failed"
    Provider -> Frontend: Pair Device()
    Frontend -> Device: Initiate Pairing Request()
    Device -> Frontend: Verify Pairing()
    Frontend -> Database: Store Pairing Details()
    Database -> Frontend: Confirmation
    Frontend -> Provider: Notify Pairing Success
end
Provider -> Patient: Display Pairing Success

== Continuous Health Data Transmission ==
loop "Continuous Health Data Transmission"
    Patient -> Platform: View Health Data()
    Platform -> Frontend: Request Data()
    Frontend -> Device: Retrieve Health Data()
    Device -> Frontend: Send Health Data()
    Frontend -> Platform: Forward Data
end
Platform -> Patient: Display Data

Provider -> Platform: Access Patient Data()
Platform -> Frontend: Forward Access Request()
Frontend -> Database: Fetch Patient Records()
Database -> Frontend: Return Patient Data
Frontend -> Platform: Forward Data
Platform -> Provider: Provide Access
Provider -> Platform: Provide Recommendations()
Platform -> Frontend: Forward Recommendation()
Frontend -> Database: Store Recommendations()
Database -> Frontend: Acknowledge Storage
Frontend -> Platform: Confirm Recommendation Stored
Platform -> Provider: Notify Recommendation Received

deactivate Platform
deactivate Frontend
deactivate Device
deactivate Database

@enduml
"""

# Save the UML code to a file
with open("sequence_diagram.puml", "w") as file:
    file.write(uml_code)

# Render the diagram using PlantUML
server = PlantUML(url="http://www.plantuml.com/plantuml/img/")
image = server.processes_file("sequence_diagram.puml")

print("UML Sequence Diagram generated successfully!")

