"""API router for authentication."""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.api.dependencies import get_db, get_current_user
from src.api.schemas.user import UserCreate, User as UserSchema
from src.api.schemas.token import Token
from src.auth.security import create_access_token, verify_password
from src.models.user import User
from src.services import user_service
from src.config import get_settings

settings = get_settings()
limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

@router.post("/register", response_model=UserSchema)
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
def register_user(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    try:
        db_user = user_service.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        db_user = user_service.get_user_by_username(db, username=user.username)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )
        return user_service.create_user(db=db, user=user)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed due to an internal error"
        )

@router.post("/login", response_model=Token)
@limiter.limit("10/minute")
def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Login for access token.
    """
    user = user_service.get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserSchema)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get current user.
    """
    return current_user
