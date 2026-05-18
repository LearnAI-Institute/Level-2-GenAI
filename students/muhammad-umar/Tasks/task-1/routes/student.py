from fastapi import APIRouter, HTTPException, Depends

from models.student import StudentCreate, StudentResponse
from services import student_service
from database import get_db

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate, db=Depends(get_db)):
    data = student.model_dump()

    return student_service.create_student(data=data, db=db)

@router.get("/", response_model=list[StudentResponse])
def get_all(db=Depends(get_db)):
    return student_service.get_all(db)

@router.get("/{student_id}", response_model=StudentResponse)
def get_one(student_id: int, db=Depends(get_db)):
    student = student_service.get_one(student_id=student_id, db=db)

    if not student:
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {student_id} not found."
        )
    
    return student

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, update_student: StudentCreate, db=Depends(get_db)):
    data = update_student.model_dump()

    student = student_service.update_student(student_id=student_id, data=data, db=db)

    if not student:
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {student_id} not found."
        )
    
    return student

@router.delete("/{student_id}")
def delete_student(student_id: int, db=Depends(get_db)):
    student = student_service.delete_student(student_id=student_id, db=db)

    if not student:
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {student_id} not found."
        )
    
    return  {
        "message": f"Student with ID {student_id} deleted!",
        "student": student
    }