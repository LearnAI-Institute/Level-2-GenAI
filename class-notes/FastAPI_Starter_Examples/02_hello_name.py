"""
Example 2: Hello with a Name (Path Parameters)
Run: uvicorn 02_hello_name:app --reload
Visit: http://localhost:8000/hello/Ali
Visit: http://localhost:8000/hello/Fatima
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello, {name}!"}
