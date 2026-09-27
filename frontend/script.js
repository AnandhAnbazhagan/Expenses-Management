/* =========================================================
   API CONFIGURATION
========================================================= */

const API_BASE_URL = "http://127.0.0.1:8000";


/* =========================================================
   API REQUEST HELPER
========================================================= */

async function apiRequest(endpoint, options = {}) {

    try {

        const config = {
            ...options,
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
                ...(options.headers || {})
            }
        };

        const response = await fetch(
            API_BASE_URL + endpoint,
            config
        );

        let data = null;

        const contentType =
            response.headers.get("content-type");

        if (
            contentType &&
            contentType.includes("application/json")
        ) {
            data = await response.json();
        }

        if (!response.ok) {

            let message = "Request failed.";

            if (data) {

                if (typeof data.detail === "string") {
                    message = data.detail;
                }

                else if (Array.isArray(data.detail)) {

                    message = data.detail
                        .map(item => item.msg || "Validation error")
                        .join(", ");
                }
            }

            throw new Error(message);
        }

        return data;

    }

    catch (error) {

        console.error(
            "API ERROR:",
            endpoint,
            error
        );

        if (error instanceof TypeError) {

            throw new Error(
                "Failed to connect to the backend. Make sure FastAPI is running on http://127.0.0.1:8000"
            );
        }

        throw error;
    }
}


async function submitReimbursement() {

    const expenseId = document.getElementById("expenseId").value;
    const amount = document.getElementById("amount").value;
    const reason = document.getElementById("reason").value;

    try {

        const response = await fetch(
            `http://127.0.0.1:8000/api/expenses/${expenseId}/employee-payment`,
            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    amount: Number(amount),
                    reason: reason
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Failed to submit reimbursement");
        }

        alert("Reimbursement submitted successfully!");

        window.location.href = "reimbursements.html";

    } catch (error) {

        console.error("Reimbursement Error:", error);

        alert(error.message);
    }
}


/* =========================================================
   CURRENT USER
========================================================= */

function getCurrentUser() {

    const storedUser =
        localStorage.getItem("user");

    if (!storedUser) {
        return null;
    }

    try {

        const data =
            JSON.parse(storedUser);

        return data.user || data;

    }

    catch (error) {

        console.error(
            "Invalid user data:",
            error
        );

        return null;
    }
}


/* =========================================================
   DISPLAY CURRENT USER
========================================================= */

function displayCurrentUser() {

    const user =
        getCurrentUser();

    if (!user) {
        return;
    }

    const nameElement =
        document.getElementById("userName");

    const avatarElement =
        document.getElementById("userAvatar");

    const name =
        user.name ||
        user.email ||
        "User";

    if (nameElement) {
        nameElement.textContent = name;
    }

    if (avatarElement) {

        avatarElement.textContent =
            name
                .charAt(0)
                .toUpperCase();
    }
}


/* =========================================================
   LOGOUT
========================================================= */

function logout() {

    localStorage.removeItem("user");

    window.location.href =
        "index.html";
}


/* =========================================================
   EMPLOYEE ACCESS
========================================================= */

function checkEmployeeAccess() {

    const user =
        getCurrentUser();

    if (!user) {

        window.location.href =
            "index.html";

        return false;
    }

    const role =
        String(user.role || "")
            .toUpperCase();

    if (role !== "EMPLOYEE") {

        alert(
            "Employee access required."
        );

        window.location.href =
            "dashboard.html";

        return false;
    }

    return true;
}


/* =========================================================
   CEO / ADMIN ACCESS
========================================================= */

function checkCEOAccess() {

    const user =
        getCurrentUser();

    if (!user) {

        window.location.href =
            "index.html";

        return false;
    }

    const role =
        String(user.role || "")
            .toUpperCase();

    if (
        role !== "CEO" &&
        role !== "ADMIN"
    ) {

        alert(
            "CEO/Admin access required."
        );

        window.location.href =
            "employee-dashboard.html";

        return false;
    }

    return true;
}


/* =========================================================
   LOGIN
========================================================= */

