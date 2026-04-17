"""
Example 3: Search with Query Parameters
Run: uvicorn 03_search:app --reload
Visit: http://localhost:8000/search?q=python
Visit: http://localhost:8000/search?q=fastapi
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/search")
def search(q: str):
    return {
        "you searched for": q,
        "results": ["result 1", "result 2", "result 3"],
        "total_results": 3
    }
