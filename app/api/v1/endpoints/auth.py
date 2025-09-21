from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional
from app.core.config import settings
from app.core.security import verify_password, create_access_token, verify_token
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.common import SuccessResponse, ErrorResponse
from app.models.user import User
from app.core.database import get_database
from app.core.exceptions import AuthenticationException, ValidationException

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register", response_model=SuccessResponse)
async def register_user(user_data: UserCreate):
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = await User.find_one(User.email == user_data.email)
        if existing_user:
            raise ValidationException(
                message="User with this email already exists",
                details={"email": user_data.email}
            )
        
        existing_username = await User.find_one(User.username == user_data.username)
        if existing_username:
            raise ValidationException(
                message="Username already taken",
                details={"username": user_data.username}
            )
        
        # Validate password confirmation
        if user_data.password != user_data.confirm_password:
            raise ValidationException(
                message="Passwords do not match",
                details={"password": "Passwords must match"}
            )
        
        # Create new user
        hashed_password = verify_password(user_data.password, user_data.password)  # This should hash the password
        # Note: The verify_password function should be get_password_hash
        from app.core.security import get_password_hash
        hashed_password = get_password_hash(user_data.password)
        
        user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            phone_number=user_data.phone_number,
            country=user_data.country,
            preferred_language=user_data.preferred_language,
            bio=user_data.bio,
            interests=user_data.interests
        )
        
        await user.insert()
        
        return SuccessResponse(
            message="User registered successfully",
            data={"user_id": str(user.id)}
        )
        
    except ValidationException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login", response_model=SuccessResponse)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login user and return access token"""
    try:
        # Find user by email
        user = await User.find_one(User.email == form_data.username)
        if not user:
            raise AuthenticationException("Invalid email or password")
        
        # Verify password
        if not verify_password(form_data.password, user.hashed_password):
            raise AuthenticationException("Invalid email or password")
        
        # Check if user is active
        if user.status != "active":
            raise AuthenticationException("Account is not active")
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )
        
        # Update last login
        user.last_login = datetime.utcnow()
        await user.save()
        
        return SuccessResponse(
            message="Login successful",
            data={
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": settings.access_token_expire_minutes * 60,
                "user": {
                    "user_id": str(user.id),
                    "email": user.email,
                    "username": user.username,
                    "full_name": user.full_name,
                    "role": user.role,
                    "preferred_language": user.preferred_language
                }
            }
        )
        
    except AuthenticationException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user information"""
    try:
        # Verify token
        payload = verify_token(token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise AuthenticationException("Invalid token")
        
        # Get user
        user = await User.get(user_id)
        if not user:
            raise AuthenticationException("User not found")
        
        return UserResponse(
            user_id=str(user.id),
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            role=user.role,
            status=user.status,
            is_verified=user.is_verified,
            phone_number=user.phone_number,
            country=user.country,
            preferred_language=user.preferred_language,
            profile_image_url=user.profile_image_url,
            bio=user.bio,
            interests=user.interests,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login
        )
        
    except AuthenticationException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user information: {str(e)}"
        )

@router.post("/refresh", response_model=SuccessResponse)
async def refresh_token(token: str = Depends(oauth2_scheme)):
    """Refresh access token"""
    try:
        # Verify current token
        payload = verify_token(token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise AuthenticationException("Invalid token")
        
        # Get user
        user = await User.get(user_id)
        if not user:
            raise AuthenticationException("User not found")
        
        # Create new access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )
        
        return SuccessResponse(
            message="Token refreshed successfully",
            data={
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": settings.access_token_expire_minutes * 60
            }
        )
        
    except AuthenticationException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token refresh failed: {str(e)}"
        )

@router.post("/logout", response_model=SuccessResponse)
async def logout_user(token: str = Depends(oauth2_scheme)):
    """Logout user (invalidate token)"""
    # In a real implementation, you would add the token to a blacklist
    # For now, we'll just return a success message
    return SuccessResponse(
        message="Logout successful"
    )