"""
Example 4: Create a User (POST Request with Request Body)
Run: uvicorn 04_create_user:app --reload
Visit: http://localhost:8000/docs to test POST
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define what a User looks like (Pydantic Model)
class User(BaseModel):
    name: str
    age: int
    email: str

# Store users in memory (just for this example)
users = []

@app.post("/users")
def create_user(user: User):
    """Create a new user"""
    users.append(user)
    return {
        "message": f"User {user.name} created successfully!",
        "user": user
    }

@app.get("/users")
def get_users():
    """Get all users"""
    return {"users": users, "total": len(users)}

@app.get("/users/{user_name}")
def get_user(user_name: str):
    """Get a specific user by name"""
    for user in users:
        if user.name.lower() == user_name.lower():
            return user
    return {"error": "User not found"}
