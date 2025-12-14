# Personal Expense Tracker System

## Overview
The **Personal Expense Tracker** is a robust, Python-based desktop application designed to help individuals and administrators manage financial data effectively. Built with a modern **Tkinter** GUI and a secure **MySQL** database backend, it offers role-based access control, detailed financial reporting, budget planning, and interactive data visualizations.

## Key Features

### 🔐 Authentication & Roles
- **Secure Login/Signup**: Validated user registration with encrypted password handling (conceptually safe).
- **Admin Role**:
  - Full access to the system.
  - **User Management**: View user details and permanently **delete users** (with cascading data removal).
  - **Admin Dashboard**: Global statistics and overview.
- **User Role**:
  - Personal Dashboard with "Welcome" landing page.
  - Manage **Expenses** and **Income**.
  - **Budget Planning**: Set monthly limits for specific categories.
  - **Profile Management**: Update contact details.

### 📊 Dashboard & Analytics
- **Visualizations**: Interactive **Bar Charts**, **Pie Charts**, and **Line Graphs** using `matplotlib`.
- **Financial Status**: Real-time summary of Total Income vs. Total Expenses.

### 📑 Reports & Budgeting
- **Monthly/Yearly Reports**: Filterable financial statements.
- **Export**: Ability to export reports to **CSV** for external analysis.
- **Budget Tracking**: Compare "Projected Budget" vs. "Actual Spending" with visual warnings.

---

## Technical Stack
- **Frontend**: Python `tkinter` (Custom Styles, ttk widgets).
- **Backend**: Python (Logic), MySQL (Data Persistence).
- **Libraries**:
  - `mysql-connector-python`: Database connectivity.
  - `tkcalendar`: Date selection widgets.
  - `matplotlib`: Data visualization.
  - `Pillow`: Image handling.

---

## Installation & Setup

### Prerequisites
- Python 3.10+
- MySQL Server installed and running.

### 1. Clone/Download Repository
Ensure the project structure is as follows:
```
RAGHU_Final/
├── src/
│   ├── assets/          # Images and icons
│   ├── database/        # Database scripts (Tables.sql, db_connection.py)
│   ├── ui/              # UI Modules (home, admin, expense, budget, etc.)
│   ├── main.py          # Entry point
│   └── scripts/         # Utility scripts
└── README.md
```

### 2. Install Dependencies
Run the following command to install required Python libraries:
```bash
pip install mysql-connector-python tkcalendar matplotlib pillow
```

### 3. Database Configuration
1. Open your MySQL client (Workbench or CLI).
2. Create a database named `expense_tracker` (or update `src/database/db_connection.py` with your DB name).
3. Execute the schema script located at `src/database/Tables.sql` to create the required tables (`tbl_login`, `tbl_users`, `tbl_expenses`, `tbl_budget`, etc.).

### 4. Application Configuration
Update `src/database/db_connection.py` with your MySQL credentials:
```python
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="YOUR_USERNAME",
        password="YOUR_PASSWORD",
        database="expense_tracker"
    )
```

---

## Usage Guide

### Starting the Application
Navigate to the project directory and run:
```bash
python src/main.py
```

### For Users
1. Click **Signup** to create a new account.
2. **Login** with your credentials.
3. Use the top navigation bar to access:
   - **Expense**: Add customized expenses or income records.
   - **Budget**: Set monthly limits for categories (e.g., Food, Transport).
   - **Reports**: View detailed breakdowns and export data.

### For Admins
1. Log in with an admin account (pre-configured in DB).
2. Access the **Admin Dashboard** to view system health.
3. Go to **Users** to manage registered accounts. Use the **Delete Selected User** button to remove users and all their associated data.

---

## Troubleshooting
- **ModuleNotFoundError**: Ensure you have activated your virtual environment and installed `pip` requirements.
- **Database Connection Failed**: Verify MySQL service is running and credentials in `db_connection.py` are correct.
- **UI Artifacts**: If visuals look odd, ensure you are running the app on a system that supports `Tkinter` adequately (Linux/Windows/macOS).

---

## License
This project is licensed under the **MIT License**.  
The LICENSE file contains full licensing details and required credits.

---
