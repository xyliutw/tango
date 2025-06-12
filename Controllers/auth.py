from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette import status
from Tools import oauth, jwt
from sqlalchemy.orm import Session
from Databases.session import SessionLocal
from Models.user import User

router = APIRouter()

class LoginRequest(BaseModel):
    provider: str  # "google" or "apple"
    id_token: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

def get_or_create_user(provider: str, sub: str, email: str = None, name: str = None) -> User:
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter_by(provider=provider, provider_id=sub).first()
        if user:
            return user
        user = User(provider=provider, provider_id=sub, email=email, name=name)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()

@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    id_token = payload.id_token
    provider = payload.provider.lower()

    try:
        if provider == "google":
            user_info = oauth.verify_google_token(id_token)
        elif provider == "apple":
            user_info = oauth.verify_apple_token(id_token)
        else:
            raise HTTPException(status_code=400, detail="Unsupported provider")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail=f"Invalid id_token: {str(e)}")

    sub = user_info.get("sub")
    email = user_info.get("email")
    name = user_info.get("name", "")

    if not sub:
        raise HTTPException(status_code=400, detail="Token missing subject")

    user = get_or_create_user(provider=provider, sub=sub, email=email, name=name)
    access_token = jwt.create_access_token(data={"user_id": str(user.id)})

    return LoginResponse(access_token=access_token)
