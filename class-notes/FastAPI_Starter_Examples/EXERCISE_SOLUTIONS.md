# FastAPI Practice Exercises - Solutions

These are the solutions to the exercises from **Class_2_Week_2_FastAPI_Basics.md**

---

## Exercise 1: Hello Name API

### Problem
Create an API that:
- Has an endpoint `/greet/{name}`
- Returns a personalized greeting
- Example: `/greet/Ali` → `{"greeting": "Hello, Ali!"}`

### Solution
**File: `exercise1_hello_name.py`**

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/greet/{name}")
def greet(name: str):
    return {"greeting": f"Hello, {name}!"}
```

### Test it
```bash
uvicorn exercise1_hello_name:app --reload
# Visit: http://localhost:8000/greet/Ali
# Visit: http://localhost:8000/greet/Fatima
```

### Expected Response
```json
{"greeting": "Hello, Ali!"}
```

---

## Exercise 2: Age Calculator

### Problem
Create an API that:
- Has an endpoint `/age-in-years`
- Takes query parameter `birth_year`
- Returns how old someone is (approximate)
- Example: `/age-in-years?birth_year=2000` → `{"age": 24}`

### Solution
**File: `exercise2_age_calculator.py`**

```python
from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/age-in-years")
def calculate_age(birth_year: int):
    current_year = datetime.now().year
    age = current_year - birth_year
    return {
        "birth_year": birth_year,
        "current_year": current_year,
        "age": age
    }
```

### Test it
```bash
uvicorn exercise2_age_calculator:app --reload
# Visit: http://localhost:8000/age-in-years?birth_year=2000
# Visit: http://localhost:8000/age-in-years?birth_year=1995
```

### Expected Response
```json
{
  "birth_year": 2000,
  "current_year": 2026,
  "age": 26
}
```

---

## Exercise 3: Simple ToDo App

### Problem
Create an API that:
- Has `/todos` GET endpoint that returns all todos
- Has `/todos` POST endpoint to add a new todo
- Returns todo data as JSON

### Solution
**File: `exercise3_todo_app.py`**

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define what a Todo looks like
class Todo(BaseModel):
    title: str
    description: str
    completed: bool = False

# Store todos in memory
todos = []

@app.get("/todos")
def get_todos():
    """Get all todos"""
    return {
        "todos": todos,
        "total": len(todos)
    }

@app.post("/todos")
def create_todo(todo: Todo):
    """Create a new todo"""
    todos.append(todo)
    return {
        "message": "Todo created!",
        "todo": todo
    }

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    """Get a specific todo by index"""
    if 0 <= todo_id < len(todos):
        return todos[todo_id]
    return {"error": "Todo not found"}
```

### Test it
```bash
uvicorn exercise3_todo_app:app --reload
# Open: http://localhost:8000/docs
```

### Using the Interactive Docs
1. Click on `GET /todos`
2. Click "Execute" (should return empty list)
3. Click on `POST /todos`
4. Click "Try it out"
5. Enter:
```json
{
  "title": "Learn FastAPI",
  "description": "Complete all exercises",
  "completed": false
}
```
6. Click "Execute"
7. Go back to `GET /todos` and check your todos

### Expected Responses
**GET /todos (empty):**
```json
{
  "todos": [],
  "total": 0
}
```

**After POST:**
```json
{
  "todos": [
    {
      "title": "Learn FastAPI",
      "description": "Complete all exercises",
      "completed": false
    }
  ],
  "total": 1
}
```

---

## Exercise 4: Student Info

### Problem
Create an API that:
- Takes a student name and subject via query parameters
- Returns a message like "Ali is studying Python"
- Example: `/student?name=Ali&subject=Python`

### Solution
**File: `exercise4_student_info.py`**

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/student")
def student_info(name: str, subject: str):
    """Get student information"""
    return {
        "student_name": name,
        "subject": subject,
        "message": f"{name} is studying {subject}",
        "status": "active"
    }
```

### Test it
```bash
uvicorn exercise4_student_info:app --reload
# Visit: http://localhost:8000/student?name=Ali&subject=Python
# Visit: http://localhost:8000/student?name=Fatima&subject=Mathematics
```

### Expected Response
```json
{
  "student_name": "Ali",
  "subject": "Python",
  "message": "Ali is studying Python",
  "status": "active"
}
```

---

## Exercise 5: Math Quiz

### Problem
Create an API that:
- Has endpoints for `/add`, `/subtract`, `/multiply`
- Each takes two numbers as query parameters
- Returns the result and shows the calculation
- Example: `/multiply?a=5&b=6` → `{"calculation": "5 * 6 = 30", "result": 30}`

### Solution
**File: `exercise5_math_quiz.py`**

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/add")
def add(a: int, b: int):
    result = a + b
    return {
        "calculation": f"{a} + {b} = {result}",
        "result": result
    }

@app.get("/subtract")
def subtract(a: int, b: int):
    result = a - b
    return {
        "calculation": f"{a} - {b} = {result}",
        "result": result
    }

@app.get("/multiply")
def multiply(a: int, b: int):
    result = a * b
    return {
        "calculation": f"{a} * {b} = {result}",
        "result": result
    }

@app.get("/divide")
def divide(a: int, b: int):
    if b == 0:
        return {
            "error": "Cannot divide by zero!",
            "calculation": f"{a} / {b}"
        }
    result = a / b
    return {
        "calculation": f"{a} / {b} = {result}",
        "result": result
    }

@app.get("/power")
def power(a: int, b: int):
    result = a ** b
    return {
        "calculation": f"{a}^{b} = {result}",
        "result": result
    }
```

