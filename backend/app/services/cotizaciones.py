from typing import List
from sqlalchemy import UUID
from sqlmodel import Session, select
from fastapi import HTTPException

from app.models import (
    DetSolicitud,
    Sucursal,
    Distribuidor,
    CotizacionObjeto,
    Cotizacion,
)
from sqlalchemy.orm import joinedload

from app.schemas import (
    CotizacionObjetoRead,
    CotizacionRead,
    CotizacionResponse,
    DetSolicitudRead,
)


class SucursalService:
    @staticmethod
    def get_sucursal_by_clave(db: Session, suc_clave: str) -> Sucursal:
        sucursal = db.exec(select(Sucursal).where(Sucursal.clave == suc_clave)).first()
        if not sucursal:
            raise HTTPException(status_code=404, detail="Sucursal no encontrada")
        return sucursal


class DistribuidorService:
    @staticmethod
    def get_distribuidor_by_clave(db: Session, distribuidor_clave: str) -> Distribuidor:
        distribuidor = db.exec(
            select(Distribuidor).where(Distribuidor.clave == distribuidor_clave)
        ).first()
        if not distribuidor:
            raise HTTPException(status_code=404, detail="Distribuidor no encontrado")
        return distribuidor


class CotizacionObjetoService:
    @staticmethod
    def get_cotizacion_objeto(
        db: Session, id_convenio: UUID, sucursal_id: int, distribuidor_id: int
    ) -> CotizacionObjeto:
        cotizacion_objeto = (
            db.exec(
                select(CotizacionObjeto)
                .where(
                    CotizacionObjeto.convenio_id == id_convenio,
                    CotizacionObjeto.sucursal_id == sucursal_id,
                    CotizacionObjeto.distribuidor_id == distribuidor_id,
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
        if not cotizacion_objeto:
            raise HTTPException(
                status_code=404, detail="Cotización objeto no encontrada"
            )
        return cotizacion_objeto


class CotizacionService:
    @staticmethod
    def get_cotizaciones_by_objeto_id(
        db: Session, cotizacion_objeto_id: int
    ) -> List[Cotizacion]:
        return (
            db.exec(
                select(Cotizacion)
                .where(Cotizacion.cotizacion_objeto_id == cotizacion_objeto_id)
                .options(
                    joinedload(Cotizacion.det_solicitudes).joinedload(
                        DetSolicitud.coberturas
                    )
                )
            )
            .unique()
            .all()
        )


def get_all_cotizaciones(
    db: Session, page: int = 1, limit: int = 10
) -> List[CotizacionResponse]:
    offset = (page - 1) * limit
    cotizaciones = (
        db.exec(
            select(CotizacionObjeto)
            .options(
                joinedload(CotizacionObjeto.cotizaciones),
                joinedload(CotizacionObjeto.convenio),
                joinedload(CotizacionObjeto.distribuidor),
                joinedload(CotizacionObjeto.sucursal),
            )
            .offset(offset)
            .limit(limit)
        )
        .unique()
        .all()
    )

    if not cotizaciones:
        raise HTTPException(status_code=404, detail="No se encontraron cotizaciones")

    cotizacion_responses = [
        CotizacionResponse(
            response_body=CotizacionObjetoRead(
                id_convenio=cotizacion.convenio_id,
                suc_clave=cotizacion.sucursal.clave if cotizacion.sucursal else None,
                suc_nombre=cotizacion.sucursal.nombre if cotizacion.sucursal else None,
                distribuidor_clave=(
                    cotizacion.distribuidor.clave if cotizacion.distribuidor else None
                ),
                distribuidor_nombre=(
                    cotizacion.distribuidor.nombre if cotizacion.distribuidor else None
                ),
                distribuidor_email=(
                    cotizacion.distribuidor.email if cotizacion.distribuidor else None
                ),
                cotizaciones=[
                    CotizacionRead(
                        id=str(cot_det.id),
                        plan_comercial=cot_det.plan_comercial,
                        prima_neta=(
                            cot_det.prima_neta
                            if hasattr(cot_det, "prima_neta")
                            else 0.0
                        ),
                        iva_notal=(
                            cot_det.iva_notal if hasattr(cot_det, "iva_notal") else 0.0
                        ),
                        prima_total=(
                            cot_det.prima_total
                            if hasattr(cot_det, "prima_total")
                            else 0.0
                        ),
                        det_solicitudes=[
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
                                coberturas=[],
                            )
                            for det_solicitud in cot_det.det_solicitudes
                        ],
                    )
                    for cot_det in cotizacion.cotizaciones
                ],
            ),
            es_dato_valido=True,
            message_error=None,
        )
        for cotizacion in cotizaciones
    ]
    return cotizacion_responses
