# DIU Find & Fix

**DIU Find & Fix** is a web-based Lost & Found and Campus Issue Reporting system designed for students and staff of Daffodil International University. This platform enables users to report lost or found items, submit campus issues or complaints, and manage their submissions through a secure, user-friendly interface.

---

## 📌 Description

In large campuses like DIU, losing personal items or facing unresolved issues is common. This platform helps solve these problems by offering a centralized portal where:

- Students can post lost or found items
- Users can report various campus-related problems
- Admins can moderate posts and reports
- Different roles (student, admin) access specific dashboards

---

## ✅ Features

- 🔐 Secure student registration/login using DIU Gmail
- 📝 Post lost or found item reports
- 🛠 Submit campus issue reports or complaints
- 👮 Admin approval for user submissions
- 🎛 Role-based dashboards (Student, Admin)
- 👤 Student profile page with edit option
- 🌙 Light/Dark mode toggle
- 📱 responsive UI using Bootstrap

---

## ⚙️ How to Install and Run the Project Locally

### 1. Clone the Repository
``` bash
git clone https://github.com/your-username/diu-find-fix.git
cd diu-find-fix 
```
### 2. Create and Activate a Virtual Environment
```
python -m venv env
source env/bin/activate        # On Windows: env\Scripts\activate
```
### 3. Install Dependencies
```
pip install -r requirements.txt
```
### 4. Run Migrations
```
python manage.py makemigrations
python manage.py migrate
```
### 5. Create a Superuser
```
python manage.py createsuperuser
```
### 6. Start the Development Server
```
python manage.py runserver
```