async function loginUser(email, password) {

    const response =
        await apiRequest(
            "/api/login",
            {
                method: "POST",

                body: JSON.stringify({
                    email: email,
                    password: password
                })
            }
        );

    localStorage.setItem(
        "user",
        JSON.stringify(response)
    );

    const user =
        response.user || response;

    const role =
        String(user.role || "")
            .toUpperCase();

    if (
        role === "CEO" ||
        role === "ADMIN"
    ) {

        window.location.href =
            "dashboard.html";

    }

    else {

        window.location.href =
            "employee-dashboard.html";
    }
}


/* =========================================================
   LOGIN FORM
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        displayCurrentUser();

        const loginForm =
            document.getElementById("loginForm");

        if (!loginForm) {
            return;
        }

        loginForm.addEventListener(
            "submit",
            async function (event) {

                event.preventDefault();

                const email =
                    document
                        .getElementById("email")
                        .value
                        .trim();

                const password =
                    document
                        .getElementById("password")
                        .value;

                const button =
                    document.getElementById(
                        "loginBtn"
                    );

                const message =
                    document.getElementById(
                        "loginMessage"
                    );

                button.disabled = true;

                button.textContent =
                    "Logging in...";

                message.textContent =
                    "Checking login...";

                message.style.color =
                    "#64748b";

                try {

                    await loginUser(
                        email,
                        password
                    );

                }

                catch (error) {

                    console.error(
                        "Login error:",
                        error
                    );

                    message.textContent =
                        error.message ||
                        "Login failed.";

                    message.style.color =
                        "#dc2626";

                    button.disabled =
                        false;

                    button.textContent =
                        "Login";
                }
            }
        );
    }
);


/* =========================================================
   SET TODAY DATE
========================================================= */

function setTodayDate() {

    const input =
        document.getElementById("date");

    if (!input) {
        return;
    }

    const today =
        new Date();

    const year =
        today.getFullYear();

    const month =
        String(
            today.getMonth() + 1
        ).padStart(2, "0");

    const day =
        String(
            today.getDate()
        ).padStart(2, "0");

    input.value =
        `${year}-${month}-${day}`;
}


/* =========================================================
   SUBMIT EXPENSE
========================================================= */

async function submitExpense(event) {

    event.preventDefault();

    const user =
        getCurrentUser();

    if (!user) {

        alert(
            "Please login first."
        );

        window.location.href =
            "index.html";

        return;
    }

    const employeeId =
        Number(user.id);

    if (!employeeId) {

        alert(
            "Employee ID is missing. Please login again."
        );

        return;
    }

    const project =
        document
            .getElementById("project")
            .value
            .trim();

    const date =
        document
            .getElementById("date")
            .value;

    const category =
        document
            .getElementById("category")
            .value;

    const description =
        document
            .getElementById("description")
            .value
            .trim();

    const amount =
        Number(
            document
                .getElementById("amount")
                .value
        );

    const message =
        document.getElementById(
            "expenseMessage"
        );

    const button =
        document.getElementById(
            "submitExpenseBtn"
        );

    if (!project) {

        message.textContent =
            "Please enter the project name.";

        message.style.color =
            "#dc2626";

        return;
    }

    if (!date) {

        message.textContent =
            "Please select the expense date.";

        message.style.color =
            "#dc2626";

        return;
    }

    if (!category) {

        message.textContent =
            "Please select a category.";

        message.style.color =
            "#dc2626";

        return;
    }

    if (!description) {

        message.textContent =
            "Please enter a description.";

        message.style.color =
            "#dc2626";

        return;
    }

    if (!amount || amount <= 0) {

        message.textContent =
            "Please enter a valid amount.";

        message.style.color =
            "#dc2626";

        return;
    }

    const expenseData = {

        employee_id:
            employeeId,

        project:
            project,

        date:
            date,

        category:
            category,

        description:
            description,

        amount:
            amount
    };

    button.disabled = true;

    button.textContent =
        "Submitting...";

    message.textContent =
        "Submitting expense...";

    message.style.color =
        "#64748b";

    try {

        await apiRequest(
            "/api/expenses",
            {
                method: "POST",

                body:
                    JSON.stringify(
                        expenseData
                    )
            }
        );

        message.textContent =
            "Expense submitted successfully.";

        message.style.color =
            "#16a34a";

        alert(
            "Expense submitted successfully!"
        );

        window.location.href =
            "employee-expenses.html";

    }

    catch (error) {

        console.error(
            "Expense submission error:",
            error
        );

        message.textContent =
            error.message ||
            "Failed to submit expense.";

        message.style.color =
            "#dc2626";

        button.disabled =
            false;

        button.textContent =
            "Submit Expense";
    }
}


