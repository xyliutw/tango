# Controllers/match.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from Databases.session import get_db
from Schemas.match import MatchRequest
from Crud import match as match_crud
from Tools.jwt import get_current_user  # 解出 user.id

router = APIRouter()

@router.post("/action")
def like_or_dislike(
    req: MatchRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return match_crud.create_match_action(
        db=db,
        actor_id=current_user.id,
        target_id=req.target_user_id,
        is_like=True  # 或根據擴充的 req 傳入 is_like
    )


@router.get("/chat-list")
def get_my_chat_partners(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return match_crud.get_chat_partners(
        db=db,
        user_id=current_user.id
    )

# @router.patch("/action", response_model=MatchResponse)
# def action(payload: LikeRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     if current_user.id == payload.to_user_id:
#         raise HTTPException(status_code=400, detail="Cannot like yourself.")

#     # 是否已有對該 user 的紀錄
#     existing = db.query(UserLike).filter_by(
#         from_user_id=current_user.id,
#         to_user_id=payload.to_user_id
#     ).first()

#     if existing:
#         existing.status = payload.status
#     else:
#         new_like = UserLike(
#             from_user_id=current_user.id,
#             to_user_id=payload.to_user_id,
#             status=payload.status
#         )
#         db.add(new_like)

#     db.commit()

#     # 如果是 like，並且對方也有 like 自己
#     if payload.status == LikeStatus.LIKE:
#         mutual = db.query(UserLike).filter_by(
#             from_user_id=payload.to_user_id,
#             to_user_id=current_user.id,
#             status=LikeStatus.LIKE
#         ).first()

#         if mutual:
#             return MatchResponse(match=True)

#     return MatchResponse(match=False)


# @router.get("/chat-list")
# def get_chat_list(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     return match_crud.get_chat_partners(db, user_id)