### Test it
```bash
uvicorn exercise5_math_quiz:app --reload
# Visit: http://localhost:8000/multiply?a=5&b=6
# Visit: http://localhost:8000/add?a=10&b=20
# Visit: http://localhost:8000/subtract?a=100&b=30
# Visit: http://localhost:8000/divide?a=20&b=4
# Visit: http://localhost:8000/divide?a=20&b=0
# Visit: http://localhost:8000/power?a=2&b=8
```

### Expected Responses
```json
// /multiply?a=5&b=6
{"calculation": "5 * 6 = 30", "result": 30}

// /add?a=10&b=20
{"calculation": "10 + 20 = 30", "result": 30}

// /divide?a=20&b=0
{"error": "Cannot divide by zero!", "calculation": "20 / 0"}
```

---

## Bonus Challenges

### Challenge 1: Multiple Operations in One Endpoint
```python
@app.get("/calculate/{operation}")
def calculate(operation: str, a: int, b: int):
    operations = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
    }
    if operation in operations:
        return {"result": operations[operation]}
    return {"error": f"Unknown operation: {operation}"}
```

### Challenge 2: User Registration with Validation
```python
from pydantic import BaseModel, EmailStr

class UserSignup(BaseModel):
    username: str
    email: str
    age: int

@app.post("/register")
def register(user: UserSignup):
    if user.age < 18:
        return {"error": "Must be 18 or older"}
    return {"message": f"Welcome, {user.username}!"}
```

### Challenge 3: Product Catalog
```python
class Product(BaseModel):
    name: str
    price: float
    stock: int

products_db = [
    {"id": 1, "name": "Laptop", "price": 999.99, "stock": 5},
    {"id": 2, "name": "Mouse", "price": 29.99, "stock": 50}
]

@app.get("/products")
def get_products():
    return products_db

@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products_db:
        if product["id"] == product_id:
            return product
    return {"error": "Product not found"}
```

---

## Grading Rubric

| Criterion | Points |
|-----------|--------|
| Code runs without errors | 20 |
| Correct endpoint path | 15 |
| Accepts correct parameters | 15 |
| Returns correct format (JSON) | 20 |
| Returns correct values/calculations | 20 |
| Good variable names | 5 |
| Documentation/comments | 5 |
| **Total** | **100** |

---

## Tips for Students

1. **Test with `/docs`** - Use the interactive documentation
2. **Read error messages** - They usually tell you what's wrong
3. **Check spelling** - Parameter names must match
4. **Type matters** - `int` vs `str` makes a difference
5. **JSON is case-sensitive** - `{"Name": "Ali"}` ≠ `{"name": "Ali"}`

---

## Common Student Mistakes

### Mistake 1: Wrong Parameter Name
```python
# Wrong
@app.get("/greet/{username}")
def greet(name: str):  # Should be 'username'
    return f"Hello {name}"

# Correct
@app.get("/greet/{name}")
def greet(name: str):
    return f"Hello {name}"
```

### Mistake 2: Forgetting Query Parameter
```python
# Wrong - this treats 'name' as path parameter
@app.get("/greet")
def greet(name: str):
    return {"message": f"Hello {name}"}

# Correct - query parameter has default or is in query
@app.get("/greet")
def greet(name: str = "Friend"):
    return {"message": f"Hello {name}"}
```

### Mistake 3: Not Using Pydantic for POST Data
```python
# Wrong - doesn't validate
@app.post("/users")
def create(data):
    return {"message": "Created"}

# Correct - validates input
from pydantic import BaseModel
class User(BaseModel):
    name: str
    age: int

@app.post("/users")
def create(user: User):
    return {"message": f"Created {user.name}"}
```

---

## How to Help Students Debug

1. **Check the error message** - Read the full error
2. **Verify imports** - Did they import BaseModel, FastAPI, etc.?
3. **Check file name** - Make sure they're running the right file
4. **Check the path** - Visit the correct URL
5. **Check the /docs** - Try from the interactive docs first

---

**Great job on completing these exercises! 🎉**

**Next week we'll learn about databases and storing data permanently!**
