from typing import List
from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from app.models import Emision


def get_all_emisiones(db: Session) -> List[Emision]:
    emisiones = db.exec(
        select(Emision).options(
            joinedload(Emision.certificados), joinedload(Emision.asegurados_adicionales)
        )
    ).all()
    if not emisiones:
        raise HTTPException(status_code=404, detail="No se encontraron emisiones")
    return emisiones
