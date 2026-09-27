USE expense_management;

SELECT id, name, email, password, role, active
FROM users
WHERE email = 'adminthemindcreater@gmail.com';

UPDATE users
SET password = 'admin123',
    role = 'ADMIN',
    active = 1
WHERE email = 'adminthemindcreater@gmail.com';

SELECT id, name, email, password, role, active
FROM users
WHERE email = 'adminthemindcreater@gmail.com';

USE expense_management;

SELECT
    id,
    name,
    email,
    role,
    active
FROM users;

SELECT
    id,
    name,
    email,
    role,
    active
FROM users
WHERE email = 'adminthemindcreater@gmail.com';

USE expense_management;

UPDATE users
SET password = 'Anandh@2013'
WHERE email = 'adminthemindcreater@gmail.com';

SELECT
    id,
    name,
    email,
    role,
    active
FROM users
WHERE email = 'adminthemindcreater@gmail.com';

USE expense_management;

DESCRIBE expenses;

SHOW COLUMNS FROM expenses;

USE expense_management;

INSERT INTO expenses (
    expense_id,
    employee_id,
    employee_name,
    project,
    date,
    category,
    description,
    amount
)
VALUES (
    'EXP-0001',
    1,
    'expense_management',
    'Official Meeting',
    '2026-09-25',
    'Travel',
    'Travel expense for official meeting',
    1500.00
);

SELECT * FROM expenses;
SHOW COLUMNS FROM expenses;


USE expense_management;

SELECT *
FROM expenses
WHERE expense_id = 'EXP-0001';

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
    approval_status,
    employee_payment_status,
    funding_status
FROM expenses
ORDER BY id DESC;

