## 🩸 Blood Bank Management System

A role-based Blood Bank Management System built using Flask, designed to manage blood donations and patient blood requests with structured workflows and admin-controlled approvals.

## 🚀 Project Overview

This system allows:

Users to register and donate blood

Public users to request blood

Admins to review and manage donations and requests

Enforced medical eligibility rules

Status-based workflow management

The application ensures secure authentication, data integrity, and real-world donation lifecycle control.

## 🏗️ System Architecture
🔹 Backend Framework

Flask

🔹 Database

SQLite

Flask-SQLAlchemy ORM

🔹 Authentication & Security

Flask-Login (Session management)

Flask-Bcrypt (Password hashing)

Flask-WTF / WTForms (Form validation + CSRF protection)

## 🗄️ Database Models
👤 User

id

username (unique)

email_address (unique)

password_hash

role (User / Admin)

relationship → Donations

🩸 Donation

id

name

age

email

address

phone_number

blood_group

gender

donation_date

donor_id (ForeignKey → User)

status (Pending / Approved / Rejected)

🏥 PatientRequest

id

name

age

email

phone_number

blood_group

hospital_name

reason

request_date

status (Open / Fulfilled / Cancelled)

## 🔐 Authentication & Authorization
✔ User Authentication

Secure password hashing using Bcrypt

Session-based login management

Protected routes using @login_required

✔ Role-Based Access Control (RBAC)

Admin and User roles

Custom admin_required decorator

Admin-only dashboard access

403 protection for unauthorized access

## 🩸 Donation Workflow

User must be logged in to donate.

Medical eligibility enforced:

Age between 18–65

90-day cooldown between donations

Donation created with status = Pending

Admin reviews donation:

Approve → status = Approved

Reject → status = Rejected

## 🏥 Patient Request Workflow

Public users can submit blood requests.

Request stored with status = Open

Admin can:

Fulfill → status = Fulfilled

Cancel → status = Cancelled

## 🧠 Business Logic Implemented

Donation age constraint (18–65)

90-day cooldown enforcement

Role-based route protection

Multi-stage status tracking

Data normalization (User ↔ Donation separation)

Secure admin approval lifecycle

## 📊 Admin Dashboard

Admin can:

View pending donations

View open patient requests

Approve / Reject donations

Fulfill / Cancel patient requests

This introduces structured decision-making and workflow control.

## 🛠️ How to Run the Project
1️⃣ Clone the repository
git clone <your-repo-link>
cd blood-bank-system
2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Initialize Database
python
from blood import app, db
with app.app_context():
    db.create_all()
5️⃣ Run the application
flask run

Visit:

http://127.0.0.1:5000
👨‍💼 Creating an Admin User

Register a normal user.

Open Python shell:

from blood import app, db
from blood.models import User

with app.app_context():
    user = User.query.filter_by(username="yourusername").first()
    user.role = "Admin"
    db.session.commit()
## 🎯 Key Features Implemented

Secure authentication system

Donation eligibility enforcement

Admin-controlled approval workflow

Status-based lifecycle management

Data integrity with relational modeling

Structured backend architecture

## 🔍 What This Project Demonstrates

Backend development using Flask

Database schema design & normalization

Business rule implementation

Secure authentication practices

Role-based authorization

Workflow-driven system architecture

## 🚀 Future Improvements (Planned)

Blood inventory management

Real-time stock updates

Email notifications

Analytics dashboard

Audit logging

📌 Project Status

✔ Authentication system complete
✔ Donation system with constraints
✔ Patient request system
✔ Admin approval workflow
🔄 Inventory system (next phase)
