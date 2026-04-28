# Pydantic Basics — A Beginner-Friendly Guide

> Just by reading this guide, you will understand Pydantic.
> Plain English, step by step, with small examples.

---

## Table of Contents

1. [Recap from the previous class](#1-recap-from-the-previous-class)
2. [The real problem — why `dict` is not enough](#2-the-real-problem--why-dict-is-not-enough)
3. [What is Pydantic? (Simple definition)](#3-what-is-pydantic)
4. [Installation](#4-installation)
5. [Your first Pydantic model — `BaseModel`](#5-your-first-pydantic-model--basemodel)
6. [Data types — `str`, `int`, `float`, `bool`, `list`](#6-data-types)
7. [Pydantic + FastAPI — replacing `dict`](#7-pydantic--fastapi)
8. [Validation in action — sending wrong data](#8-validation-in-action)
9. [Default values — fields that are optional](#9-default-values)
10. [Optional fields — value may or may not be present](#10-optional-fields)
11. [Adding rules with `Field()` — `min_length`, `max_length`, `gt`, `ge`](#11-adding-rules-with-field)
12. [All errors are shown together](#12-all-errors-at-once)
13. [What changed in `/docs`?](#13-what-changed-in-docs)
14. [Common mistakes beginners make](#14-common-mistakes)
15. [Practice exercises](#15-practice-exercises)
16. [Quick cheat sheet](#16-quick-cheat-sheet)

---

## 1. Recap from the Previous Class

In the previous **FastAPI Basic** class, we built POST endpoints for `books`, `students`, and `products`. The code looked like this:

```python
from fastapi import FastAPI

app = FastAPI()

students = []

@app.post("/students")
def add_student(student: dict):   # 👈 we used `dict` here
    student["id"] = len(students) + 1
    students.append(student)
    return {"status": "Student registered!", "student": student}
```

**It was working — so what's new to learn?**

Listen to a small story first 👇

---

## 2. The Real Problem — Why `dict` is Not Enough

**Story:** Ahmed built the student API from the previous class. Happy with himself, he tested it from `/docs`. Everything worked. Then Fatima sent this JSON:

```json
{
  "name": 12345,
  "age": "twenty",
  "class": true
}
```

Ahmed's FastAPI **accepted it without saying a word**! ✅
- `name` got a number — no error
- `age` got a string — no error
- `class` got a boolean — no error

Then when Ahmed tried to store it in a database, it crashed 💥. Server error.

### Why did this happen?

```python
def add_student(student: dict):
    # `dict` means — "accept anything, I won't check"
    ...
```

`dict` is blind — it does not check whether the data is correct or not. It just takes whatever it gets.

### What if we check manually?

```python
def add_student(student: dict):
    # First check if name is a string
    if not isinstance(student.get("name"), str):
        return {"error": "name must be string"}

    # Then check if age is an integer
    if not isinstance(student.get("age"), int):
        return {"error": "age must be integer"}

    # Then check if name is empty
    if len(student.get("name", "")) == 0:
        return {"error": "name cannot be empty"}

    # Then check if age is negative
    if student.get("age", 0) < 0:
        return {"error": "age must be positive"}

    # ... and 20 more lines like this
    students.append(student)
    return student
```

😩 This **30-line** boring task has to be repeated for every endpoint. And if you forget any check, that's a bug.

**This is where Pydantic comes in as a friend.**

---

## 3. What is Pydantic?

> **Pydantic is a Python library that reads your type hints and automatically checks whether the data is in the correct format.**

In simple words:

| Without Pydantic | With Pydantic |
|------------------|---------------|
| Type hints are just like comments | Type hints become **rules** |
| `name: str` means "maybe a string" | `name: str` means "**MUST be a string, otherwise error**" |
| 30 lines of manual checking | 6 lines of clean model |
| Wrong data gets accepted | Wrong data is rejected immediately |

**In one line:** Pydantic = automatic data validator using Python type hints.

### Real-life analogy 🎯

Imagine you are a security guard at a school gate:
- **Without Pydantic guard:** "Come in, come in, everyone in" — even if someone is not student-shaped, they get in.
- **With Pydantic guard:** "Show your ID. Photo must match. Class written? Okay, go inside. Otherwise, go back."

Pydantic = strict but fair guard for your API. 🛡️

---

## 4. Installation

Open the terminal and run this command:

```bash
pip install pydantic
```

If FastAPI is already installed, **Pydantic is already installed** (FastAPI is built on top of Pydantic). Still, running this command once is safe.

To check the version:

```bash
python -c "import pydantic; print(pydantic.__version__)"
```

You should see something like `2.x.x`.

---

## 5. Your First Pydantic Model — `BaseModel`

Let's first create a `Student` model. Pure Python — **no FastAPI for now**.

```python
# step 1: import BaseModel from pydantic
from pydantic import BaseModel

# step 2: create your model class, inherit from BaseModel
class Student(BaseModel):
    name: str
    age: int
    is_active: bool

# step 3: use it!
ali = Student(name="Ali", age=20, is_active=True)

print(ali)              # name='Ali' age=20 is_active=True
print(ali.name)         # Ali
print(ali.age)          # 20
print(type(ali.age))    # <class 'int'>
```

### That's it? Just this much?

Yes, just this much! 🎉

- `class Student(BaseModel)` — inherited from `BaseModel` = got Pydantic's magic
- `name: str` — name must be a string
- `age: int` — age must be an integer
- `is_active: bool` — boolean (True/False)

**Type hints became the rules.** This is the most important point of Pydantic.

---

## 6. Data Types

Common types in Pydantic:

```python
from pydantic import BaseModel

class Book(BaseModel):
    title: str            # text — "Python Basics"
    pages: int            # whole number — 250
    price: float          # decimal number — 499.99
    is_published: bool    # True or False
    tags: list[str]       # list of strings — ["python", "beginner"]
```

### A correct example:

```python
book = Book(
    title="Python Basics",
    pages=250,
    price=499.99,
    is_published=True,
    tags=["python", "beginner"]
)
print(book)
# title='Python Basics' pages=250 price=499.99 is_published=True tags=['python', 'beginner']
```

### A wrong example (Pydantic will block it):

```python
book = Book(
    title=12345,              # ❌ this is a number, not a string!
    pages="two fifty",        # ❌ this is text, not an integer!
    price="very expensive",
    is_published="yes",
    tags="python"
)
```

**Output:**

```
ValidationError: 4 validation errors for Book
title
  Input should be a valid string [type=string_type, input_value=12345, input_type=int]
pages
  Input should be a valid integer [type=int_type, input_value='two fifty', input_type=str]
price
  Input should be a valid number [type=float_type, input_value='very expensive', input_type=str]
tags
  Input should be a valid list [type=list_type, input_value='python', input_type=str]
```

✨ **Notice:** Pydantic reported **all errors at once** — not one, but all four! In manual code, you would stop at the first error and the other bugs would stay hidden. This is a huge advantage of Pydantic.

---

## 7. Pydantic + FastAPI

Now the real work — using it with FastAPI. Let's rewrite the previous class's student endpoint with Pydantic.

### ❌ Before (with `dict` — wrong data was accepted):

```python
from fastapi import FastAPI

app = FastAPI()
students = []

@app.post("/students")
def add_student(student: dict):
    student["id"] = len(students) + 1
    students.append(student)
    return student
```

### ✅ Now (with Pydantic — automatic validation):

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
students = []

# First, define the Pydantic model
class Student(BaseModel):
    name: str
    age: int
    class_name: str

# Then, use it in the endpoint
@app.post("/students")
def add_student(student: Student):    # 👈 Student instead of dict
    new_student = {
        "id": len(students) + 1,
        "name": student.name,          # access with `.` (dict used [])
        "age": student.age,
        "class_name": student.class_name
    }
    students.append(new_student)
    return new_student
```

### What changed?

| Before (`dict`) | Now (`BaseModel`) |
|----------------|------------------|
| `student: dict` | `student: Student` |
| `student["name"]` | `student.name` |
| Wrong data accepted | Wrong data → 422 error |
| Generic schema in `/docs` | Proper schema in `/docs` |

---

## 8. Validation in Action

Run the server:

```bash
uvicorn main:app --reload
```

Open `http://localhost:8000/docs`, go to the `/students` POST endpoint, and send this JSON:

### ✅ Correct data:

```json
{
  "name": "Ahmed",
  "age": 20,
  "class_name": "BSCS-2"
}
```

**Response:** `200 OK`

```json
{
  "id": 1,
  "name": "Ahmed",
  "age": 20,
  "class_name": "BSCS-2"
}
```

### ❌ Wrong data (string in `age`):

```json
{
  "name": "Ahmed",
  "age": "twenty",
  "class_name": "BSCS-2"
}
```

**Response:** `422 Unprocessable Entity`

```json
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["body", "age"],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "twenty"
    }
  ]
}
```

### ❌ Forgot fields:

```json
{
  "name": "Ahmed"
}
```

**Response:** `422 Unprocessable Entity`

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "age"],
      "msg": "Field required"
    },
    {
      "type": "missing",
      "loc": ["body", "class_name"],
      "msg": "Field required"
    }
  ]
}
```

🎉 **You did not write a single line of validation code — Pydantic did it all by itself!**

> **Note:** A `422` status code means "the JSON is fine, but the data inside it is wrong".
> It is different from `400` — `400` means the JSON itself is broken.

---

## 9. Default Values

Some fields have a default value already set. For example, every new student is `is_active=True` by default.

```python
from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int
    is_active: bool = True   # 👈 default value, True if client doesn't send it
    grade: str = "A"          # 👈 default "A"
```

Now you can send only the required fields:

```json
{
  "name": "Sara",
  "age": 19
}
```

Pydantic will fill the rest automatically:

```json
{
  "name": "Sara",
  "age": 19,
  "is_active": true,
  "grade": "A"
}
```

---

## 10. Optional Fields

Sometimes a field may or may not be present. For example, `description` — if someone writes it, fine; if not, also fine.

```python
from pydantic import BaseModel

class Book(BaseModel):
    title: str
    author: str
    description: str | None = None   # 👈 optional — None as default
```

`str | None` means — "either a string, or `None`".
Writing `= None` is **mandatory** — otherwise the field becomes required!

### ⚠️ Common mistake:

```python
class Book(BaseModel):
    description: str | None       # ❌ default missing — this is REQUIRED!

# Correct way:
class Book(BaseModel):
    description: str | None = None   # ✅ `= None` needed to make it optional
```

---

## 11. Adding Rules with `Field()`

Just the type is not enough. Sometimes we need extra rules:
- Title must be at least 1 character
- Title must not exceed 200 characters
- Age must be greater than 0

For this, we use `Field()`:

```python
from pydantic import BaseModel, Field

class Student(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    age: int = Field(gt=0, lt=120)              # greater than 0, less than 120
    grade_percentage: float = Field(ge=0, le=100)  # between 0 and 100
```

### Constraints cheat sheet:

| Constraint | Meaning | Example |
|-----------|---------|---------|
| `min_length` | minimum string length | `min_length=3` (at least 3 characters) |
| `max_length` | maximum string length | `max_length=100` |
| `gt` | greater than (strictly more) | `gt=0` → > 0 |
| `ge` | greater than or equal | `ge=0` → ≥ 0 |
| `lt` | less than (strictly less) | `lt=100` → < 100 |
| `le` | less than or equal | `le=100` → ≤ 100 |

### A wrong example:

```json
{
  "name": "",
  "age": -5,
  "grade_percentage": 150
}
```

Pydantic gives 3 errors:

```
name: String should have at least 1 character
age: Input should be greater than 0
grade_percentage: Input should be less than or equal to 100
```

✨ **Three small constraints replaced three manual `if/raise` blocks!**

---

## 12. All Errors at Once

A **very important feature** of Pydantic — it does not stop at the first error.

```python
from pydantic import BaseModel, ValidationError

class Student(BaseModel):
    name: str
    age: int
    grade: str

try:
    s = Student(name=123, age="twenty", grade=True)
except ValidationError as e:
    print(e)
```

**Output:**

```
2 validation errors for Student
name
  Input should be a valid string [type=string_type, input_value=123, input_type=int]
age
  Input should be a valid integer [type=int_type, input_value='twenty', input_type=str]
```

> Wait — why didn't `grade=True` give an error? 🤔
>
> Pydantic **automatically converts** some types (this is called **coercion**). It turns `True` into the string `"True"`. The same happens with numbers — `"42"` (string) becomes `42` (int).
>
> This feature is useful for JSON, where numbers sometimes arrive as strings.

---

## 13. What Changed in `/docs`?

This is a **hidden gift** 🎁

### Before (with `dict`):

```
Request body
schema
{}
```

`/docs` had no idea what to send.

### Now (with Pydantic):

```
Request body
{
  "name": "string",
  "age": 0,
  "class_name": "string"
}
```

And for every field:
- Type
- Required or optional
- Constraints (min, max)
- Example value

**All automatic.**

One more benefit — a frontend developer can read your API documentation and instantly understand what to send. No more guessing!

---

## 14. Common Mistakes

Beginners make these mistakes — watch out! 🚧

### ❌ Mistake 1: Using `[]` like `dict`

```python
# Pydantic model:
class Student(BaseModel):
    name: str

@app.post("/students")
def add_student(student: Student):
    print(student["name"])   # ❌ Error! Pydantic model is not a dict
```

✅ **Correct:**

```python
print(student.name)   # ✅ Use dot notation
```

---

### ❌ Mistake 2: Optional field without a default

```python
class Book(BaseModel):
    description: str | None    # ❌ This is REQUIRED!
```

✅ **Correct:**

```python
class Book(BaseModel):
    description: str | None = None    # ✅ default is needed
```

---

### ❌ Mistake 3: Using `class` as a field name

```python
class Student(BaseModel):
    name: str
    class: str    # ❌ `class` is a Python reserved keyword!
```

✅ **Correct:**

```python
class Student(BaseModel):
    name: str
    class_name: str    # ✅ add underscore
```

---

### ❌ Mistake 4: Forgetting to import `BaseModel`

```python
class Student(BaseModel):    # ❌ NameError: BaseModel not defined
    name: str
```

✅ **Correct:**

```python
from pydantic import BaseModel    # ✅ import first

class Student(BaseModel):
    name: str
```

---

### ❌ Mistake 5: Just writing type hints (without `BaseModel`)

```python
class Student:    # ❌ Did not inherit BaseModel — no validation
    name: str
    age: int
```

✅ **Correct:**

```python
class Student(BaseModel):    # ✅ BaseModel is necessary
    name: str
    age: int
```

---

## 15. Practice Exercises

Now get your hands dirty 👨‍💻

### Exercise 1: `Product` model
Create:
- `name`: string, at least 1 character
- `price`: float, greater than 0
- `quantity`: integer, 0 or more
- `in_stock`: boolean, default `True`

### Exercise 2: `Teacher` model
Create:
- `name`: string, between 2 and 50 characters
- `subject`: string
- `experience_years`: integer, between 0 and 50
- `email`: string, optional (default `None`)

### Exercise 3: Use it in FastAPI
Use your `Product` model in a `/products` POST endpoint. Remove `dict`.

### Exercise 4: Test with wrong data
Send this JSON from `/docs`:
```json
{
  "name": "",
  "price": -100,
  "quantity": -5
}
```
All errors will appear together — count how many!

### Exercise 5: Optional field
Add `description` (optional) and `tags` (optional, default `[]`) to a `Book` model.

---

## 16. Quick Cheat Sheet

```python
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    # Basic types
    name: str
    age: int
    price: float
    is_active: bool
    tags: list[str]

    # Default value
    grade: str = "A"

    # Optional (None allowed)
    description: str | None = None

    # With constraints
    title: str = Field(min_length=1, max_length=200)
    score: int = Field(ge=0, le=100)
```

```python
# In FastAPI:
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post("/items")
def create_item(item: Item):       # 👈 Item instead of dict
    return {
        "name": item.name,          # 👈 dot access
        "price": item.price
    }
```

---

## 🎯 Summary — What Did You Learn Today?

✅ Why `dict` is not enough — no validation
✅ Pydantic = automatic data validator
✅ Creating a model with `BaseModel`
✅ Type hints (`str`, `int`, `float`, `bool`, `list`)
✅ Pydantic model instead of `dict` in FastAPI
✅ Validation error format (422)
✅ Default values and Optional fields
✅ `Field()` constraints — min/max/gt/ge
✅ All errors are shown at once
✅ Automatic schema in `/docs`

---

## 📚 What's Next?

In the next class:
- Keeping Pydantic models in a separate file (`schemas.py`)
- Response models — what the server sends back
- Nested models (a model inside a model)
- Database integration (SQLite)

---

**Remember:** Type hints + `BaseModel` = Magic 🪄

```python
class Student(BaseModel):
    name: str
    age: int
```

Just this little code, and Pydantic gives you:
- ✅ Type checking
- ✅ Required field check
- ✅ Auto error messages
- ✅ JSON parsing
- ✅ `/docs` schema

**Happy Coding! 🚀**
