# SQLite Basics — A Beginner-Friendly Guide

> Just by reading this guide, you will understand SQLite and basic database operations.
> Plain English, step by step, with small examples — same style as the Pydantic Basics class.

> **What you should already know:**
> - FastAPI Basics (GET, POST, lists for storage)
> - Pydantic Basics (`BaseModel`, validation, type hints)

---

## Table of Contents

1. [Recap from the previous class](#1-recap-from-the-previous-class)
2. [The real problem — your data is dying!](#2-the-real-problem--your-data-is-dying)
3. [What is a database? (Smart Excel analogy)](#3-what-is-a-database)
4. [Why SQLite? (and not PostgreSQL or MySQL)](#4-why-sqlite)
5. [Connection and Cursor — the phone call analogy](#5-connection-and-cursor)
6. [Your first database file](#6-your-first-database-file)
7. [`CREATE TABLE` — compare with Pydantic models!](#7-create-table)
8. [`INSERT` — adding rows (like `list.append()`)](#8-insert)
9. [`SELECT` — reading rows (like a `for` loop)](#9-select)
10. [`UPDATE` — modifying rows](#10-update)
11. [`DELETE` — removing rows](#11-delete)
12. [Why `commit()` matters — the shopping cart story](#12-why-commit-matters)
13. [Parameterized queries — preventing SQL injection](#13-parameterized-queries)
14. [Persistence demo — close, reopen, data is still there!](#14-persistence-demo)
15. [Common mistakes beginners make](#15-common-mistakes)
16. [Practice exercises](#16-practice-exercises)
17. [Quick cheat sheet](#17-quick-cheat-sheet)
18. [What's next? (FastAPI integration teaser)](#18-whats-next)

---

## 1. Recap from the Previous Class

In the Pydantic Basics class, we built a clean `Student` model:

```python
from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int
    is_active: bool = True
```

And we used it in FastAPI:

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

Next morning, he restarts his laptop. Runs the server again. Opens `/students` ...

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

**SQL** = **S**tructured **Q**uery **L**anguage. It's the language we use to talk to a database.

In Python: `students.append(...)`
In SQL: `INSERT INTO students ...`

Same idea, different syntax.

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

---

## 8. `INSERT`

`INSERT` is the SQL version of `list.append()`.

### Side-by-side:

```python
# Python list
students.append({"name": "Ahmed", "age": 20})
```

```sql
-- SQL INSERT
INSERT INTO students (name, age) VALUES ('Ahmed', 20);
```

### In code:

```python
import sqlite3

connection = sqlite3.connect("school.db")
cursor = connection.cursor()

cursor.execute("""
    INSERT INTO students (name, age, is_active)
    VALUES ('Ahmed', 20, 1)
""")

connection.commit()
connection.close()
print("Student added!")
```

### Adding multiple students:

```python
cursor.execute("INSERT INTO students (name, age) VALUES ('Fatima', 19)")
cursor.execute("INSERT INTO students (name, age) VALUES ('Ali', 21)")
cursor.execute("INSERT INTO students (name, age) VALUES ('Sara', 22)")

connection.commit()   # commit ONCE at the end is fine
```

### Notice:

- We didn't pass `id` — SQLite generates it automatically (because we used `AUTOINCREMENT`).
- `is_active` was skipped for the last three — they got the default `1` (True).
- `'Ahmed'` is in **single quotes** — that's how you write strings in SQL.

---

## 9. `SELECT`

`SELECT` reads data from the table — just like a `for` loop reading a Python list.

### Get all students:

```python
import sqlite3

connection = sqlite3.connect("school.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()

for row in rows:
    print(row)

connection.close()
```

**Output:**

```
(1, 'Ahmed', 20, 1)
(2, 'Fatima', 19, 1)
(3, 'Ali', 21, 1)
(4, 'Sara', 22, 1)
```

Each row is a **tuple** in this order: `(id, name, age, is_active)`.

### `SELECT *` vs specific columns:

```sql
SELECT * FROM students;              -- all columns
SELECT name, age FROM students;       -- only name and age
```

### Get one specific student (by ID):

```python
cursor.execute("SELECT * FROM students WHERE id = 2")
row = cursor.fetchone()    # only ONE row
print(row)
# (2, 'Fatima', 19, 1)
```

### Filtering with `WHERE`:

```python
# All active students
cursor.execute("SELECT * FROM students WHERE is_active = 1")

# Students older than 20
cursor.execute("SELECT * FROM students WHERE age > 20")

# Students named Ali
cursor.execute("SELECT * FROM students WHERE name = 'Ali'")
```

### `fetchall()` vs `fetchone()`:

| Method | Returns | When to use |
|--------|---------|-------------|
| `fetchall()` | List of all rows | Many rows expected |
| `fetchone()` | One row (or `None`) | Looking up a single record |

---

## 10. `UPDATE`

Modify an existing row.

### Side-by-side:

```python
# Python dict
students[1]["age"] = 25
```

```sql
-- SQL UPDATE
UPDATE students SET age = 25 WHERE id = 2;
```

### In code:

```python
import sqlite3

connection = sqlite3.connect("school.db")
cursor = connection.cursor()

cursor.execute("UPDATE students SET age = 25 WHERE id = 2")

connection.commit()
connection.close()
print("Student updated!")
```

### Updating multiple fields:

```python
cursor.execute("""
    UPDATE students
    SET name = 'Fatima Khan', age = 25
    WHERE id = 2
""")
```

### ⚠️ Big warning — always use `WHERE`!

```sql
UPDATE students SET age = 30;
```

This updates **EVERY row** in the table to age 30! 💀

Always include `WHERE` to target specific rows.

---

## 11. `DELETE`

Remove rows.

### Side-by-side:

```python
# Python
del students[1]
```

```sql
-- SQL
DELETE FROM students WHERE id = 2;
```

### In code:

```python
cursor.execute("DELETE FROM students WHERE id = 2")
connection.commit()
print("Student deleted!")
```

### Same warning as `UPDATE`:

```sql
DELETE FROM students;
```

This deletes **EVERY student!** 💀💀💀

Always use `WHERE` unless you really mean to clear the whole table.

---

## 12. Why `commit()` Matters

You may have noticed `connection.commit()` after every change. **What is it?**

### Shopping cart analogy 🛒

When you shop online:
1. You **add items** to the cart (changes are pending)
2. Until you click **"Place Order"**, nothing happens
3. After clicking, the order is **finalized**

In SQLite:
1. `cursor.execute(...)` adds changes to the cart
2. Until you `connection.commit()`, nothing is saved
3. After `commit()`, changes are written to the file

### What happens without `commit()`?

```python
cursor.execute("INSERT INTO students (name, age) VALUES ('Bilal', 23)")
connection.close()    # ❌ no commit!

# Reopen the database — Bilal is NOT there!
```

The change is silently thrown away. 😱

### Rule of thumb:

> **After any `INSERT`, `UPDATE`, or `DELETE` — call `connection.commit()` before closing.**

> `SELECT` does not need `commit()` — it only reads, doesn't change anything.

---

## 13. Parameterized Queries

This is **the most important security topic** in databases. Pay attention!

### ❌ The dangerous way (string concatenation):

```python
name = input("Enter name: ")
cursor.execute(f"SELECT * FROM students WHERE name = '{name}'")
```

What if a user types this as their name?

```
'; DROP TABLE students; --
```

The final SQL becomes:

```sql
SELECT * FROM students WHERE name = ''; DROP TABLE students; --'
```

🔥 **Your entire `students` table is deleted!**

This is called **SQL Injection** — one of the most common security vulnerabilities in the world.

### ✅ The safe way (parameterized queries):

Use `?` as a placeholder, and pass values **separately**:

```python
name = input("Enter name: ")
cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
```

SQLite will safely escape the input — no injection possible. 🛡️

### Examples:

```python
# Single value
cursor.execute("SELECT * FROM students WHERE id = ?", (5,))

# Multiple values
cursor.execute(
    "INSERT INTO students (name, age) VALUES (?, ?)",
    ("Ahmed", 20)
)

# Update with parameters
cursor.execute(
    "UPDATE students SET age = ? WHERE id = ?",
    (25, 2)
)
```

> **The tuple is important!** `(5,)` not `(5)`. The trailing comma makes it a tuple.

### The Bobby Tables comic 🎓

There's a famous comic about a kid named "Robert'); DROP TABLE Students;--" whose name destroyed a school's database. Look it up — it makes the point unforgettable.

**Rule:** Never put user input directly into a SQL string. **Always use `?` placeholders.**

---

## 14. Persistence Demo

This is where the magic happens. Let's prove the data survives.

### Run this script ONCE:

```python
# add_data.py
import sqlite3

connection = sqlite3.connect("school.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER
    )
""")

cursor.execute("INSERT INTO students (name, age) VALUES (?, ?)", ("Ahmed", 20))
cursor.execute("INSERT INTO students (name, age) VALUES (?, ?)", ("Fatima", 19))

connection.commit()
connection.close()
print("Data saved! Now close this script.")
```

```bash
python add_data.py
```

### Now run a DIFFERENT script (later, even after restart):

```python
# read_data.py
import sqlite3

connection = sqlite3.connect("school.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM students")
for row in cursor.fetchall():
    print(row)

connection.close()
```

```bash
python read_data.py
```

**Output:**

```
(1, 'Ahmed', 20)
(2, 'Fatima', 19)
```

🎉 **The data is still there!**

You can:
- Restart your laptop
- Come back next week
- Send `school.db` to your friend
- The data persists.

This is the **whole point** of databases.

---

## 15. Common Mistakes

Beginners make these mistakes — watch out! 🚧

### ❌ Mistake 1: Forgot `commit()`

```python
cursor.execute("INSERT INTO students (name, age) VALUES ('Bilal', 23)")
connection.close()    # ❌ data thrown away!
```

✅ **Correct:**

```python
cursor.execute("INSERT INTO students (name, age) VALUES ('Bilal', 23)")
connection.commit()    # ✅ save first
connection.close()
```

---

### ❌ Mistake 2: String concatenation (security!)

```python
cursor.execute(f"SELECT * FROM students WHERE name = '{name}'")    # ❌ SQL injection!
```

✅ **Correct:**

```python
cursor.execute("SELECT * FROM students WHERE name = ?", (name,))    # ✅ safe
```

---

### ❌ Mistake 3: `UPDATE`/`DELETE` without `WHERE`

```sql
UPDATE students SET age = 30;     -- ❌ updates EVERY row
DELETE FROM students;             -- ❌ deletes EVERY row
```

✅ **Correct:**

```sql
UPDATE students SET age = 30 WHERE id = 5;
DELETE FROM students WHERE id = 5;
```

---

### ❌ Mistake 4: Forgot the trailing comma in single-value tuples

```python
cursor.execute("SELECT * FROM students WHERE id = ?", (5))    # ❌ this is just int 5
```

✅ **Correct:**

```python
cursor.execute("SELECT * FROM students WHERE id = ?", (5,))    # ✅ tuple of one item
```

---

### ❌ Mistake 5: Forgot to close the connection

```python
connection = sqlite3.connect("school.db")
# ... work ...
# ❌ never closed
```

✅ **Correct:**

```python
connection = sqlite3.connect("school.db")
try:
    # ... work ...
finally:
    connection.close()    # ✅ always close
```

> Or use `with` statement (Python's auto-cleanup) — we'll learn that later.

---

### ❌ Mistake 6: Calling `CREATE TABLE` without `IF NOT EXISTS`

```python
cursor.execute("CREATE TABLE students (...)")   # ❌ crashes on second run
```

✅ **Correct:**

```python
cursor.execute("CREATE TABLE IF NOT EXISTS students (...)")    # ✅ safe to run many times
```

---

## 16. Practice Exercises

Now get your hands dirty 👨‍💻

### Exercise 1: Create a `books` table
Create a table with:
- `id` (auto-generated)
- `title` (text, required)
- `author` (text, required)
- `pages` (integer)
- `is_published` (boolean, default True)

### Exercise 2: Insert 5 books
Use parameterized queries (`?`) to insert 5 different books.

### Exercise 3: Read all books
Print every book's title and author.

### Exercise 4: Filter
Find all books with more than 200 pages.

### Exercise 5: Update
Change the title of book ID 2 to "Updated Title".

### Exercise 6: Delete
Delete the book with ID 3.

### Exercise 7: Persistence test
Run your insert script, close everything, restart your laptop. Run a SELECT script — your books should still be there!

### Exercise 8: Security challenge 🛡️
Write an `add_book(title, author)` function that takes user input and inserts safely (using `?`).

---

## 17. Quick Cheat Sheet

```python
import sqlite3

# Connect
connection = sqlite3.connect("school.db")
cursor = connection.cursor()

# Create
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER
    )
""")

# Insert (use ? for safety)
cursor.execute(
    "INSERT INTO students (name, age) VALUES (?, ?)",
    ("Ahmed", 20)
)

# Select all
cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()

# Select one
cursor.execute("SELECT * FROM students WHERE id = ?", (1,))
row = cursor.fetchone()

# Update
cursor.execute(
    "UPDATE students SET age = ? WHERE id = ?",
    (25, 1)
)

# Delete
cursor.execute("DELETE FROM students WHERE id = ?", (1,))

# Save and close
connection.commit()
connection.close()
```

### SQL keywords summary:

| Keyword | Job |
|---------|-----|
| `CREATE TABLE` | Make a new table |
| `INSERT INTO ... VALUES` | Add a new row |
| `SELECT ... FROM` | Read rows |
| `WHERE` | Filter rows |
| `UPDATE ... SET` | Modify rows |
| `DELETE FROM` | Remove rows |
| `PRIMARY KEY` | Unique identifier |
| `AUTOINCREMENT` | Auto-generate IDs |
| `NOT NULL` | Field is required |
| `DEFAULT` | Set a default value |

---

## 🎯 Summary — What Did You Learn Today?

✅ Why lists are not enough — data dies on restart
✅ Database = smart Excel sheet on disk
✅ SQLite = file-based database, built into Python
✅ Connection (phone line) and Cursor (the worker)
✅ `CREATE TABLE` — define the shape (like Pydantic, but on disk)
✅ `INSERT`, `SELECT`, `UPDATE`, `DELETE` — full CRUD
✅ `commit()` saves your changes (like checkout)
✅ Parameterized queries (`?`) prevent SQL injection
✅ Data persists across restarts
✅ Common mistakes and how to avoid them

---

## 18. What's Next?

**Right now**, you can talk to a database from a regular Python script.
**But your FastAPI endpoints still use lists!**

In the **next class**, we'll connect them:

```python
# Imagine this:
@app.post("/students")
def add_student(student: StudentCreate):
    cursor.execute(
        "INSERT INTO students (name, age) VALUES (?, ?)",
        (student.name, student.age)
    )
    connection.commit()
    return {"message": "Saved to database!"}

@app.get("/students")
def get_students():
    cursor.execute("SELECT * FROM students")
    return cursor.fetchall()
```

🚀 **Imagine** — every POST goes straight into the database file. Restart the server, your data is still there!

### And after that?

Writing raw SQL strings everywhere is repetitive and error-prone. There's a cleaner way: **SQLAlchemy ORM**.

With SQLAlchemy, you'll write:

```python
new_student = Student(name="Ahmed", age=20)
session.add(new_student)
session.commit()
```

No SQL strings. Just Python objects. We'll cover that in a later class.

---

**Remember:** Lists die. Files persist. Databases are organized files with superpowers. 💪

```python
import sqlite3
connection = sqlite3.connect("school.db")    # 👈 your forever home for data
```

**Happy Coding! 🚀**
