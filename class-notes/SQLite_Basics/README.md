# SQLite Basics — A Beginner-Friendly Guide

> Just by reading this guide, you will understand what a database is, why we need one, and how to set up your first SQLite database.
> Plain English, step by step, with small examples — same style as the Pydantic Basics class.

> **What you should already know:**
> - FastAPI Basics (GET, POST, lists for storage)
> - Pydantic Basics (`BaseModel`, validation, type hints)
> - Pydantic Part 2 (input vs output models, `response_model=`, `model_dump()`)

---

## Table of Contents

1. [Recap from the previous class](#1-recap-from-the-previous-class)
2. [The real problem — your data is dying!](#2-the-real-problem--your-data-is-dying)
3. [What is a database? (Smart Excel analogy)](#3-what-is-a-database)
4. [Why SQLite? (and not PostgreSQL or MySQL)](#4-why-sqlite)
5. [Connection and Cursor — the phone call analogy](#5-connection-and-cursor)
6. [Your first database file](#6-your-first-database-file)
7. [`CREATE TABLE` — compare with Pydantic models!](#7-create-table)
8. [The big question — what about INSERT, SELECT, UPDATE, DELETE?](#8-the-big-question)
9. [The easier way — meet ORMs](#9-the-easier-way--meet-orms)
10. [Why SQLModel is perfect for us](#10-why-sqlmodel-is-perfect-for-us)
11. [Side-by-side preview — Raw SQL vs SQLModel](#11-side-by-side-preview)
12. [Common mistakes (for what you learned today)](#12-common-mistakes)
13. [Practice exercises](#13-practice-exercises)
14. [Quick cheat sheet](#14-quick-cheat-sheet)
15. [What's next?](#15-whats-next)

---

## 1. Recap from the Previous Class

In the Pydantic classes, we built clean models for our API:

```python
from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int
    is_active: bool = True
```

And we used them in FastAPI:

```python
students = []   # 👈 our "database" was just a list

@app.post("/students")
def add_student(student: Student):
    students.append(student.model_dump())
    return student
```

**Everything was working. So what's the new problem?**

Listen to a small story 👇

---

## 2. The Real Problem — Your Data is Dying!

**Story:** Ahmed builds the Student API. He runs `uvicorn main:app --reload`. From `/docs` he adds 5 students. Goes to bed happy. ✨

Next morning, he restarts his laptop. Runs the server again. Opens `/students`...

**Empty list. All 5 students gone!** 💀

### Why did this happen?

```python
students = []   # 👈 this lives in RAM (memory)
```

When the server stops:
- RAM is wiped
- The list is gone
- All your data — **vanished**

### Even worse:

```bash
uvicorn main:app --reload
```

Every time you save a file, `--reload` restarts the server → list resets → data lost.

😩 This is no good for a real app.

### What we actually need:

A place to store data **on disk** — that survives restarts, crashes, and reloads.

**This is what a database does.**

---

## 3. What is a Database?

> **A database is a smart, organized place to store your data on disk — so it survives forever (until you delete it).**

### Best analogy: think of an Excel sheet

| Excel | Database |
|-------|----------|
| Workbook (`.xlsx` file) | Database (`.db` file) |
| Sheet (e.g., "Students") | Table (e.g., `students`) |
| Row (one student's data) | Row (one record) |
| Column (e.g., "name") | Column (e.g., `name`) |
| Cell value | Field value |

### Visual representation:

```
TABLE: students
+----+----------+-----+-----------+
| id | name     | age | is_active |
+----+----------+-----+-----------+
| 1  | Ahmed    | 20  | True      |
| 2  | Fatima   | 19  | True      |
| 3  | Ali      | 21  | False     |
+----+----------+-----+-----------+
```

Looks just like Excel, right? But:
- **Faster** — built for millions of rows
- **Safer** — never corrupts your data
- **Smarter** — you can search, sort, filter with one command
- **Programmable** — Python talks to it directly

### What is SQL?

**SQL** = **S**tructured **Q**uery **L**anguage. It's the language databases speak.

In Python: `students.append(...)`
In SQL: `INSERT INTO students ...`

Same idea, different syntax.

> 💡 **Good news:** You'll see how the framework writes SQL for us soon — you mostly won't have to write SQL by hand!

---

## 4. Why SQLite?

There are many databases out there:

| Database | Type | Setup |
|----------|------|-------|
| **SQLite** | File-based | Zero setup — already in Python ✨ |
| MySQL | Server-based | Install server, manage users |
| PostgreSQL | Server-based | Install server, manage users |
| MongoDB | Server-based | Different language (NoSQL) |

### Why SQLite is perfect for beginners:

✅ **No installation needed** — comes built into Python
✅ **One file** — your whole database is just `school.db`
✅ **No server** — no ports, no users, no passwords
✅ **Same SQL** as PostgreSQL — what you learn here transfers later
✅ **Easy to delete and start over** — just delete the file!

### When NOT to use SQLite:

❌ A big website with thousands of users at once
❌ Multiple servers needing the same data
❌ Real-time chat with millions of messages

For **learning** and **small apps**: SQLite is perfect.
For **production at scale**: switch to PostgreSQL later (the SQL is almost identical!).

---

## 5. Connection and Cursor

To talk to a database, you need two things — a **Connection** and a **Cursor**.

### Phone call analogy 📞

Imagine you want to call a pizza shop:

| Real World | Database World |
|------------|----------------|
| Phone line | **Connection** — opens the link |
| You speaking on the phone | **Cursor** — sends commands and gets responses |
| Hanging up | `connection.close()` |
| Confirming the order | `connection.commit()` |

### In code:

```python
import sqlite3

# Step 1: Connect (open the phone line)
connection = sqlite3.connect("school.db")

# Step 2: Get a cursor (the person talking)
cursor = connection.cursor()

# Step 3: Use the cursor to send SQL commands
cursor.execute("SELECT * FROM students")

# Step 4: When done, close
connection.close()
```

> **Important:** `sqlite3` is already part of Python — no `pip install` needed!

---

## 6. Your First Database File

Let's create our first database. Make a new file `db_demo.py`:

```python
import sqlite3

# This creates "school.db" if it doesn't exist, or opens it if it does
connection = sqlite3.connect("school.db")
print("Database connected!")

connection.close()
print("Database closed.")
```

Run it:

```bash
python db_demo.py
```

**Output:**

```
Database connected!
Database closed.
```

### Now look at your folder! 👀

You'll see a new file: **`school.db`**

That's your entire database — just one file. You can:
- Copy it to a USB
- Share it with a friend
- Delete it (and start fresh)
- Open it in [DB Browser for SQLite](https://sqlitebrowser.org/) to view it visually

🎉 **You just created your first database!**

---

## 7. `CREATE TABLE`

Just like Pydantic models define the shape of your data, **SQL tables define the shape of stored data**.

### Side-by-side comparison:

```python
# Pydantic model (in memory)
class Student(BaseModel):
    name: str
    age: int
    is_active: bool
```

```sql
-- SQL table (on disk)
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    is_active BOOLEAN
);
```

**Same idea, different syntax!**

### Common SQLite data types:

| Pydantic type | SQLite type | Used for |
|---------------|-------------|----------|
| `str` | `TEXT` | Names, descriptions, emails |
| `int` | `INTEGER` | Age, count, IDs |
| `float` | `REAL` | Price, percentage |
| `bool` | `BOOLEAN` (stored as 0/1) | True/False flags |
| (auto) | `INTEGER PRIMARY KEY AUTOINCREMENT` | Auto-generated IDs |

### Code: create the `students` table

```python
import sqlite3

connection = sqlite3.connect("school.db")
cursor = connection.cursor()

# Create the table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        is_active BOOLEAN DEFAULT 1
    )
""")

connection.commit()   # save changes
connection.close()
print("Table created!")
```

### Breaking down the SQL:

| Part | What it does |
|------|--------------|
| `CREATE TABLE` | Make a new table |
| `IF NOT EXISTS` | Skip if table already exists (no error) |
| `students` | Table name |
| `id INTEGER PRIMARY KEY AUTOINCREMENT` | Auto-generated unique ID |
| `name TEXT NOT NULL` | Name is text, can't be empty |
| `age INTEGER NOT NULL` | Age is integer, required |
| `is_active BOOLEAN DEFAULT 1` | Defaults to True (1) |

> **Why UPPERCASE?** SQL keywords are written in CAPS by convention so you can spot them easily. SQL is **not case-sensitive**, so `create table` works too — but `CREATE TABLE` is the standard everyone uses.

✅ **Run the code above. Open the `school.db` file in DB Browser for SQLite — you can SEE the `students` table with all its columns!**

---

## 8. The Big Question

You now have:
- ✅ A database file (`school.db`)
- ✅ A table inside it (`students`)
- ✅ Connection and cursor concepts

**But the table is empty.** How do we add rows? Read them? Update them? Delete them?

In raw SQL, you would write four more types of statements:

```sql
INSERT INTO students (name, age) VALUES ('Ahmed', 20);    -- add a row
SELECT * FROM students;                                    -- read rows
UPDATE students SET age = 21 WHERE id = 1;                 -- modify a row
DELETE FROM students WHERE id = 1;                         -- remove a row
```

Plus you'd need to learn:
- Parameterized queries (to prevent SQL injection)
- `commit()` after every change
- `fetchall()` vs `fetchone()`
- Handling tuples instead of Python objects
- ... and dozens more details

**That's a LOT of SQL syntax.** 😰

### Good news: you almost never write this by hand!

In real Python projects (and especially with FastAPI), we use something called an **ORM** that writes SQL **for us**.

Let me show you 👇

---

## 9. The Easier Way — Meet ORMs

> **ORM** = **O**bject **R**elational **M**apper.
> A library that lets you talk to a database using **Python classes** instead of SQL strings.

### What does that mean?

Instead of writing:

```sql
INSERT INTO students (name, age) VALUES ('Ahmed', 20);
```

You write:

```python
student = Student(name="Ahmed", age=20)
session.add(student)
session.commit()
```

The ORM looks at your code and **writes the SQL for you, automatically**.

### Two popular ORMs in Python:

| ORM | Description |
|-----|-------------|
| **SQLAlchemy** | The industry standard. Powerful but verbose. |
| **SQLModel** ⭐ | Made by the FastAPI author. Built on SQLAlchemy + Pydantic. **Designed for beginners.** |

### We will use **SQLModel** in our class. ✨

---

## 10. Why SQLModel is Perfect for Us

SQLModel was created by **Sebastián Ramírez** — the same person who made **FastAPI**. He designed it specifically so that FastAPI students could use databases without learning a brand new tool.

### Five reasons it's perfect for our class:

1. **You already know Pydantic** — SQLModel uses **the same syntax** as Pydantic. No new mental model.
2. **One class = three things** — the same class is your database table, your API schema, and your Python object. No duplicate models!
3. **No SQL strings to write** — write Python, get database operations.
4. **Auto validation** — Pydantic-style validation works on every insert.
5. **Officially recommended by FastAPI** — the FastAPI docs literally show SQLModel as the way to use SQL databases.

> 💡 If you already know Pydantic, you already know **90% of SQLModel**.

---

## 11. Side-by-Side Preview

### Defining a `Student`:

**Raw SQL (what you just learned):**

```python
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        is_active BOOLEAN DEFAULT 1
    )
""")
```

**SQLModel (what we'll use):**

```python
from sqlmodel import SQLModel, Field

class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int
    is_active: bool = True
```

> Notice — this looks **just like Pydantic** from the previous class!
> The only differences:
> - `SQLModel` instead of `BaseModel`
> - `table=True` (this tells SQLModel "make this a real database table")
> - `Field(default=None, primary_key=True)` for the ID
>
> **That's it.** One class, and you have a database table.

---

### Adding a student:

**Raw SQL:**

```python
cursor.execute(
    "INSERT INTO students (name, age) VALUES (?, ?)",
    ("Ahmed", 20)
)
connection.commit()
```

**SQLModel:**

```python
student = Student(name="Ahmed", age=20)
session.add(student)
session.commit()
```

---

### Reading all students:

**Raw SQL:**

```python
cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()
# [(1, 'Ahmed', 20, 1)]   ← ugly tuples, you have to remember the order!
```

**SQLModel:**

```python
students = session.exec(select(Student)).all()
# [Student(id=1, name='Ahmed', age=20, is_active=True)]   ← proper objects!
print(students[0].name)    # Ahmed   ← dot notation works
```

---

### The big win:

| | Raw SQL | SQLModel |
|---|---------|----------|
| SQL strings to write | Many | None |
| Validation | Manual | Automatic |
| Return type | Tuples | Python objects |
| IDE autocomplete | ❌ | ✅ |
| Pydantic features | Lost | Built-in |
| Lines of code | Many | Few |

---

## 12. Common Mistakes

These are the mistakes that can happen with what you learned today (connection + CREATE TABLE):

### ❌ Mistake 1: Forgot `commit()` after `CREATE TABLE`

```python
cursor.execute("CREATE TABLE ...")
connection.close()    # ❌ table NOT saved!
```

✅ **Correct:**

```python
cursor.execute("CREATE TABLE ...")
connection.commit()    # ✅ save first
connection.close()
```

---

### ❌ Mistake 2: Calling `CREATE TABLE` without `IF NOT EXISTS`

```python
cursor.execute("CREATE TABLE students (...)")    # ❌ crashes on second run!
```

✅ **Correct:**

```python
cursor.execute("CREATE TABLE IF NOT EXISTS students (...)")    # ✅ safe to run many times
```

---

### ❌ Mistake 3: Forgetting to close the connection

```python
connection = sqlite3.connect("school.db")
# ... work ...
# ❌ never closed — file may stay locked
```

✅ **Correct:**

```python
connection = sqlite3.connect("school.db")
# ... work ...
connection.close()    # ✅ always close
```

---

### ❌ Mistake 4: Forgetting that `sqlite3` is built-in

Beginners often try:

```bash
pip install sqlite3   # ❌ not needed (and gives errors)
```

✅ **Correct:**

`sqlite3` is **already inside Python**. Just `import sqlite3` and use it. No install needed.

---

## 13. Practice Exercises

Now get your hands dirty 👨‍💻

### Exercise 1: Create the database
Write a script that creates a `school.db` file and prints "Database created!" — confirm the file appears in your folder.

### Exercise 2: Create a `books` table
Add a `books` table with these columns:
- `id` (auto-generated)
- `title` (text, required)
- `author` (text, required)
- `pages` (integer)
- `is_published` (boolean, default True)

### Exercise 3: Open in DB Browser
Download [DB Browser for SQLite](https://sqlitebrowser.org/). Open your `school.db` file. You should see your `students` and `books` tables — with all the columns you defined!

### Exercise 4: Compare with Pydantic
Take any Pydantic model you wrote in the previous class (e.g., `Product` or `Teacher`). Write the equivalent `CREATE TABLE` statement for it.

### Exercise 5: Multiple tables in one file
In a single `setup_db.py` script, create three tables: `students`, `books`, and `teachers`. Run the script. Open `school.db` in DB Browser — verify all three tables are there.

> 💡 We are **not** doing INSERT/SELECT/UPDATE/DELETE practice here — because in the next class, we will do all of that with **SQLModel**, which is much easier!

---

## 14. Quick Cheat Sheet

```python
import sqlite3

# Connect (creates file if missing)
connection = sqlite3.connect("school.db")
cursor = connection.cursor()

# Define a table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        is_active BOOLEAN DEFAULT 1
    )
""")

# Save changes and close
connection.commit()
connection.close()
```

### SQL keywords you saw today:

| Keyword | Job |
|---------|-----|
| `CREATE TABLE` | Make a new table |
| `IF NOT EXISTS` | Don't crash if table is already there |
| `PRIMARY KEY` | Unique identifier for each row |
| `AUTOINCREMENT` | Auto-generate IDs |
| `NOT NULL` | Field is required |
| `DEFAULT` | Set a default value |

### Common SQLite data types:

| Type | Used for |
|------|----------|
| `TEXT` | Strings |
| `INTEGER` | Whole numbers |
| `REAL` | Decimal numbers |
| `BOOLEAN` | True/False (stored as 0/1) |

---

## 🎯 Summary — What You Learned Today

✅ Why lists are not enough — data dies on restart
✅ Database = smart Excel sheet on disk
✅ SQLite = file-based database, built into Python
✅ Connection (phone line) and Cursor (the worker)
✅ Creating a database file is just one line of code
✅ `CREATE TABLE` defines the shape (just like a Pydantic model)
✅ We **don't** have to write all the other SQL queries by hand
✅ Frameworks use **ORMs** that write SQL for us
✅ We will use **SQLModel** — built by the FastAPI author for FastAPI users

---

## 15. What's Next?

You are now standing at an important point in your learning journey. Here's exactly where you are and what's coming up:

### 🗺️ Upcoming Classes Roadmap

| | Class | What you'll learn | When |
|---|---|---|---|
| ✅ | **SQLite Basics** | Why databases, `CREATE TABLE`, file-based storage | **This class — done!** |
| 🆕 | **SQLModel** | Replace raw SQL with Python classes. Insert, read, update, delete — all without SQL strings. | **Next class** |
| 🔜 | **SQLModel + FastAPI Integration** | Connect SQLModel to your FastAPI endpoints. Your `/students` POST will actually save data to the database! | **Class after that** |

---

### Next class — SQLModel:

You'll learn:
- How to install SQLModel
- How `class Student(SQLModel, table=True)` becomes a real database table
- `session.add(student)` — adding rows the easy way
- `session.exec(select(Student))` — reading rows the easy way
- Updating and deleting — without SQL strings

### Class after that — SQLModel + FastAPI:

This is where **everything comes together**! You'll learn:
- How to wire SQLModel into your FastAPI app
- How a POST endpoint saves data to the database (not a list anymore!)
- How a GET endpoint reads real records from the database
- How `response_model=` (from Pydantic Part 2) combines beautifully with SQLModel
- Restart the server — your data is **still there** 🎉

> 💡 By the end of these two classes, you will have a **real, production-style API** that stores data permanently — using just Python classes, no SQL strings!

### What if I'm curious about raw SQL anyway?

We've kept a full **raw SQL reference** in this folder:

📚 **[RAW_SQL_REFERENCE.md](RAW_SQL_REFERENCE.md)** — full guide to `INSERT`, `SELECT`, `UPDATE`, `DELETE`, parameterized queries, security, persistence demos, and more.

> ⚠️ **You don't need to read it for class.** But it's there if you're curious, want to understand what SQLModel does under the hood, or are preparing for a job interview that asks about SQL.

---

**Remember:** Lists die. Files persist. Databases are organized files with superpowers. And **ORMs save you from writing SQL by hand**. 💪

```python
# Today:
import sqlite3
sqlite3.connect("school.db")    # 👈 first step — make the database file

# Next class:
class Student(SQLModel, table=True):    # 👈 next step — define tables as Python classes
    ...
```

**Happy Coding! 🚀**
