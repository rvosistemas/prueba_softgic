from sqlmodel import Session
from app import crud
from app.models import Plan, PlanCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_plan(db: Session) -> Plan:
    nombre = random_lower_string()
    descripcion = random_lower_string()
    plan_in = PlanCreate(nombre=nombre, descripcion=descripcion, activo=True)
    return crud.plan.create(session=db, plan_in=plan_in)
