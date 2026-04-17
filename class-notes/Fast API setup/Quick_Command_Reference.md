# ⚡ FastAPI Quick Command Reference

**Copy-paste these commands in order to get started quickly!**

---

## 1️⃣ Check Python is Installed

```bash
python --version
```

**You should see:** `Python 3.10.5` (or similar version)

---

## 2️⃣ Create Project Folder

```bash
cd Desktop
mkdir fastapi_learn
cd fastapi_learn
```

**Now you are in:** `Desktop\fastapi_learn>`

---

## 3️⃣ Create Virtual Environment

```bash
python -m venv venv
```

**This creates:** A `venv` folder in your project

---

## 4️⃣ Activate Virtual Environment

### On Windows (PowerShell):
```bash
.\venv\Scripts\Activate.ps1
```

### On Windows (Command Prompt):
```bash
venv\Scripts\activate
```

### On Mac/Linux:
```bash
source venv/bin/activate
```

**You will see:** `(venv)` at start of your terminal line

---

## 5️⃣ Install FastAPI

```bash
pip install fastapi uvicorn
```

**Wait for:** `Successfully installed fastapi uvicorn ...`

---

## 6️⃣ Create main.py File

**Create a file named `main.py` in your `fastapi_learn` folder**

**Copy this code into main.py:**

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello World!"}
```

---

## 7️⃣ Run Your API

```bash
uvicorn main:app --reload
```

**You will see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## 8️⃣ Open in Browser

**Copy-paste this in your browser address bar:**

```
http://localhost:8000/
```

**You will see:**
```json
{"message":"Hello World!"}
```

✅ **Success!**

---

## 🎁 Bonus: Interactive Documentation

**Open this in browser:**

```
http://localhost:8000/docs
```

**You will see:** A beautiful interactive API interface

---

## 🛑 Stop the Server

**Press in terminal:**

```
Ctrl + C
```

---

## 🔄 Next Time You Work on Your Project

```bash
cd Desktop/fastapi_learn
.\venv\Scripts\activate  # Activate virtual environment
uvicorn main:app --reload  # Run your API
```

---

## ⚠️ Common Errors & Quick Fixes

### "Module not found: fastapi"
```bash
# Make sure (venv) is showing
# Then reinstall:
pip install fastapi uvicorn
```

### "Port 8000 already in use"
```bash
# Use different port:
uvicorn main:app --port 8001 --reload
# Then visit: http://localhost:8001/
```

### "'python' not recognized"
- Reinstall Python from python.org
- Check "Add Python to PATH" during installation

### Virtual environment not activating on PowerShell
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📝 Code Templates to Try

### Template 1: Hello with Name
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello, {name}!"}
```

**Try:** `http://localhost:8000/hello/Ali`

---

### Template 2: Simple Math
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/add")
def add(a: int, b: int):
    return {"result": a + b}

@app.get("/multiply")
def multiply(a: int, b: int):
    return {"result": a * b}
```

**Try:**
- `http://localhost:8000/add?a=5&b=3`
- `http://localhost:8000/multiply?a=4&b=7`

---

### Template 3: Multiple Endpoints
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome!"}

@app.get("/user/{name}")
def user(name: str):
    return {"name": name, "message": f"Hello, {name}!"}

@app.get("/age")
def age(birth_year: int):
    return {"age": 2024 - birth_year}
```

**Try:**
- `http://localhost:8000/`
- `http://localhost:8000/user/Ali`
- `http://localhost:8000/age?birth_year=2000`

---

## 📚 Running Starter Examples

### Go to examples folder:
```bash
cd FastAPI_Starter_Examples
```

### Run examples:
```bash
uvicorn 01_hello:app --reload
uvicorn 02_hello_name:app --reload
uvicorn 03_search:app --reload
uvicorn 04_create_user:app --reload
uvicorn 05_calculator:app --reload
```

---

## ✅ Success Checklist

- [ ] Python installed
- [ ] Project folder created
- [ ] Virtual environment created
- [ ] Virtual environment activated (see `(venv)`)
- [ ] FastAPI installed
- [ ] `main.py` created with code
- [ ] Server running (`uvicorn main:app --reload`)
- [ ] Browser shows: `{"message":"Hello World!"}`
- [ ] `/docs` page works: `http://localhost:8000/docs`

**If all checked ✅, you are ready to code!**

---

## 🎓 What You Learned

✅ Python setup
✅ Virtual environments
✅ FastAPI basics
✅ Running a local server
✅ Accessing your API in browser
✅ API documentation

---

**Congratulations! You are a FastAPI developer! 🚀**

Next: Learn path parameters, query parameters, and request bodies!
