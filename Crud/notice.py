
from sqlalchemy.orm import Session
from Models.notice import Notice
from uuid import UUID
from typing import List


def get_unread_notices(db: Session, user_id: str):
    return db.query(Notice).filter_by(receiver_id=user_id, is_read=False).order_by(Notice.created_at.desc()).all()


def get_unread_notices(db: Session, user_id: UUID) -> List[Notice]:
    return db.query(Notice)\
        .filter(Notice.user_id == user_id, Notice.is_read == False)\
        .order_by(Notice.created_at.desc())\
        .all()

def get_all_notices(db: Session, user_id: UUID) -> List[Notice]:
    return db.query(Notice)\
        .filter(Notice.user_id == user_id)\
        .order_by(Notice.created_at.desc())\
        .all()

def mark_notices_as_read(db: Session, user_id: UUID, notice_ids: List[UUID]) -> int:
    result = db.query(Notice)\
        .filter(Notice.user_id == user_id, Notice.id.in_(notice_ids))\
        .update({Notice.is_read: True}, synchronize_session=False)
    db.commit()
    return result