"""
This file handles turning plain-text passwords into secure hashes,
checking a plain-text password against a stored hash during login,
and creating/verifying JWT tokens for authentication.
"""

from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In a real production app, this secret would come from an environment
# variable, never hardcoded. For learning, we'll keep it simple here.
SECRET_KEY = "this-is-a-learning-project-secret-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def hash_password(plain_password: str) -> str:
    """Turn a plain password into a secure, one-way hash for storage."""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if a plain password matches a previously stored hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """
    Create a signed JWT containing the given data (e.g. {"sub": username}),
    plus an expiration time.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import get_db

# This tells FastAPI where clients should go to get a token (our login endpoint).
# It also makes /docs show a "lock" icon and an "Authorize" button.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Reads the token from the Authorization header, verifies it,
    and returns the actual User object it belongs to.
    """
    from app.models.user import User  # imported here to avoid circular imports

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


def require_admin(current_user=Depends(get_current_user)):
    """A dependency that only allows the request through if the user is an admin."""
    if current_user.is_admin != 1:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user