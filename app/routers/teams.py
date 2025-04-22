from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/teams", tags=["teams"])

@router.get("/", response_model=List[schemas.Team])
def read_teams(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_teams(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.Team, status_code=status.HTTP_201_CREATED)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    return crud.create_team(db=db, team=team)

@router.get("/{team_id}", response_model=schemas.Team)
def read_team(team_id: int, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id=team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team

@router.put("/{team_id}", response_model=schemas.Team)
def update_team(
    team_id: int, 
    team: schemas.TeamUpdate, 
    db: Session = Depends(get_db)
):
    db_team = crud.update_team(db, team_id=team_id, team=team)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team

@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    success = crud.delete_team(db, team_id=team_id)
    if not success:
        raise HTTPException(status_code=404, detail="Team not found")
    return None

@router.get("/{team_id}/projects", response_model=List[schemas.Project])
def get_team_projects(team_id: int, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id=team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team.projects