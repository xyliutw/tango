# Schemas/notice.py

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import List

class NoticeResponse(BaseModel):
    id: UUID
    message: str
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class NoticeOut(BaseModel):
    id: UUID
    message: str
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class NoticeReadRequest(BaseModel):
    notice_ids: List[UUID]