/* =========================================================
   LOAD EMPLOYEE EXPENSES
========================================================= */

async function loadEmployeeExpenses() {

    const user =
        getCurrentUser();

    const table =
        document.getElementById(
            "employeeExpensesTable"
        );

    if (!user || !table) {
        return;
    }

    table.innerHTML = `
        <tr>
            <td colspan="7">
                Loading expenses...
            </td>
        </tr>
    `;

    try {

        const response =
            await apiRequest(
                "/api/expenses"
            );

        const allExpenses =
            response.expenses || [];

        const employeeId =
            Number(user.id);

        const expenses =
            allExpenses.filter(
                expense =>
                    Number(
                        expense.employee_id
                    ) === employeeId
            );

        table.innerHTML = "";

        if (!expenses.length) {

            table.innerHTML = `
                <tr>
                    <td colspan="7">
                        No expenses found.
                    </td>
                </tr>
            `;

            return;
        }

        expenses.forEach(
            expense => {

                const row =
                    document.createElement("tr");

                row.innerHTML = `

                    <td>
                        ${escapeHTML(
                            expense.expense_id ||
                            expense.id ||
                            "-"
                        )}
                    </td>

                    <td>
                        ${escapeHTML(
                            expense.project ||
                            "-"
                        )}
                    </td>

                    <td>
                        ${escapeHTML(
                            expense.date ||
                            "-"
                        )}
                    </td>

                    <td>
                        ${escapeHTML(
                            expense.category ||
                            "-"
                        )}
                    </td>

                    <td>
                        ${escapeHTML(
                            expense.description ||
                            "-"
                        )}
                    </td>

                    <td>
                        ₹${Number(
                            expense.amount || 0
                        ).toLocaleString("en-IN")}
                    </td>

                    <td>
                        ${getStatusBadge(
                            expense.approval_status
                        )}
                    </td>
                `;

                table.appendChild(row);
            }
        );
    }

    catch (error) {

        console.error(error);

        table.innerHTML = `
            <tr>
                <td colspan="7">
                    Failed to load expenses:
                    ${escapeHTML(error.message)}
                </td>
            </tr>
        `;
    }
}


/* =========================================================
   EMPLOYEE DASHBOARD
========================================================= */

async function loadEmployeeDashboard() {

    const user =
        getCurrentUser();

    if (!user) {
        return;
    }

    try {

        const response =
            await apiRequest(
                "/api/expenses"
            );

        const allExpenses =
            response.expenses || [];

        const expenses =
            allExpenses.filter(
                expense =>
                    Number(
                        expense.employee_id
                    ) === Number(user.id)
            );

        let pending = 0;
        let approved = 0;
        let total = 0;

        expenses.forEach(
            expense => {

                const status =
                    String(
                        expense.approval_status ||
                        "PENDING"
                    ).toUpperCase();

                if (status === "PENDING") {
                    pending++;
                }

                if (status === "APPROVED") {
                    approved++;
                }

                total +=
                    Number(
                        expense.amount || 0
                    );
            }
        );

        setText(
            "expenseCount",
            expenses.length
        );

        setText(
            "pendingCount",
            pending
        );

        setText(
            "approvedCount",
            approved
        );

        setText(
            "amountTotal",
            "₹" +
            total.toLocaleString("en-IN")
        );
    }

    catch (error) {

        console.error(
            "Employee dashboard error:",
            error
        );
    }
}


