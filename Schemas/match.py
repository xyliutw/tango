# Schemas/match.py

from pydantic import BaseModel
from uuid import UUID
from enum import Enum

class LikeStatus(str, Enum):
    LIKE = "like"
    DISLIKE = "dislike"

class LikeRequest(BaseModel):
    to_user_id: UUID
    status: LikeStatus

class MatchRequest(BaseModel):
    target_user_id: UUID

class MatchResponse(BaseModel):
    match: bool
