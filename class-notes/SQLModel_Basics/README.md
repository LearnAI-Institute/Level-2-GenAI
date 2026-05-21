# SQLModel Basics — A Beginner-Friendly Guide

> Just by reading this guide, you will understand how to use SQLModel to talk to a database **without writing SQL queries**.
> Plain English, step by step, with small examples — same style as the previous classes.

> **What you should already know:**
> - FastAPI Basics (GET, POST)
> - Pydantic Basics (`BaseModel`, type hints, validation, `Field()`)
> - Pydantic Part 2 (input vs output models, `model_dump()`, nested models)
> - SQLite Basics (what a database is, connection, `CREATE TABLE`)

> ⚠️ **This class is pure SQLModel — no FastAPI yet.** We'll combine them in the **next** class.

---

## Table of Contents

1. [Recap — where we left off](#1-recap--where-we-left-off)
2. [The pain we are about to remove](#2-the-pain-we-are-about-to-remove)
3. [What is SQLModel?](#3-what-is-sqlmodel)
4. [Installation](#4-installation)
5. [Your first SQLModel — and the "wow" moment](#5-your-first-sqlmodel)
6. [Three new words you'll see: Engine, Session, `select`](#6-three-new-words)
7. [Creating the database and tables](#7-creating-the-database-and-tables)
8. [INSERT — adding rows the easy way](#8-insert--adding-rows-the-easy-way)
9. [`session.refresh()` — getting the auto-generated ID](#9-sessionrefresh)
10. [SELECT — reading all rows](#10-select--reading-all-rows)
11. [SELECT one — `.first()`, `.one()`](#11-select-one--first-one)
12. [Filtering with `.where()`](#12-filtering-with-where)
13. [UPDATE — just change the object](#13-update--just-change-the-object)
14. [DELETE — remove a row](#14-delete--remove-a-row)
15. [The `with` statement — clean session management](#15-the-with-statement)
16. [`Field()` extras — `index`, `unique`, `default`, `nullable`](#16-field-extras)
17. [The complete picture — a full CRUD script](#17-the-complete-picture)
18. [Why SQLModel beats raw SQL — final summary](#18-why-sqlmodel-beats-raw-sql)
19. [Common mistakes](#19-common-mistakes)
20. [Practice exercises](#20-practice-exercises)
21. [Quick cheat sheet](#21-quick-cheat-sheet)
22. [What's next?](#22-whats-next)

---

## 1. Recap — Where We Left Off

In **SQLite Basics**, you learned:
- Why lists are not enough — data dies on restart
- A database is like a smart Excel sheet on disk
- SQLite = file-based database, built into Python
- How to write `CREATE TABLE` in raw SQL

In **Pydantic Basics + Part 2**, you learned:
- `BaseModel` and type hints
- Input vs output models (`StudentCreate`, `StudentResponse`)
- `response_model=`, `model_dump()`, nested models

**Now we combine the two worlds** — Pydantic-style models that are ALSO database tables.

---

## 2. The Pain We Are About to Remove

**Story:** Ahmed wants to add 3 students to his database. He starts writing:

```python
import sqlite3

connection = sqlite3.connect("school.db")
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, age INTEGER NOT NULL)")

cursor.execute("INSERT INTO students (name, age) VALUES (?, ?)", ("Ahmed", 20))
cursor.execute("INSERT INTO students (name, age) VALUES (?, ?)", ("Fatima", 19))
cursor.execute("INSERT INTO students (name, age) VALUES (?, ?)", ("Sara", 22))

cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()
for row in rows:
    # row is a tuple: (id, name, age)
    # I have to remember the order!
    print(f"id={row[0]}, name={row[1]}, age={row[2]}")

connection.commit()
connection.close()
```

Then Sara walks in. 👀

> **Sara:** "You're still writing raw SQL? Bro, just use SQLModel."
>
> **Ahmed:** "What's that?"
>
> **Sara:** "It lets you write your tables as Python classes. No SQL strings. And it returns proper objects, not tuples. You'll never go back."

😏 Let's see what Sara is talking about.

---

## 3. What is SQLModel?

> **SQLModel = Pydantic + SQLAlchemy fused together.**
> One class becomes your **database table**, your **API schema**, and your **Python object** — all at the same time.

### Who built it?

**Sebastián Ramírez** — the same person who built FastAPI. He built SQLModel specifically so FastAPI students could use databases without learning a brand-new tool.

### What does it do for us?

| Job | Without SQLModel | With SQLModel |
|-----|------------------|---------------|
| Define a table | Write `CREATE TABLE` SQL | Write a Python class |
| Insert a row | Write `INSERT INTO ...` | `session.add(obj)` |
| Read rows | Write `SELECT ...` | `session.exec(select(Model))` |
| Get a Python object | Manually map tuples | Already an object! |
| Validate data | Manual checks | Automatic (Pydantic) |
| Get IDE autocomplete | ❌ | ✅ |

### The key insight:

> **If you know Pydantic, you already know 90% of SQLModel.**

---

## 4. Installation

Open your terminal:

```bash
pip install sqlmodel
```

That's it. SQLModel comes with **SQLAlchemy + Pydantic** bundled inside it — you don't install them separately.

To confirm:

```bash
python -c "import sqlmodel; print(sqlmodel.__version__)"
```

You should see a version like `0.0.x`.

> 💡 SQLModel uses `sqlite3` under the hood — no extra database setup. The same `.db` file you'd make with raw SQLite is what SQLModel will use.

---

## 5. Your First SQLModel

Compare these two side by side. Slowly.

### Pydantic model (from previous classes):

```python
from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int
    is_active: bool = True
```

### SQLModel — the SAME class but now it's also a database table:

```python
from sqlmodel import SQLModel, Field

class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int
    is_active: bool = True
```

### What changed? Only 3 things:

| Change | Pydantic | SQLModel |
|--------|----------|----------|
| Base class | `BaseModel` | `SQLModel` |
| Decorator/argument | (nothing) | `table=True` |
| ID field | (none usually) | `id: int \| None = Field(default=None, primary_key=True)` |

That's it. **Everything else is identical** to a Pydantic model.

### Why `id: int | None`?

Before you insert a student, the database hasn't assigned an ID yet — so it's `None`. After insertion, the database fills it in.

This is why the type is `int | None` with `default=None`.

### Why `table=True`?

This argument tells SQLModel: *"This is not just a Pydantic model — also make it a real database table."*

If you forget `table=True`, you get a normal Pydantic model only. **No table is created.** This is a common confusion.

### The "wow" moment:

Same Python knowledge you used for Pydantic — but now this object can be **saved to a database**, **fetched back**, **updated**, **deleted**. Without writing any SQL. ✨

---

## 6. Three New Words

To use SQLModel you'll meet 3 new words. Don't worry — each one has a simple job.

### 1. **Engine** — the database "factory"

Think of the **engine** as the **address** of your database. It says: *"Here is where the database lives."*

```python
from sqlmodel import create_engine

engine = create_engine("sqlite:///school.db")
```

- `"sqlite:///school.db"` means: "SQLite database in the file `school.db`"
- You create the engine **once** in your whole program

### 2. **Session** — your conversation with the database

Think of the **session** as **one conversation** with the database. You open it, do some work, then close it.

```python
from sqlmodel import Session

with Session(engine) as session:
    # do some work here
    ...
```

> If a session is a phone call, then `engine` is the phone number you dial.

### 3. **`select`** — building queries

When you want to read rows, you use the `select()` function:

```python
from sqlmodel import select

statement = select(Student)              # "SELECT * FROM students"
students = session.exec(statement).all() # actually run it
```

> Think of `select(Student)` as Python's way of writing `SELECT * FROM students` — but type-safe, with autocomplete.

---

## 7. Creating the Database and Tables

Here's a minimal script. Put this in `db_setup.py`:

```python
from sqlmodel import SQLModel, Field, create_engine

# Step 1: Define the model
class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int
    is_active: bool = True

# Step 2: Set up the engine
engine = create_engine("sqlite:///school.db", echo=True)

# Step 3: Create ALL tables
SQLModel.metadata.create_all(engine)
```

Run it:

```bash
python db_setup.py
```

### What just happened?

1. SQLModel looked at every class that inherits from `SQLModel` with `table=True`.
2. For each one, it generated a proper `CREATE TABLE IF NOT EXISTS ...` SQL statement.
3. It executed those statements on your database (`school.db`).

✅ Open `school.db` in DB Browser for SQLite — you'll see the `student` table with `id`, `name`, `age`, `is_active`.

### What is `echo=True`?

It makes SQLModel **print** the SQL it generates. While learning, keep it on — you'll see *exactly* what SQL each Python operation produces. Once you're comfortable, set `echo=False`.

> 💡 **Tip:** With `echo=True`, you can verify: yes, my Python code did write the right SQL. This builds trust.

---

## 8. INSERT — Adding Rows the Easy Way

Here's the entire process of adding a student:

```python
from sqlmodel import Session

with Session(engine) as session:
    student = Student(name="Ahmed", age=20)
    session.add(student)
    session.commit()
```

### Compare to raw SQL:

```python
# RAW SQL (what you're leaving behind)
cursor.execute("INSERT INTO students (name, age) VALUES (?, ?)", ("Ahmed", 20))
connection.commit()
```

### Walking through each line:

1. `with Session(engine) as session:` — open a conversation with the database.
2. `student = Student(name="Ahmed", age=20)` — create a Python object (Pydantic validates the types).
3. `session.add(student)` — tell the session: "I want to save this."
4. `session.commit()` — write it to disk.

Notice how `id` was not provided — the database auto-generates it.

### Adding multiple students:

```python
with Session(engine) as session:
    session.add(Student(name="Ahmed", age=20))
    session.add(Student(name="Fatima", age=19))
    session.add(Student(name="Sara", age=22))
    session.commit()    # one commit saves them all
```

### Validation works automatically:

```python
student = Student(name="Ali", age="twenty")    # ❌ age is not int!
# pydantic.ValidationError: Input should be a valid integer
```

The same Pydantic validation you know from previous classes — it works **before** the data ever reaches the database.

---

## 9. `session.refresh()`

After `session.commit()`, the database assigns an ID to your new row. But your Python object **doesn't know about it yet** — unless you ask.

```python
with Session(engine) as session:
    student = Student(name="Ahmed", age=20)
    session.add(student)
    session.commit()

    print(student.id)        # ❓ might be None or raise error
    session.refresh(student) # 👈 reloads the object from DB
    print(student.id)        # ✅ 1 (or whatever ID was assigned)
```

### When do you need `refresh()`?

You need it whenever you want to **read fields that the database fills in for you**:
- `id` (auto-generated)
- `created_at` (if you add a default timestamp)
- `is_active` (if you only relied on the database default)

### Typical pattern:

```python
def create_student(name: str, age: int):
    with Session(engine) as session:
        student = Student(name=name, age=age)
        session.add(student)
        session.commit()
        session.refresh(student)    # 👈 important!
        return student               # now this has its full id
```

> 💡 In our next class (FastAPI integration), we'll always `refresh()` before returning a student from a POST endpoint — so the response includes the generated `id`.

---

## 10. SELECT — Reading All Rows

The function for queries is `select`. Here's reading all students:

```python
from sqlmodel import select

with Session(engine) as session:
    statement = select(Student)
    students = session.exec(statement).all()

    for s in students:
        print(s.id, s.name, s.age)
```

### Compare to raw SQL:

```python
# RAW SQL
cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()
for row in rows:
    print(row[0], row[1], row[2])   # ❌ have to know column order
```

### The huge advantage:

`session.exec(...).all()` returns a **list of `Student` objects** — not tuples.

```python
students[0].name        # ✅ dot notation
students[0].is_active   # ✅ Pydantic validation, IDE autocomplete
```

### Shortcut — one-liner:

```python
students = session.exec(select(Student)).all()
```

You'll see this style a lot in real code.

---

## 11. SELECT One — `.first()`, `.one()`

What if you want a **single** student, not a list?

### `.first()` — gives you the first match, or `None`

```python
with Session(engine) as session:
    statement = select(Student).where(Student.id == 1)
    student = session.exec(statement).first()

    if student:
        print(student.name)
    else:
        print("Not found")
```

Use `.first()` when:
- You expect one result, OR
- The row may not exist (and you want to handle that)

### `.one()` — gives you exactly one match, errors otherwise

```python
student = session.exec(select(Student).where(Student.id == 1)).one()
```

Use `.one()` when:
- You are 100% sure exactly one row matches
- You want the program to **crash** if it finds 0 or 2+ rows (a safety net)

### Comparison:

| Method | 0 matches | 1 match | 2+ matches |
|--------|-----------|---------|-----------|
| `.all()` | `[]` | `[obj]` | `[obj1, obj2, ...]` |
| `.first()` | `None` | `obj` | `obj` (first one) |
| `.one()` | ❌ error | `obj` | ❌ error |

> 💡 For looking up by ID, beginners usually use `.first()`. It's safer.

---

## 12. Filtering with `.where()`

`.where()` is SQLModel's version of SQL's `WHERE`.

### Basic comparisons:

```python
# Students older than 20
statement = select(Student).where(Student.age > 20)

# Students named "Ahmed"
statement = select(Student).where(Student.name == "Ahmed")

# Inactive students
statement = select(Student).where(Student.is_active == False)
```

> Notice — you use `Student.age > 20` (the class attribute), not `student.age > 20` (an instance). SQLModel reads this to build the SQL.

### Multiple conditions:

Chain `.where()` — they combine with **AND**:

```python
# Active students older than 20
statement = (
    select(Student)
    .where(Student.age > 20)
    .where(Student.is_active == True)
)
```

### Comparison operators you can use:

| Python | SQL meaning |
|--------|-------------|
| `Student.age == 20` | equals |
| `Student.age != 20` | not equal |
| `Student.age > 20` | greater than |
| `Student.age >= 20` | greater than or equal |
| `Student.age < 20` | less than |
| `Student.age <= 20` | less than or equal |

### Example: get all active students above age 18

```python
with Session(engine) as session:
    statement = (
        select(Student)
        .where(Student.age > 18)
        .where(Student.is_active == True)
    )
    results = session.exec(statement).all()
    for s in results:
        print(s.name, s.age)
```

---

## 13. UPDATE — Just Change the Object

This is where SQLModel feels truly magical.

### The pattern:

1. Fetch the row.
2. Change the field on the Python object.
3. Commit.

```python
with Session(engine) as session:
    student = session.exec(select(Student).where(Student.id == 1)).first()

    student.age = 25               # 👈 just change the attribute
    student.name = "Ahmed Khan"    # 👈 and another

    session.add(student)            # tell the session "this changed"
    session.commit()
    session.refresh(student)        # reload to confirm
```

### Compare to raw SQL:

```python
cursor.execute("UPDATE students SET age = 25, name = 'Ahmed Khan' WHERE id = 1")
connection.commit()
```

### What's happening?

When you fetch an object inside a session, the session **tracks** it. When you change a field and call `commit()`, the session figures out exactly what changed and writes the right `UPDATE` statement.

> 💡 You don't need `session.add(student)` if the student was just fetched in the same session — but adding it doesn't hurt and is the safe default for beginners.

---

## 14. DELETE — Remove a Row

Same pattern: fetch, then delete.

```python
with Session(engine) as session:
    student = session.exec(select(Student).where(Student.id == 1)).first()

    if student:
        session.delete(student)
        session.commit()
        print("Deleted!")
    else:
        print("Not found")
```

### Compare to raw SQL:

```python
cursor.execute("DELETE FROM students WHERE id = 1")
connection.commit()
```

### Safety note:

`session.delete()` only deletes the **specific row** of the object you fetched. You can't accidentally wipe the whole table the way you could with `DELETE FROM students` (no `WHERE`).

This is another safety win of SQLModel.

---

## 15. The `with` Statement

You've seen `with Session(engine) as session:` in every example. What is it doing?

### Without `with` (the bad way):

```python
session = Session(engine)
student = Student(name="Ahmed", age=20)
session.add(student)
session.commit()
session.close()      # ❌ easy to forget!
```

### With `with` (the safe way):

```python
with Session(engine) as session:
    student = Student(name="Ahmed", age=20)
    session.add(student)
    session.commit()
# session.close() is called automatically when the block ends
```

### Why is this important?

- A session uses a database connection.
- If you forget to close it, the connection stays open → eventually problems.
- `with` **guarantees** cleanup — even if an error happens inside the block.

> 🎯 **Always use the `with` pattern.** It is the standard Python way to handle resources cleanly.

---

## 16. `Field()` Extras

You already know `Field()` from Pydantic Part 1 (`min_length`, `max_length`, `gt`, `ge`, ...). In SQLModel, `Field()` adds **a few extra database-only options**.

### `primary_key=True` — the unique identifier

```python
id: int | None = Field(default=None, primary_key=True)
```

Already familiar — marks the ID column.

### `index=True` — makes searches faster

```python
name: str = Field(index=True)
```

If you'll often search by `name`, set `index=True`. The database creates an index for fast lookups.

> 💡 Use indexes only for fields you actually filter/search by. Too many indexes slow down inserts.

### `unique=True` — no duplicates allowed

```python
email: str = Field(unique=True)
```

If you try to insert two students with the same email, the database refuses.

### `nullable=False` — required at the DB level

By default, optional Python fields can be `NULL` in the database. To enforce required at the DB level:

```python
name: str = Field(nullable=False)
```

> Usually you don't need this for required fields — Pydantic and the type hint already enforce it.

### `default=...` — initial value

```python
is_active: bool = Field(default=True)
```

Same as Pydantic — gives the field a default if not provided.

### Combining options:

```python
class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=1, max_length=50)
    email: str = Field(unique=True, index=True)
    age: int = Field(gt=0, lt=120)
    is_active: bool = Field(default=True)
```

All Pydantic validators **plus** all SQL options — in one place. ✨

---

## 17. The Complete Picture

Here is a single script that does **everything** — create table, insert, read, update, delete.

```python
# crud_demo.py

from sqlmodel import SQLModel, Field, Session, create_engine, select

# 1. Define the model
class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int
    is_active: bool = True

# 2. Set up the engine
engine = create_engine("sqlite:///school.db", echo=False)

# 3. Create tables
SQLModel.metadata.create_all(engine)


# 4. INSERT
def add_students():
    with Session(engine) as session:
        session.add(Student(name="Ahmed", age=20))
        session.add(Student(name="Fatima", age=19))
        session.add(Student(name="Sara", age=22))
        session.commit()
        print("Students added!")


# 5. READ all
def list_students():
    with Session(engine) as session:
        students = session.exec(select(Student)).all()
        for s in students:
            print(f"{s.id}: {s.name} ({s.age})")


# 6. READ one
def get_student(student_id: int):
    with Session(engine) as session:
        student = session.exec(
            select(Student).where(Student.id == student_id)
        ).first()
        if student:
            print(f"Found: {student.name}")
        else:
            print("Not found")


# 7. UPDATE
def update_age(student_id: int, new_age: int):
    with Session(engine) as session:
        student = session.exec(
            select(Student).where(Student.id == student_id)
        ).first()
        if student:
            student.age = new_age
            session.add(student)
            session.commit()
            print("Updated!")


# 8. DELETE
def delete_student(student_id: int):
    with Session(engine) as session:
        student = session.exec(
            select(Student).where(Student.id == student_id)
        ).first()
        if student:
            session.delete(student)
            session.commit()
            print("Deleted!")


# Run them in order
if __name__ == "__main__":
    add_students()
    list_students()
    get_student(1)
    update_age(1, 25)
    delete_student(2)
    list_students()
```

> Run this script — you've just done a full CRUD round-trip **without writing a single SQL string**.

---

## 18. Why SQLModel Beats Raw SQL

Now let's prove it visually.

### Defining a table:

| | Raw SQL | SQLModel |
|---|---------|----------|
| Lines of code | 7 | 5 |
| Type hints | ❌ | ✅ |
| Validation | Manual | Automatic |
| Same as Pydantic? | ❌ | ✅ |

### Inserting:

| | Raw SQL | SQLModel |
|---|---------|----------|
| Code | `cursor.execute("INSERT INTO students (name, age) VALUES (?, ?)", (...))` | `session.add(Student(name=..., age=...))` |
| Need to remember column order? | ✅ | ❌ |
| SQL injection risk? | If you forget `?` | None |
| Validation? | Manual | Automatic |

### Reading:

| | Raw SQL | SQLModel |
|---|---------|----------|
| Result type | Tuples `(1, 'Ahmed', 20)` | Objects `Student(id=1, name='Ahmed', age=20)` |
| Access by name? | ❌ row[1] | ✅ student.name |
| IDE autocomplete? | ❌ | ✅ |

### Updating:

| | Raw SQL | SQLModel |
|---|---------|----------|
| Code | `UPDATE students SET age=? WHERE id=?` | `student.age = 25; commit` |
| Risk of forgetting `WHERE`? | High | Low |

### Conclusion:

**Less code. Safer code. Type-safe code. Easier to read.**

Every benefit of Pydantic + every benefit of a database, in one tool.

---

## 19. Common Mistakes

### ❌ Mistake 1: Forgot `table=True`

```python
class Student(SQLModel):    # ❌ no table=True
    name: str
```

Result: SQLModel treats this as a normal Pydantic model. No database table is created.

✅ **Correct:**

```python
class Student(SQLModel, table=True):
    ...
```

---

### ❌ Mistake 2: ID field with wrong type

```python
class Student(SQLModel, table=True):
    id: int = Field(primary_key=True)    # ❌ before insert, id is None!
```

✅ **Correct:**

```python
class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
```

---

### ❌ Mistake 3: Forgot `session.commit()`

```python
with Session(engine) as session:
    session.add(Student(name="Ahmed", age=20))
    # ❌ no commit — data NOT saved
```

✅ **Correct:**

```python
with Session(engine) as session:
    session.add(Student(name="Ahmed", age=20))
    session.commit()
```

---

### ❌ Mistake 4: Forgot `SQLModel.metadata.create_all(engine)`

```python
engine = create_engine("sqlite:///school.db")
# ❌ tables NEVER created
with Session(engine) as session:
    session.add(Student(...))   # crashes — table doesn't exist
```

✅ **Correct:**

```python
engine = create_engine("sqlite:///school.db")
SQLModel.metadata.create_all(engine)    # ✅ create tables first
```

---

### ❌ Mistake 5: Using `student.age > 20` (instance) instead of `Student.age > 20` (class)

```python
statement = select(Student).where(student.age > 20)    # ❌ student, lowercase!
```

✅ **Correct:**

```python
statement = select(Student).where(Student.age > 20)    # ✅ class, uppercase
```

Remember: filters are built on the **class**, not an instance.

---

### ❌ Mistake 6: Forgot to `refresh()` before reading `.id`

```python
with Session(engine) as session:
    student = Student(name="Ahmed", age=20)
    session.add(student)
    session.commit()
    print(student.id)    # ❓ might error or show None
```

✅ **Correct:**

```python
with Session(engine) as session:
    student = Student(name="Ahmed", age=20)
    session.add(student)
    session.commit()
    session.refresh(student)
    print(student.id)    # ✅
```

---

### ❌ Mistake 7: Forgot the `with` block — session not closed

```python
session = Session(engine)
session.add(Student(...))
session.commit()
# ❌ session never closed
```

✅ **Correct:**

```python
with Session(engine) as session:
    session.add(Student(...))
    session.commit()
# auto-closed here
```

---

## 20. Practice Exercises

### Exercise 1: Define a `Book` model
Build a `Book` SQLModel with:
- `id` (primary key, auto)
- `title` (text, required, indexed)
- `author` (text, required)
- `pages` (integer, optional)
- `is_published` (bool, default True)

### Exercise 2: Create the database
Set up an engine and call `metadata.create_all`. Open the `.db` file in DB Browser — confirm the `book` table is there.

### Exercise 3: Insert 5 books
Add 5 different books in one session, then commit.

### Exercise 4: List all books
Use `select(Book)` to print every book's title and author.

### Exercise 5: Filter
Find all books with more than 200 pages.

### Exercise 6: Update
Change the title of book ID 1 to "Updated Title". Verify.

### Exercise 7: Delete
Delete book ID 2. Confirm with a re-read.

### Exercise 8: refresh demo
After inserting a new book, print `book.id` before AND after `session.refresh(book)`. Observe the difference.

### Exercise 9: Compare with raw SQL
Take any exercise above and write it in **two** versions — once with raw `sqlite3`, once with SQLModel. Count the lines. Notice the difference.

### Exercise 10: `unique` constraint
Add `email: str = Field(unique=True)` to a `User` model. Try to insert two users with the same email. Observe the error.

---

## 21. Quick Cheat Sheet

```python
from sqlmodel import SQLModel, Field, Session, create_engine, select

# 1. Define
class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int
    is_active: bool = True

# 2. Engine + tables
engine = create_engine("sqlite:///school.db")
SQLModel.metadata.create_all(engine)

# 3. Insert
with Session(engine) as session:
    session.add(Student(name="Ahmed", age=20))
    session.commit()

# 4. Read all
with Session(engine) as session:
    students = session.exec(select(Student)).all()

# 5. Read one
with Session(engine) as session:
    student = session.exec(
        select(Student).where(Student.id == 1)
    ).first()

# 6. Filter
with Session(engine) as session:
    older = session.exec(
        select(Student).where(Student.age > 20)
    ).all()

# 7. Update
with Session(engine) as session:
    s = session.exec(select(Student).where(Student.id == 1)).first()
    s.age = 25
    session.add(s)
    session.commit()

# 8. Delete
with Session(engine) as session:
    s = session.exec(select(Student).where(Student.id == 1)).first()
    session.delete(s)
    session.commit()
```

### `Field()` options summary:

| Option | Job |
|--------|-----|
| `default=...` | initial value |
| `primary_key=True` | unique row identifier |
| `index=True` | speed up lookups |
| `unique=True` | no duplicates |
| `nullable=False` | required at DB level |
| `min_length` / `max_length` | string length rules (from Pydantic) |
| `gt` / `ge` / `lt` / `le` | numeric rules (from Pydantic) |

### `.exec()` result methods:

| Method | Returns | Use when |
|--------|---------|----------|
| `.all()` | list | many rows expected |
| `.first()` | first match or `None` | one row, may not exist |
| `.one()` | exactly one row, else error | strict — must exist exactly once |

---

## 🎯 Summary — What You Learned Today

✅ Why raw SQL is painful for everyday CRUD
✅ SQLModel = Pydantic + SQLAlchemy in one
✅ One class becomes table + schema + Python object
✅ `class Student(SQLModel, table=True)` syntax
✅ `Engine`, `Session`, `select` — the three new words
✅ `SQLModel.metadata.create_all(engine)` builds your tables
✅ INSERT = `session.add()` + `session.commit()`
✅ `session.refresh()` to get auto-generated values like `id`
✅ SELECT all = `session.exec(select(Model)).all()`
✅ `.first()`, `.one()`, `.all()` — three reading methods
✅ Filtering with `.where()` and Python comparisons
✅ UPDATE = change the attribute + commit (no SQL!)
✅ DELETE = `session.delete()` + commit
✅ The `with Session(engine)` pattern for safe sessions
✅ `Field()` extras — `index`, `unique`, `nullable`
✅ Why SQLModel beats raw SQL in every way

---

## 22. What's Next?

**You can now write a full database-backed Python script with no SQL strings.**

But your FastAPI endpoints still use lists `[]`!

### Next class — SQLModel + FastAPI Integration:

This is where **everything you've learned comes together**:

```python
# Imagine this in your FastAPI app:

@app.post("/students", response_model=StudentResponse)
def create_student(student: StudentCreate, session: Session = Depends(get_session)):
    new = Student.model_validate(student)
    session.add(new)
    session.commit()
    session.refresh(new)
    return new

@app.get("/students", response_model=list[StudentResponse])
def list_students(session: Session = Depends(get_session)):
    return session.exec(select(Student)).all()
```

✨ Look at that — Pydantic Part 2 (`response_model`, `model_validate`), SQLite Basics (database concepts), and SQLModel today — **all coming together**.

After the next class, restart your server and your data **stays.** Your API becomes real. 🎉

### Future classes:

- Relationships — `Student → School`, `Book → Author` (foreign keys)
- Many-to-many tables
- Layered architecture (routes → services → database)
- Authentication + JWT
- Migrations with Alembic

---

**Remember:** SQLModel is just Pydantic that knows how to live on disk. Everything you learned about Pydantic — type hints, `Field()`, validation — still works. Plus `table=True` makes it a real table. Plus `Session` lets you save, read, change, and delete. 💪

```python
class Student(SQLModel, table=True):    # ← Pydantic + database in one line
    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int
```

**Happy Coding! 🚀**