/* =========================================================
   LOAD EMPLOYEE CLAIMS
========================================================= */

async function loadEmployeeClaims() {

    const user =
        getCurrentUser();

    const table =
        document.getElementById(
            "employeeClaimsTable"
        );

    if (!user || !table) {
        return;
    }

    try {

        const response =
            await apiRequest(
                "/api/claims"
            );

        const allClaims =
            response.claims || [];

        const claims =
            allClaims.filter(
                claim =>
                    Number(
                        claim.employee_id
                    ) === Number(user.id)
            );

        let pending = 0;
        let approved = 0;
        let total = 0;

        claims.forEach(
            claim => {

                const status =
                    String(
                        claim.funding_status ||
                        "PENDING"
                    ).toUpperCase();

                if (status === "PENDING") {
                    pending++;
                }

                if (status === "APPROVED") {
                    approved++;
                }

                total +=
                    Number(
                        claim.amount || 0
                    );
            }
        );

        setText(
            "claimCount",
            claims.length
        );

        setText(
            "claimPending",
            pending
        );

        setText(
            "claimApproved",
            approved
        );

        setText(
            "claimAmount",
            "₹" +
            total.toLocaleString("en-IN")
        );

        table.innerHTML = "";

        if (!claims.length) {

            table.innerHTML = `
                <tr>
                    <td colspan="6">
                        No reimbursement claims found.
                    </td>
                </tr>
            `;

            return;
        }

        claims.forEach(
            claim => {

                const row =
                    document.createElement("tr");

                const status =
                    claim.funding_status ||
                    "PENDING";

                row.innerHTML = `

                    <td>
                        ${escapeHTML(
                            claim.id || "-"
                        )}
                    </td>

                    <td>
                        ${escapeHTML(
                            claim.expense_id || "-"
                        )}
                    </td>

                    <td>
                        ₹${Number(
                            claim.amount || 0
                        ).toLocaleString("en-IN")}
                    </td>

                    <td>
                        ${escapeHTML(
                            claim.description || "-"
                        )}
                    </td>

                    <td>
                        ${getStatusBadge(status)}
                    </td>

                    <td>
                        ${escapeHTML(
                            claim.created_at || "-"
                        )}
                    </td>
                `;

                table.appendChild(row);
            }
        );
    }

    catch (error) {

        console.error(
            "Employee claims error:",
            error
        );

        table.innerHTML = `
            <tr>
                <td colspan="6">
                    Failed to load claims:
                    ${escapeHTML(error.message)}
                </td>
            </tr>
        `;
    }
}


/* =========================================================
   SUBMIT CLAIM
========================================================= */

async function submitClaim(event) {

    event.preventDefault();

    const user =
        getCurrentUser();

    if (!user) {

        alert(
            "Please login first."
        );

        window.location.href =
            "index.html";

        return;
    }

    const employeeId =
        Number(user.id);

    const expenseId =
        Number(
            document
                .getElementById("expenseId")
                .value
        );

    const amount =
        Number(
            document
                .getElementById("claimAmount")
                .value
        );

    const description =
        document
            .getElementById("claimDescription")
            .value
            .trim();

    const message =
        document.getElementById(
            "claimMessage"
        );

    const button =
        document.getElementById(
            "submitClaimBtn"
        );

    /* IMPORTANT:
       expense_id MUST be an integer
       such as 1, 2, 3.
       
       Do NOT send:
       EXP-0001
    */

    if (
        !Number.isInteger(expenseId) ||
        expenseId <= 0
    ) {

        message.textContent =
            "Please enter a valid numeric Expense ID.";

        message.style.color =
            "#dc2626";

        return;
    }

    if (!amount || amount <= 0) {

        message.textContent =
            "Please enter a valid amount.";

        message.style.color =
            "#dc2626";

        return;
    }

    if (!description) {

        message.textContent =
            "Please enter a description.";

        message.style.color =
            "#dc2626";

        return;
    }

    const claimData = {

        employee_id:
            employeeId,

        expense_id:
            expenseId,

        amount:
            amount,

        description:
            description
    };

    button.disabled = true;

    button.textContent =
        "Submitting...";

    try {

        await apiRequest(
            "/api/claims",
            {
                method: "POST",

                body:
                    JSON.stringify(
                        claimData
                    )
            }
        );

        message.textContent =
            "Claim submitted successfully!";

        message.style.color =
            "#16a34a";

        alert(
            "Reimbursement claim submitted successfully."
        );

        window.location.href =
            "employee-claims.html";
    }

    catch (error) {

        console.error(
            "Claim error:",
            error
        );

        message.textContent =
            error.message ||
            "Failed to submit claim.";

        message.style.color =
            "#dc2626";

        button.disabled = false;

        button.textContent =
            "Submit Claim";
    }
}


