# Controllers/notice.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Tools.jwt import get_current_user
from Databases.session import get_db
from Crud.notice import get_unread_notices, get_all_notices, mark_notices_as_read
from Models.user import User
from Schemas.notice import NoticeResponse
from typing import List
from Schemas.notice import NoticeOut, NoticeReadRequest

router = APIRouter()

@router.get("/", response_model=list[NoticeResponse])
def list_all_notices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_notices(db, current_user.id)

@router.get("/unread", response_model=List[NoticeOut])
def list_unread_notices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_unread_notices(db, current_user.id)

@router.post("/read")
def mark_as_read(
    request: NoticeReadRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_count = mark_notices_as_read(db, current_user.id, request.notice_ids)
    return {"updated": updated_count}