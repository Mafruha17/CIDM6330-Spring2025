@startuml
class Patient {
  + connectDevice()
  + viewHealthData()
  + authenticateUser()
  + receiveAlerts()
}

class HealthcareOrganization {
  + monitorSystemUptime()
  + ensureCompliance()
  + manageUserAccess()
}

class DeviceManufacturer {
  + supportMultipleFormats()
  + integrateWithDevices()
  + provideFirmwareUpdates()
}

class HealthcarePlatform {
  + integrateDevices()
  + manageData()
  + secureCommunication()
  + storeHealthRecords()
}

class DataProcessing {
  + analyzeData()
  + generateAlerts()
  + processHealthMetrics()
}

class HealthcareProvider {
  + accessPatientData()
  + provideRecommendations()
  + sendAlerts()
}

class DeviceFrontend {
  + handleUserInterface()
  + manageDevicePairing()
  + authenticateDevice()
}

class AuthenticationService {
  + validateUser()
  + validateDevice()
  + manageSessions()
}

class Database {
  + storePatientRecords()
  + storeDeviceData()
  + logSystemEvents()
}

class MedicalRecord {
  + addRecord()
  + updateRecord()
  + retrieveRecords()
}

class Appointment {
  + scheduleAppointment()
  + cancelAppointment()
  + viewAppointments()
}

class Billing_Insurance {
  + generateInvoice()
  + processPayment()
  + validateInsurance()
}

class RemoteMonitoring {
  + trackVitals()
  + sendRealTimeAlerts()
  + generateReports()
}

class UserRoles_AccessControl {
  + assignRole()
  + checkPermissions()
  + updateAccessRights()
}

' Relationships
Patient --> HealthcarePlatform : Uses
HealthcareOrganization --> HealthcarePlatform : Monitors
DeviceManufacturer --> HealthcarePlatform : Supports
HealthcarePlatform --> DataProcessing : Processes Data
HealthcarePlatform --> Database : Stores Data
HealthcarePlatform --> DeviceFrontend : Interfaces With
HealthcareProvider --> DataProcessing : Accesses
DataProcessing --> HealthcareProvider : Sends Alerts
Database --> DataProcessing : Logs Metrics
Database --> AuthenticationService : Validates User and Device
AuthenticationService --> DeviceFrontend : Authenticates

MedicalRecord --> Database : Stores Records
MedicalRecord --> Patient : Linked To
MedicalRecord --> HealthcareProvider : Managed By

Appointment --> Patient : Scheduled By
Appointment --> HealthcareProvider : Attended By

Billing_Insurance --> Patient : Pays For Services
Billing_Insurance --> HealthcareOrganization : Manages Payments

RemoteMonitoring --> Patient : Tracks Vitals
RemoteMonitoring --> DeviceManufacturer : Uses Devices

UserRoles_AccessControl --> Patient : Manages Access
UserRoles_AccessControl --> HealthcareProvider : Manages Roles
UserRoles_AccessControl --> HealthcareOrganization : Administers
@enduml