/* =========================================================
   CEO DASHBOARD
========================================================= */

async function loadCEODashboard() {

    try {

        const usersResponse =
            await apiRequest(
                "/api/users"
            );

        const expensesResponse =
            await apiRequest(
                "/api/expenses"
            );

        const users =
            usersResponse.users || [];

        const expenses =
            expensesResponse.expenses || [];

        let pending = 0;
        let total = 0;

        expenses.forEach(
            expense => {

                const status =
                    String(
                        expense.approval_status ||
                        "PENDING"
                    ).toUpperCase();

                if (status === "PENDING") {
                    pending++;
                }

                total +=
                    Number(
                        expense.amount || 0
                    );
            }
        );

        setText(
            "totalUsers",
            users.length
        );

        setText(
            "totalExpenses",
            expenses.length
        );

        setText(
            "pendingExpenses",
            pending
        );

        setText(
            "totalExpenseAmount",
            "₹" +
            total.toLocaleString("en-IN")
        );

    }

    catch (error) {

        console.error(
            "CEO dashboard error:",
            error
        );
    }
}


/* =========================================================
   LOAD USERS
========================================================= */

async function loadUsers() {

    const table =
        document.getElementById(
            "usersTable"
        );

    if (!table) {
        return;
    }

    table.innerHTML = `
        <tr>
            <td colspan="6">
                Loading users...
            </td>
        </tr>
    `;

    try {

        const response =
            await apiRequest(
                "/api/users"
            );

        const users =
            response.users || [];

        table.innerHTML = "";

        if (!users.length) {

            table.innerHTML = `
                <tr>
                    <td colspan="6">
                        No users found.
                    </td>
                </tr>
            `;

            return;
        }

        users.forEach(
            user => {

                const row =
                    document.createElement("tr");

                row.innerHTML = `

                    <td>
                        ${escapeHTML(user.id)}
                    </td>

                    <td>
                        ${escapeHTML(user.name)}
                    </td>

                    <td>
                        ${escapeHTML(user.email)}
                    </td>

                    <td>
                        ${escapeHTML(user.role)}
                    </td>

                    <td>
                        ${
                            Number(user.active) === 1
                                ? getStatusBadge("APPROVED")
                                : getStatusBadge("REJECTED")
                        }
                    </td>

                    <td>
                        ${escapeHTML(
                            user.created_at || "-"
                        )}
                    </td>
                `;

                table.appendChild(row);
            }
        );
    }

    catch (error) {

        console.error(
            "Users error:",
            error
        );

        table.innerHTML = `
            <tr>
                <td colspan="6">
                    Failed to load users:
                    ${escapeHTML(error.message)}
                </td>
            </tr>
        `;
    }
}


/* =========================================================
   LOAD CEO EXPENSES
========================================================= */

