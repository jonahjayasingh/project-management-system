from pydantic import BaseModel
from typing import Optional
from datetime import date
import enum

class RoleEnum(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    developer = "developer"

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
class UserBase(BaseModel):
    username: str
    role: RoleEnum

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    name :str
    description: Optional[str] = None
    
class ProjectOut(ProjectBase):
    id: int
    owner: Optional[UserOut] = None
    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    title: str
    status: Optional[str] = "To-Do"
    priority: Optional[str] = "Medium"
    due_date: Optional[date]
    project_id: int
    assigned_to: int

class TaskCreate(TaskBase):
    title: str
    status: Optional[str] = "To-Do"
    priority: Optional[str] = "Medium"
    due_date: Optional[date]
    project_id: int
    assigned_to: int

class TaskOut(TaskBase):
    id: int
    class Config:
        orm_mode = True

class TaskUpdate(TaskBase):
    id: int
    title: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None
    project_id: Optional[int] = None
    assigned_to: Optional[int] = None