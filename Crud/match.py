# Crud/match.py

from sqlalchemy.orm import Session
from Models.user_action import UserAction
from Models.match import Match
from Models.notice import Notice
from Models.user import User
from uuid import uuid4
from datetime import datetime
from sqlalchemy import or_

def create_match_action(db: Session, actor_id: str, target_id: str, is_like: bool):
    # 檢查是否已經對該對象按過
    existing_action = db.query(UserAction).filter_by(user_id=actor_id, target_user_id=target_id).first()
    if existing_action:
        return {"message": "Already acted", "matched": False}

    # 建立新的 UserAction
    new_action = UserAction(
        user_id=actor_id,
        target_user_id=target_id,
        is_like=is_like
    )
    db.add(new_action)
    db.commit()

    if not is_like:
        return {"message": "Action recorded", "matched": False}

    # 檢查對方是否先前也 like 了自己
    reciprocal = db.query(UserAction).filter_by(user_id=target_id, target_user_id=actor_id, is_like=True).first()
    if reciprocal:
        # 避免重複 match 紀錄（順序不定）
        user1, user2 = sorted([actor_id, target_id])
        existing_match = db.query(Match).filter_by(user1_id=user1, user2_id=user2).first()
        if not existing_match:
            # 新增 Match
            match = Match(user1_id=user1, user2_id=user2)
            db.add(match)

            # 建立 notice 給先按 like 的對方（即 reciprocal.user_id）
            matched_user = db.query(User).filter(User.id == actor_id).first()
            notice = Notice(
                user_id=reciprocal.user_id,
                message=f"您與 {matched_user.name} 已配對成功"
            )
            db.add(notice)

            db.commit()
        return {"message": "Matched!", "matched": True}

    return {"message": "Liked", "matched": False}


def get_chat_partners(db: Session, user_id: str):
    matches = db.query(Match).filter(
        or_(
            Match.user1_id == user_id,
            Match.user2_id == user_id
        )
    ).all()

    partner_ids = [
        match.user2_id if match.user1_id == user_id else match.user1_id
        for match in matches
    ]

    from Models.user import User  # 為了取得使用者基本資料
    partners = db.query(User).filter(User.id.in_(partner_ids)).all()

    return [
        {
            "id": str(user.id),
            "name": user.name,
            "city": user.city,
            "personality_type": user.personality_type,
            "avatar": user.avatar,
        }
        for user in partners
    ]
