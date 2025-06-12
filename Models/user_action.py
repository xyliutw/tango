# Models/user_action.py

from sqlalchemy import Column, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from uuid import uuid4
from Databases.session import Base


class UserAction(Base):
    __tablename__ = "user_actions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    target_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_like = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
