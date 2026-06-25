![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![SQLite](https://img.shields.io/badge/SQLite-database-lightblue)
![Pytest](https://img.shields.io/badge/tests-pytest-orange)

# Personal Finance Tracker API

A FastAPI backend for a finance tracking system, built with SQLite and SQLAlchemy. This backend includes user management, transaction management, financial summaries, and role-based access control.

---

## Features
- User CRUD endpoints
- Transaction CRUD endpoints
- Filter transactions by: 
  - Min amount
  - Max amount 
  - Transaction type
  - Category Type
  - Date
- Financial summaries including total income, expenses and current balance
- Analytical summaries incling Monthly expense summaries and Category-wise breakdowns 
- Role based access control hooks via dependencies
- Automatic SQLite database setup

---

## Tech Stack
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Pytest
- Uvicorn

---

## Getting Started

### Requirements
- Python 3.11+ (recommended)
- `pip`

## Installation

### Create a virtual environment
```bash
python -m venv .venv
```

### Activate the virtual environment
#### On Windows:
```bash
.venv\Scripts\activate
```

#### On Mac/Linux:
```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

### Run the application
Start the FastAPI server using:

```bash
uvicorn main:app --reload
```
The server will be available at `http://127.0.0.1:8000`.

---

### API documentation
FastAPI provides built-in interactive API docs:

- **Swagger UI:**
 `http://127.0.0.1:8000/docs`

---

## Database
This project uses SQLite by default. The database file is configured in `database.py` as:
```python
db_url = "sqlite:///./transactions.db"
```

When the app runs, SQLAlchemy creates tables automatically using the models in `database_models.py`.

---

## Project Structure

```bash
Personal-Finance-Tracker-API/
│
├── main.py                     # FastAPI application entry point
├── database.py                 # Database setup and session management
├── database_models.py          # ORM models for User and Transaction
│
├── routers/
│   ├── users.py                # User-related endpoints
│   └── transactions.py         # Transaction and reporting endpoints
│
├── schemas/
│   ├── user_schema.py          # Pydantic schemas for User
│   └── transaction_schema.py   # Pydantic schemas for Transaction
│
├── tests/
│   ├── test_users.py           # Unit tests for user endpoints
│   └── test_transactions.py    # Unit tests for transaction endpoints
│
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

---

## API Endpoints Overview

### Users
- `GET /users/` -> Get all users
- `GET /users/{user_id}` -> Get user by ID
- `POST /users/` -> Create a user
- `PUT /users/{user_id}` -> Update a user
- `DELETE /users/{user_id}` -> Delete a user

### Transactions
- `GET /transactions/` -> Get all transactions
- `GET /transactions/recent` -> Get recent transactions
- `GET /transactions/summary` -> Get Financial Summary (total income, expenses and current balance)
- `GET /transactions/monthly-expense` -> Get Monthly Expense Summary
- `GET /transactions/category-wise-breakdown` -> Get Category-wise Expenses
- `GET /transactions/{transaction_id}` -> Get transaction by ID
- `POST /transactions/` -> Create a transaction
- `PUT /transactions/{transaction_id}` -> Update a transaction
- `DELETE /transactions/{transaction_id}` -> Delete a transaction

---

## Running Tests
Run unit tests with:

```bash
pytest -v
```

or 

```bash
python -m pytest -v
```

