from fastapi import FastAPI
from routes.student import router as student_router
from routes.course import router as course_router

app = FastAPI()

app.include_router(student_router)
app.include_router(course_router)