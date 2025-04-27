from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud, schemas
from database import SessionLocal
from auth import get_current_user
from models import User,Project

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.ProjectCreate)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_exist = db.query(User).filter(User.id == current_user.id).first()
    if not user_exist:
        raise HTTPException(status_code=400, detail="User not found")
    elif user_exist.role == "developer":
        raise HTTPException(status_code=400, detail="Developer cannot create project")

    return crud.create_project(db, project, user_exist)

@router.get("/", response_model=list[schemas.ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return crud.get_projects(db)

@router.get("/{project_id}", response_model=schemas.ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=schemas.ProjectCreate )
def update_project(project_id: int, project: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    print(project)
    print(project_id)

    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return crud.update_project(db, project_id, project)

@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return crud.delete_project(db, project_id)
