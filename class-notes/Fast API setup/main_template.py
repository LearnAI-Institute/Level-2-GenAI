# FastAPI Hello World Program
# Copy this code into a file named: main.py
# Then run: uvicorn main:app --reload
# Then visit: http://localhost:8000/

from fastapi import FastAPI

# Create a FastAPI application
app = FastAPI()

# Create an endpoint
# When someone visits http://localhost:8000/
# This function will run and return the message
@app.get("/")
def hello():
    return {"message": "Hello World!"}


# ============================================
# TRY THESE MODIFICATIONS BELOW:
# ============================================

# Uncomment one section at a time to try different things

# ------- MODIFICATION 1: Hello with Name -------
# @app.get("/hello/{name}")
# def greet(name: str):
#     return {"message": f"Hello, {name}!"}
#
# Visit: http://localhost:8000/hello/Ali
# Visit: http://localhost:8000/hello/Fatima


# ------- MODIFICATION 2: Simple Math -------
# @app.get("/add")
# def add(a: int, b: int):
#     return {"a": a, "b": b, "result": a + b}
#
# @app.get("/multiply")
# def multiply(a: int, b: int):
#     return {"a": a, "b": b, "result": a * b}
#
# Visit: http://localhost:8000/add?a=5&b=3
# Visit: http://localhost:8000/multiply?a=4&b=7


# ------- MODIFICATION 3: Calculate Age -------
# from datetime import datetime
#
# @app.get("/age")
# def calculate_age(birth_year: int):
#     current_year = datetime.now().year
#     age = current_year - birth_year
#     return {
#         "birth_year": birth_year,
#         "current_year": current_year,
#         "age": age
#     }
#
# Visit: http://localhost:8000/age?birth_year=2000


# ------- MODIFICATION 4: Multiple Endpoints -------
# @app.get("/")
# def home():
#     return {"message": "Welcome to my API!"}
#
# @app.get("/user/{username}")
# def get_user(username: str):
#     return {"username": username, "status": "active"}
#
# @app.get("/info")
# def info():
#     return {"author": "Your Name", "version": "1.0"}
#
# Visit: http://localhost:8000/
# Visit: http://localhost:8000/user/ali
# Visit: http://localhost:8000/info
