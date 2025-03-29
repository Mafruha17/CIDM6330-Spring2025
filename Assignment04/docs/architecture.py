"""@startuml
title Django Healthcare Management API - Request to CRUD Flow

actor Client

Client -> URLConf : Request (e.g., POST /patients/)
URLConf -> ViewLayer : Route to patient_views.py
ViewLayer -> Serializer : Validate & Parse Input
Serializer -> Repository : Call create_patient()
Repository -> Model : ORM Operations
Model -> Database : Save to DB

Database -> Model : DB Response
Model -> Repository : Return Model Object
Repository -> Serializer : Serialize Data
Serializer -> ViewLayer : Return JSON
ViewLayer -> Client : Response

' Authentication flow
Client -> "JWT Token Endpoint" : /api/token/
"JWT Token Endpoint" -> AuthMiddleware : Issue Token
Client -> ProtectedEndpoint : Access with Token
ProtectedEndpoint -> AuthMiddleware : Validate JWT
AuthMiddleware -> ProtectedEndpoint : Grant Access

@enduml
"""