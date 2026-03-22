"""API dependencies."""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from src.database.base import get_db
from src.models.user import User
from src.models.subject import Subject
from src.models.document import Document
from src.api.exceptions import NotFoundException
from src.auth.security import SECRET_KEY, ALGORITHM
from src.services import user_service
from src.api.schemas.token import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Get current user from JWT token. 
    Bypasses to demo_user if no token provided (Development Mode).
    """
    if not token:
        # Development fallback: Auto-login demo user
        user = user_service.get_user_by_username(db, username="demo_user")
        if user:
            return user
        # If demo user doesn't exist, try to get the first user
        user = db.query(User).first()
        if user:
            return user
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No users in database. Run seeding script.",
        )

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = user_service.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_current_user_id(current_user: User = Depends(get_current_user)) -> str:
    """Get current user's ID."""
    return current_user.id


def get_subject_or_404(
    subject_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Subject:
    """Get subject by ID or raise 404."""
    subject = db.query(Subject).filter(
        Subject.id == subject_id,
        Subject.user_id == current_user.id
    ).first()
    
    if not subject:
        raise NotFoundException(f"Subject with ID {subject_id} not found")
    
    return subject


from src.models.topic import Topic

def get_topic_or_404(
    topic_id: str,
    db: Session = Depends(get_db)
) -> Topic:
    """Get topic by ID or raise 404."""
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    
    if not topic:
        raise NotFoundException(f"Topic with ID {topic_id} not found")
    
    return topic


def get_document_or_404(
    document_id: str,
    db: Session = Depends(get_db)
) -> Document:
    """Get document by ID or raise 404."""
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise NotFoundException(f"Document with ID {document_id} not found")
    
    return document
