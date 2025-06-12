from sqlalchemy import Column, String, DateTime, Date, Enum
import enum
from Databases.session import Base
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from Databases.session import Base

class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"

class PersonalityType(enum.Enum):
    ANALYST = "ANALYST"
    DIPLOMAT = "DIPLOMAT"
    SENTINEL = "SENTINEL"
    EXPLORER = "EXPLORER"
    CAMPAIGNER = "CAMPAIGNER"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider = Column(String, nullable=False)  # google / apple
    provider_id = Column(String, nullable=False, unique=True)  # sub
    email = Column(String, nullable=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    gender = Column(Enum(GenderEnum), nullable=True)
    birthday = Column(Date, nullable=True)
    city = Column(String, nullable=True)
    personality_type = Column(Enum(PersonalityType), nullable=True)
    avatar = Column(String, nullable=True)
