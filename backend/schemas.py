from datetime import date
from typing import Optional, List
from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

class ExpenseCreate(BaseModel):
    employee_id: int
    employee_name: str
    project: str
    date: date
    category: str
    description: str
    amount: float

class ExpenseApproval(BaseModel):
    approved: bool
    note: Optional[str] = ""

class EmployeePayment(BaseModel):
    reference: Optional[str] = ""

class FundingClaimCreate(BaseModel):
    expense_ids: List[int]
    notes: Optional[str] = ""

class FundingPayment(BaseModel):
    reference: Optional[str] = ""
