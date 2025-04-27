# Project Management API (SQLite Version)

A FastAPI-based project management system with JWT authentication, projects, tasks, and role-based access control.

## Features

- 🔐 JWT Authentication
- 📝 Project CRUD operations
- ✅ Task management with status tracking
- 👥 Role-based access (Admin, Manager, Developer)
- 🔍 Filtering & pagination
- 📊 Automatic API documentation
- 💾 SQLite database (no setup required)

## Tech Stack

- Python 3.9+
- FastAPI
- SQLAlchemy (ORM)
- SQLite (embedded database)
- Pydantic (data validation)

## 📥 Installation

### Prerequisites
- Python 3.9 or later
- pip package manager

### 1. Clone the repository

git clone https://github.com/jonahjayasingh/project-management-system.git
cd project-management-system

# Linux/MacOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/MacOS
pip install -r requirements.txt

### 2. Run the application

fastapi dev main.py
