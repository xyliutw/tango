# Crud/user.py

from sqlalchemy.orm import Session
from Models.user import User
from uuid import UUID

def get_user_by_id(db: Session, user_id: UUID) -> User:
    return db.query(User).filter(User.id == user_id).first()