async function loadCEOExpenses() {

    const table =
        document.getElementById(
            "expensesTable"
        );

    if (!table) {
        return;
    }

    table.innerHTML = `
        <tr>
            <td colspan="8">
                Loading expenses...
            </td>
        </tr>
    `;

    try {

        const response =
            await apiRequest(
                "/api/expenses"
            );

        const expenses =
            response.expenses || [];

        let pending = 0;
        let approved = 0;
        let total = 0;

        expenses.forEach(
            expense => {

                const status =
                    String(
                        expense.approval_status ||
                        "PENDING"
                    ).toUpperCase();

                if (status === "PENDING") {
                    pending++;
                }

                if (status === "APPROVED") {
                    approved++;
                }

                total +=
                    Number(
                        expense.amount || 0
                    );
            }
        );

        setText(
            "expenseCount",
            expenses.length
        );

        setText(
            "pendingCount",
            pending
        );

        setText(
            "approvedCount",
            approved
        );

        setText(
            "amountTotal",
            "₹" +
            total.toLocaleString("en-IN")
        );

        table.innerHTML = "";

        if (!expenses.length) {

            table.innerHTML = `
                <tr>
                    <td colspan="8">
                        No expenses found.
                    </td>
                </tr>
            `;

            return;
        }

        expenses.forEach(
            expense => {

                const row =
                    document.createElement("tr");

                const status =
                    String(
                        expense.approval_status ||
                        "PENDING"
                    ).toUpperCase();

                let actions = "";

                if (status === "PENDING") {

                    actions = `

                        <button
                            class="approve-btn"
                            onclick="approveExpense(${Number(expense.id)})"
                        >
                            Approve
                        </button>

                        <button
                            class="reject-btn"
                            onclick="rejectExpense(${Number(expense.id)})"
                        >
                            Reject
                        </button>
                    `;
                }

                actions += `

                    <button
                        class="delete-btn"
                        onclick="deleteExpense(${Number(expense.id)})"
                    >
                        Delete
                    </button>
                `;

                row.innerHTML = `

                    <td>
                        ${escapeHTML(
                            expense.expense_id ||
                            expense.id ||
                            "-"
                        )}
                    </td>

                    <td>
                        ${escapeHTML(
                            expense.employee_name ||
                            "-"
                        )}
                    </td>

                    <td>
                        ${escapeHTML(
                            expense.project ||
                            "-"
                        )}
                    </td>

                    <td>
                        ${escapeHTML(
                            expense.date ||
                            "-"
                        )}
                    </td>

                    <td>
                        ${escapeHTML(
                            expense.category ||
                            "-"
                        )}
                    </td>

                    <td>
                        ₹${Number(
                            expense.amount || 0
                        ).toLocaleString("en-IN")}
                    </td>

                    <td>
                        ${getStatusBadge(status)}
                    </td>

                    <td>
                        <div class="action-buttons">
                            ${actions}
                        </div>
                    </td>
                `;

                table.appendChild(row);
            }
        );
    }

    catch (error) {

        console.error(
            "CEO expense error:",
            error
        );

        table.innerHTML = `
            <tr>
                <td colspan="8">
                    Failed to load expenses:
                    ${escapeHTML(error.message)}
                </td>
            </tr>
        `;
    }
}


/* =========================================================
   APPROVE EXPENSE
========================================================= */

async function approveExpense(id) {

    const expenseId =
        Number(id);

    if (
        !Number.isInteger(expenseId) ||
        expenseId <= 0
    ) {

        alert(
            "Invalid expense ID."
        );

        return;
    }

    if (
        !confirm(
            "Approve this expense?"
        )
    ) {
        return;
    }

    try {

        await apiRequest(
            `/api/expenses/${expenseId}/approve`,
            {
                method: "PUT"
            }
        );

        alert(
            "Expense approved successfully."
        );

        await loadCEOExpenses();

    }

    catch (error) {

        console.error(
            "Approve expense error:",
            error
        );

        alert(
            error.message ||
            "Failed to approve expense."
        );
    }
}


/* =========================================================
   REJECT EXPENSE
========================================================= */

