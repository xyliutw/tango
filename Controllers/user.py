from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_401_UNAUTHORIZED
from Tools import jwt
from sqlalchemy.orm import Session
from Databases.session import get_db
from Models.user import User
from Schemas.user import UserUpdate, UserMe
import random
from Schemas.user import PersonalityTestRequest, PersonalityTestResponse, PersonalityType
from Tools.jwt import get_current_user


router = APIRouter()


@router.patch("/me")
def update_user_info(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user.gender = data.gender
    current_user.birthday = data.birthday
    current_user.city = data.city
    db.commit()
    db.refresh(current_user)
    return {
        "message": "User info updated successfully",
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "gender": current_user.gender,
            "birthday": current_user.birthday,
            "city": current_user.city,
        },
    }


@router.post("/me/personality", response_model=PersonalityTestResponse)
def submit_personality_test(
    request: PersonalityTestRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if len(request.answers) != 5:
        raise HTTPException(status_code=400, detail="Must provide exactly 5 answers")

    personality = random.choice(list(PersonalityType))

    current_user.personality_type = personality
    db.commit()
    db.refresh(current_user)

    return PersonalityTestResponse(personality_type=personality)

@router.get("/users/recommendations")
def recommend_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.gender:
        raise HTTPException(status_code=400, detail="User gender not set")

    # 推薦異性使用者
    opposite_gender = "female" if current_user.gender == "male" else "male"

    # 查詢 10 位異性使用者（以便隨機挑出 3 個）
    candidates = db.query(User).filter(
        User.gender == opposite_gender,
        User.id != current_user.id
    ).all()

    # 隨機挑選 3 名
    sampled = random.sample(candidates, min(3, len(candidates)))

    return [
        {
            "id": user.id,
            "name": user.name,
            "city": user.city,
            "personality_type": user.personality_type,
            "avatar": user.avatar
        }
        for user in sampled
    ]

@router.get("/me", response_model=UserMe)
def get_me(
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    return current_user
