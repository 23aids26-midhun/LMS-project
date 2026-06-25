# 🎓 EduVerse LMS – Learning Management System

A complete Learning Management System built with **Flask (Python)**, **HTML/CSS/JS**, and **MySQL**.

---

## 👥 Three User Roles
| Role | What They Can Do |
|------|-----------------|
| 🎓 **Student** | Browse courses, enroll, view lessons, submit assignments, track progress |
| 👨‍🏫 **Trainer** | Create & publish courses, add lessons, manage students |
| 🏛️ **Institute** | Manage trainers, oversee courses, view student analytics |

---

## ⚙️ STEP-BY-STEP SETUP IN VS CODE

### ✅ STEP 1 – Open the Project in VS Code
1. Open **VS Code**
2. Go to **File → Open Folder**
3. Select **`M:\LMS project`**
4. The folder will open in VS Code Explorer

---

### ✅ STEP 2 – Set Up the MySQL Database
1. Open **MySQL Workbench**
2. Connect using:
   - **Host:** localhost
   - **Port:** 3306
   - **User:** root
   - **Password:** dexter
3. In the top menu, click **File → Open SQL Script**
4. Navigate to: `M:\LMS project\database\lms_schema.sql`
5. Click **Run (⚡)** or press **Ctrl+Shift+Enter** to execute
6. You should see `lms_db` appear in the left panel under **Schemas**

---

### ✅ STEP 3 – Open Terminal in VS Code
1. In VS Code, go to **Terminal → New Terminal**
2. This opens a PowerShell terminal inside VS Code

---

### ✅ STEP 4 – Create a Python Virtual Environment
Run these commands **one by one** in the VS Code terminal:

```powershell
# Navigate to project (if needed)
cd "M:\LMS project"

# Create virtual environment
python -m venv venv

# Activate it (Windows PowerShell)
.\venv\Scripts\Activate.ps1
```

> If you get a permission error, run:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
> Then try activating again.

---

### ✅ STEP 5 – Install Python Dependencies
After activating the virtual environment, run:

```powershell
pip install -r requirements.txt
```

Wait for all packages to install. You should see output like:
```
Successfully installed Flask-2.3.3 mysql-connector-python-8.1.0 ...
```

---

### ✅ STEP 6 – Run the Flask Application
```powershell
python app.py
```

You should see:
```
============================================================
   EduVerse LMS Starting...
   URL: http://localhost:5000
   DB:  localhost:3306 | lms_db
============================================================
 * Running on http://127.0.0.1:5000
```

---

### ✅ STEP 7 – Open in Browser
Open your browser and go to:
```
http://localhost:5000
```

You will see the **EduVerse LMS landing page** 🎉

---

## 🗂️ Project Structure
```
M:\LMS project\
├── app.py                      ← Main Flask app (all routes)
├── requirements.txt            ← Python packages
├── database\
│   └── lms_schema.sql          ← Run this in MySQL Workbench
├── static\
│   ├── css\
│   │   └── style.css           ← All styling
│   ├── js\
│   │   └── main.js             ← All JavaScript
│   └── uploads\                ← Auto-created for uploads
└── templates\
    ├── base.html               ← Shared layout (sidebar)
    ├── index.html              ← Landing page
    ├── login.html              ← Login page
    ├── register.html           ← Registration (3 roles)
    ├── profile.html            ← User profile
    ├── student\
    │   ├── dashboard.html
    │   ├── courses.html
    │   ├── my_courses.html
    │   └── view_course.html
    ├── trainer\
    │   ├── dashboard.html
    │   ├── create_course.html
    │   ├── manage_courses.html
    │   ├── add_lesson.html
    │   └── students.html
    └── institute\
        ├── dashboard.html
        ├── manage_trainers.html
        └── courses.html
```

---

## 🔑 Database Info
| Field | Value |
|-------|-------|
| Host | localhost |
| Port | 3306 |
| User | root |
| Password | dexter |
| Database | lms_db |

---

## 🧪 Test the System (Quick Guide)

### As a Student:
1. Go to `http://localhost:5000/register`
2. Select **Student**, fill in details, register
3. Login → Browse Courses → Enroll → View Lessons

### As a Trainer:
1. Register as **Trainer** with specialization
2. Login → Create Course → Add Lessons → View Students

### As an Institute:
1. Register as **Institute** with institute name
2. Login → Add Trainers (by email) → View Courses → Monitor Students

---

## ❓ Troubleshooting

### "Module not found" error
Make sure your virtual environment is activated:
```powershell
.\venv\Scripts\Activate.ps1
```

### "Can't connect to MySQL" error
1. Make sure MySQL service is running
2. Open MySQL Workbench and verify connection works
3. Check that `lms_schema.sql` was executed successfully

### "Port 5000 already in use"
Change the port in `app.py` (last line):
```python
app.run(debug=True, port=5001)  # change 5000 to 5001
```

### PowerShell execution policy error
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🛑 Stop the Server
Press **Ctrl + C** in the VS Code terminal.

---

Built with ❤️ using Flask, MySQL & pure HTML/CSS/JS
