from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Association table for many-to-many relationship
user_team = Table(
    'user_team',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('team_id', Integer, ForeignKey('teams.id'))
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    teams = relationship("Team", secondary=user_team, back_populates="members")

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(300))
    members = relationship("User", secondary=user_team, back_populates="teams")
    projects = relationship("Project", back_populates="team")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    team_id = Column(Integer, ForeignKey("teams.id"))
    team = relationship("Team", back_populates="projects")
    tasks = relationship("Task", back_populates="project")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    status = Column(String(20), default="todo")
    priority = Column(String(20), default="medium")
    deadline = Column(DateTime)
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="tasks")
    comments = relationship("Comment", back_populates="task")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(500), nullable=False)
    created_at = Column(DateTime, server_default='now()')
    task_id = Column(Integer, ForeignKey("tasks.id"))
    task = relationship("Task", back_populates="comments")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")