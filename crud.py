from sqlalchemy.orm import Session
import models
import schemas


# STUDENT CRUD

def create_student(db: Session, data: schemas.StudentCreate):
    student = models.Student(**data.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def get_students(db: Session):
    return db.query(models.Student).all()


def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()


def update_student(db: Session, student_id: int, data: schemas.StudentUpdate):
    student = get_student(db, student_id)

    if student is None:
        return None

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(student, field, value)

    db.commit()
    db.refresh(student)
    return student


def delete_student(db: Session, student_id: int):
    student = get_student(db, student_id)

    if student is None:
        return False

    db.delete(student)
    db.commit()
    return True


# COURSE CRUD

def create_course(db: Session, data: schemas.CourseCreate):
    course = models.Course(**data.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def get_courses(db: Session):
    return db.query(models.Course).all()


def get_course(db: Session, course_id: int):
    return db.query(models.Course).filter(
        models.Course.id == course_id
    ).first()


def update_course(db: Session, course_id: int, data: schemas.CourseUpdate):
    course = get_course(db, course_id)

    if course is None:
        return None

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(course, field, value)

    db.commit()
    db.refresh(course)
    return course


def delete_course(db: Session, course_id: int):
    course = get_course(db, course_id)

    if course is None:
        return False

    db.delete(course)
    db.commit()
    return True