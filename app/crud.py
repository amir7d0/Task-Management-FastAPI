from sqlalchemy.orm import Session
from . import models, schemas


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()


def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(title=task.title, description=task.description or "")
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    for field, value in task.dict(exclude_unset=True).items():
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    db.delete(db_task)
    db.commit()
    return db_task


def get_user_by_phone(db: Session, phone_number: str):
    return db.query(models.User).filter(models.User.phone_number == phone_number).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(phone_number=user.phone_number, name=user.name or "")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_otp(db: Session, phone_number: str):
    from datetime import datetime, timedelta
    import random

    user = get_user_by_phone(db, phone_number)
    if not user:
        user = create_user(db, schemas.UserCreate(phone_number=phone_number))

    otp_code = f"{random.randint(100000, 999999)}"
    user.otp_code = otp_code
    user.otp_expires_at = datetime.utcnow() + timedelta(minutes=5)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user, otp_code


def verify_otp(db: Session, phone_number: str, code: str):
    from datetime import datetime

    user = get_user_by_phone(db, phone_number)
    if not user or not user.otp_code:
        return None

    if user.otp_code != code:
        return None

    if not user.otp_expires_at or user.otp_expires_at < datetime.utcnow():
        return None

    user.otp_code = None
    user.otp_expires_at = None
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
