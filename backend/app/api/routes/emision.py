from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import Emision, CertificadoDetalle, AseguradosAdicionales
from app.schemas import (
    EmisionRequest,
    EmisionResponse,
    CertificadoResponse,
)
from app.api.deps import get_db

router = APIRouter()


@router.post("/", response_model=EmisionResponse)
def create_emision(emision_request: EmisionRequest, db: Session = Depends(get_db)):
    # Crear la emisión
    emision = Emision(
        id_convenio=emision_request.idConvenio,
        suc_clave=emision_request.sucClave,
        suc_nombre=emision_request.sucNombre,
        distribuidor_clave=emision_request.distribuidorClave,
        distribuidor_nombre=emision_request.distribuidorNombre,
        distribuidor_email=emision_request.distribuidorEmail,
    )

    # Agregar certificados
    certificados = []
    for cert in emision_request.certificados:
        certificado = CertificadoDetalle(
            tipo=cert.tipo,
            tipo_identificacion=cert.tipoIdentificacion,
            numero_identificacion=cert.numeroIdentificacion,
            nombre=cert.nombre,
            sexo=cert.sexo,
            etiqueta_adicional1=cert.etiquetaAdicional1,
            data_adicional1=cert.dataAdicional1,
            etiqueta_adicional2=cert.etiquetaAdicional2,
            data_adicional2=cert.dataAdicional2,
            etiqueta_adicional3=cert.etiquetaAdicional3,
            data_adicional3=cert.dataAdicional3,
            emision=emision,
        )
        db.add(certificado)
        certificados.append(certificado)

    # Agregar asegurados adicionales
    if emision_request.aseguradosAdicionales:
        for aseg in emision_request.aseguradosAdicionales:
            asegurado = AseguradosAdicionales(
                parentesco=aseg.parentesco,
                tipo_identificacion=aseg.tipoIdentificacion,
                numero_identificacion=aseg.numeroIdentificacion,
                nombre=aseg.nombre,
                fecha_nacimiento=aseg.fechaNacimiento,
                sexo=aseg.sexo,
                edad=aseg.edad,
                emision=emision,
            )
            db.add(asegurado)

    db.add(emision)
    db.commit()
    db.refresh(emision)

    # Crear la respuesta
    certificados_response = []
    for cert in certificados:
        certificado_response = CertificadoResponse(
            identificador=str(cert.id),
            primaNeta=0.0,  # Estos valores deben ser calculados
            ivaTotal=0.0,  # según la lógica de negocio
            primaTotal=0.0,  # aquí van los valores reales
            vigenciaInicial="",  # valores de ejemplo
            vigenciaFinal="",
            planCertificado="",
            paquete="",
            coberturas=[],  # Este debe contener los datos reales de coberturas
        )
        certificados_response.append(certificado_response)

    emision_response = EmisionResponse(
        identificador=str(emision.id),
        mensajeError=None,
        confirmacionEmitida=None,
        idConvenio=emision.id_convenio,
        sucClave=emision.suc_clave,
        sucNombre=emision.suc_nombre,
        distribuidorClave=emision.distribuidor_clave,
        distribuidorNombre=emision.distribuidor_nombre,
        distribuidorEmail=emision.distribuidor_email,
        certificados=certificados_response,
    )

    return emision_response
