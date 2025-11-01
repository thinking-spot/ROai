"""
Authentication service
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.models.user import User
from app.models.organization import Organization
from app.schemas.auth import UserCreate, Token, TokenData

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Authentication service for user management and JWT tokens"""

    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    async def register_user(self, user_data: UserCreate) -> User:
        """
        Register a new user and organization
        """
        # Create organization first
        org_slug = user_data.organization_name.lower().replace(" ", "-")
        organization = Organization(
            name=user_data.organization_name,
            slug=org_slug,
            subscription_tier="trial",
            is_active=True,
        )
        self.db.add(organization)
        await self.db.flush()  # Get the organization ID

        # Create user
        hashed_password = self.get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            organization_id=organization.id,
            role="org_admin",  # First user is admin
            is_active=True,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def authenticate_user(self, email: str, password: str) -> Optional[Token]:
        """
        Authenticate user and return JWT token
        """
        # Get user by email
        result = await self.db.execute(select(User).filter(User.email == email))
        user = result.scalar_one_or_none()

        if not user or not self.verify_password(password, user.hashed_password):
            return None

        if not user.is_active:
            return None

        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={
                "sub": str(user.id),
                "user_id": user.id,
                "organization_id": user.organization_id,
                "role": user.role,
            },
            expires_delta=access_token_expires,
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    async def get_current_user(self, token: str) -> Optional[User]:
        """
        Get current user from JWT token
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: int = int(payload.get("sub"))
            if user_id is None:
                return None
        except JWTError:
            return None

        result = await self.db.execute(select(User).filter(User.id == user_id))
        user = result.scalar_one_or_none()
        return user