async function rejectExpense(id) {

    const expenseId =
        Number(id);

    if (
        !Number.isInteger(expenseId) ||
        expenseId <= 0
    ) {

        alert(
            "Invalid expense ID."
        );

        return;
    }

    if (
        !confirm(
            "Reject this expense?"
        )
    ) {
        return;
    }

    try {

        await apiRequest(
            `/api/expenses/${expenseId}/reject`,
            {
                method: "PUT"
            }
        );

        alert(
            "Expense rejected successfully."
        );

        await loadCEOExpenses();

    }

    catch (error) {

        console.error(
            "Reject expense error:",
            error
        );

        alert(
            error.message ||
            "Failed to reject expense."
        );
    }
}


/* =========================================================
   DELETE EXPENSE
========================================================= */

async function deleteExpense(id) {

    const expenseId =
        Number(id);

    if (
        !Number.isInteger(expenseId) ||
        expenseId <= 0
    ) {

        alert(
            "Invalid expense ID."
        );

        return;
    }

    if (
        !confirm(
            "Delete this expense permanently?"
        )
    ) {
        return;
    }

    try {

        await apiRequest(
            `/api/expenses/${expenseId}`,
            {
                method: "DELETE"
            }
        );

        alert(
            "Expense deleted successfully."
        );

        await loadCEOExpenses();

    }

    catch (error) {

        console.error(
            "Delete expense error:",
            error
        );

        alert(
            error.message ||
            "Failed to delete expense."
        );
    }
}


/* =========================================================
   LOAD CEO CLAIMS
========================================================= */

async function loadCEOClaims() {

    const table =
        document.getElementById(
            "claimsTable"
        );

    if (!table) {
        return;
    }

    table.innerHTML = `
        <tr>
            <td colspan="7">
                Loading claims...
            </td>
        </tr>
    `;

    try {

        const response =
            await apiRequest(
                "/api/claims"
            );

        const claims =
            response.claims || [];

        let pending = 0;
        let approved = 0;
        let total = 0;

        claims.forEach(
            claim => {

                const status =
                    String(
                        claim.funding_status ||
                        "PENDING"
                    ).toUpperCase();

                if (status === "PENDING") {
                    pending++;
                }

                if (status === "APPROVED") {
                    approved++;
                }

                total +=
                    Number(
                        claim.amount || 0
                    );
            }
        );

        setText(
            "totalClaims",
            claims.length
        );

        setText(
            "pendingClaims",
            pending
        );

        setText(
            "approvedClaims",
            approved
        );

        setText(
            "claimTotalAmount",
            "₹" +
            total.toLocaleString("en-IN")
        );

        table.innerHTML = "";

        if (!claims.length) {

            table.innerHTML = `
                <tr>
                    <td colspan="7">
                        No claims found.
                    </td>
                </tr>
            `;

            return;
        }

        claims.forEach(
            claim => {

                const row =
                    document.createElement("tr");

                /*
                    IMPORTANT:
                    claim.id = funding_claims.id

                    Example:
                    claim.id = 1
                    claim.expense_id = 3

                    Approve must use claim.id.
                */

                const claimId =
                    Number(claim.id);

                const status =
                    String(
                        claim.funding_status ||
                        "PENDING"
                    ).toUpperCase();

                let actions = "";

                if (status === "PENDING") {

                    actions = `

                        <button
                            class="approve-btn"
                            onclick="approveClaim(${claimId})"
                        >
                            Approve
                        </button>

                        <button
                            class="reject-btn"
                            onclick="rejectClaim(${claimId})"
                        >
                            Reject
                        </button>
                    `;
                }

                actions += `

                    <button
                        class="delete-btn"
                        onclick="deleteClaim(${claimId})"
                    >
                        Delete
                    </button>
                `;

                row.innerHTML = `

                    <td>
                        ${escapeHTML(
                            claim.id || "-"
                        )}
                    </td>

                    <td>
                        ${escapeHTML(
                            claim.employee_name ||
                            "-"
                        )}
                    </td>

                    <td>
                        ${escapeHTML(
                            claim.expense_id ||
                            "-"
                        )}
                    </td>

                    <td>
                        ₹${Number(
                            claim.amount || 0
                        ).toLocaleString("en-IN")}
                    </td>

                    <td>
                        ${escapeHTML(
                            claim.description ||
                            "-"
                        )}
                    </td>

                    <td>
                        ${getStatusBadge(status)}
                    </td>

                    <td>
                        <div class="action-buttons">
                            ${actions}
                        </div>
                    </td>
                `;

                table.appendChild(row);
            }
        );
    }

    catch (error) {

        console.error(
            "CEO claims error:",
            error
        );

        table.innerHTML = `
            <tr>
                <td colspan="7">
                    Failed to load claims:
                    ${escapeHTML(error.message)}
                </td>
            </tr>
        `;
    }
}


