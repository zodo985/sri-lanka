from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional, Dict, Any
from app.schemas.common import SuccessResponse
from app.core.exceptions import ValidationException
from app.core.security import verify_token
from app.services.recommendation_service import RecommendationService
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Initialize service
recommendation_service = RecommendationService()

@router.get("/attractions")
async def get_attraction_recommendations(
    limit: int = 5,
    location: Optional[Dict[str, float]] = None,
    token: Optional[str] = Depends(oauth2_scheme)
):
    """Get personalized attraction recommendations"""
    try:
        user_id = None
        preferences = None
        
        if token:
            # Verify token and get user preferences
            payload = verify_token(token)
            user_id = payload.get("sub")
            
            if user_id:
                from app.models.user import UserPreference
                user_preferences = await UserPreference.find_one(UserPreference.user_id == user_id)
                if user_preferences:
                    preferences = {
                        "interests": user_preferences.interests,
                        "difficulty_level": user_preferences.difficulty_level,
                        "accessibility_needs": user_preferences.accessibility_needs
                    }
        
        recommendations = await recommendation_service.get_attraction_recommendations(
            user_id=user_id,
            preferences=preferences,
            location=location,
            limit=limit
        )
        
        return SuccessResponse(
            message="Attraction recommendations retrieved successfully",
            data=recommendations
        )
        
    except ValidationException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get attraction recommendations: {str(e)}"
        )

@router.get("/restaurants")
async def get_restaurant_recommendations(
    limit: int = 5,
    location: Optional[Dict[str, float]] = None,
    token: Optional[str] = Depends(oauth2_scheme)
):
    """Get personalized restaurant recommendations"""
    try:
        user_id = None
        preferences = None
        
        if token:
            # Verify token and get user preferences
            payload = verify_token(token)
            user_id = payload.get("sub")
            
            if user_id:
                from app.models.user import UserPreference
                user_preferences = await UserPreference.find_one(UserPreference.user_id == user_id)
                if user_preferences:
                    preferences = {
                        "cuisine_preferences": user_preferences.interests,
                        "dietary_restrictions": user_preferences.dietary_restrictions
                    }
        
        recommendations = await recommendation_service.get_restaurant_recommendations(
            user_id=user_id,
            preferences=preferences,
            location=location,
            limit=limit
        )
        
        return SuccessResponse(
            message="Restaurant recommendations retrieved successfully",
            data=recommendations
        )
        
    except ValidationException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get restaurant recommendations: {str(e)}"
        )

@router.get("/accommodations")
async def get_accommodation_recommendations(
    limit: int = 5,
    location: Optional[Dict[str, float]] = None,
    token: Optional[str] = Depends(oauth2_scheme)
):
    """Get personalized accommodation recommendations"""
    try:
        user_id = None
        preferences = None
        
        if token:
            # Verify token and get user preferences
            payload = verify_token(token)
            user_id = payload.get("sub")
            
            if user_id:
                from app.models.user import UserPreference
                user_preferences = await UserPreference.find_one(UserPreference.user_id == user_id)
                if user_preferences:
                    preferences = {
                        "accommodation_types": user_preferences.accommodation_type,
                        "budget_range": user_preferences.budget_range,
                        "travel_style": user_preferences.travel_style
                    }
        
        recommendations = await recommendation_service.get_accommodation_recommendations(
            user_id=user_id,
            preferences=preferences,
            location=location,
            limit=limit
        )
        
        return SuccessResponse(
            message="Accommodation recommendations retrieved successfully",
            data=recommendations
        )
        
    except ValidationException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get accommodation recommendations: {str(e)}"
        )

@router.get("/personalized")
async def get_personalized_recommendations(
    limit: int = 10,
    location: Optional[Dict[str, float]] = None,
    token: str = Depends(oauth2_scheme)
):
    """Get comprehensive personalized recommendations"""
    try:
        # Verify token
        payload = verify_token(token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise ValidationException("Invalid token")
        
        # Get user preferences
        from app.models.user import UserPreference
        user_preferences = await UserPreference.find_one(UserPreference.user_id == user_id)
        
        preferences = None
        if user_preferences:
            preferences = {
                "interests": user_preferences.interests,
                "difficulty_level": user_preferences.difficulty_level,
                "accessibility_needs": user_preferences.accessibility_needs,
                "cuisine_preferences": user_preferences.interests,
                "dietary_restrictions": user_preferences.dietary_restrictions,
                "accommodation_types": user_preferences.accommodation_type,
                "budget_range": user_preferences.budget_range,
                "travel_style": user_preferences.travel_style
            }
        
        # Get recommendations for all categories
        attraction_recs = await recommendation_service.get_attraction_recommendations(
            user_id=user_id,
            preferences=preferences,
            location=location,
            limit=limit // 3
        )
        
        restaurant_recs = await recommendation_service.get_restaurant_recommendations(
            user_id=user_id,
            preferences=preferences,
            location=location,
            limit=limit // 3
        )
        
        accommodation_recs = await recommendation_service.get_accommodation_recommendations(
            user_id=user_id,
            preferences=preferences,
            location=location,
            limit=limit // 3
        )
        
        return SuccessResponse(
            message="Personalized recommendations retrieved successfully",
            data={
                "attractions": attraction_recs,
                "restaurants": restaurant_recs,
                "accommodations": accommodation_recs
            }
        )
        
    except ValidationException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get personalized recommendations: {str(e)}"
        )