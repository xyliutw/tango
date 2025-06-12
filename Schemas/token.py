from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class TokenData(BaseModel):
    user_id: UUID
    gender: Optional[str] = None  # "male" / "female" / None
