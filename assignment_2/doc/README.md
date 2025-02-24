Folder	Purpose
models/	Stores Pydantic models (data validation).
routes/	Stores API endpoints (e.g., patient_routes.py).
database/	Manages database connection and CRUD logic.
docs/	Contains ERD diagrams, API documentation, etc.
venv/	Virtual environment (ignored in Git).
requirements.txt	Dependencies list for easy setup.

----------------------
🚀 Benefits of Using crud.py
✅ Separation of concerns → Keeps database logic separate from API routes.
✅ Reusability → crud.py can be used across different route files.
✅ Scalability → If we add a real database later (SQLAlchemy, PostgreSQL), we just modify crud.py.

