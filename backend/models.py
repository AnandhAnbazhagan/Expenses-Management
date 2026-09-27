from sqlalchemy import Boolean, Column, Integer, String, Float, Date, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="EMPLOYEE")
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

class FundingClaim(Base):
    __tablename__ = "funding_claims"
    id = Column(Integer, primary_key=True)
    claim_id = Column(String(30), unique=True, nullable=False)
    claim_date = Column(DateTime, server_default=func.now())
    total_amount = Column(Float, default=0)
    funding_status = Column(String(30), default="Pending payment")
    submission_date = Column(DateTime)
    payment_date = Column(DateTime)
    payment_reference = Column(String(150))
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True)
    expense_id = Column(String(30), unique=True, nullable=False)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    employee_name = Column(String(100), nullable=False)
    project = Column(String(150), nullable=False)
    date = Column(Date, nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    amount = Column(Float, nullable=False)
    receipt_url = Column(String(500))
    approval_status = Column(String(20), default="Pending")
    approval_note = Column(Text)
    employee_payment_status = Column(String(20), default="Pending")
    employee_payment_date = Column(DateTime)
    employee_payment_reference = Column(String(150))
    claim_id = Column(Integer, ForeignKey("funding_claims.id"))
    funding_status = Column(String(30))
    funding_status_note = Column(Text)
    funding_payment_date = Column(DateTime)
    funding_payment_reference = Column(String(150))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, server_default=func.now())
