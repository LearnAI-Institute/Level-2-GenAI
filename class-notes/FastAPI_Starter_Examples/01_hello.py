"""
Example 1: Simple Hello World API
Run: uvicorn 01_hello:app --reload
Visit: http://localhost:8000/
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Pakistan zinda bad!"}
