from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import date
from Models.user import GenderEnum
from typing import List, Optional
from enum import Enum
from uuid import UUID


class UserUpdate(BaseModel):
    gender: Optional[GenderEnum]
    birthday: Optional[date]
    city: Optional[str]

class PersonalityType(str, Enum):
    ANALYST = "ANALYST"
    DIPLOMAT = "DIPLOMAT"
    SENTINEL = "SENTINEL"
    EXPLORER = "EXPLORER"
    CAMPAIGNER = "CAMPAIGNER"

class PersonalityTestRequest(BaseModel):
    answers: List[str]  # 可以是任意 5 答

class PersonalityTestResponse(BaseModel):
    personality_type: PersonalityType

class UserMe(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    gender: str
    birthday: Optional[date]
    city: Optional[str]
    personality_type: Optional[str]
    avatar: Optional[str]

    model_config = ConfigDict(from_attributes=True)