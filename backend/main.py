from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionLocal


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Expense Management API",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# DATABASE
# =========================================================

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return {
        "success": True,
        "message": "Expense Management API is running",
        "status": "OK"
    }


# =========================================================
# LOGIN
# =========================================================

@app.post("/api/login")
def login(
    data: dict,
    db: Session = Depends(get_db)
):

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:

        user = db.execute(
            text("""
                SELECT
                    id,
                    name,
                    email,
                    password,
                    role,
                    active
                FROM users
                WHERE email = :email
                LIMIT 1
            """),
            {
                "email": email
            }
        ).mappings().first()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        if user["password"] != password:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        if not user["active"]:
            raise HTTPException(
                status_code=403,
                detail="User account is inactive"
            )

        return {
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            }
        }

    except HTTPException:
        raise

    except Exception as e:

        print("LOGIN ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# USERS
# =========================================================

@app.get("/api/users")
def get_users(
    db: Session = Depends(get_db)
):

    try:

        users = db.execute(
            text("""
                SELECT
                    id,
                    name,
                    email,
                    role,
                    active,
                    created_at
                FROM users
                ORDER BY id DESC
            """)
        ).mappings().all()

        return {
            "success": True,
            "users": [
                dict(user)
                for user in users
            ]
        }

    except Exception as e:

        print("GET USERS ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# DASHBOARD
# =========================================================

@app.get("/api/dashboard")
def dashboard(
    db: Session = Depends(get_db)
):

    try:

        total_users = db.execute(
            text("""
                SELECT COUNT(*)
                FROM users
            """)
        ).scalar() or 0

        total_expenses = db.execute(
            text("""
                SELECT COUNT(*)
                FROM expenses
            """)
        ).scalar() or 0

        total_claims = db.execute(
            text("""
                SELECT COUNT(*)
                FROM funding_claims
            """)
        ).scalar() or 0

        pending_claims = db.execute(
            text("""
                SELECT COUNT(*)
                FROM funding_claims
                WHERE funding_status = 'PENDING'
            """)
        ).scalar() or 0

        pending_expenses = db.execute(
            text("""
                SELECT COUNT(*)
                FROM expenses
                WHERE approval_status = 'PENDING'
            """)
        ).scalar() or 0

        approved_expenses = db.execute(
            text("""
                SELECT COUNT(*)
                FROM expenses
                WHERE approval_status = 'APPROVED'
            """)
        ).scalar() or 0

        total_expense_amount = db.execute(
            text("""
                SELECT COALESCE(SUM(amount), 0)
                FROM expenses
            """)
        ).scalar() or 0

        return {
            "success": True,
            "users": int(total_users),
            "expenses": int(total_expenses),
            "claims": int(total_claims),
            "pending_claims": int(pending_claims),
            "pending_expenses": int(pending_expenses),
            "approved_expenses": int(approved_expenses),
            "total_expenses": float(total_expense_amount)
        }

    except Exception as e:

        db.rollback()

        print("DASHBOARD ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# GET ALL EXPENSES
# =========================================================

@app.get("/api/expenses")
def get_expenses(
    db: Session = Depends(get_db)
):

    try:

        expenses = db.execute(
            text("""
                SELECT
                    id,
                    expense_id,
                    employee_id,
                    employee_name,
                    project,
                    date,
                    category,
                    description,
                    amount,
                    receipt_url,
                    approval_status,
                    approval_note,
                    employee_payment_status,
                    employee_payment_date,
                    employee_payment_reference,
                    claim_id,
                    funding_status,
                    funding_payment_date,
                    funding_payment_reference,
                    created_at,
                    updated_at
                FROM expenses
                ORDER BY id DESC
            """)
        ).mappings().all()

        return {
            "success": True,
            "expenses": [
                dict(expense)
                for expense in expenses
            ]
        }

    except Exception as e:

        print("GET EXPENSES ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# GET SINGLE EXPENSE
# =========================================================

@app.get("/api/expenses/{expense_id}")
def get_single_expense(
    expense_id: int,
    db: Session = Depends(get_db)
):

    try:

        expense = db.execute(
            text("""
                SELECT
                    id,
                    expense_id,
                    employee_id,
                    employee_name,
                    project,
                    date,
                    category,
                    description,
                    amount,
                    receipt_url,
                    approval_status,
                    approval_note,
                    employee_payment_status,
                    employee_payment_date,
                    employee_payment_reference,
                    claim_id,
                    funding_status,
                    funding_payment_date,
                    funding_payment_reference,
                    created_at,
                    updated_at
                FROM expenses
                WHERE id = :expense_id
                LIMIT 1
            """),
            {
                "expense_id": expense_id
            }
        ).mappings().first()

        if not expense:
            raise HTTPException(
                status_code=404,
                detail="Expense not found"
            )

        return {
            "success": True,
            "expense": dict(expense)
        }

    except HTTPException:
        raise

    except Exception as e:

        print("GET SINGLE EXPENSE ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# GET EMPLOYEE EXPENSES
# =========================================================

@app.get("/api/expenses/employee/{employee_id}")
def get_employee_expenses(
    employee_id: int,
    db: Session = Depends(get_db)
):

    try:

        expenses = db.execute(
            text("""
                SELECT
                    id,
                    expense_id,
                    employee_id,
                    employee_name,
                    project,
                    date,
                    category,
                    description,
                    amount,
                    receipt_url,
                    approval_status,
                    approval_note,
                    employee_payment_status,
                    employee_payment_date,
                    employee_payment_reference,
                    claim_id,
                    funding_status,
                    funding_payment_date,
                    funding_payment_reference,
                    created_at,
                    updated_at
                FROM expenses
                WHERE employee_id = :employee_id
                ORDER BY id DESC
            """),
            {
                "employee_id": employee_id
            }
        ).mappings().all()

        return {
            "success": True,
            "expenses": [
                dict(expense)
                for expense in expenses
            ]
        }

    except Exception as e:

        print("EMPLOYEE EXPENSE ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# CREATE EXPENSE
# =========================================================

@app.post("/api/expenses")
def create_expense(
    data: dict,
    db: Session = Depends(get_db)
):

    employee_id = data.get("employee_id")
    project = data.get("project")
    expense_date = data.get("date")
    category = data.get("category")
    description = data.get("description")
    amount = data.get("amount")

    if not employee_id:
        raise HTTPException(
            status_code=400,
            detail="Employee ID is required"
        )

    if not project:
        raise HTTPException(
            status_code=400,
            detail="Project is required"
        )

    if not expense_date:
        raise HTTPException(
            status_code=400,
            detail="Expense date is required"
        )

    if not category:
        raise HTTPException(
            status_code=400,
            detail="Category is required"
        )

    if not description:
        raise HTTPException(
            status_code=400,
            detail="Description is required"
        )

    try:

        amount = float(amount)

    except (TypeError, ValueError):

        raise HTTPException(
            status_code=400,
            detail="Amount must be a valid number"
        )

    if amount <= 0:

        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than zero"
        )

    try:

        employee = db.execute(
            text("""
                SELECT
                    id,
                    name
                FROM users
                WHERE id = :employee_id
                LIMIT 1
            """),
            {
                "employee_id": employee_id
            }
        ).mappings().first()

        if not employee:

            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        last_expense = db.execute(
            text("""
                SELECT expense_id
                FROM expenses
                WHERE expense_id IS NOT NULL
                ORDER BY id DESC
                LIMIT 1
            """)
        ).mappings().first()

        next_number = 1

        if last_expense and last_expense["expense_id"]:

            try:

                last_number = int(
                    str(last_expense["expense_id"])
                    .replace("EXP-", "")
                )

                next_number = last_number + 1

            except (ValueError, TypeError):

                next_number = 1

        expense_id = f"EXP-{next_number:04d}"

        db.execute(
            text("""
                INSERT INTO expenses
                (
                    expense_id,
                    employee_id,
                    employee_name,
                    project,
                    date,
                    category,
                    description,
                    amount,
                    approval_status,
                    employee_payment_status,
                    funding_status
                )
                VALUES
                (
                    :expense_id,
                    :employee_id,
                    :employee_name,
                    :project,
                    :date,
                    :category,
                    :description,
                    :amount,
                    'PENDING',
                    'UNPAID',
                    'PENDING'
                )
            """),
            {
                "expense_id": expense_id,
                "employee_id": employee_id,
                "employee_name": employee["name"],
                "project": project,
                "date": expense_date,
                "category": category,
                "description": description,
                "amount": amount
            }
        )

        db.commit()

        return {
            "success": True,
            "message": "Expense submitted successfully",
            "expense_id": expense_id
        }

    except HTTPException:
        raise

    except Exception as e:

        db.rollback()

        print("CREATE EXPENSE ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# APPROVE EXPENSE
# =========================================================

@app.put("/api/expenses/{expense_id}/approve")
def approve_expense(
    expense_id: int,
    db: Session = Depends(get_db)
):

    try:

        expense = db.execute(
            text("""
                SELECT
                    id,
                    expense_id,
                    approval_status
                FROM expenses
                WHERE id = :expense_id
                LIMIT 1
            """),
            {
                "expense_id": expense_id
            }
        ).mappings().first()

        if not expense:

            raise HTTPException(
                status_code=404,
                detail="Expense not found"
            )

        db.execute(
            text("""
                UPDATE expenses
                SET approval_status = 'APPROVED'
                WHERE id = :expense_id
            """),
            {
                "expense_id": expense_id
            }
        )

        db.commit()

        return {
            "success": True,
            "message": "Expense approved successfully",
            "expense_id": expense_id,
            "approval_status": "APPROVED"
        }

    except HTTPException:
        raise

    except Exception as e:

        db.rollback()

        print("APPROVE EXPENSE ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# REJECT EXPENSE
# =========================================================

@app.put("/api/expenses/{expense_id}/reject")
def reject_expense(
    expense_id: int,
    db: Session = Depends(get_db)
):

    try:

        expense = db.execute(
            text("""
                SELECT id
                FROM expenses
                WHERE id = :expense_id
                LIMIT 1
            """),
            {
                "expense_id": expense_id
            }
        ).mappings().first()

        if not expense:

            raise HTTPException(
                status_code=404,
                detail="Expense not found"
            )

        db.execute(
            text("""
                UPDATE expenses
                SET approval_status = 'REJECTED'
                WHERE id = :expense_id
            """),
            {
                "expense_id": expense_id
            }
        )

        db.commit()

        return {
            "success": True,
            "message": "Expense rejected successfully",
            "expense_id": expense_id,
            "approval_status": "REJECTED"
        }

    except HTTPException:
        raise

    except Exception as e:

        db.rollback()

        print("REJECT EXPENSE ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# DELETE EXPENSE
# =========================================================

@app.delete("/api/expenses/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db)
):

    try:

        expense = db.execute(
            text("""
                SELECT id
                FROM expenses
                WHERE id = :expense_id
                LIMIT 1
            """),
            {
                "expense_id": expense_id
            }
        ).mappings().first()

        if not expense:

            raise HTTPException(
                status_code=404,
                detail="Expense not found"
            )

        db.execute(
            text("""
                DELETE FROM expenses
                WHERE id = :expense_id
            """),
            {
                "expense_id": expense_id
            }
        )

        db.commit()

        return {
            "success": True,
            "message": "Expense deleted successfully",
            "expense_id": expense_id
        }

    except HTTPException:
        raise

    except Exception as e:

        db.rollback()

        print("DELETE EXPENSE ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# GET ALL CLAIMS
# =========================================================

@app.get("/api/claims")
def get_claims(
    db: Session = Depends(get_db)
):

    try:

        claims = db.execute(
            text("""
                SELECT
                    id,
                    claim_id,
                    employee_id,
                    employee_name,
                    expense_id,
                    amount,
                    total_amount,
                    description,
                    claim_date,
                    funding_status,
                    submission_date,
                    payment_date,
                    payment_reference,
                    notes,
                    created_at
                FROM funding_claims
                ORDER BY id DESC
            """)
        ).mappings().all()

        return {
            "success": True,
            "claims": [
                dict(claim)
                for claim in claims
            ]
        }

    except Exception as e:

        print("GET CLAIMS ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# GET SINGLE CLAIM
# =========================================================

@app.get("/api/claims/{claim_id}")
def get_single_claim(
    claim_id: int,
    db: Session = Depends(get_db)
):

    try:

        claim = db.execute(
            text("""
                SELECT *
                FROM funding_claims
                WHERE id = :claim_id
                LIMIT 1
            """),
            {
                "claim_id": claim_id
            }
        ).mappings().first()

        if not claim:

            raise HTTPException(
                status_code=404,
                detail="Claim not found"
            )

        return {
            "success": True,
            "claim": dict(claim)
        }

    except HTTPException:
        raise

    except Exception as e:

        print("GET SINGLE CLAIM ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# CREATE REIMBURSEMENT
# =========================================================
@app.post("/api/reimbursements")
def create_reimbursement(
    data: dict,
    db: Session = Depends(get_db)
):
    try:

        # =====================================================
        # GET DATA
        # =====================================================

        expense_id_input = data.get("expense_id")
        amount = data.get("amount")
        reason = data.get("reason")

        # =====================================================
        # VALIDATION
        # =====================================================

        if expense_id_input is None or str(expense_id_input).strip() == "":
            raise HTTPException(
                status_code=400,
                detail="Expense ID is required"
            )

        if amount is None or str(amount).strip() == "":
            raise HTTPException(
                status_code=400,
                detail="Amount is required"
            )

        if not reason or not str(reason).strip():
            raise HTTPException(
                status_code=400,
                detail="Reason is required"
            )

        try:
            amount = float(amount)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=400,
                detail="Amount must be a valid number"
            )

        if amount <= 0:
            raise HTTPException(
                status_code=400,
                detail="Amount must be greater than zero"
            )

        # =====================================================
        # FIND EXPENSE
        # Accept BOTH:
        #   6
        #   EXP-0006
        # =====================================================

        expense_input = str(expense_id_input).strip()

        expense = db.execute(
            text("""
                SELECT
                    id,
                    expense_id,
                    employee_id,
                    employee_name,
                    amount,
                    approval_status,
                    funding_status
                FROM expenses
                WHERE
                    CAST(id AS CHAR) = :expense_input
                    OR expense_id = :expense_input
                LIMIT 1
            """),
            {
                "expense_input": expense_input
            }
        ).mappings().first()

        # =====================================================
        # EXPENSE NOT FOUND
        # =====================================================

        if not expense:
            raise HTTPException(
                status_code=404,
                detail=f"Expense not found: {expense_input}"
            )

        # =====================================================
        # CHECK APPROVAL
        # =====================================================

        if expense["approval_status"] != "APPROVED":
            raise HTTPException(
                status_code=400,
                detail="Expense must be approved before reimbursement"
            )

        # =====================================================
        # CHECK EXISTING CLAIM
        # =====================================================

        existing_claim = db.execute(
            text("""
                SELECT
                    id,
                    claim_id,
                    funding_status
                FROM funding_claims
                WHERE expense_id = :expense_id
                LIMIT 1
            """),
            {
                "expense_id": expense["id"]
            }
        ).mappings().first()

        if existing_claim:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Reimbursement already exists for this expense "
                    f"({existing_claim['claim_id']})"
                )
            )

        # =====================================================
        # GENERATE CLAIM ID
        # =====================================================

        last_claim = db.execute(
            text("""
                SELECT claim_id
                FROM funding_claims
                WHERE claim_id IS NOT NULL
                ORDER BY id DESC
                LIMIT 1
            """)
        ).mappings().first()

        next_number = 1

        if last_claim and last_claim["claim_id"]:

            try:
                next_number = (
                    int(
                        str(last_claim["claim_id"])
                        .replace("CLM-", "")
                    ) + 1
                )

            except (ValueError, TypeError):
                next_number = 1

        claim_id = f"CLM-{next_number:04d}"

        # =====================================================
        # INSERT CLAIM
        # =====================================================

        result = db.execute(
            text("""
                INSERT INTO funding_claims
                (
                    claim_id,
                    employee_id,
                    employee_name,
                    expense_id,
                    amount,
                    total_amount,
                    description,
                    funding_status,
                    claim_date,
                    submission_date,
                    notes
                )
                VALUES
                (
                    :claim_id,
                    :employee_id,
                    :employee_name,
                    :expense_id,
                    :amount,
                    :total_amount,
                    :description,
                    'PENDING',
                    NOW(),
                    NOW(),
                    :notes
                )
            """),
            {
                "claim_id": claim_id,
                "employee_id": expense["employee_id"],
                "employee_name": expense["employee_name"],
                "expense_id": expense["id"],
                "amount": amount,
                "total_amount": amount,
                "description": reason,
                "notes": reason
            }
        )

        # =====================================================
        # GET DATABASE CLAIM ID
        # =====================================================

        new_claim_id = result.lastrowid

        # =====================================================
        # UPDATE EXPENSE
        # =====================================================

        db.execute(
            text("""
                UPDATE expenses
                SET
                    funding_status = 'PENDING',
                    claim_id = :claim_id
                WHERE id = :expense_id
            """),
            {
                "claim_id": new_claim_id,
                "expense_id": expense["id"]
            }
        )

        # =====================================================
        # COMMIT
        # =====================================================

        db.commit()

        # =====================================================
        # RESPONSE
        # =====================================================

        return {
            "success": True,
            "message": "Reimbursement submitted successfully",
            "claim_id": claim_id,
            "database_claim_id": new_claim_id,
            "expense_id": expense["id"],
            "expense_code": expense["expense_id"],
            "amount": amount,
            "status": "PENDING"
        }

    except HTTPException:
        raise

    except Exception as e:

        db.rollback()

        print(
            "CREATE REIMBURSEMENT ERROR:",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# =========================================================
# CREATE CLAIM
# =========================================================

@app.post("/api/claims")
def create_claim(
    data: dict,
    db: Session = Depends(get_db)
):

    amount = data.get("amount")
    description = data.get("description")
    expense_id = data.get("expense_id")

    if amount is None or amount == "":

        raise HTTPException(
            status_code=400,
            detail="Amount is required"
        )

    if not description:

        raise HTTPException(
            status_code=400,
            detail="Description is required"
        )

    try:

        amount = float(amount)

    except (TypeError, ValueError):

        raise HTTPException(
            status_code=400,
            detail="Amount must be a valid number"
        )

    if amount <= 0:

        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than zero"
        )

    try:

        last_claim = db.execute(
            text("""
                SELECT claim_id
                FROM funding_claims
                WHERE claim_id IS NOT NULL
                ORDER BY id DESC
                LIMIT 1
            """)
        ).mappings().first()

        next_number = 1

        if last_claim and last_claim["claim_id"]:

            try:

                next_number = (
                    int(
                        str(last_claim["claim_id"])
                        .replace("CLM-", "")
                    ) + 1
                )

            except (ValueError, TypeError):

                next_number = 1

        claim_id = f"CLM-{next_number:04d}"

        notes = description

        if expense_id:

            notes = (
                f"Expense ID: {expense_id} | "
                f"{description}"
            )

        result = db.execute(
            text("""
                INSERT INTO funding_claims
                (
                    claim_id,
                    claim_date,
                    total_amount,
                    amount,
                    funding_status,
                    submission_date,
                    notes,
                    description
                )
                VALUES
                (
                    :claim_id,
                    NOW(),
                    :total_amount,
                    :amount,
                    'PENDING',
                    NOW(),
                    :notes,
                    :description
                )
            """),
            {
                "claim_id": claim_id,
                "total_amount": amount,
                "amount": amount,
                "notes": notes,
                "description": description
            }
        )

        new_claim_id = result.lastrowid

        db.commit()

        return {
            "success": True,
            "message": "Claim submitted successfully",
            "claim_id": claim_id,
            "database_id": new_claim_id,
            "status": "PENDING"
        }

    except Exception as e:

        db.rollback()

        print("CREATE CLAIM ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# APPROVE CLAIM
# =========================================================

@app.put("/api/claims/{claim_id}/approve")
def approve_claim(
    claim_id: int,
    db: Session = Depends(get_db)
):

    try:

        print(f"APPROVE CLAIM REQUEST: database id = {claim_id}")

        claim = db.execute(
            text("""
                SELECT
                    id,
                    claim_id,
                    funding_status,
                    expense_id
                FROM funding_claims
                WHERE id = :claim_id
                LIMIT 1
            """),
            {
                "claim_id": claim_id
            }
        ).mappings().first()

        if not claim:

            print(
                f"CLAIM NOT FOUND: funding_claims.id = {claim_id}"
            )

            raise HTTPException(
                status_code=404,
                detail=f"Claim with database id {claim_id} not found"
            )

        current_status = str(
            claim["funding_status"] or ""
        ).upper()

        print(
            f"CLAIM FOUND: {claim['claim_id']} | "
            f"status={current_status}"
        )

        if current_status == "PAID":

            raise HTTPException(
                status_code=400,
                detail="Claim has already been paid"
            )

        if current_status == "APPROVED":

            raise HTTPException(
                status_code=400,
                detail="Claim is already approved"
            )

        if current_status == "REJECTED":

            raise HTTPException(
                status_code=400,
                detail="Rejected claim cannot be approved"
            )

        db.execute(
            text("""
                UPDATE funding_claims
                SET funding_status = 'APPROVED'
                WHERE id = :claim_id
            """),
            {
                "claim_id": claim_id
            }
        )

        if claim["expense_id"] is not None:

            db.execute(
                text("""
                    UPDATE expenses
                    SET funding_status = 'APPROVED'
                    WHERE id = :expense_id
                """),
                {
                    "expense_id": claim["expense_id"]
                }
            )

        db.commit()

        print(
            f"CLAIM APPROVED SUCCESSFULLY: {claim['claim_id']}"
        )

        return {
            "success": True,
            "message": "Claim approved successfully",
            "claim_id": claim["claim_id"],
            "database_id": claim["id"],
            "status": "APPROVED"
        }

    except HTTPException:
        raise

    except Exception as e:

        db.rollback()

        print(
            "APPROVE CLAIM ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# REJECT CLAIM
# =========================================================

@app.put("/api/claims/{claim_id}/reject")
def reject_claim(
    claim_id: int,
    db: Session = Depends(get_db)
):

    try:

        claim = db.execute(
            text("""
                SELECT
                    id,
                    claim_id,
                    funding_status,
                    expense_id
                FROM funding_claims
                WHERE id = :claim_id
                LIMIT 1
            """),
            {
                "claim_id": claim_id
            }
        ).mappings().first()

        if not claim:

            raise HTTPException(
                status_code=404,
                detail=f"Claim with database id {claim_id} not found"
            )

        current_status = str(
            claim["funding_status"] or ""
        ).upper()

        if current_status == "PAID":

            raise HTTPException(
                status_code=400,
                detail="Paid claim cannot be rejected"
            )

        if current_status == "REJECTED":

            raise HTTPException(
                status_code=400,
                detail="Claim is already rejected"
            )

        db.execute(
            text("""
                UPDATE funding_claims
                SET funding_status = 'REJECTED'
                WHERE id = :claim_id
            """),
            {
                "claim_id": claim_id
            }
        )

        if claim["expense_id"] is not None:

            db.execute(
                text("""
                    UPDATE expenses
                    SET funding_status = 'REJECTED'
                    WHERE id = :expense_id
                """),
                {
                    "expense_id": claim["expense_id"]
                }
            )

        db.commit()

        return {
            "success": True,
            "message": "Claim rejected successfully",
            "claim_id": claim["claim_id"],
            "database_id": claim["id"],
            "status": "REJECTED"
        }

    except HTTPException:
        raise

    except Exception as e:

        db.rollback()

        print(
            "REJECT CLAIM ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# PAY CLAIM
# =========================================================

@app.put("/api/claims/{claim_id}/pay")
def pay_claim(
    claim_id: int,
    data: dict,
    db: Session = Depends(get_db)
):

    try:

        payment_reference = data.get("payment_reference")

        if not payment_reference:

            raise HTTPException(
                status_code=400,
                detail="Payment reference is required"
            )

        claim = db.execute(
            text("""
                SELECT
                    id,
                    claim_id,
                    employee_id,
                    employee_name,
                    expense_id,
                    amount,
                    total_amount,
                    funding_status
                FROM funding_claims
                WHERE id = :claim_id
                LIMIT 1
            """),
            {
                "claim_id": claim_id
            }
        ).mappings().first()

        if not claim:

            raise HTTPException(
                status_code=404,
                detail=f"Claim with database id {claim_id} not found"
            )

        current_status = str(
            claim["funding_status"] or ""
        ).upper()

        if current_status == "PAID":

            raise HTTPException(
                status_code=400,
                detail="Claim has already been paid"
            )

        if current_status != "APPROVED":

            raise HTTPException(
                status_code=400,
                detail="Claim must be approved before payment"
            )

        amount = claim["total_amount"]

        if amount is None:
            amount = claim["amount"]

        if amount is None:

            raise HTTPException(
                status_code=400,
                detail="Claim amount is missing"
            )

        try:

            amount = float(amount)

        except (TypeError, ValueError):

            raise HTTPException(
                status_code=400,
                detail="Invalid claim amount"
            )

        db.execute(
            text("""
                UPDATE funding_claims
                SET
                    funding_status = 'PAID',
                    payment_date = NOW(),
                    payment_reference = :payment_reference,
                    total_amount = :total_amount,
                    amount = :amount
                WHERE id = :claim_id
            """),
            {
                "claim_id": claim_id,
                "payment_reference": payment_reference,
                "total_amount": amount,
                "amount": amount
            }
        )

        if claim["expense_id"] is not None:

            db.execute(
                text("""
                    UPDATE expenses
                    SET
                        funding_status = 'PAID',
                        funding_payment_date = NOW(),
                        funding_payment_reference = :payment_reference
                    WHERE id = :expense_id
                """),
                {
                    "expense_id": claim["expense_id"],
                    "payment_reference": payment_reference
                }
            )

        db.commit()

        return {
            "success": True,
            "message": "Claim paid successfully",
            "claim_id": claim["claim_id"],
            "database_id": claim["id"],
            "expense_id": claim["expense_id"],
            "amount": amount,
            "funding_status": "PAID",
            "payment_reference": payment_reference
        }

    except HTTPException:
        raise

    except Exception as e:

        db.rollback()

        print(
            "PAY CLAIM ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# DELETE CLAIM
# =========================================================

@app.delete("/api/claims/{claim_id}")
def delete_claim(
    claim_id: int,
    db: Session = Depends(get_db)
):

    try:

        claim = db.execute(
            text("""
                SELECT
                    id,
                    claim_id
                FROM funding_claims
                WHERE id = :claim_id
                LIMIT 1
            """),
            {
                "claim_id": claim_id
            }
        ).mappings().first()

        if not claim:

            raise HTTPException(
                status_code=404,
                detail=f"Claim with database id {claim_id} not found"
            )

        db.execute(
            text("""
                DELETE FROM funding_claims
                WHERE id = :claim_id
            """),
            {
                "claim_id": claim_id
            }
        )

        db.commit()

        return {
            "success": True,
            "message": "Claim deleted successfully",
            "claim_id": claim["claim_id"],
            "database_id": claim["id"]
        }

    except HTTPException:
        raise

    except Exception as e:

        db.rollback()

        print(
            "DELETE CLAIM ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
