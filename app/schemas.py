from pydantic import BaseModel, Field, validator, EmailStr, field_validator
from typing import Optional
from datetime import datetime, timedelta
from enum import Enum
import re

class StatusEnum(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class UserBase(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z0-9_]+$",
        examples=["john_doe"],
        description="Username must be 3-50 chars, alphanumeric with underscores"
    )
    
    email: EmailStr = Field(..., examples=["user@example.com"])

    @field_validator('username')
    def username_not_contain_spaces(cls, v):
        if ' ' in v:
            raise ValueError('Username cannot contain spaces')
        return v

class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Password must be 8-100 chars"
    )
    
    @field_validator('password')
    def password_complexity(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100)

class TeamBase(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        examples=["Dream Team"],
        description="Team name must be 2-100 chars"
    )
    
    description: Optional[str] = Field(None, max_length=500)

    @field_validator('name')
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Team name cannot be empty')
        return v

class ProjectBase(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        examples=["Awesome Project"],
        description="Project name must be 3-100 chars"
    )
    
    description: Optional[str] = Field(None, max_length=1000)
    team_id: int = Field(..., gt=0, examples=[1])

    @field_validator('name')
    def validate_project_name(cls, v):
        if not v[0].isupper():
            raise ValueError('Project name should start with uppercase letter')
        return v

class TaskBase(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=200,
        examples=["Implement feature X"],
        description="Task title must be 3-200 chars"
    )
    
    description: Optional[str] = Field(None, max_length=2000)
    status: StatusEnum = Field(default=StatusEnum.todo)
    priority: PriorityEnum = Field(default=PriorityEnum.medium)
    deadline: Optional[datetime] = None
    project_id: int = Field(..., gt=0)

    @field_validator('deadline')
    def deadline_in_future(cls, v):
        if v and v < datetime.now() + timedelta(hours=1):
            raise ValueError('Deadline must be at least 1 hour in the future')
        return v

    @field_validator('title')
    def title_not_all_caps(cls, v):
        if v.isupper():
            raise ValueError('Title should not be in all caps')
        return v

class CommentBase(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Comment text must be 1-2000 chars"
    )
    task_id: int = Field(..., gt=0)
    user_id: int = Field(..., gt=0)

    @field_validator('text')
    def text_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Comment cannot be empty or whitespace')
        return v

    @field_validator('text')
    def no_bad_words(cls, v):
        bad_words = ["spam", "ads", "http://", "https://"]
        if any(word in v.lower() for word in bad_words):
            raise ValueError('Comment contains prohibited content')
        return v