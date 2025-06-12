from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from Databases.session import get_db
from Models.user import User

SECRET_KEY = "tango-prototype"  # 改為你自己的
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def _decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        print(f"JWTError: {e}")
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")

def get_current_user_id(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Missing token")
    token = auth.split(" ")[1]
    user_id = _decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    return user_id

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = _decode_access_token(token)
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token error")
