# FastAPI Starter Examples

These are ready-to-run examples for learning FastAPI basics.

## Quick Start

### 1. Install Requirements
```bash
pip install fastapi uvicorn
```

### 2. Run Any Example
```bash
# Example 1
uvicorn 01_hello:app --reload

# Example 2
uvicorn 02_hello_name:app --reload

# Example 3
uvicorn 03_search:app --reload

# Example 4
uvicorn 04_create_user:app --reload

# Example 5
uvicorn 05_calculator:app --reload
```

### 3. Access Your API
- **API:** http://localhost:8000/
- **Interactive Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc

---

## Examples Included

### 01_hello.py
**What it teaches:** Basic endpoint, JSON response

**Try it:**
```
http://localhost:8000/
```

**Response:**
```json
{"message": "Pakistan zinda bad!"}
```

---

### 02_hello_name.py
**What it teaches:** Path parameters (variables in URL)

**Try it:**
```
http://localhost:8000/hello/Ali
http://localhost:8000/hello/Fatima
```

**Response:**
```json
{"message": "Hello, Ali!"}
```

---

### 03_search.py
**What it teaches:** Query parameters (variables after ?)

**Try it:**
```
http://localhost:8000/search?q=python
http://localhost:8000/search?q=fastapi
http://localhost:8000/search?q=your_search_term
```

**Response:**
```json
{
  "you searched for": "python",
  "results": ["result 1", "result 2", "result 3"],
  "total_results": 3
}
```

---

### 04_create_user.py
**What it teaches:** POST requests, request body, Pydantic models

**Try it using http://localhost:8000/docs:**
1. Open the interactive docs
2. Click on "POST /users" endpoint
3. Click "Try it out"
4. Enter user data:
```json
{
  "name": "Ali",
  "age": 25,
  "email": "ali@example.com"
}
```
5. Click "Execute"

**Also try:**
```
http://localhost:8000/users (GET - see all users)
http://localhost:8000/users/Ali (GET - find specific user)
```

---

### 05_calculator.py
**What it teaches:** Multiple endpoints, type checking, error handling

**Try it:**
```
http://localhost:8000/add?a=5&b=3
http://localhost:8000/subtract?a=10&b=4
http://localhost:8000/multiply?a=6&b=7
http://localhost:8000/divide?a=20&b=4
http://localhost:8000/divide?a=20&b=0  (see error handling)
```

**Response:**
```json
{
  "operation": "addition",
  "a": 5,
  "b": 3,
  "calculation": "5 + 3",
  "result": 8
}
```

---

## Key Concepts Covered

| Example | Concept | URL Pattern |
|---------|---------|-------------|
| 01_hello | Basic endpoint | `/` |
| 02_hello_name | Path parameters | `/hello/{name}` |
| 03_search | Query parameters | `/search?q=something` |
| 04_create_user | POST, request body, model | `POST /users` |
| 05_calculator | Multiple endpoints, validation | `/add?a=1&b=2` |

---

## Common Commands

```bash
# Run with specific port
uvicorn 01_hello:app --port 8001 --reload

# Run without auto-reload (faster startup)
uvicorn 01_hello:app

# Run on all network interfaces (to access from other machines)
uvicorn 01_hello:app --host 0.0.0.0 --reload
```

---

## Troubleshooting

### "Module not found: fastapi"
```bash
pip install fastapi uvicorn
```

### "Port 8000 already in use"
```bash
# Use a different port
uvicorn 01_hello:app --port 8001 --reload
```

### "Connection refused"
- Make sure the API is running
- Check that you used `--reload` flag
- Wait a second for it to start

### "ModuleNotFoundError: No module named '01_hello'"
- Make sure you're in the same directory as the Python file
- Or use the full path: `uvicorn path.to.01_hello:app --reload`

---

## Next Steps

1. Run all examples and see how they work
2. Modify the examples (change messages, add new endpoints)
3. Try the exercises in the Class_2_Week_2_FastAPI_Basics.md file
4. Create your own API from scratch

---

## Important Notes for Students

- `@app.get()` = GET request (read data)
- `@app.post()` = POST request (create data)
- `@app.put()` = PUT request (update data)
- `@app.delete()` = DELETE request (delete data)

The **`--reload`** flag makes the server restart when you save changes. Great for development!

---

**Happy Learning! 🚀**
