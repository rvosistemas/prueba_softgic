from typing import List, Optional
import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str = Field(min_length=1, max_length=255)


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


# ---------  my models for project ------------------------------------------------
class Convenio(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    cotizaciones: List["CotizacionObjeto"] = Relationship(back_populates="convenio")


class Sucursal(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    clave: str
    nombre: str
    cotizaciones: List["CotizacionObjeto"] = Relationship(back_populates="sucursal")


class Distribuidor(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    clave: str
    nombre: str
    email: str
    cotizaciones: List["CotizacionObjeto"] = Relationship(back_populates="distribuidor")


class Cobertura(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    clave_cobertura: str
    prima: float
    det_solicitud_id: int = Field(foreign_key="detsolicitud.id")
    det_solicitud: "DetSolicitud" = Relationship(back_populates="coberturas")


class DetSolicitud(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    plan: str
    renovacion: int
    tipo: str
    paquete: str
    fecha_nacimiento: Optional[str] = None
    ini_vig_reportada: str
    fin_vig_reportada: Optional[str] = None
    plazo_reportado: int
    tipo_vig: int
    sum_aseg_4: float
    sum_aseg_5: Optional[float] = None
    sum_aseg_6: Optional[float] = None
    cotizacion_id: int = Field(foreign_key="cotizacion.id")
    cotizacion: "Cotizacion" = Relationship(back_populates="det_solicitudes")
    coberturas: List[Cobertura] = Relationship(back_populates="det_solicitud")


class Cotizacion(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    plan_comercial: str
    cotizacion_objeto_id: int = Field(foreign_key="cotizacionobjeto.id")
    cotizacion_objeto: "CotizacionObjeto" = Relationship(back_populates="cotizaciones")
    det_solicitudes: List[DetSolicitud] = Relationship(back_populates="cotizacion")


class CotizacionObjeto(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    convenio_id: uuid.UUID = Field(foreign_key="convenio.id")
    convenio: Convenio = Relationship(back_populates="cotizaciones")
    sucursal_id: int = Field(foreign_key="sucursal.id")
    sucursal: Sucursal = Relationship(back_populates="cotizaciones")
    distribuidor_id: int = Field(foreign_key="distribuidor.id")
    distribuidor: Distribuidor = Relationship(back_populates="cotizaciones")
    cotizaciones: List[Cotizacion] = Relationship(back_populates="cotizacion_objeto")


class CertificadoDetalle(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    tipo: str
    tipo_identificacion: str
    numero_identificacion: str
    nombre: str
    sexo: str
    etiqueta_adicional1: Optional[str] = None
    data_adicional1: Optional[str] = None
    etiqueta_adicional2: Optional[str] = None
    data_adicional2: Optional[str] = None
    etiqueta_adicional3: Optional[str] = None
    data_adicional3: Optional[str] = None
    emision_id: Optional[uuid.UUID] = Field(default=None, foreign_key="emision.id")
    emision: "Emision" = Relationship(back_populates="certificados")


class AseguradosAdicionales(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    parentesco: str
    tipo_identificacion: str
    numero_identificacion: str
    nombre: str
    fecha_nacimiento: Optional[str] = None
    sexo: Optional[str] = None
    edad: Optional[int] = None
    emision_id: Optional[uuid.UUID] = Field(default=None, foreign_key="emision.id")
    emision: "Emision" = Relationship(back_populates="asegurados_adicionales")


class Emision(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    id_convenio: uuid.UUID
    suc_clave: str
    suc_nombre: str
    distribuidor_clave: str
    distribuidor_nombre: str
    distribuidor_email: str
    certificados: List[CertificadoDetalle] = Relationship(back_populates="emision")
    asegurados_adicionales: List[AseguradosAdicionales] = Relationship(
        back_populates="emision"
    )


class Plan(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    nombre: str
    descripcion: str
    activo: bool = True


class PlanCreate(SQLModel):
    nombre: str
    descripcion: str


class PlanUpdate(SQLModel):
    nombre: str | None = None
    descripcion: str | None = None
    activo: bool | None = None
