from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.user import UserRole, UserStatus

class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=2, max_length=100)
    phone_number: Optional[str] = None
    country: Optional[str] = None
    preferred_language: str = "en"
    bio: Optional[str] = None
    interests: List[str] = []

class UserCreate(UserBase):
    """User creation schema"""
    password: str = Field(..., min_length=8, max_length=100)
    confirm_password: str

class UserUpdate(BaseModel):
    """User update schema"""
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    country: Optional[str] = None
    preferred_language: Optional[str] = None
    bio: Optional[str] = None
    interests: Optional[List[str]] = None
    profile_image_url: Optional[str] = None

class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str

class UserResponse(UserBase):
    """User response schema"""
    user_id: str
    role: UserRole
    status: UserStatus
    is_verified: bool
    profile_image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

class UserProfile(BaseModel):
    """User profile schema"""
    user_id: str
    full_name: str
    email: str
    username: str
    profile_image_url: Optional[str] = None
    bio: Optional[str] = None
    country: Optional[str] = None
    preferred_language: str
    interests: List[str] = []
    created_at: datetime

class UserPreferenceCreate(BaseModel):
    """User preference creation schema"""
    primary_language: str = "en"
    secondary_languages: List[str] = []
    auto_translate: bool = True
    email_notifications: bool = True
    push_notifications: bool = True
    sms_notifications: bool = False
    notification_frequency: str = "immediate"
    content_categories: List[str] = []
    difficulty_level: str = "beginner"
    content_rating: str = "family_friendly"
    budget_range: Optional[Dict[str, float]] = None
    travel_style: List[str] = []
    accommodation_type: List[str] = []
    transportation_preference: List[str] = []
    accessibility_needs: List[str] = []
    dietary_restrictions: List[str] = []
    data_sharing: bool = True
    location_tracking: bool = False
    personalized_recommendations: bool = True

class UserPreferenceUpdate(BaseModel):
    """User preference update schema"""
    primary_language: Optional[str] = None
    secondary_languages: Optional[List[str]] = None
    auto_translate: Optional[bool] = None
    email_notifications: Optional[bool] = None
    push_notifications: Optional[bool] = None
    sms_notifications: Optional[bool] = None
    notification_frequency: Optional[str] = None
    content_categories: Optional[List[str]] = None
    difficulty_level: Optional[str] = None
    content_rating: Optional[str] = None
    budget_range: Optional[Dict[str, float]] = None
    travel_style: Optional[List[str]] = None
    accommodation_type: Optional[List[str]] = None
    transportation_preference: Optional[List[str]] = None
    accessibility_needs: Optional[List[str]] = None
    dietary_restrictions: Optional[List[str]] = None
    data_sharing: Optional[bool] = None
    location_tracking: Optional[bool] = None
    personalized_recommendations: Optional[bool] = None

class UserPreferenceResponse(BaseModel):
    """User preference response schema"""
    user_id: str
    primary_language: str
    secondary_languages: List[str]
    auto_translate: bool
    email_notifications: bool
    push_notifications: bool
    sms_notifications: bool
    notification_frequency: str
    content_categories: List[str]
    difficulty_level: str
    content_rating: str
    budget_range: Optional[Dict[str, float]] = None
    travel_style: List[str]
    accommodation_type: List[str]
    transportation_preference: List[str]
    accessibility_needs: List[str]
    dietary_restrictions: List[str]
    data_sharing: bool
    location_tracking: bool
    personalized_recommendations: bool
    created_at: datetime
    updated_at: datetime