from fastapi import APIRouter, HTTPException, Depends

from services import course_service
from database import get_db

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)

@router.post("/{student_id}/{course_no}")
def assign_course(student_id: int, course_no: int, db=Depends(get_db)):
    data = course_service.assign_course(student_id=student_id, course_no=course_no, db=db)

    if data == "Student not found":
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {student_id} not found"
        )
    
    if data == "Course not found":
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )
    
    if data == "Student already exist":
        raise HTTPException(
            status_code=404,
            detail=f"The student with ID {student_id} has already been assigned to the course."
        )
    
    return {
        "message": f"Course assigned to student with ID {student_id} successfully",
        "course": data
    }

@router.get("/")
def get_all_courses(db=Depends(get_db)):
    return course_service.get_all_courses(db)

@router.get("/{student_id}")
def get_one_course(student_id: int, db=Depends(get_db)):
    data = course_service.get_one_course(student_id=student_id, db=db)

    if not data:
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {student_id} not found"
        )
    
    return data

@router.put("/{student_id}/{course_no}")
def update_course(student_id: int, course_no: int,  db=Depends(get_db)):
    data = course_service.update_student(student_id=student_id, course_no=course_no, db=db)

    if data == "Student not found":
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {student_id} not found"
        )
    
    if data == "Course not found":
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )
    
    return {
        "message": "Course updated successfully",
        "course": data
    }

@router.delete("/{student_id}")
def delete_course(student_id: int, db=Depends(get_db)):
    data = course_service.delete_student(student_id=student_id, db=db)

    if data == "Student not found":
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {student_id} not found"
        )
    
    return {
        "message": "Course deleted successfully",
        "course": data
    }