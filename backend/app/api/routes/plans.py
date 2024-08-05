from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from uuid import UUID

from app.schemas import PlanCreate, PlanRead, PlanUpdate
from app.crud import create_plan, get_plan, get_plans, update_plan, delete_plan
from app.api import deps
from app import models

router = APIRouter()


@router.get("/", response_model=List[PlanRead])
def read_plans(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    plans = get_plans(db, skip=skip, limit=limit)
    return plans


@router.get("/{plan_id}", response_model=PlanRead)
def read_plan(
    *,
    db: Session = Depends(deps.get_db),
    plan_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_superuser)
):
    plan = get_plan(db=db, plan_id=plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan


@router.post("/", response_model=PlanRead)
def write_plan(
    *,
    db: Session = Depends(deps.get_db),
    plan_in: PlanCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser)
):
    plan = create_plan(db=db, plan_in=plan_in)
    return plan


@router.put("/{plan_id}", response_model=PlanRead)
def upgrade_plan(
    *,
    db: Session = Depends(deps.get_db),
    plan_id: UUID,
    plan_in: PlanUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser)
):
    plan = update_plan(db=db, plan_id=plan_id, plan_in=plan_in)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan


@router.delete("/{plan_id}", response_model=PlanRead)
def drop_plan(
    *,
    db: Session = Depends(deps.get_db),
    plan_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_superuser)
):
    plan = delete_plan(db=db, plan_id=plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan
