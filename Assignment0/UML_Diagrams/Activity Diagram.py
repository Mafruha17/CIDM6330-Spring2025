from plantuml import PlantUML

uml_code = """
@startuml

== Device Lifecycle ==

(*) --> "Unpaired"
"Unpaired" --> "Pairing" : "Initiate Pairing"
"Pairing" --> "Unpaired" : "Pairing Failed"
"Pairing" --> "Paired" : "Successful Pairing"
"Paired" --> "Connected" : "User Authenticated"
"Connected" --> "Transmitting" : "Data Exchange Active"
"Connected" --> "Temporary Pause"
"Temporary Pause" --> "Connected"
"Connected" --> "Disconnected" : "User Logout / Timeout"
"Disconnected" --> "Connected" : "Reconnect"
"Paired" --> "Unpaired" : "Device Reset"

== User Authentication ==

(*) --> "NotAuthenticated"
"NotAuthenticated" --> "Authenticating" : "User Login / Failure"
"Authenticating" --> "NotAuthenticated" : "Failure"
"Authenticating" --> "Authenticated" : "Success"
"Authenticated" --> "LoggedIn" : "Access Granted"
"LoggedIn" --> "NotAuthenticated" : "Logout"

== Activity Flow ==

(*) --> "Start"
"Start" --> "DeviceAuthentication" : "User Initiates Pairing"
"DeviceAuthentication" --> "Success" : "Valid Credentials"
"DeviceAuthentication" --> "Failure" : "Invalid Credentials"
"Failure" --> "DeviceAuthentication" : "Retry Login"
"Success" --> "DevicePaired" : "Device Successfully Connected"
"DevicePaired" --> "TransmitData" : "Real-time Monitoring"
"DevicePaired" --> "NotifyProvider"
"NotifyProvider" --> "LogEvent" : "Store Alert Record"
"TransmitData" --> "ProcessData" : "Normal Monitoring Complete"
"ProcessData" --> "End" : "Analyze and Store"

== Health Data Processing ==

(*) --> "ReceivingData"
"ReceivingData" --> "Processing" : "Data Validation"
"Processing" --> "AlertGenerated" : "Abnormal Condition Detected"
"AlertGenerated" --> "Stored" : "Save to Database"
"AlertGenerated" --> "Notified" : "Send Alert to Provider"
"Notified" --> "Stored" : "Log Event"
"Stored" --> "ReceivingData" : "If Abnormal Condition Detected"

@enduml
"""

# Save UML to a file
uml_file = "activity_diagram.puml"
with open(uml_file, "w") as file:
    file.write(uml_code)

# Render the UML diagram using PlantUML
server = PlantUML(url="http://www.plantuml.com/plantuml/img/")
image = server.processes_file(uml_file)

print("Activity Diagram Generated Successfully!")
