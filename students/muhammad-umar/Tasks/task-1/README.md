# 🚀 Student Management System API

A professional backend API built using **FastAPI** for managing students and course enrollments.

---

# 📌 Project Overview

The **Student Management System API** is a backend application designed to manage:

* 👨‍🎓 Students
* 📚 Course Assignments
* 🧾 Student Information
* ✅ Data Validation

The project follows a clean and organized **layered architecture** using:

* Routes Layer
* Services Layer
* Models Layer
* Database Layer

This structure helps keep the project scalable, readable, and easy to maintain.

---

# ⚙️ Tech Stack

| Technology | Purpose                   |
| ---------- | ------------------------- |
| Python     | Core programming language |
| FastAPI    | Backend framework         |
| Pydantic   | Data validation           |
| REST API   | API architecture          |
| Uvicorn    | ASGI server               |

---

# 📂 Project Structure

```bash
TASK-1/
│
├── models/
│   └── student.py
│
├── routes/
│   ├── student.py
│   └── course.py
│
├── services/
│   ├── student_service.py
│   └── course_service.py
│
├── database.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ✨ Features

## 👨‍🎓 Student Management

* Create Student
* Get All Students
* Get Single Student
* Update Student
* Delete Student

---

## 📚 Course Management

* Assign Course to Student
* Get Assigned Course
* Update Assigned Course
* Delete Assigned Course

---

## ✅ Validation Features

The API uses **Pydantic** for strong validation.

### Validations Implemented:

* Minimum & maximum name length
* Age validation
* Class validation
* Email validation using `EmailStr`
* Nested address validation

---

# 🧠 Architecture Explanation

## 📍 Routes Layer

Responsible for:

* Handling API endpoints
* Managing HTTP requests/responses
* Raising exceptions
* Connecting routes with services

---

## 📍 Services Layer

Responsible for:

* Business logic
* Data processing
* CRUD operations
* Database interactions

This separation keeps the code clean and maintainable.

---

## 📍 Models Layer

Responsible for:

* Data schemas
* Validation rules
* Request & response structure

---

## 📍 Database Layer

A fake in-memory database is used using Python dictionaries.

This is suitable for:

* Learning purposes
* Fast prototyping
* Understanding API flow

---

# 📄 Student Model

## Student Fields

| Field                 | Type    |
| --------------------- | ------- |
| student_name          | string  |
| father_name           | string  |
| student_age           | integer |
| student_current_class | integer |
| admission_date        | date    |
| parent_email          | email   |
| address               | object  |

---

## Address Fields

| Field    | Type   |
| -------- | ------ |
| city     | string |
| area     | string |
| house_no | string |

---

# 📚 Available Courses

| Course No | Course Name           | Duration |
| --------- | --------------------- | -------- |
| 1         | Python Basics         | 2 months |
| 2         | Python Advanced       | 3 months |
| 3         | Front-end Development | 4 months |
| 4         | Back-end Development  | 4 months |

---

# 🔌 API Endpoints

## 👨‍🎓 Student Routes

| Method | Endpoint                 | Description        |
| ------ | ------------------------ | ------------------ |
| POST   | `/students/`             | Create student     |
| GET    | `/students/`             | Get all students   |
| GET    | `/students/{student_id}` | Get single student |
| PUT    | `/students/{student_id}` | Update student     |
| DELETE | `/students/{student_id}` | Delete student     |

---

## 📚 Course Routes

| Method | Endpoint                            | Description              |
| ------ | ----------------------------------- | ------------------------ |
| POST   | `/courses/{student_id}/{course_no}` | Assign course            |
| GET    | `/courses/`                         | Get all assigned courses |
| GET    | `/courses/{student_id}`             | Get assigned course      |
| PUT    | `/courses/{student_id}/{course_no}` | Update course            |
| DELETE | `/courses/{student_id}`             | Delete course            |

---

# 🚨 Error Handling

The project uses FastAPI's `HTTPException` for handling errors.

Examples:

* Student not found
* Course not found
* Duplicate course assignment

---

# ▶️ How to Run the Project

## 1️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

---

## 2️⃣ Activate Virtual Environment

### Windows

```bash
.venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Run Server

```bash
uvicorn main:app --reload
```

---

# 📖 API Documentation

FastAPI automatically provides interactive documentation.

## Swagger UI

```bash
http://127.0.0.1:8000/docs
```

## ReDoc

```bash
http://127.0.0.1:8000/redoc
```

---

# 🔮 Future Improvements

Planned future enhancements:

* 🔐 JWT Authentication
* 🗄️ SQLite/PostgreSQL Integration
* 📊 Attendance Management
* 📝 Marks Management
* 👥 User Roles
* 🧪 Automated Testing
* ☁️ Deployment Support

---

# 🎯 Learning Outcomes

This project helped me understand:

* FastAPI fundamentals
* API architecture
* Dependency Injection
* Pydantic validation
* CRUD operations
* Service layer structure
* REST API development

---

# 👨‍💻 Author

## Muhammad Umar

Passionate learner exploring:

* Artificial Intelligence
* Generative AI
* Backend Development
* FastAPI
* Python

---

# ⭐ Final Note

This project was built for learning and practice purposes as part of my backend development and FastAPI learning journey.

Continuous improvement and learning are the main goals of this repository 🚀