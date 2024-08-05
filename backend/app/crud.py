import uuid
from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import (
    Item,
    ItemCreate,
    User,
    UserCreate,
    UserUpdate,
    Plan,
    PlanCreate,
    PlanUpdate,
)


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def get_plan(db: Session, plan_id: uuid.UUID):
    return db.get(Plan, plan_id)


def get_plans(db: Session, skip: int = 0, limit: int = 10):
    return db.exec(select(Plan).offset(skip).limit(limit)).all()


def create_plan(db: Session, plan_in: PlanCreate):
    db_plan = Plan.model_validate(plan_in)
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


def update_plan(db: Session, plan_id: uuid.UUID, plan_in: PlanUpdate):
    db_plan = get_plan(db, plan_id)
    if not db_plan:
        return None
    plan_data = plan_in.model_dump(exclude_unset=True)
    for key, value in plan_data.items():
        setattr(db_plan, key, value)
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


def delete_plan(db: Session, plan_id: uuid.UUID):
    db_plan = get_plan(db, plan_id)
    if not db_plan:
        return None
    db.delete(db_plan)
    db.commit()
    return db_plan
