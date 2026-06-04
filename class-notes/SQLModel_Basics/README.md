# SQLModel + FastAPI — A Beginner-Friendly Guide

> Just by reading this guide, you will build a **real, working API** that saves data to a database — using only Python classes.
> Same beginner-friendly style as all previous classes. We will test **everything** in `/docs` (Swagger UI), exactly like you did in the Pydantic class.

> **What you should already know:**
> - FastAPI Basics (GET, POST, `/docs`)
> - Pydantic Basics (`BaseModel`, `Field()`, type hints)
> - Pydantic Part 2 (`response_model=`, `StudentCreate` vs `StudentResponse`)
> - SQLite Basics (what a database is, `CREATE TABLE`)

---

## Table of Contents

1. [Recap — what you already know](#1-recap)
2. [The mission — bring everything together](#2-the-mission)
3. [What is SQLModel? (one paragraph)](#3-what-is-sqlmodel)
4. [Installation](#4-installation)
5. [Step 1 — Define the SQLModel class](#5-step-1--define-the-sqlmodel-class)
6. [Step 2 — Set up the FastAPI app](#6-step-2--set-up-the-fastapi-app)
7. [Step 3 — The `get_session()` helper](#7-step-3--the-get_session-helper)
8. [POST `/students` — your first database insert!](#8-post-students)
9. [GET `/students` — list all students](#9-get-students)
10. [GET `/students/{id}` — get one student](#10-get-studentsid)
11. [PUT `/students/{id}` — update a student](#11-put-studentsid)
12. [DELETE `/students/{id}` — remove a student](#12-delete-studentsid)
13. [The magic moment — restart the server!](#13-the-magic-moment)
14. [Full example — `main.py` from start to finish](#14-full-example)
15. [Try it yourself — Teacher model](#15-try-it-yourself--teacher-model)
16. [Bonus example — Book model](#16-bonus-example--book-model)
17. [Common mistakes](#17-common-mistakes)
18. [Practice exercises](#18-practice-exercises)
19. [Quick cheat sheet](#19-quick-cheat-sheet)
20. [What's next?](#20-whats-next)

---

## 1. Recap

Look at how much you've learned. Each class added one new piece:

| Class | What you learned |
|-------|------------------|
| FastAPI Basics | GET, POST, `/docs` testing |
| Pydantic Basics | `BaseModel`, types, validation |
| Pydantic Part 2 | `response_model=`, input vs output |
| SQLite Basics | What a database is, `CREATE TABLE` |

**Today, all four come together.** 🎉

---

## 2. The Mission

Remember the problem from SQLite Basics?

- You **created** a `school.db` file ✅
- You **made** a `students` table ✅
- But the table was **empty** ❌
- And we said: *"we won't write INSERT/SELECT/UPDATE/DELETE by hand — we'll use SQLModel"*

**Today is that day.** We will:

1. Replace `CREATE TABLE` SQL with a **Python class** (SQLModel)
2. Build **5 FastAPI endpoints** for full CRUD
3. Test **everything in `/docs`** — just like the Pydantic class
4. Restart the server — and our data **stays!** 🎉

---

## 3. What is SQLModel?

> **SQLModel** is a library that lets you define your database tables as **Python classes** — using the same syntax as Pydantic.
>
> One class = your database table + your API schema + your Python object.

Made by **Sebastián Ramírez** (the same person who built FastAPI). Designed so that students who know Pydantic can use databases instantly.

If you know Pydantic — you already know **90% of SQLModel**.

---

## 4. Installation

Open your terminal:

```bash
pip install sqlmodel
```

That's it. SQLModel includes everything you need (FastAPI users may already have it).

Verify:

```bash
python -c "import sqlmodel; print('SQLModel installed!')"
```

> 💡 You **don't** need `pip install sqlite3` — that's already in Python.

---

## 5. Step 1 — Define the SQLModel Class

Create a new file `main.py`. Start with just the model:

```python
from sqlmodel import SQLModel, Field

class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int
    is_active: bool = True
```

### Look at this side by side with what you know:

**Pydantic (from previous classes):**

```python
class Student(BaseModel):
    name: str
    age: int
    is_active: bool = True
```

**SQLModel (now):**

```python
class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int
    is_active: bool = True
```

### What's different?

Only **three** things:

1. `BaseModel` → `SQLModel`
2. Add `table=True` (this tells SQLModel: "make this a real database table!")
3. Add `id: int | None = Field(default=None, primary_key=True)` (the auto-generated ID)

**Everything else is identical to Pydantic.** ✨

### Why `id: int | None`?

Before you insert a student, the database hasn't given an ID yet — so it's `None`.
After insert, the database fills it in.

That's why the type is `int | None` with `default=None`.

---

## 6. Step 2 — Set Up the FastAPI App

Add to `main.py`:

```python
from fastapi import FastAPI
from sqlmodel import SQLModel, Field, create_engine

# Your model from Step 1
class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int
    is_active: bool = True

# 1. The engine — where the database lives
engine = create_engine("sqlite:///school.db")

# 2. The FastAPI app
app = FastAPI()

# 3. Create the tables when the app starts
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
```

### What's happening?

| Line | What it does |
|------|--------------|
| `create_engine("sqlite:///school.db")` | "My database lives in `school.db`" |
| `SQLModel.metadata.create_all(engine)` | "Create all tables that have `table=True`" |
| `@app.on_event("startup")` | "Do this when the server starts" |

### Run it:

```bash
uvicorn main:app --reload
```

✅ Open `http://localhost:8000/docs` — empty (no endpoints yet), but no errors.
✅ Look in your folder — `school.db` was created!

Open it in **DB Browser for SQLite** — you'll see the `student` table with all your columns. 🎉

---

## 7. Step 3 — The `get_session()` Helper

To talk to the database, every endpoint needs a **Session**. Instead of writing the same setup in every endpoint, we write **one** helper:

```python
from sqlmodel import Session

def get_session():
    with Session(engine) as session:
        yield session
```

Then in your endpoints, you ask FastAPI for it using `Depends()`:

```python
from fastapi import Depends

@app.get("/something")
def my_endpoint(session: Session = Depends(get_session)):
    # use `session` here
    ...
```

### What does `Depends(get_session)` mean?

> "Hey FastAPI — give my function a database session to use. And clean it up automatically when done."

That's it. **One helper, used by every endpoint.** Don't worry about understanding `yield` deeply — just know this is the standard pattern.

---

## 8. POST `/students`

Time for your first database insert!

```python
@app.post("/students")
def create_student(student: Student, session: Session = Depends(get_session)):
    session.add(student)
    session.commit()
    session.refresh(student)
    return student
```

### Walking through it:

| Line | What it does |
|------|--------------|
| `student: Student` | FastAPI reads the JSON body and creates a `Student` object (with Pydantic validation!) |
| `session.add(student)` | "Save this — but don't commit yet" |
| `session.commit()` | "Now write it to the database file" |
| `session.refresh(student)` | "Reload from DB so I can see the auto-generated `id`" |
| `return student` | Send back the saved student (now with `id`) |

### Test in `/docs`! 🎯

1. Open `http://localhost:8000/docs`
2. Find **POST `/students`** — click to expand
3. Click **"Try it out"**
4. Enter this JSON:

```json
{
  "name": "Ahmed",
  "age": 20,
  "is_active": true
}
```

5. Click **"Execute"**

### Response: `200 OK`

```json
{
  "id": 1,
  "name": "Ahmed",
  "age": 20,
  "is_active": true
}
```

🎉 **You just saved data to a real database!** Notice `id: 1` — the database auto-assigned it.

### Try sending bad data:

```json
{
  "name": "Sara",
  "age": "twenty"
}
```

Response: `422 Unprocessable Entity` — same Pydantic validation you know! Type hints still rule.

---

## 9. GET `/students`

Now let's read all students.

```python
from sqlmodel import select

@app.get("/students")
def list_students(session: Session = Depends(get_session)):
    students = session.exec(select(Student)).all()
    return students
```

### Walking through it:

| Line | What it does |
|------|--------------|
| `select(Student)` | "Build a SELECT query for the `Student` table" |
| `session.exec(...)` | "Run this query against the database" |
| `.all()` | "Give me back all rows as a list of `Student` objects" |

### Test in `/docs`:

1. Find **GET `/students`** — click to expand
2. Click **"Try it out"** → **"Execute"**

### Response:

```json
[
  {
    "id": 1,
    "name": "Ahmed",
    "age": 20,
    "is_active": true
  }
]
```

Add 2-3 more students from POST first, then call GET again — you'll see them all in the list.

### Compare to raw SQL:

```python
# Raw SQL (what you avoided!)
cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()
# rows = [(1, 'Ahmed', 20, 1)]   ← ugly tuples!
```

vs

```python
# SQLModel
students = session.exec(select(Student)).all()
# students = [Student(id=1, name='Ahmed', age=20, is_active=True)]   ← proper objects!
```

---

## 10. GET `/students/{id}`

Get a specific student by ID.

```python
from fastapi import HTTPException

@app.get("/students/{student_id}")
def get_student(student_id: int, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
```

### What's new?

- **`session.get(Student, student_id)`** — fastest way to fetch by primary key. Returns the object or `None`.
- **`HTTPException(status_code=404, ...)`** — proper way to say "not found" in FastAPI.

### Test in `/docs`:

1. Find **GET `/students/{student_id}`**
2. Enter `student_id`: `1`
3. Click **"Execute"**

### Response (if student 1 exists):

```json
{
  "id": 1,
  "name": "Ahmed",
  "age": 20,
  "is_active": true
}
```

### Response (if student 99 doesn't exist):

```json
{
  "detail": "Student not found"
}
```

Status code: `404 Not Found`. 🛡️

---

## 11. PUT `/students/{id}`

Update an existing student.

```python
@app.put("/students/{student_id}")
def update_student(student_id: int, updated: Student, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student.name = updated.name
    student.age = updated.age
    student.is_active = updated.is_active

    session.add(student)
    session.commit()
    session.refresh(student)
    return student
```

### What's happening?

1. **Find the student** — by ID
2. If not found → 404
3. **Change the fields** on the existing object
4. **Commit** — SQLModel writes the right `UPDATE` SQL for us

### Test in `/docs`:

1. Find **PUT `/students/{student_id}`**
2. Enter `student_id`: `1`
3. Enter JSON body:

```json
{
  "name": "Ahmed Khan",
  "age": 25,
  "is_active": true
}
```

4. Click **"Execute"**

### Response:

```json
{
  "id": 1,
  "name": "Ahmed Khan",
  "age": 25,
  "is_active": true
}
```

✅ The student is updated! Call **GET `/students/1`** again to confirm.

### The magic:

You **never wrote** `UPDATE students SET name=... WHERE id=...`. SQLModel did it for you. 🪄

---

## 12. DELETE `/students/{id}`

Remove a student.

```python
@app.delete("/students/{student_id}")
def delete_student(student_id: int, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    session.delete(student)
    session.commit()
    return {"message": "Student deleted successfully"}
```

### What's happening?

1. Find the student
2. If not found → 404
3. **`session.delete(student)`** — mark for deletion
4. **`session.commit()`** — actually delete

### Test in `/docs`:

1. Find **DELETE `/students/{student_id}`**
2. Enter `student_id`: `2`
3. Click **"Execute"**

### Response:

```json
{
  "message": "Student deleted successfully"
}
```

✅ Call **GET `/students`** again — student 2 is gone.

---

## 13. The Magic Moment

This is the moment that proves **everything works**.

### Try this:

1. From `/docs`, **add 3 students** with POST
2. **Stop the server** (Ctrl+C in terminal)
3. **Start it again** (`uvicorn main:app --reload`)
4. Open `/docs`, call **GET `/students`**

### What do you see?

```json
[
  {"id": 1, "name": "Ahmed", "age": 20, "is_active": true},
  {"id": 2, "name": "Fatima", "age": 19, "is_active": true},
  {"id": 3, "name": "Sara", "age": 22, "is_active": true}
]
```

🎉 **All your data is still there!**

### Compare to before:

| | Old way (list `[]`) | Now (SQLModel + DB) |
|---|---------------------|---------------------|
| After server restart | ❌ All data lost | ✅ All data still there |
| After laptop restart | ❌ All data lost | ✅ All data still there |
| Send `school.db` to a friend | (no DB to send) | ✅ Works on their machine too |

This is what a **real application** does. You just built one. ✨

---

## 14. Full Example

Here is the complete `main.py` — all in one place:

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select

# 1. Define the model
class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int
    is_active: bool = True

# 2. Set up the engine
engine = create_engine("sqlite:///school.db")

# 3. Create the FastAPI app
app = FastAPI()

# 4. Create tables on startup
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# 5. Session helper
def get_session():
    with Session(engine) as session:
        yield session

# ---- ENDPOINTS ----

@app.post("/students")
def create_student(student: Student, session: Session = Depends(get_session)):
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

@app.get("/students")
def list_students(session: Session = Depends(get_session)):
    return session.exec(select(Student)).all()

@app.get("/students/{student_id}")
def get_student(student_id: int, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/students/{student_id}")
def update_student(student_id: int, updated: Student, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student.name = updated.name
    student.age = updated.age
    student.is_active = updated.is_active
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    session.delete(student)
    session.commit()
    return {"message": "Student deleted successfully"}
```

**That's it.** A full database-backed API in about 50 lines. ✨

---

## 15. Try It Yourself — Teacher Model

Now let's apply the same pattern with a `Teacher` model.

### Step 1: Define the model

```python
class Teacher(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    subject: str
    experience_years: int
```

Add this to your `main.py` (next to the `Student` class).

### Step 2: Build the 5 endpoints

```python
@app.post("/teachers")
def create_teacher(teacher: Teacher, session: Session = Depends(get_session)):
    session.add(teacher)
    session.commit()
    session.refresh(teacher)
    return teacher

@app.get("/teachers")
def list_teachers(session: Session = Depends(get_session)):
    return session.exec(select(Teacher)).all()

@app.get("/teachers/{teacher_id}")
def get_teacher(teacher_id: int, session: Session = Depends(get_session)):
    teacher = session.get(Teacher, teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

@app.put("/teachers/{teacher_id}")
def update_teacher(teacher_id: int, updated: Teacher, session: Session = Depends(get_session)):
    teacher = session.get(Teacher, teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    teacher.name = updated.name
    teacher.subject = updated.subject
    teacher.experience_years = updated.experience_years
    session.add(teacher)
    session.commit()
    session.refresh(teacher)
    return teacher

@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int, session: Session = Depends(get_session)):
    teacher = session.get(Teacher, teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    session.delete(teacher)
    session.commit()
    return {"message": "Teacher deleted successfully"}
```

### Test in `/docs`:

Try POST `/teachers` with:

```json
{
  "name": "Mr. Khan",
  "subject": "Mathematics",
  "experience_years": 10
}
```

You now have **two** working CRUD APIs! Both share the same `school.db` file. 🎉

> 💡 Notice — the **exact same 5-endpoint pattern** works for any model. Just swap the class name. This is the power of patterns.

---

## 16. Bonus Example — Book Model

One more example for variety. Try this on your own — it's a great practice.

```python
class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    author: str
    pages: int
    is_published: bool = True
```

Add 5 endpoints for `/books` — same pattern as `/students` and `/teachers`.

Test in `/docs`:

```json
{
  "title": "Python for Beginners",
  "author": "Sara Khan",
  "pages": 250,
  "is_published": true
}
```

### See the pattern?

Every new model = **same 5 endpoints**. Different name, same shape. 🎯

This is why real codebases use **patterns** — once you know the pattern, every new feature is just typing.

---

## 17. Common Mistakes

### ❌ Mistake 1: Forgot `table=True`

```python
class Student(SQLModel):    # ❌ no table=True
    ...
```

Result: No database table is created. SQLModel treats this as a normal Pydantic model.

✅ **Correct:**

```python
class Student(SQLModel, table=True):
    ...
```

---

### ❌ Mistake 2: ID field with wrong type

```python
class Student(SQLModel, table=True):
    id: int = Field(primary_key=True)    # ❌ no default — must always provide!
```

✅ **Correct:**

```python
class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
```

---

### ❌ Mistake 3: Forgot `session.commit()`

```python
session.add(student)
# ❌ no commit — student NOT saved
```

✅ **Correct:**

```python
session.add(student)
session.commit()
session.refresh(student)
```

---

### ❌ Mistake 4: Forgot to create tables

```python
engine = create_engine("sqlite:///school.db")
# ❌ tables never created — endpoints will crash
```

✅ **Correct:**

```python
engine = create_engine("sqlite:///school.db")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
```

---

### ❌ Mistake 5: Forgot `Depends(get_session)`

```python
@app.post("/students")
def create_student(student: Student):    # ❌ no session!
    session.add(student)                  # NameError: session is not defined
```

✅ **Correct:**

```python
@app.post("/students")
def create_student(student: Student, session: Session = Depends(get_session)):
    session.add(student)
```

---

### ❌ Mistake 6: Returning a 404 incorrectly

```python
return {"error": "Not found"}     # ❌ wrong — status is still 200
```

✅ **Correct:**

```python
raise HTTPException(status_code=404, detail="Not found")
```

---

### ❌ Mistake 7: Forgot `refresh()` and returning `id` as `None`

```python
session.add(student)
session.commit()
return student              # ❌ student.id might be None
```

✅ **Correct:**

```python
session.add(student)
session.commit()
session.refresh(student)    # ✅ reloads, including the new id
return student
```

---

## 18. Practice Exercises

All exercises should be tested from `/docs`. 🎯

### Exercise 1 — Build the Teacher API
Add the `Teacher` model and all 5 endpoints from section 15. Test each one in `/docs`.

### Exercise 2 — Build the Book API
Add the `Book` model and all 5 endpoints. Test each in `/docs`.

### Exercise 3 — Add validation
On `Student`, add:
- `name`: `Field(min_length=1, max_length=50)`
- `age`: `Field(gt=0, lt=120)`

Test by sending invalid data — confirm 422 errors.

### Exercise 4 — Persistence test
- Add 3 students, 2 teachers, 2 books
- Stop the server (Ctrl+C)
- Restart it
- Call GET on all three endpoints — confirm all data is still there

### Exercise 5 — DB Browser inspection
Open `school.db` in DB Browser for SQLite. You should see THREE tables: `student`, `teacher`, `book`. Open each — your data is right there.

### Exercise 6 — `is_active` filter
Add `is_active: bool = True` field to `Teacher`. Modify GET `/teachers` to return only active teachers. (Hint: `select(Teacher).where(Teacher.is_active == True)`)

### Exercise 7 — Build a `Course` model
Design and build CRUD for `Course` with fields: `id`, `name`, `instructor`, `duration_hours`, `is_available`.

### Exercise 8 — Find your own bug
Intentionally remove `session.commit()` from POST. Try creating a student. Then restart the server. What happens? Why? Fix it.

---

## 19. Quick Cheat Sheet

```python
# ---- imports ----
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select

# ---- model ----
class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int

# ---- setup ----
engine = create_engine("sqlite:///school.db")
app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# ---- 5 endpoints (the pattern) ----

# POST — create
@app.post("/students")
def create(student: Student, session: Session = Depends(get_session)):
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

# GET all — list
@app.get("/students")
def list_all(session: Session = Depends(get_session)):
    return session.exec(select(Student)).all()

# GET one
@app.get("/students/{id}")
def get_one(id: int, session: Session = Depends(get_session)):
    s = session.get(Student, id)
    if not s:
        raise HTTPException(404, "Not found")
    return s

# PUT — update
@app.put("/students/{id}")
def update(id: int, new: Student, session: Session = Depends(get_session)):
    s = session.get(Student, id)
    if not s:
        raise HTTPException(404, "Not found")
    s.name = new.name
    s.age = new.age
    session.add(s)
    session.commit()
    session.refresh(s)
    return s

# DELETE
@app.delete("/students/{id}")
def delete(id: int, session: Session = Depends(get_session)):
    s = session.get(Student, id)
    if not s:
        raise HTTPException(404, "Not found")
    session.delete(s)
    session.commit()
    return {"message": "Deleted"}
```

### Session methods (the essentials):

| Method | Use it for |
|--------|-----------|
| `session.add(obj)` | Add or update an object |
| `session.commit()` | Save changes to the database file |
| `session.refresh(obj)` | Reload object from DB (gets new `id`) |
| `session.get(Model, id)` | Fast fetch by primary key |
| `session.exec(select(Model)).all()` | Fetch all rows as objects |
| `session.exec(select(Model).where(...)).first()` | Fetch one row (or `None`) |
| `session.delete(obj)` | Delete an object |

---

## 🎯 Summary — What You Built Today

✅ A **real working API** that saves data to disk
✅ One Python class becomes a database table (no SQL written!)
✅ Five endpoints — POST, GET all, GET one, PUT, DELETE
✅ All tested visually in `/docs` (Swagger UI)
✅ Same Pydantic syntax, same validation, same `/docs` experience
✅ Data **survives server restarts** — like a real production app
✅ The 5-endpoint pattern works for any model (Student, Teacher, Book, ...)

---

## 20. What's Next?

**You can now build database-backed APIs for any single-table model.** 🎉

### In future classes, we will cover:

**1. Cleaner code with separate input/output models (Pydantic Part 2 style)**
- `StudentCreate` (no `id`) for POST input
- `StudentResponse` for GET output
- `response_model=StudentResponse` for clean `/docs`

**2. Relationships — connecting tables**
- A `Student` belongs to a `School`
- A `Book` has an `Author`
- A `Course` has many `Students` and many `Teachers`

**3. Layered architecture**
- Split big `main.py` into folders: `models/`, `routes/`, `services/`
- Real production project structure

**4. Authentication + JWT**
- Login system
- Each user sees only their own data
- Bearer token security

**5. PostgreSQL**
- Same SQLModel code, but use Postgres instead of SQLite
- For real production deployments

---

**Remember:**

```python
# This is your entire database table:
class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int

# This is your entire INSERT:
session.add(student); session.commit()

# This is your entire SELECT:
session.exec(select(Student)).all()
```

No SQL strings. No tuples. No manual validation. Just Python + `/docs` + magic. 💪

**Happy Coding! 🚀**
