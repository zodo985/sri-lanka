from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    TOURIST = "tourist"
    ADMIN = "admin"
    MODERATOR = "moderator"
    LOCAL_GUIDE = "local_guide"

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"

class User(Document):
    """User model for tourists and administrators"""
    email: EmailStr = Indexed(unique=True)
    username: str = Indexed(unique=True)
    full_name: str
    hashed_password: str
    role: UserRole = UserRole.TOURIST
    status: UserStatus = UserStatus.ACTIVE
    
    # Profile Information
    phone_number: Optional[str] = None
    country: Optional[str] = None
    preferred_language: str = "en"
    profile_image_url: Optional[str] = None
    bio: Optional[str] = None
    
    # Location & Preferences
    current_location: Optional[Dict[str, float]] = None  # {lat, lng}
    home_country: Optional[str] = None
    interests: List[str] = []  # ["culture", "nature", "adventure", "food"]
    
    # Authentication
    is_verified: bool = False
    verification_token: Optional[str] = None
    reset_password_token: Optional[str] = None
    last_login: Optional[datetime] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Privacy & Security
    privacy_settings: Dict[str, bool] = {
        "profile_public": True,
        "location_sharing": False,
        "data_analytics": True
    }
    
    # Social Features
    social_connections: List[str] = []  # User IDs of connected users
    blocked_users: List[str] = []  # User IDs of blocked users
    
    class Settings:
        name = "users"
        indexes = [
            "email",
            "username", 
            "role",
            "status",
            "created_at"
        ]

class UserPreference(Document):
    """User preferences and settings"""
    user_id: str = Indexed()
    
    # Language Preferences
    primary_language: str = "en"
    secondary_languages: List[str] = []
    auto_translate: bool = True
    
    # Notification Preferences
    email_notifications: bool = True
    push_notifications: bool = True
    sms_notifications: bool = False
    notification_frequency: str = "immediate"  # immediate, daily, weekly
    
    # Content Preferences
    content_categories: List[str] = []  # ["attractions", "food", "culture", "transport"]
    difficulty_level: str = "beginner"  # beginner, intermediate, advanced
    content_rating: str = "family_friendly"  # family_friendly, adult, all_ages
    
    # Travel Preferences
    budget_range: Optional[Dict[str, float]] = None  # {min, max}
    travel_style: List[str] = []  # ["budget", "luxury", "adventure", "cultural"]
    accommodation_type: List[str] = []  # ["hotel", "guesthouse", "hostel", "resort"]
    transportation_preference: List[str] = []  # ["public", "private", "walking", "cycling"]
    
    # Accessibility
    accessibility_needs: List[str] = []  # ["wheelchair", "hearing", "visual", "mobility"]
    dietary_restrictions: List[str] = []  # ["vegetarian", "vegan", "halal", "gluten_free"]
    
    # Privacy Settings
    data_sharing: bool = True
    location_tracking: bool = False
    personalized_recommendations: bool = True
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "user_preferences"
        indexes = ["user_id"]