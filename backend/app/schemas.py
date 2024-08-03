from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID


class ConvenioCreate(BaseModel):
    id: UUID


class SucursalCreate(BaseModel):
    clave: str
    nombre: str


class DistribuidorCreate(BaseModel):
    clave: str
    nombre: str
    email: str


class CoverageCreate(BaseModel):
    clave_cobertura: Optional[str]
    prima: Optional[float]


class DetSolicitudCreate(BaseModel):
    plan: str
    renovacion: int
    tipo: str
    paquete: str
    fecha_nacimiento: Optional[str]
    ini_vig_reportada: str
    fin_vig_reportada: Optional[str]
    plazo_reportado: int
    tipo_vig: int
    sum_aseg_4: float
    sum_aseg_5: Optional[float]
    sum_aseg_6: Optional[float]
    coberturas_prima_neta: Optional[List[CoverageCreate]]


class CotizacionCreate(BaseModel):
    plan_comercial: str
    det_solicitudes: List[DetSolicitudCreate]


class CotizacionObjetoCreate(BaseModel):
    convenio: ConvenioCreate
    sucursal: SucursalCreate
    distribuidor: DistribuidorCreate
    cotizaciones: List[CotizacionCreate]


class CotizacionObjetoRead(CotizacionObjetoCreate):
    id: int
