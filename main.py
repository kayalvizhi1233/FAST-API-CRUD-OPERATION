
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import Base, engine, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Student Management API",
    lifespan=lifespan
)


@app.get("/")
def read_database_contents(db: Session = Depends(get_db)):
    return {
        "message": "Data currently stored in MySQL",
        "students": crud.get_students(db),
        "courses": crud.get_courses(db),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)


# -------- STUDENT CRUD --------

@app.post(
    "/students",
    response_model=schemas.StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(
    data: schemas.StudentCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(models.Student).filter(
        models.Student.email == data.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    return crud.create_student(db, data)


@app.get("/students", response_model=list[schemas.StudentResponse])
def read_students(db: Session = Depends(get_db)):
    return crud.get_students(db)


@app.get("/students/{student_id}", response_model=schemas.StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


@app.put("/students/{student_id}", response_model=schemas.StudentResponse)
def edit_student(
    student_id: int,
    data: schemas.StudentUpdate,
    db: Session = Depends(get_db)
):
    if data.email is not None:
        existing = db.query(models.Student).filter(
            models.Student.email == data.email,
            models.Student.id != student_id
        ).first()

        if existing:
            raise HTTPException(status_code=409, detail="Email already exists")

    student = crud.update_student(db, student_id, data)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


@app.delete("/students/{student_id}")
def remove_student(student_id: int, db: Session = Depends(get_db)):
    if not crud.delete_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Student deleted successfully"}


# -------- COURSE CRUD --------

@app.post(
    "/courses",
    response_model=schemas.CourseResponse,
    status_code=status.HTTP_201_CREATED
)
def create_course(
    data: schemas.CourseCreate,
    db: Session = Depends(get_db)
):
    if crud.get_student(db, data.student_id) is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return crud.create_course(db, data)


@app.get("/courses", response_model=list[schemas.CourseResponse])
def read_courses(db: Session = Depends(get_db)):
    return crud.get_courses(db)


@app.get("/courses/{course_id}", response_model=schemas.CourseResponse)
def read_course(course_id: int, db: Session = Depends(get_db)):
    course = crud.get_course(db, course_id)

    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    return course


@app.put("/courses/{course_id}", response_model=schemas.CourseResponse)
def edit_course(
    course_id: int,
    data: schemas.CourseUpdate,
    db: Session = Depends(get_db)
):
    if data.student_id is not None:
        if crud.get_student(db, data.student_id) is None:
            raise HTTPException(status_code=404, detail="Student not found")

    course = crud.update_course(db, course_id, data)

    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    return course


@app.delete("/courses/{course_id}")
def remove_course(course_id: int, db: Session = Depends(get_db)):
    if not crud.delete_course(db, course_id):
        raise HTTPException(status_code=404, detail="Course not found")

    return {"message": "Course deleted successfully"}