INSERT INTO expenses (
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
VALUES (
    'EXP-0002',
    1,
    'expense_management',
    'Client Meeting',
    '2026-09-25',
    'Travel',
    'Travel expense for client meeting',
    850.00,
    'PENDING',
    'UNPAID',
    'PENDING'
);

SELECT * FROM expenses;

USE expense_management;

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
ORDER BY id DESC;


USE expense_management;



DESCRIBE funding_claims;

SHOW COLUMNS FROM funding_claims;

SELECT COUNT(*) FROM funding_claims WHERE status = 'PENDING';

USE expense_management;

DESCRIBE funding_claims;
USE expense_management;

SELECT COUNT(*) AS pending_claims
FROM funding_claims
WHERE funding_status = 'PENDING';

USE expense_management;

SELECT
    (SELECT COUNT(*) FROM users) AS users,
    (SELECT COUNT(*) FROM expenses) AS expenses,
    (SELECT COUNT(*) FROM funding_claims) AS claims,
    (SELECT COUNT(*)
     FROM funding_claims
     WHERE funding_status = 'PENDING') AS pending_claims,
    (SELECT COALESCE(SUM(amount), 0)
     FROM expenses) AS total_expenses;
     
USE expense_management;

UPDATE users
SET role = 'CEO'
WHERE email = 'adminthemindcreater@gmail.com';

SELECT id, name, email, role, active
FROM users;

INSERT INTO users
(
    name,
    email,
    password,
    role,
    active
)
VALUES
(
    'Employee One',
    'employee@gmail.com',
    'Employee@123',
    'EMPLOYEE',
    1
);

SELECT id, name, email, role, active
FROM users;

USE expense_management;
SELECT id, name, email, role, active
FROM users;

USE expense_management;
SELECT id, name, email, role, active
FROM users;

UPDATE users
SET role = 'CEO'
WHERE email = 'adminthemindcreater@gmail.com';

INSERT INTO users
(
    name,
    email,
    password,
    role,
    active
)
VALUES
(
    'Employee One',
    'employee@gmail.com',
    'Employee@123',
    'EMPLOYEE',
    1
);

UPDATE users
SET
    name = 'Employee One',
    password = 'Employee@123',
    role = 'EMPLOYEE',
    active = 1
WHERE email = 'employee@gmail.com';

SELECT id, name, email, role, active
FROM users;

UPDATE users
SET role = 'CEO'
WHERE email = 'adminthemindcreater@gmail.com';

SELECT id, name, email, role, active
FROM users;

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
    approval_status,
    employee_payment_status,
    funding_status
FROM expenses
ORDER BY id DESC;

DESCRIBE funding_claims;

DESCRIBE funding_claims;

DESCRIBE funding_claims;

SELECT *
FROM funding_claims
LIMIT 5;

DESCRIBE funding_claims;

SELECT * FROM funding_claims LIMIT 5;

DESCRIBE funding_claims;

SELECT *
FROM funding_claims
LIMIT 5;

DESCRIBE funding_claims;

DESCRIBE funding_claims;

USE expense_management;

DESCRIBE funding_claims;

SELECT *
FROM funding_claims
LIMIT 10;

DESCRIBE funding_claims;

USE expense_management;

SELECT *
FROM expenses
LIMIT 5;

DESCRIBE expenses;

DESCRIBE expenses;

SELECT
    id,
    expense_id,
    employee_id,
    employee_name,
    project,
    date,
    category,
    amount,
    approval_status,
    employee_payment_status,
    funding_status
FROM expenses
ORDER BY id DESC;

DESCRIBE funding_claims;

DESCRIBE funding_claims;

DESCRIBE funding_claims;

SELECT *
FROM funding_claims
ORDER BY id DESC;

USE expense_management;

SELECT id, name, email, role, active
FROM users
ORDER BY id;

USE expense_management;

SELECT id, name, email, role, active

SELECT *
FROM users
WHERE email = 'YOUR_EMPLOYEE_EMAIL';
FROM users;

SELECT *
FROM users
WHERE email = 'anandh@gmail.com';

USE expense_management;

SHOW TABLES;

USE expense_management;

DESCRIBE funding_claims;


USE expense_management;

DESCRIBE funding_claims;

SELECT * FROM funding_claims LIMIT 5;

DESCRIBE funding_claims;

USE expense_management;

DESCRIBE funding_claims;

USE expense_management;

DESCRIBE funding_claims;

DESCRIBE funding_claims;

SELECT * FROM funding_claims;


SELECT *
FROM expenses
WHERE id = 1;

SELECT
    id,
    expense_id,
    employee_id,
    employee_name,
    amount,
    approval_status,
    funding_status
FROM expenses
ORDER BY id ASC;

SELECT *
FROM funding_claims
ORDER BY id DESC;

WHERE id = :expense_id

SELECT *
FROM expenses
WHERE id = 6;

SELECT *
FROM funding_claims
ORDER BY id DESC;

WHERE id = 6

SELECT *
FROM expenses
WHERE id = 6;

SELECT
    id,
    expense_id,
    employee_id,
    employee_name,
    amount,
    approval_status,
    funding_status
FROM expenses
WHERE id = 6;

USE expense_management;


SELECT *
FROM expenses
WHERE id = 6;

WHERE id = :expense_id

SELECT *
FROM expenses
WHERE id = 6;

UPDATE expenses
SET funding_status = 'PENDING'
WHERE id = 6;

SELECT
    id,
    expense_id,
    employee_id,
    employee_name,
    amount,
    approval_status,
    funding_status,
    claim_id
FROM expenses
WHERE id = 6;

UPDATE expenses
SET funding_status = 'PENDING'
WHERE id = 6;

SELECT
    id,
    expense_id,
    employee_id,
    employee_name,
    amount,
    approval_status,
    funding_status,
    claim_id
FROM expenses
WHERE id = 6;

SELECT *
FROM expenses
WHERE id = 6;

WHERE id = :expense_id

USE expense_management;

SELECT *
FROM expenses
WHERE id = 6;

USE expense_management;

SELECT
    id,
    expense_id,
    employee_id,
    employee_name,
    amount,
    approval_status,
    funding_status,
    claim_id
FROM expenses
WHERE id = 6;





SELECT *
FROM expenses
WHERE id = 6;



SELECT *
FROM expenses
WHERE expense_id = 'EXP-0003';

SELECT
    id,
    expense_id,
    employee_id,
    employee_name,
    amount,
    approval_status,
    funding_status
FROM expenses
WHERE id = 6;

SELECT
    id,
    funding_status
FROM funding_claims
WHERE expense_id = :expense_id
LIMIT 1


WHERE expense_id = :expense_id

SELECT
    id,
    funding_status
FROM funding_claims
WHERE expense_id = 6
LIMIT 1;

USE expense_management;

ALTER TABLE funding_claims
ADD COLUMN expense_id INT NULL;

DESCRIBE funding_claims;

SELECT
    id,
    expense_id,
    funding_status
FROM funding_claims
WHERE expense_id = 6
LIMIT 1;

USE expense_management;

ALTER TABLE funding_claims
ADD COLUMN employee_id INT NULL,
ADD COLUMN employee_name VARCHAR(100) NULL,
ADD COLUMN amount DECIMAL(12,2) NULL,
ADD COLUMN description TEXT NULL;

DESCRIBE funding_claims;

SELECT DATABASE();

DESCRIBE funding_claims;

SELECT
    COLUMN_NAME,
    DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'expense_management'
AND TABLE_NAME = 'funding_claims'
ORDER BY ORDINAL_POSITION;

SELECT
    COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'expense_management'
AND TABLE_NAME = 'funding_claims'
AND COLUMN_NAME IN (
    'employee_id',
    'employee_name',
    'expense_id',
    'amount',
    'description',
    'funding_status'


ALTER TABLE expense_management.funding_claims
ADD COLUMN employee_id INT NULL;

SELECT
    DATABASE() AS current_database,
    @@hostname AS mysql_host,
    @@port AS mysql_port;
    
    SELECT
    COLUMN_NAME,
    DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'expense_management'
AND TABLE_NAME = 'funding_claims'
ORDER BY ORDINAL_POSITION;

SELECT
    id,
    employee_id,
    employee_name,
    expense_id,
    amount,
    description,
    funding_status
FROM expense_management.funding_claims
LIMIT 5;

USE expense_management;

DESCRIBE funding_claims;

SELECT
    COLUMN_NAME,
    DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'expense_management'
AND TABLE_NAME = 'funding_claims'
ORDER BY ORDINAL_POSITION;

SELECT
    id,
    employee_id,
    employee_name,
    expense_id,
    amount,
    description,
    funding_status
FROM expense_management.funding_claims
LIMIT 5;

USE expense_management;

DESCRIBE funding_claims;

ALTER TABLE funding_claims
ADD COLUMN expense_id INT NULL,
ADD COLUMN amount DECIMAL(12,2) NULL,
ADD COLUMN description TEXT NULL;

USE expense_management;

DESCRIBE funding_claims;

SHOW CREATE TABLE funding_claims;


DESCRIBE funding_claims;

USE expense_management;

DESCRIBE funding_claims;

SELECT COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'expense_management'
AND TABLE_NAME = 'funding_claims'
ORDER BY ORDINAL_POSITION;

SELECT
    employee_id,
    employee_name,
    expense_id,
    amount,
    description,
    funding_status
FROM funding_claims
LIMIT 1;

WHERE expense_id = 6

SELECT
    id,
    expense_id,
    employee_id,
    employee_name,
    amount,
    approval_status,
    funding_status
FROM expenses
WHERE id = 6;

SELECT
    id,
    claim_id,
    employee_id,
    employee_name,
    expense_id,
    amount,
    description,
    funding_status
FROM funding_claims
WHERE expense_id = 6;

SELECT *
FROM funding_claims
WHERE expense_id = 6;

USE expense_management;

SHOW CREATE TABLE funding_claims;

WHERE expense_id = :expense_id

WHERE expense_id = :expense_id

USE expense_management;

SELECT *
FROM funding_claims
WHERE expense_id = 6;

SELECT *
FROM funding_claims
WHERE expense_id = :expense_id;

USE expense_management;

SELECT
    id,
    claim_id,
    employee_id,
    employee_name,
    expense_id,
    amount,
    description,
    funding_status
FROM funding_claims
WHERE expense_id = 6
LIMIT 1;

WHERE expense_id = :expense_id


SELECT *
FROM funding_claims
WHERE expense_id = 1;

SELECT *
FROM funding_claims
WHERE expense_id = 5;

SELECT *
FROM funding_claims
ORDER BY id DESC;

SELECT *
FROM expenses
ORDER BY id DESC;

WHERE expense_id = :expense_id


USE expense_management;

SELECT
    id,
    expense_id,
    employee_id,
    employee_name,
    amount,
    approval_status,
    funding_status
FROM expenses
ORDER BY id DESC;

SELECT
    id,
    claim_id,
    employee_id,
    employee_name,
    expense_id,
    amount,
    funding_status
FROM funding_claims
ORDER BY id DESC;

FROM expenses
WHERE id = 1

SELECT *
FROM expenses
WHERE id = 1;

USE expense_management;

SELECT *
FROM expenses
WHERE id = 1;

DESCRIBE expenses;
SELECT *
FROM funding_claims;

SELECT ...
FROM expenses
WHERE id = 1
LIMIT 1

SELECT id, expense_id, employee_id, employee_name, amount, approval_status, funding_status
FROM expenses
ORDER BY id;

USE expense_management;

SELECT *
FROM funding_claims
ORDER BY id DESC
LIMIT 5;

SELECT
    id,
    expense_id,
    employee_id,
    employee_name,
    amount,
    approval_status,
    funding_status,
    claim_id
FROM expenses
WHERE id = 2;

USE expense_management;

SELECT
    id,
    claim_id,
    employee_id,
    employee_name,
    expense_id,
    amount,
    funding_status,
    submission_date
FROM funding_claims
ORDER BY id DESC;

SELECT
    id,
    claim_id,
    expense_id,
    amount,
    funding_status
FROM funding_claims
WHERE id = 2;


SELECT
    id,
    expense_id,
    approval_status,
    funding_status,
    claim_id
FROM expenses
WHERE id = 2;

SELECT
    id,
    claim_id,
    expense_id,
    amount,
    funding_status
FROM funding_claims
WHERE id = 2;

UPDATE funding_claims
SET
    funding_status = 'PAID',
    payment_date = NOW(),
    payment_reference = 'PAY-0002'
WHERE id = 2;

UPDATE expenses
SET
    funding_status = 'PAID',
    funding_payment_date = NOW(),
    funding_payment_reference = 'PAY-0002',
    employee_payment_status = 'PAID',
    employee_payment_date = NOW(),
    employee_payment_reference = 'PAY-0002'
WHERE id = 2;

DESCRIBE funding_claims;

DESCRIBE expenses;

ALTER TABLE expenses
ADD COLUMN funding_payment_date DATETIME NULL,
ADD COLUMN funding_payment_reference VARCHAR(100) NULL,
ADD COLUMN employee_payment_status VARCHAR(20) DEFAULT 'UNPAID',
ADD COLUMN employee_payment_date DATETIME NULL,
ADD COLUMN employee_payment_reference VARCHAR(100) NULL;

DESCRIBE expenses;

SELECT
    COLUMN_NAME,
    DATA_TYPE,
    COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'expense_management'
  AND TABLE_NAME = 'expenses'
  AND COLUMN_NAME IN (
      'funding_payment_date',
      'funding_payment_reference',
      'employee_payment_status',
      'employee_payment_date',
      'employee_payment_reference'
  );
  
  
  USE expense_management;

SELECT
    id,
    claim_id,
    expense_id,
    amount,
    funding_status,
    payment_date,
    payment_reference
FROM funding_claims
WHERE id = 2;


SELECT
    id,
    expense_id,
    approval_status,
    funding_status,
    claim_id,
    employee_payment_status,
    employee_payment_date,
    employee_payment_reference,
    funding_payment_date,
    funding_payment_reference
FROM expenses
WHERE id = 2;


SELECT
    id,
    expense_id,
    employee_name,
    project,
    amount,
    approval_status,
    funding_status,
    claim_id,
    employee_payment_status
FROM expenses
ORDER BY id DESC;

SELECT
    id,
    claim_id,
    expense_id,
    amount,
    funding_status,
    payment_date,
    payment_reference
FROM funding_claims
ORDER BY id DESC;

SELECT
    id,
    claim_id,
    expense_id,
    funding_status,
    payment_date,
    payment_reference
FROM funding_claims
ORDER BY id DESC;

SELECT
    id,
    expense_id,
    employee_name,
    amount,
    approval_status,
    funding_status,
    funding_payment_date,
    funding_payment_reference,
    employee_payment_status,
    employee_payment_date,
    employee_payment_reference
FROM expenses
ORDER BY id DESC;

SELECT
    id,
    claim_id,
    employee_id,
    employee_name,
    expense_id,
    amount,
    funding_status,
    payment_date,
    payment_reference
FROM funding_claims
ORDER BY id DESC;


WHERE id = 3

WHERE claim_id = 'CLM-0003'

WHERE claim_id = 'CLM-0003';

USE expense_management;

SELECT *
FROM funding_claims
WHERE claim_id = 'CLM-0003';

SELECT
    id,
    claim_id,
    employee_id,
    employee_name,
    expense_id,
    amount,
    funding_status,
    claim_date,
    submission_date,
    payment_date,
    payment_reference
FROM funding_claims
ORDER BY id DESC;

UPDATE funding_claims
SET
    funding_status = 'PAID',
    payment_date = NOW(),
    payment_reference = 'PAY-0003'
WHERE claim_id = 'CLM-0003';

SELECT
    id,
    claim_id,
    funding_status,
    payment_date,
    payment_reference
FROM funding_claims
WHERE claim_id = 'CLM-0003';

SELECT id, claim_id, funding_status
FROM funding_claims
ORDER BY id;

SELECT id, claim_id, funding_status, expense_id
FROM funding_claims
ORDER BY id;


USE expense_management;

SELECT
    id,
    claim_id,
    expense_id,
    amount,
    funding_status,
    payment_date,
    payment_reference
FROM funding_claims
ORDER BY id DESC;

USE expense_management;

SELECT
    id,
    claim_id,
    expense_id,
    amount,
    funding_status,
    payment_date,
    payment_reference
FROM funding_claims
ORDER BY id ASC;

DESCRIBE funding_claims;
UPDATE funding_claims
SET total_amount = amount
WHERE total_amount IS NULL
  AND amount IS NOT NULL;
  
  
  UPDATE funding_claims
SET total_amount = amount
WHERE total_amount IS NULL
  AND amount IS NOT NULL;
  
UPDATE funding_claims
SET total_amount = amount
WHERE id > 0
  AND total_amount IS NULL
  AND amount IS NOT NULL;
  
SELECT id, claim_id, amount, total_amount
FROM funding_claims
ORDER BY id;

UPDATE funding_claims
SET total_amount = amount
WHERE id > 0
  AND total_amount IS NULL
  AND amount IS NOT NULL;
  
SELECT
    id,
    claim_id,
    amount,
    total_amount,
    funding_status,
    payment_date,
    payment_reference
FROM funding_claims
ORDER BY id DESC;

UPDATE funding_claims
SET total_amount = amount
WHERE id > 0
  AND total_amount IS NULL
  AND amount IS NOT NULL;
  
SELECT
    id,
    claim_id,
    employee_id,
    employee_name,
    expense_id,
    amount,
    total_amount,
    funding_status,
    payment_date,
    payment_reference
FROM funding_claims
ORDER BY id DESC;


SELECT
    id,
    claim_id,
    expense_id,
    amount,
    total_amount,
    funding_status
FROM funding_claims
WHERE id = 1;


SELECT
    id,
    expense_id,
    amount,
    approval_status,
    funding_status
FROM expenses
WHERE id = 3;


UPDATE funding_claims
SET total_amount = 1000
WHERE id = 1;


SELECT
    id,
    claim_id,
    expense_id,
    total_amount,
    funding_status,
    payment_date,
    payment_reference
FROM funding_claims
WHERE id = 1;


SELECT
    id,
    expense_id,
    amount,
    funding_status,
    funding_payment_date,
    funding_payment_reference
FROM expenses
WHERE id = 3;

USE expense_management;

SELECT * FROM expenses;


SELECT id FROM expenses ORDER BY id;

DESCRIBE funding_claims;

SELECT id, claim_id, total_amount, funding_status,
       payment_date, payment_reference
FROM funding_claims
ORDER BY id DESC;