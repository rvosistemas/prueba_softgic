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
    id_convenio: UUID
    suc_clave: Optional[str]
    suc_nombre: Optional[str]
    distribuidor_clave: Optional[str]
    distribuidor_nombre: Optional[str]
    distribuidor_email: Optional[str]
    cotizaciones: List[CotizacionCreate]


class CoberturaRead(BaseModel):
    id_cobertura: str
    prima_neta: float
    iva_notal: float
    prima_total: float


class DetSolicitudRead(BaseModel):
    id: str
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
    coberturas: List[CoberturaRead]


class CotizacionRead(BaseModel):
    id: str
    plan_comercial: str
    prima_neta: float
    iva_notal: float
    prima_total: float
    det_solicitudes: List[DetSolicitudRead]


class CotizacionRead(BaseModel):
    id: str
    plan_comercial: str
    prima_neta: float
    iva_notal: float
    prima_total: float
    det_solicitudes: List[DetSolicitudRead]


class CotizacionObjetoRead(BaseModel):
    id_convenio: UUID
    suc_clave: Optional[str]
    suc_nombre: Optional[str]
    distribuidor_clave: Optional[str]
    distribuidor_nombre: Optional[str]
    distribuidor_email: Optional[str]
    cotizaciones: List[CotizacionRead]


class CotizacionResponse(BaseModel):
    response_body: CotizacionObjetoRead
    message_error: Optional[str] = None
    es_dato_valido: bool


class CertificadoDetalle(BaseModel):
    tipo: str
    tipoIdentificacion: str
    numeroIdentificacion: str
    nombre: str
    sexo: str
    etiquetaAdicional1: Optional[str] = None
    dataAdicional1: Optional[str] = None
    etiquetaAdicional2: Optional[str] = None
    dataAdicional2: Optional[str] = None
    etiquetaAdicional3: Optional[str] = None
    dataAdicional3: Optional[str] = None


class AseguradosAdicionales(BaseModel):
    parentesco: str
    tipoIdentificacion: str
    numeroIdentificacion: str
    nombre: str
    fechaNacimiento: Optional[str]
    sexo: Optional[str]
    edad: Optional[int]


class EmisionRequest(BaseModel):
    idConvenio: UUID
    sucClave: str
    sucNombre: str
    distribuidorClave: str
    distribuidorNombre: str
    distribuidorEmail: str
    certificados: List[CertificadoDetalle]
    aseguradosAdicionales: Optional[List[AseguradosAdicionales]]


class CoberturaResponse(BaseModel):
    primaNeta: float
    ivaTotal: float
    primaTotal: float


class CertificadoResponse(BaseModel):
    identificador: str
    primaNeta: float
    ivaTotal: float
    primaTotal: float
    vigenciaInicial: str
    vigenciaFinal: str
    planCertificado: str
    paquete: str
    coberturas: List[CoberturaResponse]


class EmisionResponse(BaseModel):
    identificador: str
    mensajeError: Optional[str]
    confirmacionEmitida: Optional[str]
    idConvenio: UUID
    sucClave: str
    sucNombre: str
    distribuidorClave: str
    distribuidorNombre: str
    distribuidorEmail: str
    certificados: List[CertificadoResponse]


class PlanBase(BaseModel):
    nombre: str
    descripcion: str
    activo: bool


class PlanCreate(PlanBase):
    pass


class PlanUpdate(BaseModel):
    nombre: Optional[str]
    descripcion: Optional[str]
    activo: Optional[bool]


class PlanRead(PlanBase):
    id: UUID
