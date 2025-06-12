# Models/match.py

from sqlalchemy import Column, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from uuid import uuid4
from Databases.session import Base

class Match(Base):
    __tablename__ = "matches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user1_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user2_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("user1_id", "user2_id", name="_user_match_uc"),
    )
