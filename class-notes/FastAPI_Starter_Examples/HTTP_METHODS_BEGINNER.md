# FastAPI HTTP Methods - Beginner Guide

Learn the basics of GET, POST, PUT, and DELETE without Pydantic!

---

## 1. GET - Read Data

**What it does:** Fetch/read data from the server

### Simple GET Example
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def say_hello():
    return {"message": "Hello, World!"}
```

**Test it:** `http://localhost:8000/hello`

**Response:**
```json
{"message": "Hello, World!"}
```

---

## 2. POST - Create/Add Data

**What it does:** Send data to the server to create something new

### Simple POST Example
```python
from fastapi import FastAPI

app = FastAPI()

messages = []

@app.post("/messages")
def add_message(msg: dict):
    messages.append(msg)
    return {"status": "Message added!", "message": msg}
```

**Test it in /docs:**
1. Go to `POST /messages`
2. Click "Try it out"
3. Enter in JSON body:
```json
{"text": "Hello", "author": "Ali"}
```
4. Click Execute

**Response:**
```json
{
  "status": "Message added!",
  "message": {"text": "Hello", "author": "Ali"}
}
```

---

## 3. DELETE - Remove Data

**What it does:** Delete something from the server

### Simple DELETE Example
```python
from fastapi import FastAPI

app = FastAPI()

items = [
    {"id": 1, "name": "Apple"},
    {"id": 2, "name": "Banana"},
    {"id": 3, "name": "Orange"}
]

@app.delete("/items/{item_id}")
def remove_item(item_id: int):
    global items
    items = [item for item in items if item["id"] != item_id]
    return {"status": "Item deleted!", "id": item_id}
```

**Test it:** `http://localhost:8000/items/1`

**Response:**
```json
{"status": "Item deleted!", "id": 1}
```

---

## 4. PUT - Update Data

**What it does:** Update/replace data on the server

### Simple PUT Example
```python
from fastapi import FastAPI

app = FastAPI()

users = [
    {"id": 1, "name": "Ali", "age": 20},
    {"id": 2, "name": "Fatima", "age": 22}
]

@app.put("/users/{user_id}")
def update_user(user_id: int, user: dict):
    for i, u in enumerate(users):
        if u["id"] == user_id:
            users[i] = {**u, **user}  # Merge updates
            return {"status": "User updated!", "user": users[i]}
    return {"error": "User not found"}
```

**Test it in /docs:**
1. Go to `PUT /users/1`
2. Click "Try it out"
3. Enter in JSON body:
```json
{"name": "Ahmed", "age": 25}
```
4. Click Execute

**Response:**
```json
{
  "status": "User updated!",
  "user": {"id": 1, "name": "Ahmed", "age": 25}
}
```

---

## Complete Example: Simple Todo API

Here's a complete API using GET, POST, PUT, DELETE:

```python
from fastapi import FastAPI

app = FastAPI()

todos = [
    {"id": 1, "task": "Learn FastAPI", "done": False},
    {"id": 2, "task": "Build API", "done": False}
]

# GET all todos
@app.get("/todos")
def get_todos():
    return {"todos": todos, "total": len(todos)}

# GET one todo
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    return {"error": "Todo not found"}

# POST - Add new todo
@app.post("/todos")
def create_todo(todo: dict):
    todo["id"] = len(todos) + 1
    todos.append(todo)
    return {"status": "Todo created!", "todo": todo}

# PUT - Update todo
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updates: dict):
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            todos[i] = {**todo, **updates}
            return {"status": "Todo updated!", "todo": todos[i]}
    return {"error": "Todo not found"}

# DELETE - Remove todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    return {"status": "Todo deleted!", "id": todo_id}
```

---

## Testing Guide

### Using Browser (Only for GET)
```
http://localhost:8000/todos
http://localhost:8000/todos/1
```

### Using /docs (All Methods)
1. Run: `uvicorn app:app --reload`
2. Go to: `http://localhost:8000/docs`
3. Expand each endpoint
4. Click "Try it out"
5. For POST/PUT: Enter JSON body
6. Click "Execute"

### Using curl (All Methods)
```bash
# GET
curl http://localhost:8000/todos

# POST
curl -X POST http://localhost:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"task": "New task", "done": false}'

# PUT
curl -X PUT http://localhost:8000/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'

# DELETE
curl -X DELETE http://localhost:8000/todos/1
```

---

## HTTP Methods Summary

| Method | Purpose | Example |
|--------|---------|---------|
| **GET** | Read/Fetch data | Get all users, Get one user |
| **POST** | Create new data | Add new user, Create post |
| **PUT** | Update existing data | Change user info, Update post |
| **DELETE** | Remove data | Delete user, Remove post |

---

## Key Points for Students

1. **GET** - No body needed, only query params
2. **POST** - Send data in JSON body
3. **PUT** - Update existing item, send new data in body
4. **DELETE** - No body needed, item ID in URL

**Remember:** Use `/docs` in your browser to test all methods easily!

---

**Next: Learn about data validation with Pydantic!**
