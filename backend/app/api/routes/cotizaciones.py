from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import PyJWTError
from sqlmodel import Session, select
from app.models import CotizacionObjeto
from app.schemas import CotizacionObjetoRead
from app.core.db import get_session
from app.core.config import settings
from app.core import security

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    return username


@router.get("/cotizaciones", response_model=List[CotizacionObjetoRead])
def get_cotizaciones(
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    result = session.exec(select(CotizacionObjeto)).all()
    return result
