from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/", response_model=List[schemas.Project])
def read_projects(
    skip: int = 0,
    limit: int = 100,
    sort: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud.get_projects(db, skip=skip, limit=limit, sort=sort, status=status)

@router.post("/", response_model=schemas.Project, status_code=status.HTTP_201_CREATED)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db=db, project=project)

@router.get("/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.put("/{project_id}", response_model=schemas.Project)
def update_project(
    project_id: int, 
    project: schemas.ProjectUpdate, 
    db: Session = Depends(get_db)
):
    db_project = crud.update_project(db, project_id=project_id, project=project)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    success = crud.delete_project(db, project_id=project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return None

@router.post("/{project_id}/teams/{team_id}", response_model=schemas.Project)
def add_team_to_project(
    project_id: int, 
    team_id: int, 
    db: Session = Depends(get_db)
):
    project = crud.add_team_to_project(db, project_id=project_id, team_id=team_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project or Team not found")
    return project

@router.get("/{project_id}/tasks", response_model=List[schemas.Task])
def get_project_tasks(
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    sort: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud.get_tasks(db, skip=skip, limit=limit, project_id=project_id, status=status, sort=sort)