from pydantic import BaseModel, ConfigDict, EmailStr


class StudentCreate(BaseModel):
    name: str
    email: EmailStr


class StudentUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class CourseCreate(BaseModel):
    title: str
    student_id: int


class CourseUpdate(BaseModel):
    title: str | None = None
    student_id: int | None = None


class CourseResponse(BaseModel):
    id: int
    title: str
    student_id: int

    model_config = ConfigDict(from_attributes=True)