from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.api.deps import CurrentUser, SessionDep, get_db
from app.schemas import CotizacionObjetoCreate, CotizacionObjetoRead, CotizacionResponse
from app.services.cotizaciones import (
    SucursalService,
    DistribuidorService,
    CotizacionObjetoService,
    CotizacionService,
)
from app.assemblers.cotizaciones import CotizacionAssembler, CotizacionObjetoAssembler
from app.models import CotizacionObjeto

router = APIRouter()


def process_cotizacion(
    cotizacion_objeto: CotizacionObjetoCreate, db: Session
) -> CotizacionObjetoRead:
    sucursal = SucursalService.get_sucursal_by_clave(db, cotizacion_objeto.suc_clave)
    distribuidor = DistribuidorService.get_distribuidor_by_clave(
        db, cotizacion_objeto.distribuidor_clave
    )
    cotizacion_objeto_db = CotizacionObjetoService.get_cotizacion_objeto(
        db, cotizacion_objeto.id_convenio, sucursal.id, distribuidor.id
    )
    cotizaciones_db = CotizacionService.get_cotizaciones_by_objeto_id(
        db, cotizacion_objeto_db.id
    )

    cotizaciones = [
        CotizacionAssembler.assemble_cotizacion(cotizacion)
        for cotizacion in cotizaciones_db
    ]

    return CotizacionObjetoAssembler.assemble_cotizacion_objeto(
        cotizacion_objeto_db, sucursal, distribuidor, cotizaciones, cotizacion_objeto
    )


@router.get("/", response_model=List[CotizacionObjetoRead])
def get_cotizaciones(current_user: CurrentUser, session: SessionDep):
    result = session.exec(select(CotizacionObjeto)).all()
    return result


@router.post("/", response_model=CotizacionResponse)
def filter_get_cotizacion(
    cotizacion_objeto: CotizacionObjetoCreate,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    response_body = process_cotizacion(cotizacion_objeto, db)
    return CotizacionResponse(
        response_body=response_body, message_error=None, es_dato_valido=True
    )