/* =========================================================
   APPROVE CLAIM
========================================================= */

async function approveClaim(id) {

    const claimId =
        Number(id);

    /*
       VERY IMPORTANT

       This must be the funding_claims.id.

       Example:

       Claim ID = 1
       Expense ID = 3

       URL becomes:

       /api/claims/1/approve

       NOT:

       /api/claims/3/approve
    */

    if (
        !Number.isInteger(claimId) ||
        claimId <= 0
    ) {

        alert(
            "Invalid claim ID."
        );

        return;
    }

    if (
        !confirm(
            "Approve this reimbursement claim?"
        )
    ) {
        return;
    }

    try {

        console.log(
            "Approving claim:",
            claimId
        );

        const response =
            await apiRequest(
                `/api/claims/${claimId}/approve`,
                {
                    method: "PUT"
                }
            );

        console.log(
            "Approve response:",
            response
        );

        alert(
            "Claim approved successfully."
        );

        await loadCEOClaims();

    }

    catch (error) {

        console.error(
            "Approve claim error:",
            error
        );

        alert(
            error.message ||
            "Failed to approve claim."
        );
    }
}


/* =========================================================
   REJECT CLAIM
========================================================= */

async function rejectClaim(id) {

    const claimId =
        Number(id);

    if (
        !Number.isInteger(claimId) ||
        claimId <= 0
    ) {

        alert(
            "Invalid claim ID."
        );

        return;
    }

    if (
        !confirm(
            "Reject this reimbursement claim?"
        )
    ) {
        return;
    }

    try {

        await apiRequest(
            `/api/claims/${claimId}/reject`,
            {
                method: "PUT"
            }
        );

        alert(
            "Claim rejected successfully."
        );

        await loadCEOClaims();

    }

    catch (error) {

        console.error(
            "Reject claim error:",
            error
        );

        alert(
            error.message ||
            "Failed to reject claim."
        );
    }
}


/* =========================================================
   DELETE CLAIM
========================================================= */

async function deleteClaim(id) {

    const claimId =
        Number(id);

    if (
        !Number.isInteger(claimId) ||
        claimId <= 0
    ) {

        alert(
            "Invalid claim ID."
        );

        return;
    }

    if (
        !confirm(
            "Delete this reimbursement claim permanently?"
        )
    ) {
        return;
    }

    try {

        await apiRequest(
            `/api/claims/${claimId}`,
            {
                method: "DELETE"
            }
        );

        alert(
            "Claim deleted successfully."
        );

        await loadCEOClaims();

    }

    catch (error) {

        console.error(
            "Delete claim error:",
            error
        );

        alert(
            error.message ||
            "Failed to delete claim."
        );
    }
}


/* =========================================================
   STATUS BADGE
========================================================= */

function getStatusBadge(status) {

    const value =
        String(
            status ||
            "PENDING"
        ).toUpperCase();

    if (value === "APPROVED") {

        return `
            <span class="status approved">
                APPROVED
            </span>
        `;
    }

    if (value === "REJECTED") {

        return `
            <span class="status rejected">
                REJECTED
            </span>
        `;
    }

    return `
        <span class="status pending">
            PENDING
        </span>
    `;
}


/* =========================================================
   SET TEXT
========================================================= */

function setText(id, value) {

    const element =
        document.getElementById(id);

    if (element) {
        element.textContent = value;
    }
}


/* =========================================================
   ESCAPE HTML
========================================================= */

function escapeHTML(value) {

    return String(value ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}