from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from app.models.user import User, UserPreference
from app.schemas.user import UserUpdate, UserResponse, UserPreferenceCreate, UserPreferenceUpdate, UserPreferenceResponse
from app.schemas.common import SuccessResponse
from app.core.exceptions import NotFoundException, ValidationException
from app.core.security import verify_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/me", response_model=UserResponse)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user information"""
    try:
        # Verify token
        payload = verify_token(token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise ValidationException("Invalid token")
        
        # Get user
        user = await User.get(user_id)
        if not user:
            raise NotFoundException("User not found")
        
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
        
    except (ValidationException, NotFoundException):
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user information: {str(e)}"
        )

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    token: str = Depends(oauth2_scheme)
):
    """Update current user information"""
    try:
        # Verify token
        payload = verify_token(token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise ValidationException("Invalid token")
        
        # Get user
        user = await User.get(user_id)
        if not user:
            raise NotFoundException("User not found")
        
        # Update user fields
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        user.updated_at = datetime.utcnow()
        await user.save()
        
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
        
    except (ValidationException, NotFoundException):
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user: {str(e)}"
        )

@router.get("/preferences", response_model=UserPreferenceResponse)
async def get_user_preferences(token: str = Depends(oauth2_scheme)):
    """Get user preferences"""
    try:
        # Verify token
        payload = verify_token(token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise ValidationException("Invalid token")
        
        # Get user preferences
        preferences = await UserPreference.find_one(UserPreference.user_id == user_id)
        if not preferences:
            raise NotFoundException("User preferences not found")
        
        return UserPreferenceResponse(
            user_id=preferences.user_id,
            primary_language=preferences.primary_language,
            secondary_languages=preferences.secondary_languages,
            auto_translate=preferences.auto_translate,
            email_notifications=preferences.email_notifications,
            push_notifications=preferences.push_notifications,
            sms_notifications=preferences.sms_notifications,
            notification_frequency=preferences.notification_frequency,
            content_categories=preferences.content_categories,
            difficulty_level=preferences.difficulty_level,
            content_rating=preferences.content_rating,
            budget_range=preferences.budget_range,
            travel_style=preferences.travel_style,
            accommodation_type=preferences.accommodation_type,
            transportation_preference=preferences.transportation_preference,
            accessibility_needs=preferences.accessibility_needs,
            dietary_restrictions=preferences.dietary_restrictions,
            data_sharing=preferences.data_sharing,
            location_tracking=preferences.location_tracking,
            personalized_recommendations=preferences.personalized_recommendations,
            created_at=preferences.created_at,
            updated_at=preferences.updated_at
        )
        
    except (ValidationException, NotFoundException):
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user preferences: {str(e)}"
        )

@router.post("/preferences", response_model=UserPreferenceResponse)
async def create_user_preferences(
    preferences_data: UserPreferenceCreate,
    token: str = Depends(oauth2_scheme)
):
    """Create user preferences"""
    try:
        # Verify token
        payload = verify_token(token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise ValidationException("Invalid token")
        
        # Check if preferences already exist
        existing_preferences = await UserPreference.find_one(UserPreference.user_id == user_id)
        if existing_preferences:
            raise ValidationException("User preferences already exist")
        
        # Create preferences
        preferences = UserPreference(
            user_id=user_id,
            **preferences_data.dict()
        )
        
        await preferences.insert()
        
        return UserPreferenceResponse(
            user_id=preferences.user_id,
            primary_language=preferences.primary_language,
            secondary_languages=preferences.secondary_languages,
            auto_translate=preferences.auto_translate,
            email_notifications=preferences.email_notifications,
            push_notifications=preferences.push_notifications,
            sms_notifications=preferences.sms_notifications,
            notification_frequency=preferences.notification_frequency,
            content_categories=preferences.content_categories,
            difficulty_level=preferences.difficulty_level,
            content_rating=preferences.content_rating,
            budget_range=preferences.budget_range,
            travel_style=preferences.travel_style,
            accommodation_type=preferences.accommodation_type,
            transportation_preference=preferences.transportation_preference,
            accessibility_needs=preferences.accessibility_needs,
            dietary_restrictions=preferences.dietary_restrictions,
            data_sharing=preferences.data_sharing,
            location_tracking=preferences.location_tracking,
            personalized_recommendations=preferences.personalized_recommendations,
            created_at=preferences.created_at,
            updated_at=preferences.updated_at
        )
        
    except (ValidationException, NotFoundException):
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user preferences: {str(e)}"
        )

@router.put("/preferences", response_model=UserPreferenceResponse)
async def update_user_preferences(
    preferences_update: UserPreferenceUpdate,
    token: str = Depends(oauth2_scheme)
):
    """Update user preferences"""
    try:
        # Verify token
        payload = verify_token(token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise ValidationException("Invalid token")
        
        # Get user preferences
        preferences = await UserPreference.find_one(UserPreference.user_id == user_id)
        if not preferences:
            raise NotFoundException("User preferences not found")
        
        # Update preferences
        update_data = preferences_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(preferences, field, value)
        
        preferences.updated_at = datetime.utcnow()
        await preferences.save()
        
        return UserPreferenceResponse(
            user_id=preferences.user_id,
            primary_language=preferences.primary_language,
            secondary_languages=preferences.secondary_languages,
            auto_translate=preferences.auto_translate,
            email_notifications=preferences.email_notifications,
            push_notifications=preferences.push_notifications,
            sms_notifications=preferences.sms_notifications,
            notification_frequency=preferences.notification_frequency,
            content_categories=preferences.content_categories,
            difficulty_level=preferences.difficulty_level,
            content_rating=preferences.content_rating,
            budget_range=preferences.budget_range,
            travel_style=preferences.travel_style,
            accommodation_type=preferences.accommodation_type,
            transportation_preference=preferences.transportation_preference,
            accessibility_needs=preferences.accessibility_needs,
            dietary_restrictions=preferences.dietary_restrictions,
            data_sharing=preferences.data_sharing,
            location_tracking=preferences.location_tracking,
            personalized_recommendations=preferences.personalized_recommendations,
            created_at=preferences.created_at,
            updated_at=preferences.updated_at
        )
        
    except (ValidationException, NotFoundException):
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user preferences: {str(e)}"
        )