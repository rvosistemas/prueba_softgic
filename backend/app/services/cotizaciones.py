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
