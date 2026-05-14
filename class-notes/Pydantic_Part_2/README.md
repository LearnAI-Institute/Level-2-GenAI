# Pydantic for APIs — Part 2

> A beginner-friendly continuation of Pydantic Basics.
> Just by reading this guide, you will understand the next layer of Pydantic features used in real APIs.
> Plain English, step by step, with small examples — same style as Pydantic Basics.

> **What you should already know:**
> - FastAPI Basics (GET, POST, lists for storage)
> - Pydantic Basics (`BaseModel`, type hints, validation, `Field()`, default values, optional fields)

---

## Table of Contents

1. [Quick recap from Pydantic Basics](#1-quick-recap-from-pydantic-basics)
2. [The new problem — `main.py` is getting messy](#2-the-new-problem)
3. [Solution 1 — Move models to `schemas.py`](#3-move-models-to-schemaspy)
4. [The most important new idea — Input vs Output models](#4-input-vs-output-models)
5. [Response Models — what the server sends back](#5-response-models)
6. [Using `response_model=` in FastAPI](#6-using-response_model)
7. [The hidden security benefit (password example)](#7-hidden-security-benefit)
8. [`model_dump()` — Pydantic object → Python dict](#8-model_dump)
9. [`model_dump_json()` — Pydantic object → JSON string](#9-model_dump_json)
10. [`Model(**data)` and `model_validate()` — dict → Pydantic object](#10-dict-to-pydantic)
11. [Nested Models — a model inside a model](#11-nested-models)
12. [Multiple levels of nesting](#12-multiple-levels-of-nesting)
13. [Lists of nested models — `list[Tag]`](#13-lists-of-nested-models)
14. [`list[Model]` as a response type](#14-list-of-models-as-response)
15. [Optional nested models](#15-optional-nested-models)
16. [`default_factory` — safe defaults for lists and dicts](#16-default_factory)
17. [Common mistakes](#17-common-mistakes)
18. [Practice exercises](#18-practice-exercises)
19. [Quick cheat sheet](#19-quick-cheat-sheet)
20. [What's next?](#20-whats-next)

---

## 1. Quick Recap from Pydantic Basics

In Part 1 you learned:

```python
from pydantic import BaseModel, Field

class Student(BaseModel):
    name: str = Field(min_length=1)
    age: int = Field(gt=0)
    is_active: bool = True
    description: str | None = None
```

You also learned:
- How `dict` is unsafe and Pydantic is safe
- How type hints become rules
- How FastAPI uses `BaseModel` instead of `dict` for POST bodies
- How validation errors show with status code `422`

**You can now define models and use them as INPUT.**

But there's more to learn — especially about **what the server sends BACK**, how to organize models in big projects, and how to model **structured data**.

---

## 2. The New Problem — `main.py` is Getting Messy

**Story:** Sara is happy with her new Pydantic skills. She adds a Pydantic model for `Student`. Then a model for `Book`. Then `Product`. Then `Teacher`. Then `Course`. Then `Enrollment`...

After a few days, her `main.py` looks like this:

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Student(BaseModel):
    ...

class Book(BaseModel):
    ...

class Product(BaseModel):
    ...

class Teacher(BaseModel):
    ...

class Course(BaseModel):
    ...

# ... 20 more models ...

@app.post("/students")
def add_student(student: Student):
    ...

# ... 50 more endpoints ...
```

**400 lines.** Finding anything is a nightmare. 😫

### Why this is a real problem:

| Problem | Impact |
|---------|--------|
| Hard to find a specific model | You scroll forever |
| Models mixed with endpoints | Two different jobs in one file |
| Hard to share models | Other files can't easily import them |
| Hard to read | New teammates get lost |

### The professional solution:

> **Split your models into a separate file called `schemas.py`.**

This is so common that **almost every real FastAPI project does it**.

---

## 3. Move Models to `schemas.py`

### Step 1: New folder structure

```
my_project/
├── main.py        # FastAPI app and endpoints ONLY
└── schemas.py     # Pydantic models ONLY
```

### Step 2: `schemas.py` — only models

```python
# schemas.py
from pydantic import BaseModel, Field

class Student(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    age: int = Field(gt=0, lt=120)
    is_active: bool = True
```

### Step 3: `main.py` — import and use

```python
# main.py
from fastapi import FastAPI
from schemas import Student     # 👈 import from your new file

app = FastAPI()
students = []

@app.post("/students")
def add_student(student: Student):    # 👈 same as before, just imported
    students.append(student.model_dump())
    return student
```

### That's it!

The behavior is **exactly the same**. But now:

✅ Models live in one clean file
✅ Endpoints live in another clean file
✅ You can grow each independently
✅ Other files (`tests.py`, `database.py`, etc.) can also `from schemas import Student`

### What does the word "schemas" mean?

A **schema** is a "shape" — a description of what data should look like. Pydantic models *are* schemas. So `schemas.py` literally means "the file that holds the shapes of our data."

> 💡 In real projects you may see other names too: `models.py`, `dtos.py`, `validators.py`. They all mean roughly the same thing.

---

## 4. Input vs Output Models

This is the **most important idea** in Part 2. Read it slowly. 🎯

### The form-vs-receipt analogy

Imagine you visit a bank to deposit money:

| You give to bank | Bank gives to you |
|------------------|-------------------|
| **Deposit slip** (your name, amount) | **Receipt** (slip details + transaction ID + date + balance) |
| You filled it in | Bank filled it in |
| Slip → bank | Receipt → you |

The two are **different documents** — they have different fields, different purposes, different shapes.

### The same is true in APIs

When a client creates a student:

| Client sends (INPUT) | Server returns (OUTPUT) |
|----------------------|-------------------------|
| `name`, `age` | `id`, `name`, `age`, `created_at` |
| What user typed | What system stored, with extras |

The client **doesn't know** the `id` yet — the server creates it. So input and output have **different shapes**.

### One model is not enough!

If you use one Pydantic model for both:

```python
class Student(BaseModel):
    id: int      # 👈 problem: client must provide this!
    name: str
    age: int
```

Now the client is forced to send `id` even though they don't have one.

If you make `id` optional:

```python
class Student(BaseModel):
    id: int | None = None
    name: str
    age: int
```

Now the response can have `id=None` for new students — also wrong!

### The clean solution: TWO models

```python
class StudentCreate(BaseModel):    # 👈 INPUT: what client sends
    name: str
    age: int

class StudentResponse(BaseModel):  # 👈 OUTPUT: what server returns
    id: int
    name: str
    age: int
```

- **`StudentCreate`** — client → server (no `id`)
- **`StudentResponse`** — server → client (has `id`)

Different shapes, different purposes. **Clear and clean.** ✨

> **Naming convention:** `XxxCreate` for input, `XxxResponse` (or `XxxOut`) for output. Real projects use these names.

---

## 5. Response Models

Now the question: **how do you tell FastAPI what shape the response should be?**

### Without a response model (the messy way):

```python
@app.post("/students")
def add_student(student: StudentCreate):
    new_student = {
        "id": len(students) + 1,
        "name": student.name,
        "age": student.age,
        "secret_internal_field": "hidden_data",   # 👈 oops, this leaks!
    }
    students.append(new_student)
    return new_student    # FastAPI returns whatever you give it
```

The client receives:

```json
{
  "id": 1,
  "name": "Ahmed",
  "age": 20,
  "secret_internal_field": "hidden_data"
}
```

😱 **The internal field leaked!** No validation, no filtering. FastAPI just returns the dictionary as-is.

### With a response model (the clean way):

```python
@app.post("/students", response_model=StudentResponse)
def add_student(student: StudentCreate):
    new_student = {
        "id": len(students) + 1,
        "name": student.name,
        "age": student.age,
        "secret_internal_field": "hidden_data",
    }
    students.append(new_student)
    return new_student
```

The client receives:

```json
{
  "id": 1,
  "name": "Ahmed",
  "age": 20
}
```

✅ The secret field is **gone** — `response_model` filtered it out.

---

## 6. Using `response_model=`

### Where do you put it?

`response_model=` goes inside the route decorator:

```python
@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int):
    ...

@app.post("/students", response_model=StudentResponse)
def add_student(student: StudentCreate):
    ...

@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student: StudentCreate):
    ...
```

### What does `response_model` actually do?

When you set `response_model=StudentResponse`, FastAPI does **four things automatically**:

1. **Filters** — drops any field not listed in `StudentResponse`
2. **Validates** — makes sure the data matches `StudentResponse` types
3. **Documents** — shows the response shape in `/docs`
4. **Serializes** — converts Pydantic objects to clean JSON

> Think of `response_model` as a "border guard" who checks every response leaving your API.

### Example with full code:

```python
# schemas.py
from pydantic import BaseModel, Field

class StudentCreate(BaseModel):
    name: str = Field(min_length=1)
    age: int = Field(gt=0)

class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
```

```python
# main.py
from fastapi import FastAPI, HTTPException
from schemas import StudentCreate, StudentResponse

app = FastAPI()
students = []

@app.post("/students", response_model=StudentResponse)
def add_student(student: StudentCreate):
    new_student = {
        "id": len(students) + 1,
        "name": student.name,
        "age": student.age,
    }
    students.append(new_student)
    return new_student

@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int):
    for s in students:
        if s["id"] == student_id:
            return s
    raise HTTPException(status_code=404, detail="Student not found")
```

Now `/docs` shows:
- POST `/students` — Body: `StudentCreate`, Response: `StudentResponse`
- GET `/students/{id}` — Response: `StudentResponse`

Cleanly documented. Frontend developers love this.

---

## 7. Hidden Security Benefit

Let's see why `response_model` saves you from real disasters.

### Story:

Ali builds a User API. He stores the password in his data dictionary (he'll learn proper hashing later):

```python
# schemas.py
class UserCreate(BaseModel):
    name: str
    email: str
    password: str    # client sends password to register

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    # 👆 NOTE: no password field
```

```python
# main.py
@app.post("/users", response_model=UserResponse)
def register(user: UserCreate):
    new_user = {
        "id": 1,
        "name": user.name,
        "email": user.email,
        "password": user.password,    # stored internally
    }
    users.append(new_user)
    return new_user
```

### What does the client see?

```json
{
  "id": 1,
  "name": "Ali",
  "email": "ali@example.com"
}
```

🛡️ **The password is hidden!** Even though `new_user` had it, `response_model` removed it before sending.

### Without `response_model`:

```json
{
  "id": 1,
  "name": "Ali",
  "email": "ali@example.com",
  "password": "ali123"
}
```

😱 **Password leaked in the response!** This is a real security incident.

### Lesson:

> **Always use `response_model=` for endpoints that return user data.**
> It is your last line of defense against accidentally leaking data.

---

## 8. `model_dump()`

You have a Pydantic object. You want a regular Python dictionary. **What do you do?**

```python
student = Student(name="Ahmed", age=20)

# This is a Pydantic object, NOT a dict
print(student)
# name='Ahmed' age=20

# Convert to dict:
data = student.model_dump()
print(data)
# {'name': 'Ahmed', 'age': 20}

print(type(data))
# <class 'dict'>
```

### When do you need `model_dump()`?

| Use case | Why |
|----------|-----|
| Saving to a list (`students.append(...)`) | Lists usually hold dicts |
| Saving to JSON file | `json.dump()` needs a dict |
| Passing to a database | Most DB libraries take dicts |
| Logging or printing | Cleaner than the Pydantic format |
| Sending to another API | Most HTTP libraries need a dict |

### Example: appending to a list

```python
# Before model_dump:
students.append(student)               # ❌ a Pydantic object inside a list of dicts → mixed types!

# After model_dump:
students.append(student.model_dump())  # ✅ all items are dicts
```

### Useful options

**Skip some fields:**

```python
student.model_dump(exclude={"age"})
# {'name': 'Ahmed'}
```

**Keep only some fields:**

```python
student.model_dump(include={"name"})
# {'name': 'Ahmed'}
```

**Skip fields that are `None`:**

```python
class Book(BaseModel):
    title: str
    author: str | None = None

book = Book(title="Python")
book.model_dump()
# {'title': 'Python', 'author': None}

book.model_dump(exclude_none=True)
# {'title': 'Python'}
```

> **Quick note on the old name:** In Pydantic v1, this method was called `.dict()`. In Pydantic v2 (which we're using), it is `.model_dump()`. If you see `.dict()` in old tutorials, that's why.

---

## 9. `model_dump_json()`

Sometimes you need a **JSON string** (not a dict).

```python
student = Student(name="Ahmed", age=20)

json_string = student.model_dump_json()
print(json_string)
# '{"name":"Ahmed","age":20}'

print(type(json_string))
# <class 'str'>
```

### Difference between `model_dump()` and `model_dump_json()`:

| Method | Returns | Looks like |
|--------|---------|------------|
| `model_dump()` | `dict` (Python object) | `{'name': 'Ahmed', 'age': 20}` |
| `model_dump_json()` | `str` (text) | `'{"name":"Ahmed","age":20}'` |

### When to use which?

- **`model_dump()`** — when you stay inside Python (lists, function arguments, DB)
- **`model_dump_json()`** — when you write to a file or send over the network as text

### Example: saving to a file

```python
with open("student.json", "w") as f:
    f.write(student.model_dump_json())
```

Pretty-print with indentation:

```python
print(student.model_dump_json(indent=2))
# {
#   "name": "Ahmed",
#   "age": 20
# }
```

---

## 10. Dict → Pydantic

The reverse direction — you **have** a dictionary, you want a Pydantic object.

### Why would you need this?

You read data from somewhere (a JSON file, a database, an external API). You get back a `dict`. To validate it and use Pydantic features, you must convert it.

### Way 1: Unpacking with `**`

```python
data = {"name": "Ahmed", "age": 20}

student = Student(**data)        # 👈 unpacks dict as keyword arguments
print(student.name)              # Ahmed
```

The `**` unpacks the dict so it becomes:

```python
Student(name="Ahmed", age=20)    # same thing, after unpacking
```

### Way 2: `model_validate()` (preferred)

```python
data = {"name": "Ahmed", "age": 20}

student = Student.model_validate(data)
print(student.name)              # Ahmed
```

### Way 3: From a JSON string — `model_validate_json()`

```python
json_text = '{"name": "Ahmed", "age": 20}'

student = Student.model_validate_json(json_text)
print(student.name)              # Ahmed
```

### Both apply full validation!

Wrong types still fail:

```python
data = {"name": 123, "age": "twenty"}    # ❌ wrong types

student = Student.model_validate(data)
# pydantic.ValidationError: 2 validation errors for Student
# name: Input should be a valid string
# age: Input should be a valid integer
```

### Round-trip example:

```python
# 1. Object → dict
student = Student(name="Ahmed", age=20)
data = student.model_dump()                # dict

# 2. dict → object
student2 = Student.model_validate(data)    # Pydantic object again

# Same data, both directions work!
```

---

## 11. Nested Models

Real-world data is **structured**. A student has an address. An address has a street, city, and country. This is **nesting**.

### Naive approach (flat fields):

```python
class Student(BaseModel):
    name: str
    age: int
    street: str
    city: str
    country: str
```

This works for one address, but:
- Field names are mixed (student fields + address fields)
- Can't reuse `Address` for `Teacher` or `School`
- JSON looks flat, missing real structure

### Better approach: a separate `Address` model

```python
class Address(BaseModel):
    street: str
    city: str
    country: str

class Student(BaseModel):
    name: str
    age: int
    address: Address    # 👈 a model inside a model!
```

### How JSON looks now:

```json
{
  "name": "Ahmed",
  "age": 20,
  "address": {
    "street": "Main Road",
    "city": "Karachi",
    "country": "Pakistan"
  }
}
```

Notice the **nested object** — `address` is itself an object with its own fields. This matches how the data is in real life.

### How does Pydantic validate it?

It validates **both levels at once**.

```python
data = {
    "name": "Ahmed",
    "age": 20,
    "address": {
        "street": 123,           # ❌ should be string
        "city": "Karachi",
        "country": "Pakistan"
    }
}

student = Student.model_validate(data)
# ValidationError: 1 validation error for Student
# address.street
#   Input should be a valid string
```

The error path is `address.street` — Pydantic walks **into** the nested model.

### Accessing nested fields:

```python
student = Student(
    name="Ahmed",
    age=20,
    address=Address(
        street="Main Road",
        city="Karachi",
        country="Pakistan"
    )
)

print(student.address.city)        # Karachi
print(student.address.country)     # Pakistan
```

Use **dot chaining** — `student.address.city`.

### `model_dump()` works on nested models too:

```python
student.model_dump()
# {
#   'name': 'Ahmed',
#   'age': 20,
#   'address': {
#     'street': 'Main Road',
#     'city': 'Karachi',
#     'country': 'Pakistan'
#   }
# }
```

The nested `Address` was automatically converted to a dict.

---

## 12. Multiple Levels of Nesting

You can nest as deep as you want.

### Example: `School → Student → Address`

```python
class Address(BaseModel):
    street: str
    city: str

class Student(BaseModel):
    name: str
    address: Address

class School(BaseModel):
    name: str
    principal: Student     # 👈 a Student is inside a School
```

```python
school = School(
    name="Greenfield High",
    principal=Student(
        name="Mr. Khan",
        address=Address(
            street="Park Road",
            city="Lahore"
        )
    )
)

print(school.principal.address.city)    # Lahore
```

JSON form:

```json
{
  "name": "Greenfield High",
  "principal": {
    "name": "Mr. Khan",
    "address": {
      "street": "Park Road",
      "city": "Lahore"
    }
  }
}
```

> **Tip:** In practice, keep nesting reasonable (2–3 levels max). Deep nesting becomes hard to read and use.

---

## 13. Lists of Nested Models

What if a student has **multiple tags**? Or multiple emails? Or multiple addresses?

### Simple list of strings (what you already know):

```python
class Student(BaseModel):
    name: str
    tags: list[str]
```

```json
{
  "name": "Ahmed",
  "tags": ["python", "beginner", "smart"]
}
```

### List of nested models (new and powerful):

```python
class Tag(BaseModel):
    name: str
    priority: int

class Student(BaseModel):
    name: str
    tags: list[Tag]    # 👈 a list of Tag objects
```

```json
{
  "name": "Ahmed",
  "tags": [
    {"name": "python", "priority": 1},
    {"name": "beginner", "priority": 2}
  ]
}
```

### Pydantic validates each item in the list:

```python
data = {
    "name": "Ahmed",
    "tags": [
        {"name": "python", "priority": 1},
        {"name": "smart", "priority": "high"}     # ❌ priority should be int
    ]
}

Student.model_validate(data)
# ValidationError: tags.1.priority
#   Input should be a valid integer
```

The error path `tags.1.priority` means: "in the `tags` list, item at index 1, field `priority`".

### Real-world example: a student with multiple addresses

```python
class Address(BaseModel):
    street: str
    city: str

class Student(BaseModel):
    name: str
    addresses: list[Address]    # home + hostel + office, etc.
```

```json
{
  "name": "Sara",
  "addresses": [
    {"street": "House #5", "city": "Karachi"},
    {"street": "Hostel Block A", "city": "Lahore"}
  ]
}
```

---

## 14. `list[Model]` as Response

What if your endpoint returns **many** students at once?

```python
@app.get("/students", response_model=list[StudentResponse])
def get_students():
    return students       # a list of dicts → FastAPI converts each to StudentResponse
```

The client receives:

```json
[
  {"id": 1, "name": "Ahmed", "age": 20},
  {"id": 2, "name": "Sara", "age": 19},
  {"id": 3, "name": "Ali", "age": 22}
]
```

Each item is filtered through `StudentResponse` — extra fields removed, types validated, JSON cleanly produced.

### Comparison:

| Endpoint | `response_model` | Result |
|----------|-------------------|--------|
| GET `/students/{id}` | `StudentResponse` | one object |
| GET `/students` | `list[StudentResponse]` | a list of objects |

> **Tip:** `list[StudentResponse]` is read as: "a list where each item is a `StudentResponse`."

---

## 15. Optional Nested Models

Sometimes a nested object may not exist. A student might not have provided an address yet.

```python
class Student(BaseModel):
    name: str
    age: int
    address: Address | None = None       # 👈 optional nested model
```

Now both of these are valid:

```json
{ "name": "Ahmed", "age": 20 }
```

```json
{
  "name": "Ahmed",
  "age": 20,
  "address": {"street": "Main Road", "city": "Karachi"}
}
```

### Accessing safely:

```python
if student.address is not None:
    print(student.address.city)
else:
    print("No address provided")
```

If you do `student.address.city` when `address` is `None`, Python will crash with `AttributeError`. Always check.

---

## 16. `default_factory`

There's a small but **important** gotcha when you use a list or dict as a default.

### ❌ The wrong way:

```python
class Student(BaseModel):
    name: str
    tags: list[str] = []    # ⚠️ careful — this looks fine but can cause bugs
```

In **regular Python classes**, this would be dangerous because all instances would share the same list. Pydantic actually handles this safely for you — but the **clearer**, **more explicit** way is:

### ✅ The correct way:

```python
from pydantic import BaseModel, Field

class Student(BaseModel):
    name: str
    tags: list[str] = Field(default_factory=list)
```

`default_factory=list` says: "for each new student, call `list()` to make a brand-new empty list."

### Why this matters:

```python
s1 = Student(name="Ahmed")
s2 = Student(name="Sara")

s1.tags.append("python")
print(s2.tags)
# [] ✅ Sara's tags untouched
```

If you used a shared default, modifying `s1.tags` could secretly modify `s2.tags`.

### When to use `default_factory`:

| Default value | Use |
|---------------|-----|
| `0`, `""`, `True`, `None` | Plain `= 0`, `= ""`, `= None` |
| `[]`, `{}`, `set()` | `Field(default_factory=list)`, `Field(default_factory=dict)` |
| Current time, random ID | `Field(default_factory=datetime.now)` |

> **Rule of thumb:** Anything that should be **fresh for every new object** uses `default_factory`.

---

## 17. Common Mistakes

Beginners trip on these. Watch out! 🚧

### ❌ Mistake 1: Using one model for input AND output

```python
class Student(BaseModel):
    id: int    # ❌ client must send this!
    name: str
```

✅ **Correct:**

```python
class StudentCreate(BaseModel):
    name: str

class StudentResponse(BaseModel):
    id: int
    name: str
```

---

### ❌ Mistake 2: Forgetting `response_model=`

```python
@app.post("/students")          # ❌ no response_model — fields can leak
def add_student(s: StudentCreate):
    return {"id": 1, "name": s.name, "secret": "oops"}
```

✅ **Correct:**

```python
@app.post("/students", response_model=StudentResponse)
def add_student(s: StudentCreate):
    return {"id": 1, "name": s.name, "secret": "oops"}    # secret filtered out
```

---

### ❌ Mistake 3: Treating Pydantic objects like dicts

```python
student.model_dump()["name"]    # ✅ dict, square brackets work
student["name"]                  # ❌ Pydantic object, this fails
```

✅ **Correct:**

```python
student.name                     # ✅ dot notation on Pydantic object
```

---

### ❌ Mistake 4: Forgetting to import nested models

```python
# schemas.py
class Address(BaseModel):
    ...

class Student(BaseModel):
    address: Address
```

```python
# main.py
from schemas import Student        # ❌ Address not imported

# When sending data, use a dict — Pydantic handles nesting:
student = Student(
    name="Ahmed",
    age=20,
    address={"street": "...", "city": "..."}    # dict is fine
)
```

✅ **Best practice:** import what you actually use:

```python
from schemas import Student, Address
```

---

### ❌ Mistake 5: Mutable defaults without `default_factory`

```python
class Student(BaseModel):
    tags: list[str] = []     # works in Pydantic, but bad habit
```

✅ **Correct (clearer):**

```python
class Student(BaseModel):
    tags: list[str] = Field(default_factory=list)
```

---

### ❌ Mistake 6: `list[Model]` confusion in response

```python
@app.get("/students", response_model=StudentResponse)    # ❌ wrong — single object
def get_students():
    return students
```

✅ **Correct:**

```python
@app.get("/students", response_model=list[StudentResponse])    # ✅ a list
def get_students():
    return students
```

---

### ❌ Mistake 7: Using `.dict()` instead of `.model_dump()`

```python
student.dict()        # ❌ Pydantic v1 — old, deprecated
```

✅ **Correct (Pydantic v2):**

```python
student.model_dump()
```

---

## 18. Practice Exercises

Now get your hands dirty 👨‍💻

### Exercise 1: Split into `schemas.py`
Take any of your old FastAPI files. Move all Pydantic models to a new file called `schemas.py`. Import them in `main.py`.

### Exercise 2: `BookCreate` vs `BookResponse`
Create:
- `BookCreate` with `title`, `author`, `pages`
- `BookResponse` with `id`, `title`, `author`, `pages`, `is_published`

Use them in POST `/books` and GET `/books/{id}` endpoints.

### Exercise 3: Hide a sensitive field
Create a `User` system:
- `UserCreate` (name, email, password)
- `UserResponse` (id, name, email — NO password)

Test from `/docs` — confirm password never appears in the response.

### Exercise 4: `model_dump()` round trip
- Create a `Student` object
- Convert to dict with `model_dump()`
- Convert back to a `Student` with `Student.model_validate(...)`
- Print both — should be identical.

### Exercise 5: Save to JSON file
Create a `Book` object, then save it to `book.json` using `model_dump_json(indent=2)`. Open the file in your editor — verify it's pretty-printed JSON.

### Exercise 6: Nested model
Create `Address` and `Student` with `address: Address`. Build a sample object. Print `student.address.city`.

### Exercise 7: List of nested models
Build a `Course` model with `enrolled_students: list[Student]`. Add 3 students. Print each student's address city.

### Exercise 8: List response
Create GET `/students` that returns `list[StudentResponse]`. Add a few students with extra hidden fields. Confirm the response only shows `StudentResponse` fields.

### Exercise 9: Optional nested
Make `address` optional in `Student`. Try creating a student without an address — it should work. Try printing the address — handle the `None` case safely.

### Exercise 10: `default_factory`
Create a `Student` with `tags: list[str] = Field(default_factory=list)`. Build two students, append a tag to one, and confirm the other's list stays empty.

---

## 19. Quick Cheat Sheet

```python
# schemas.py — separate file for models
from pydantic import BaseModel, Field

# Input model
class StudentCreate(BaseModel):
    name: str = Field(min_length=1)
    age: int = Field(gt=0)

# Output model
class StudentResponse(BaseModel):
    id: int
    name: str
    age: int

# Nested model
class Address(BaseModel):
    street: str
    city: str

class StudentWithAddress(BaseModel):
    name: str
    address: Address                                         # nested
    tags: list[str] = Field(default_factory=list)            # safe default
    nicknames: list[str] | None = None                        # optional list
```

```python
# main.py — using them
from fastapi import FastAPI
from schemas import StudentCreate, StudentResponse

app = FastAPI()

@app.post("/students", response_model=StudentResponse)        # 👈 response model
def add_student(student: StudentCreate):
    new = {"id": 1, **student.model_dump()}                   # 👈 dump and merge
    return new

@app.get("/students", response_model=list[StudentResponse])   # 👈 list response
def get_students():
    return students
```

```python
# Conversion methods
student.model_dump()             # → dict
student.model_dump_json()        # → JSON string
Student(**data)                  # dict → object (unpack)
Student.model_validate(data)     # dict → object (preferred)
Student.model_validate_json(s)   # JSON string → object
```

---

## 🎯 Summary — What You Learned Today

✅ Why a separate `schemas.py` keeps your project clean
✅ The fundamental difference between **input** and **output** models
✅ `response_model=` in FastAPI — clean responses, hidden fields
✅ Real security benefit (password example)
✅ `model_dump()` — Pydantic → dict
✅ `model_dump_json()` — Pydantic → JSON string
✅ `Model(**data)` and `model_validate()` — dict → Pydantic
✅ `model_validate_json()` — JSON string → Pydantic
✅ Nested models — a model inside a model
✅ Multiple levels of nesting
✅ Lists of nested models — `list[Tag]`
✅ `list[Model]` as a response shape
✅ Optional nested models
✅ `default_factory` for safe list/dict defaults
✅ Common mistakes and how to avoid them

---

## 20. What's Next?

You now have **everything you need to write clean, professional Pydantic models for any API.**

In the **next class**, we leave Pydantic for a moment and move to **databases** with **SQLite**:
- Why lists die when the server restarts
- What a database actually is
- Storing data on disk so it survives forever
- Basic SQL: `CREATE TABLE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`
- Parameterized queries (security!)

After that, we'll **combine Pydantic + FastAPI + SQLite** so your API endpoints save data permanently. That's where everything you've learned starts working together.

### Future classes will cover:

- Custom validators (`@field_validator`) — your own validation logic
- Cross-field validation (`@model_validator`)
- Special types like `EmailStr`, `HttpUrl`, dates
- Pydantic settings for environment variables
- Generic models for reusable shapes

But you don't need any of that yet. **What you've learned in Part 1 + Part 2 covers 80% of real-world Pydantic use cases.**

---

**Remember:** Input ≠ Output. Models live in `schemas.py`. Use `response_model=`. `model_dump()` is your bridge between Pydantic and dicts. 💪

```python
# The Part 2 mantra:
class XxxCreate(BaseModel): ...    # what client sends
class XxxResponse(BaseModel): ...  # what server returns
@app.post(..., response_model=XxxResponse)
```

**Happy Coding! 🚀**
