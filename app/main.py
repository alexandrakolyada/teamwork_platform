from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
import models
import schemas
import crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Users endpoints
@app.post("/users/", response_model=schemas.UserBase, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.UserBase])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

@app.get("/users/{user_id}", response_model=schemas.UserBase)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

@app.put("/users/{user_id}", response_model=schemas.UserBase)
def update_user(
    user_id: int, 
    user: schemas.UserUpdate, 
    db: Session = Depends(get_db)
):
    db_user = crud.update_user(db, user_id=user_id, user_update=user)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    if not crud.delete_user(db, user_id=user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

# Teams endpoints
@app.post("/teams/", response_model=schemas.TeamBase, status_code=status.HTTP_201_CREATED)
def create_team(team: schemas.TeamBase, db: Session = Depends(get_db)):
    return crud.create_team(db=db, team=team)

@app.get("/teams/", response_model=List[schemas.TeamBase])
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_teams(db, skip=skip, limit=limit)

@app.get("/teams/{team_id}", response_model=schemas.TeamBase)
def read_team(team_id: int, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id=team_id)
    if db_team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    return db_team

@app.put("/teams/{team_id}", response_model=schemas.TeamBase)
def update_team(
    team_id: int, 
    team: schemas.TeamBase, 
    db: Session = Depends(get_db)
):
    db_team = crud.update_team(db, team_id=team_id, team_update=team)
    if db_team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    return db_team

@app.delete("/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    if not crud.delete_team(db, team_id=team_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )

# Projects endpoints
@app.post("/projects/", response_model=schemas.ProjectBase, status_code=status.HTTP_201_CREATED)
def create_project(project: schemas.ProjectBase, db: Session = Depends(get_db)):
    return crud.create_project(db=db, project=project)

@app.get("/projects/", response_model=List[schemas.ProjectBase])
def read_projects(
    skip: int = 0,
    limit: int = 100,
    team_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_projects(db, skip=skip, limit=limit, team_id=team_id)

@app.get("/projects/{project_id}", response_model=schemas.ProjectBase)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return db_project

@app.put("/projects/{project_id}", response_model=schemas.ProjectBase)
def update_project(
    project_id: int,
    project: schemas.ProjectBase,
    db: Session = Depends(get_db)
):
    db_project = crud.update_project(db, project_id=project_id, project_update=project)
    if db_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return db_project

@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    if not crud.delete_project(db, project_id=project_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

# Tasks endpoints
@app.post("/tasks/", response_model=schemas.TaskBase, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskBase, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)

@app.get("/tasks/", response_model=List[schemas.TaskBase])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[int] = None,
    status: Optional[schemas.StatusEnum] = None,
    priority: Optional[schemas.PriorityEnum] = None,
    deadline_before: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    return crud.get_tasks(
        db,
        skip=skip,
        limit=limit,
        project_id=project_id,
        status=status,
        priority=priority,
        deadline_before=deadline_before
    )

@app.get("/tasks/{task_id}", response_model=schemas.TaskBase)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return db_task

@app.put("/tasks/{task_id}", response_model=schemas.TaskBase)
def update_task(
    task_id: int,
    task: schemas.TaskBase,
    db: Session = Depends(get_db)
):
    db_task = crud.update_task(db, task_id=task_id, task_update=task)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return db_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    if not crud.delete_task(db, task_id=task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

# Comments endpoints
@app.post("/comments/", response_model=schemas.CommentBase, status_code=status.HTTP_201_CREATED)
def create_comment(comment: schemas.CommentBase, db: Session = Depends(get_db)):
    return crud.create_comment(db=db, comment=comment)

@app.get("/comments/", response_model=List[schemas.CommentBase])
def read_comments(
    skip: int = 0,
    limit: int = 100,
    task_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_comments(db, skip=skip, limit=limit, task_id=task_id)

@app.get("/comments/{comment_id}", response_model=schemas.CommentBase)
def read_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = crud.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    return db_comment

@app.put("/comments/{comment_id}", response_model=schemas.CommentBase)
def update_comment(
    comment_id: int,
    comment: schemas.CommentBase,
    db: Session = Depends(get_db)
):
    db_comment = crud.update_comment(db, comment_id=comment_id, comment_update=comment)
    if db_comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    return db_comment

@app.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    if not crud.delete_comment(db, comment_id=comment_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

# Team Members endpoints
@app.post("/teams/{team_id}/members/{user_id}", status_code=status.HTTP_201_CREATED)
def add_team_member(
    team_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    team = crud.get_team(db, team_id=team_id)
    user = crud.get_user(db, user_id=user_id)
    
    if not team or not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team or User not found"
        )
    
    if user in team.members:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already in team"
        )
    
    team.members.append(user)
    db.commit()
    return {"message": "Member added successfully"}

@app.delete("/teams/{team_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_team_member(
    team_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    team = crud.get_team(db, team_id=team_id)
    user = crud.get_user(db, user_id=user_id)
    
    if not team or not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team or User not found"
        )
    
    if user not in team.members:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not a member of this team"
        )
    
    team.members.remove(user)
    db.commit()