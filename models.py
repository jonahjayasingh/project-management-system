from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum

# ----- Enums -----

class RoleEnum(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    developer = "developer"

class TaskStatus(str, enum.Enum):
    todo = "To-Do"
    in_progress = "In Progress"
    done = "Done"

class TaskPriority(str, enum.Enum):
    low = "Low"
    medium = "Medium"
    high = "High"

# ----- Models -----

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(Enum(RoleEnum), default=RoleEnum.developer)
    
    tasks = relationship("Task", back_populates="assigned_user")
    projects = relationship("Project", back_populates="owner")


class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    
    created_at = Column(Date, default=datetime.utcnow)
    updated_at = Column(Date, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="projects")
    
    tasks = relationship("Task", back_populates="project")


class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    title = Column(String, index=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.todo)
    priority = Column(Enum(TaskPriority), default=TaskPriority.medium)
    due_date = Column(Date, nullable=True)

    created_at = Column(Date, default=datetime.utcnow)
    updated_at = Column(Date, default=datetime.utcnow, onupdate=datetime.utcnow)

    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    assigned_to = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    project = relationship("Project", back_populates="tasks")
    assigned_user = relationship("User", back_populates="tasks")
