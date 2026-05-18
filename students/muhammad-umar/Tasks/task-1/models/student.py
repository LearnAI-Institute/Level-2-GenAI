from pydantic import BaseModel, Field, EmailStr
from datetime import date

class StudentBase(BaseModel):
    student_name: str = Field(
        ...,
        min_length=3,
        max_length=20
    )
    father_name: str = Field(
        ...,
        min_length=3,
        max_length=20
    )
    student_age: int = Field(
        ...,
        ge=5,
        le=18
    )
    student_current_class: int = Field(
        ...,
        ge=3,
        le=10
    )

class Address(BaseModel):
    city: str = Field(...)
    area: str = Field(...)
    house_no: str = Field(...)

class StudentCreate(StudentBase):
    admission_date: date = Field(...)
    parent_email: EmailStr = Field(...)
    address: Address = Field(...)

class StudentResponse(StudentBase):
    student_id: int