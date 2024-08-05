from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import List
from app.schemas import CotizacionResponse
from app.api.deps import get_db
from app.services.cotizaciones import get_all_cotizaciones

router = APIRouter()


@router.get("/", response_model=List[CotizacionResponse])
def get_emisiones(
    db: Session = Depends(get_db),
    page: int = Query(1, alias="page"),
    limit: int = Query(10, alias="limit"),
):
    return get_all_cotizaciones(db, page=page, limit=limit)
