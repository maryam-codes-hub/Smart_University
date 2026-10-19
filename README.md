# Smart University Complaint & Feedback Management System

A Django web application where university students submit complaints, track their progress and give feedback once an issue is resolved, while administrators review all complaints, update their status and read student feedback.

Built as a hands-on learning project to understand **Django (MVT, ORM, authentication, templates)** together with **MySQL**.

---

## Features

### Students
- Register and log in with a university email
- Dashboard with live counts: total, in progress and resolved complaints
- Submit a new complaint (it starts as **Pending**)
- Track status of all own complaints, newest first, with filters (All, Pending, In Progress, Resolved)
- Open a details page for any of their own complaints
- Give feedback on **resolved** complaints (one feedback per complaint)

### Administrators
- Separate admin login (staff accounts only)
- Dashboard with system-wide statistics: total, pending, in progress, resolved
- View all complaints with student name and email, filter by status
- Update complaint status: Pending, In Progress, Resolved
- Read all student feedback in one place

### Public pages
- Single-page landing site (Home, Services, About, Contact) with smooth scrolling and active-link highlight
- Portal selection page (Student / Admin)
- Contact form that saves messages to the database and redirects to a thank-you page

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django 5.2 (LTS) |
| Database | MySQL 8.0+ (via `mysqlclient`) |
| Frontend | HTML, CSS, a little vanilla JavaScript |
| Config | `python-dotenv` for secrets in `.env` |
| Fonts | Poppins (Google Fonts) |

---

## How a Complaint Moves

```
Student submits  ->  Pending  ->  Admin: In Progress  ->  Admin: Resolved
                                                              |
                                          Student can now give feedback
                                                              |
                                          Admin reads the feedback
```

---

## Data Model

| Model | Purpose | Key fields |
|---|---|---|
| `User` (built-in) | Students and admins (admins have `is_staff=True`) | username, email, first_name, password (hashed) |
| `Complaint` | A complaint raised by a student | `student` (ForeignKey), title, description, status, submission_date |
| `Feedback` | Feedback on a resolved complaint | `complaint` (OneToOneField), comment, created_at |
| `ContactMessage` | Messages sent from the contact form | name, email, message, created_at |

---

## Project Structure

```
Smart_University/
├── manage.py
├── requirements.txt
├── .env.example
├── smart_uni/               # project settings and root URLs
└── complaints/              # main app
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    ├── migrations/
    ├── templates/           # landing, student pages, admin pages, includes/
    └── static/complaints/
        ├── css/
        └── js/
```

---

## Getting Started

### Prerequisites
- Python 3.10 or newer
- MySQL Server 8.0 or newer
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/<repo-name>.git
   cd <repo-name>
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate          # Windows
   # source venv/bin/activate     # macOS / Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   If `mysqlclient` fails to install on Windows, see its installation notes or use `pymysql` as a drop-in alternative.

4. **Create the database** (MySQL Workbench or command line)
   ```sql
   CREATE DATABASE smart_uni_db CHARACTER SET utf8mb4;
   ```

5. **Configure environment variables**

   Copy `.env.example` to `.env` and fill in your values:
   ```
   DB_NAME=smart_uni_db
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   ```

6. **Create the tables**
   ```bash
   python manage.py migrate
   ```

7. **Create an admin account**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the server**
   ```bash
   python manage.py runserver
   ```
   Open http://127.0.0.1:8000/

> Note: Django 5.2 is used on purpose. Newer Django versions require MySQL 8.4+, while 5.2 LTS works with MySQL 8.0.

---

## Admin Accounts

There is **no public admin registration** by design, otherwise anyone could make themselves an admin and see every student's complaints.

Admin accounts are created by the system owner:
- `python manage.py createsuperuser`, or
- from the Django admin site (`/admin/`): **Users, Add user**, then tick **Staff status**.

Admins log in at `/admin-portal/login/`.

---

## Main URLs

| URL | Page |
|---|---|
| `/` | Landing page |
| `/get-started/` | Choose Student or Admin portal |
| `/contact-us/` | Contact form |
| `/student/register/` | Student registration |
| `/student/login/` | Student login |
| `/student/dashboard/` | Student dashboard |
| `/student/complaint/new/` | Submit a complaint |
| `/student/track/` | Track complaints (supports `?status=pending`) |
| `/student/complaint/<id>/` | Complaint details |
| `/student/feedback/` | Give feedback |
| `/admin-portal/login/` | Admin login |
| `/admin-portal/dashboard/` | Admin dashboard |
| `/admin-portal/complaints/` | All complaints and status update |
| `/admin-portal/feedbacks/` | Student feedbacks |
| `/admin/` | Django's built-in admin site |

---

## Security Notes

- Passwords are hashed by Django (`create_user`), never stored in plain text
- All forms that change data use POST with CSRF protection
- Pages are protected with `@login_required` (students) and `@user_passes_test` on `is_staff` (admins)
- A student can only open or give feedback on **their own** complaints (checked on the server, not just in the browser)
- Form input is validated again in the views, not trusted from the browser
- Secrets live in `.env`, which is excluded from Git

---

## Django Concepts Practiced

- Project vs app structure, settings, MySQL configuration
- URL routing with names and URL parameters (`<int:pk>`)
- Views, templates, template inheritance (`extends`, `block`) and `include`
- Static files (`{% static %}`)
- Models, migrations, ForeignKey and OneToOneField, `choices`
- ORM queries: `filter`, `order_by`, `count`, `select_related`, `get_object_or_404`
- GET and POST forms, CSRF, redirect after POST (Post/Redirect/Get)
- Authentication and authorization (login, logout, sessions, `is_staff`)
- Messages framework and template filters

---

## Roadmap

- Student ID and complaint categories
- Optional rating on feedback
- Search and pagination on the admin complaints list
- Email notifications when a status changes
- Rewrite forms with Django Forms / ModelForms
- Deployment

---

<!--
## Screenshots

Add images to a `screenshots/` folder, then remove this comment markers.

| Landing | Student Dashboard |
|---|---|
| ![Landing](screenshots/landing.png) | ![Student Dashboard](screenshots/student-dashboard.png) |

| Track Status | Admin Complaints |
|---|---|
| ![Track Status](screenshots/track-status.png) | ![Admin Complaints](screenshots/admin-complaints.png) |
-->

## Author

Designed by **Sidra Farooq** and built by **Maryam Ehsan** , University of Sargodha.
