from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from app.schemas import EmisionResponse
from app.api.deps import get_db
from app.services.emision import get_all_emisiones

router = APIRouter()


@router.get("/", response_model=List[EmisionResponse])
def get_emisiones(db: Session = Depends(get_db)):
    return get_all_emisiones(db)
