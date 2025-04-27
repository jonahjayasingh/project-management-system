from sqlalchemy.orm import Session
import models, schemas
from models import User
from database import SessionLocal
from fastapi import HTTPException

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, password=user.password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(models.User).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_project(db: Session, project: schemas.ProjectCreate, user_exist: User):
    db_project = models.Project(name=project.name, description=project.description, user_id=user_exist.id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project(db: Session, project_id: int, project: schemas.ProjectCreate):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    db_project.name = project.name
    db_project.description = project.description
    db.commit()
    db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    db.delete(db_project)
    db.commit()
    return {"detail": "Project deleted successfully"}

def get_projects(db: Session):
    return db.query(models.Project).all()

def create_task(db: Session, task: schemas.TaskCreate):
    print(task)
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session, project_id: int = None):
    print(project_id)
    query = db.query(models.Task)
    if project_id:
        query = query.filter(models.Task.project_id == project_id)
    return query.all()

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()
    
def update_task(db: Session, task_id: int, task: schemas.TaskCreate):
    print(db)
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    db_task.title = task.title
    db_task.status = task.status
    db_task.priority = task.priority
    db_task.due_date = task.due_date
    db_task.project_id = task.project_id
    db_task.assigned_to = task.assigned_to
    db.commit()
    db.refresh(db_task)
    return db_task

    
def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted successfully"}
    