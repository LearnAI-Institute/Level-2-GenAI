# 🚀 FastAPI Setup Guide for Beginners

Complete step-by-step guide to install FastAPI and create your first API that prints "Hello World".

---

## What is FastAPI?

**FastAPI** is a modern Python library that makes it very easy to build web APIs.

**API** = A way for programs to communicate with each other over the internet.

---

## ✅ Step 1: Check if Python is Installed

First, verify that Python is installed on your computer.

### Open Command Prompt or PowerShell and type:

```bash
python --version
```

### If you see something like this:
```
Python 3.10.5
```

✅ Great! Python is installed.

### If you see an error:
```
'python' is not recognized as an internal or external command
```

❌ You need to install Python. Download from [python.org](https://www.python.org)

**Important:** During installation, check the box that says "Add Python to PATH"

---

## 📁 Step 2: Create a Folder for Your Project

Open Command Prompt or PowerShell and type these commands:

### Go to your Desktop:
```bash
cd Desktop
```

### Create a new folder:
```bash
mkdir fastapi_learn
```

### Enter that folder:
```bash
cd fastapi_learn
```

**Now you are in your project folder** ✓

You should see:
```
Desktop\fastapi_learn>
```

---

## 🔧 Step 3: Create a Virtual Environment

### What is a Virtual Environment?

A **virtual environment** is an isolated space on your computer where you can install Python packages for your specific project. This keeps your project clean and organized.

### Command to create virtual environment:

```bash
python -m venv venv
```

### What happens:
- A folder named `venv` is created
- Inside it is a copy of Python
- You will install all packages here for this project

---

## ✅ Step 4: Activate the Virtual Environment

### If you are using Windows PowerShell:

```bash
.\venv\Scripts\Activate.ps1
```

### If you are using Windows Command Prompt (CMD):

```bash
venv\Scripts\activate
```

### If you are using Mac or Linux:

```bash
source venv/bin/activate
```

### How to know it worked:

You will see `(venv)` at the beginning of your terminal line:

```
(venv) Desktop\fastapi_learn>
```

✅ The `(venv)` shows that your virtual environment is active!

---

## 📦 Step 5: Install FastAPI and Uvicorn

**Make sure virtual environment is activated (you should see `(venv)` in your terminal)**

### Type this command:

```bash
pip install fastapi uvicorn
```

### What this does:
- **fastapi** = Library for building APIs
- **uvicorn** = Server to run your API

Wait a moment while it downloads and installs...

### When installation is complete, you will see:

```
Successfully installed fastapi uvicorn ...
```

✅ Done! FastAPI is installed.

---

## 📝 Step 6: Create Your First FastAPI Program

### Create a new file named: `main.py`

You can create this file using:

- VS Code
- PyCharm
- Any text editor

**In your `fastapi_learn` folder, create a file called `main.py`**

### Write this code in main.py:

```python
from fastapi import FastAPI

# Create a FastAPI application
app = FastAPI()

# Create an endpoint
@app.get("/")
def hello():
    return {"message": "Hello World!"}
```

### Understanding the code:

| Code | Meaning |
|------|---------|
| `from fastapi import FastAPI` | Import FastAPI library |
| `app = FastAPI()` | Create a new FastAPI application |
| `@app.get("/")` | When someone visits the root URL (`/`), run the function below |
| `def hello():` | Define a function that will run |
| `return {"message": "Hello World!"}` | Return a response in JSON format |

---

## 🎯 Step 7: Run Your FastAPI Program

**Make sure:**
1. You are in your `fastapi_learn` folder
2. Virtual environment is activated (you see `(venv)` in terminal)
3. You have `main.py` file created

### Type this command:

```bash
uvicorn main:app --reload
```

### What does this mean:
- `uvicorn` = The server program
- `main` = Your file (`main.py`)
- `app` = The variable in your code named `app`
- `--reload` = Restart automatically when you save changes

### What you will see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
INFO:     Application startup complete
```

✅ **Your FastAPI server is running!**

---

## 🌐 Step 8: View Your API in Browser

Open your web browser and go to:

```
http://localhost:8000/
```

or

```
http://127.0.0.1:8000/
```

### You will see:

```json
{"message":"Hello World!"}
```

🎉 **Congratulations! Your first FastAPI program works!**

---

## 📚 Step 9: Interactive API Documentation (Bonus)

FastAPI automatically creates beautiful documentation for your API.

### Open this URL in your browser:

```
http://localhost:8000/docs
```

### You will see:
- Interactive API documentation
- A testing interface for your API
- Everything automatically generated!

### This is called "Swagger UI"

You can click on endpoints and test them right here.

---

## 🛑 How to Stop Your Program

### Press these keys in your terminal:

```
Ctrl + C
```

This will stop the server.

You will see:
```
Shutting down
```

---

## 📋 Quick Reference - All Commands Together

Here are all the commands in order:

```bash
# Step 1: Create and enter folder
cd Desktop
mkdir fastapi_learn
cd fastapi_learn

# Step 2: Create virtual environment
python -m venv venv

# Step 3: Activate virtual environment
# For Windows PowerShell:
.\venv\Scripts\Activate.ps1
# For Windows CMD:
venv\Scripts\activate

# Step 4: Install FastAPI
pip install fastapi uvicorn

# Step 5: Run the program
# (Make sure main.py exists first)
uvicorn main:app --reload

# Step 6: Open in browser
# http://localhost:8000/
```

---

## ❓ Common Problems and Solutions

### Problem 1: "venv command not found"

**Solution:**
```bash
# Make sure Python is installed
python --version

# Create virtual environment again
python -m venv venv
```

### Problem 2: "'python' is not recognized"

**Solution:**
- Reinstall Python from [python.org](https://www.python.org)
- During installation, make sure to check "Add Python to PATH"
- Restart your computer after installation

### Problem 3: "Port 8000 already in use"

**Solution:**
```bash
# Use a different port number
uvicorn main:app --port 8001 --reload
```

Then open in browser:
```
http://localhost:8001/
```

### Problem 4: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:**
```bash
# Check if virtual environment is active
# You should see (venv) at the start of your terminal

# If not, activate it:
.\venv\Scripts\activate

# Then install again:
pip install fastapi uvicorn
```

### Problem 5: "pip: command not found"

**Solution:**
```bash
python -m pip install fastapi uvicorn
```

### Problem 6: Virtual Environment not activating

**For Windows PowerShell:**

If you get an error about execution policy, try:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:
```bash
.\venv\Scripts\Activate.ps1
```

---

## ✨ Next Steps - Modify Your Program

Once your first program works, try these modifications:

### Modification 1: Add a name parameter

Change `main.py` to:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello, {name}!"}
```

Save the file. The server will restart automatically (because of `--reload`).

Try these URLs:
```
http://localhost:8000/hello/Ali
http://localhost:8000/hello/Fatima
http://localhost:8000/hello/YourName
```

### Modification 2: Add a simple calculator

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

Try these URLs:
```
http://localhost:8000/add?a=5&b=3
http://localhost:8000/multiply?a=4&b=7
```

---

## 📚 Learning Resources

### Files provided in this course:
- `FastAPI_Starter_Examples/` - 5 complete working examples
- `Class_2_Week_2_FastAPI_Basics.ipynb` - Interactive Jupyter notebook
- `Class_2_Week_2_FastAPI_Basics.md` - Detailed course notes

### Commands to run examples:

```bash
cd FastAPI_Starter_Examples
uvicorn 01_hello:app --reload
uvicorn 02_hello_name:app --reload
uvicorn 03_search:app --reload
uvicorn 04_create_user:app --reload
uvicorn 05_calculator:app --reload
```

---

## 🎓 Important Concepts to Remember

### Virtual Environment
- **Why:** Keeps packages organized per project
- **How:** `python -m venv venv` to create, then activate it
- **Remember:** Always activate before working on your project

### Uvicorn Server
- **What:** A server that runs your FastAPI application
- **Start:** `uvicorn main:app --reload`
- **Stop:** Press `Ctrl + C`

### API Endpoint
- **Meaning:** A URL path that your API responds to
- **Example:** `/hello`, `/add`, `/multiply`

### JSON Response
- **What:** Data format for API responses
- **Format:** `{"key": "value", "number": 42}`
- **Automatic:** FastAPI converts Python dicts to JSON automatically

---

## ✅ Checklist - Everything Ready?

Before you start, make sure you have checked all of these:

- [ ] Python is installed (`python --version` works)
- [ ] Folder created (`fastapi_learn`)
- [ ] Virtual environment created (`python -m venv venv`)
- [ ] Virtual environment activated (`(venv)` shows in terminal)
- [ ] FastAPI installed (`pip install fastapi uvicorn`)
- [ ] `main.py` file created in your folder
- [ ] Code from Step 6 copied into `main.py`
- [ ] Server started (`uvicorn main:app --reload`)
- [ ] Browser shows response (`http://localhost:8000/`)
- [ ] You can see `/docs` page (`http://localhost:8000/docs`)

If all items are checked ✅, you are ready to learn FastAPI!

---

## 💡 Tips for Success

1. **Always activate virtual environment** - When you open a new terminal
2. **Use `--reload` flag** - During development, it saves time
3. **Check `/docs` page** - Use it to test your API
4. **Read error messages** - They usually tell you what's wrong
5. **Take breaks** - Programming is fun, but take breaks!

---

## 🚀 You Are Ready!

Congratulations! You have successfully:
- ✅ Installed Python
- ✅ Created a virtual environment
- ✅ Installed FastAPI
- ✅ Created your first API
- ✅ Ran it on a server
- ✅ Accessed it in your browser

**You are now a FastAPI developer! 👨‍💻👩‍💻**

---

## 📞 Need Help?

### If something goes wrong:

1. Read the error message carefully
2. Check the "Common Problems" section above
3. Make sure virtual environment is active
4. Make sure you saved the `main.py` file
5. Try reinstalling the packages

### If still stuck:

1. Review the steps again
2. Check that your file is named exactly `main.py`
3. Make sure there are no typos in the code
4. Restart your computer and try again

---

**Happy Coding! 🎉**

**Next: Learn about path parameters, query parameters, and POST requests!**
