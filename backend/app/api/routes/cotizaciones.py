from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from uuid import UUID

from app.models import (
    Cotizacion,
    CotizacionObjeto,
    DetSolicitud,
    Sucursal,
    Distribuidor,
    Cobertura,
)
from app.schemas import (
    CoberturaRead,
    CotizacionObjetoCreate,
    CotizacionObjetoRead,
    CotizacionRead,
    CotizacionResponse,
    DetSolicitudRead,
)
from app.api.deps import CurrentUser, SessionDep, get_db

router = APIRouter()


@router.get("/", response_model=List[CotizacionObjetoRead])
def get_cotizaciones(current_user: CurrentUser, session: SessionDep):
    result = session.exec(select(CotizacionObjeto)).all()
    return result


@router.post("/", response_model=CotizacionResponse)
def create_cotizacion(
    cotizacion_objeto: CotizacionObjetoCreate,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    response_body = process_cotizacion(cotizacion_objeto, db)
    return CotizacionResponse(
        response_body=response_body, message_error=None, es_dato_valido=True
    )


def process_cotizacion(
    cotizacion_objeto: CotizacionObjetoCreate, db: Session
) -> CotizacionObjetoRead:
    # Buscar la sucursal por clave
    sucursal = db.exec(
        select(Sucursal).where(Sucursal.clave == cotizacion_objeto.suc_clave)
    ).first()
    if not sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")

    # Buscar el distribuidor por clave
    distribuidor = db.exec(
        select(Distribuidor).where(
            Distribuidor.clave == cotizacion_objeto.distribuidor_clave
        )
    ).first()
    if not distribuidor:
        raise HTTPException(status_code=404, detail="Distribuidor no encontrado")

    # Obtener la cotización objeto
    cotizacion_objeto_db = (
        db.exec(
            select(CotizacionObjeto)
            .where(
                CotizacionObjeto.convenio_id == cotizacion_objeto.id_convenio,
                CotizacionObjeto.sucursal_id == sucursal.id,
                CotizacionObjeto.distribuidor_id == distribuidor.id,
            )
            .options(
                joinedload(CotizacionObjeto.convenio),
                joinedload(CotizacionObjeto.sucursal),
                joinedload(CotizacionObjeto.distribuidor),
            )
        )
        .unique()
        .first()
    )

    if not cotizacion_objeto_db:
        raise HTTPException(status_code=404, detail="Cotización objeto no encontrada")

    # Obtener la cotización usando el id de CotizacionObjeto
    cotizacion_db = (
        db.exec(
            select(Cotizacion)
            .where(Cotizacion.cotizacion_objeto_id == cotizacion_objeto_db.id)
            .options(
                joinedload(Cotizacion.det_solicitudes).joinedload(
                    DetSolicitud.coberturas
                )
            )
        )
        .unique()
        .all()
    )

    cotizaciones = []
    for cotizacion in cotizacion_db:
        det_solicitudes = []
        for det_solicitud in cotizacion.det_solicitudes:
            coberturas = [
                CoberturaRead(
                    id_cobertura=str(cobertura.id),
                    prima_neta=cobertura.prima,
                    iva_notal=cobertura.prima * 0.16,
                    prima_total=cobertura.prima * 1.16,
                )
                for cobertura in det_solicitud.coberturas
            ]
            det_solicitudes.append(
                DetSolicitudRead(
                    id=str(det_solicitud.id),
                    plan=det_solicitud.plan,
                    renovacion=det_solicitud.renovacion,
                    tipo=det_solicitud.tipo,
                    paquete=det_solicitud.paquete,
                    fecha_nacimiento=det_solicitud.fecha_nacimiento,
                    ini_vig_reportada=det_solicitud.ini_vig_reportada,
                    fin_vig_reportada=det_solicitud.fin_vig_reportada,
                    plazo_reportado=det_solicitud.plazo_reportado,
                    tipo_vig=det_solicitud.tipo_vig,
                    sum_aseg_4=det_solicitud.sum_aseg_4,
                    sum_aseg_5=det_solicitud.sum_aseg_5,
                    sum_aseg_6=det_solicitud.sum_aseg_6,
                    coberturas=coberturas,
                )
            )
        cotizaciones.append(
            CotizacionRead(
                id=str(cotizacion.id),
                plan_comercial=cotizacion.plan_comercial,
                prima_neta=sum(c.prima_neta for c in det_solicitudes[0].coberturas),
                iva_notal=sum(c.iva_notal for c in det_solicitudes[0].coberturas),
                prima_total=sum(c.prima_total for c in det_solicitudes[0].coberturas),
                det_solicitudes=det_solicitudes,
            )
        )

    cotizacion_objeto_read = CotizacionObjetoRead(
        id=str(cotizacion_objeto_db.id),
        id_convenio=str(cotizacion_objeto_db.convenio.id),
        sucursal_id=str(cotizacion_objeto_db.sucursal.id),
        distribuidor_id=str(cotizacion_objeto_db.distribuidor.id),
        suc_clave=cotizacion_objeto.suc_clave,
        suc_nombre=sucursal.nombre,
        distribuidor_clave=cotizacion_objeto.distribuidor_clave,
        distribuidor_nombre=distribuidor.nombre,
        distribuidor_email=distribuidor.email,
        cotizaciones=cotizaciones,
    )

    return cotizacion_objeto_read
