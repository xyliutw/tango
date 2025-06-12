# models/notice.py

from sqlalchemy import Column, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from uuid import uuid4
from Databases.session import Base

class Notice(Base):
    __tablename__ = "notices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
