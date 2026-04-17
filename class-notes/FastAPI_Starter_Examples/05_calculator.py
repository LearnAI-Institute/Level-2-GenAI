"""
Example 5: Simple Calculator API
Run: uvicorn 05_calculator:app --reload
Visit: http://localhost:8000/add?a=5&b=3
Visit: http://localhost:8000/multiply?a=4&b=7
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/add")
def add(a: int, b: int):
    """Add two numbers"""
    result = a + b
    return {
        "operation": "addition",
        "a": a,
        "b": b,
        "calculation": f"{a} + {b}",
        "result": result
    }

@app.get("/subtract")
def subtract(a: int, b: int):
    """Subtract two numbers"""
    result = a - b
    return {
        "operation": "subtraction",
        "a": a,
        "b": b,
        "calculation": f"{a} - {b}",
        "result": result
    }

@app.get("/multiply")
def multiply(a: int, b: int):
    """Multiply two numbers"""
    result = a * b
    return {
        "operation": "multiplication",
        "a": a,
        "b": b,
        "calculation": f"{a} * {b}",
        "result": result
    }

@app.get("/divide")
def divide(a: int, b: int):
    """Divide two numbers"""
    if b == 0:
        return {"error": "Cannot divide by zero!"}
    result = a / b
    return {
        "operation": "division",
        "a": a,
        "b": b,
        "calculation": f"{a} / {b}",
        "result": result
    }
