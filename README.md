# Expense & Reimbursement Management System

## Stack
Python + FastAPI + MySQL

## Setup
1. Install MySQL.
2. Run `database/schema.sql`.
3. Edit `backend/database.py` and replace the MySQL username/password.
4. Open terminal in `backend`.
5. Run:
   `pip install -r requirements.txt`
   `uvicorn main:app --reload`
6. Open `http://127.0.0.1:8000/docs`.

Demo:
Admin: admin@example.com / admin123
Employee: employee@example.com / employee123

The API implements expense submission, receipt upload, CEO approval/rejection, employee reimbursement, funding claims, funding payment, and dashboard statistics.
