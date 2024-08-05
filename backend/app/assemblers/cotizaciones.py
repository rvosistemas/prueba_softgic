from typing import List
from app.models import Cotizacion, CotizacionObjeto, Sucursal, Distribuidor
from app.schemas import (
    CoberturaRead,
    CotizacionRead,
    DetSolicitudRead,
    CotizacionObjetoRead,
    CotizacionObjetoCreate,
)


class CotizacionAssembler:
    @staticmethod
    def assemble_cotizacion(cotizacion_db: Cotizacion) -> CotizacionRead:
        det_solicitudes = []
        for det_solicitud in cotizacion_db.det_solicitudes:
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
        return CotizacionRead(
            id=str(cotizacion_db.id),
            plan_comercial=cotizacion_db.plan_comercial,
            prima_neta=sum(c.prima_neta for c in det_solicitudes[0].coberturas),
            iva_notal=sum(c.iva_notal for c in det_solicitudes[0].coberturas),
            prima_total=sum(c.prima_total for c in det_solicitudes[0].coberturas),
            det_solicitudes=det_solicitudes,
        )


class CotizacionObjetoAssembler:
    @staticmethod
    def assemble_cotizacion_objeto(
        cotizacion_objeto_db: CotizacionObjeto,
        sucursal: Sucursal,
        distribuidor: Distribuidor,
        cotizaciones: List[CotizacionRead],
        cotizacion_objeto: CotizacionObjetoCreate,
    ) -> CotizacionObjetoRead:
        return CotizacionObjetoRead(
            id=str(cotizacion_objeto_db.id),
            id_convenio=str(cotizacion_objeto_db.convenio.id),
            suc_clave=cotizacion_objeto.suc_clave,
            suc_nombre=sucursal.nombre,
            distribuidor_clave=cotizacion_objeto.distribuidor_clave,
            distribuidor_nombre=distribuidor.nombre,
            distribuidor_email=distribuidor.email,
            cotizaciones=cotizaciones,
        )
