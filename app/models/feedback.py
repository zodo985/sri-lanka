from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class FeedbackType(str, Enum):
    CHATBOT_RESPONSE = "chatbot_response"
    ATTRACTION_INFO = "attraction_info"
    RESTAURANT_RECOMMENDATION = "restaurant_recommendation"
    TRANSPORTATION_INFO = "transportation_info"
    ITINERARY_SUGGESTION = "itinerary_suggestion"
    GENERAL_EXPERIENCE = "general_experience"

class FeedbackRating(str, Enum):
    VERY_POOR = "very_poor"
    POOR = "poor"
    NEUTRAL = "neutral"
    GOOD = "good"
    EXCELLENT = "excellent"

class Feedback(Document):
    """User feedback and ratings"""
    feedback_id: str = Indexed(unique=True)
    user_id: Optional[str] = Indexed()
    session_id: Optional[str] = Indexed()
    
    # Feedback Details
    feedback_type: FeedbackType = Indexed()
    rating: FeedbackRating
    comment: Optional[str] = None
    
    # Context
    context: Dict[str, Any] = {}  # Related items, conversation context
    item_id: Optional[str] = None  # ID of the item being rated
    item_type: Optional[str] = None  # Type of item being rated
    
    # Language
    language: str = "en"
    original_text: Optional[str] = None  # Original text if translated
    
    # Sentiment Analysis
    sentiment_score: Optional[float] = None  # -1.0 to 1.0
    emotion: Optional[str] = None  # "happy", "frustrated", "satisfied"
    
    # Processing
    is_processed: bool = False
    is_acknowledged: bool = False
    admin_response: Optional[str] = None
    admin_user_id: Optional[str] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    processed_at: Optional[datetime] = None
    
    class Settings:
        name = "feedback"
        indexes = [
            "feedback_id",
            "user_id",
            "session_id",
            "feedback_type",
            "rating",
            "created_at"
        ]

class Review(Document):
    """Detailed reviews for attractions, restaurants, accommodations"""
    review_id: str = Indexed(unique=True)
    user_id: str = Indexed()
    item_id: str = Indexed()
    item_type: str = Indexed()  # "tourist_attraction", "restaurant", "accommodation"
    
    # Review Content
    title: str
    content: str
    rating: int = Field(..., ge=1, le=5)
    
    # Detailed Ratings
    detailed_ratings: Dict[str, int] = {}  # {"service": 4, "cleanliness": 5, "value": 3}
    
    # Review Metadata
    language: str = "en"
    is_verified: bool = False
    is_anonymous: bool = False
    
    # Media
    images: List[str] = []
    videos: List[str] = []
    
    # Visit Information
    visit_date: Optional[date] = None
    visit_type: Optional[str] = None  # "solo", "couple", "family", "business"
    
    # Social Features
    helpful_votes: int = 0
    not_helpful_votes: int = 0
    is_featured: bool = False
    
    # Moderation
    is_approved: bool = True
    is_flagged: bool = False
    moderation_notes: Optional[str] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "reviews"
        indexes = [
            "review_id",
            "user_id",
            "item_id",
            "item_type",
            "rating",
            "is_approved"
        ]

class Analytics(Document):
    """Analytics and usage statistics"""
    analytics_id: str = Indexed(unique=True)
    
    # Time Period
    date: date = Indexed()
    hour: Optional[int] = None  # 0-23 for hourly analytics
    
    # Metrics
    total_users: int = 0
    active_users: int = 0
    new_users: int = 0
    returning_users: int = 0
    
    # Chat Metrics
    total_messages: int = 0
    total_sessions: int = 0
    average_session_duration: float = 0.0
    average_messages_per_session: float = 0.0
    
    # Language Usage
    language_usage: Dict[str, int] = {}  # {"en": 100, "si": 50, "ta": 25}
    
    # Feature Usage
    feature_usage: Dict[str, int] = {}  # {"attraction_search": 100, "voice_input": 50}
    
    # Geographic Distribution
    country_distribution: Dict[str, int] = {}  # {"Sri Lanka": 100, "India": 50}
    city_distribution: Dict[str, int] = {}  # {"Colombo": 50, "Kandy": 30}
    
    # Performance Metrics
    average_response_time: float = 0.0
    error_rate: float = 0.0
    satisfaction_score: float = 0.0
    
    # Content Popularity
    popular_attractions: List[Dict[str, Any]] = []
    popular_queries: List[Dict[str, Any]] = []
    popular_intents: List[Dict[str, Any]] = []
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "analytics"
        indexes = [
            "analytics_id",
            "date",
            "hour"
        ]

class UserBehavior(Document):
    """Individual user behavior tracking"""
    behavior_id: str = Indexed(unique=True)
    user_id: str = Indexed()
    session_id: Optional[str] = Indexed()
    
    # Behavior Details
    action: str  # "search", "click", "view", "save", "share"
    target_type: str  # "attraction", "restaurant", "message", "recommendation"
    target_id: Optional[str] = None
    
    # Context
    context: Dict[str, Any] = {}
    page_url: Optional[str] = None
    referrer: Optional[str] = None
    
    # Device Information
    device_type: Optional[str] = None  # "mobile", "desktop", "tablet"
    browser: Optional[str] = None
    os: Optional[str] = None
    
    # Location
    location: Optional[Dict[str, float]] = None
    country: Optional[str] = None
    city: Optional[str] = None
    
    # Timestamps
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "user_behavior"
        indexes = [
            "behavior_id",
            "user_id",
            "session_id",
            "action",
            "timestamp"
        ]

class SystemMetrics(Document):
    """System performance and health metrics"""
    metric_id: str = Indexed(unique=True)
    
    # Time Period
    timestamp: datetime = Indexed()
    metric_type: str  # "performance", "error", "usage", "health"
    
    # Metric Values
    metric_name: str
    metric_value: float
    metric_unit: Optional[str] = None  # "ms", "bytes", "count", "percentage"
    
    # Context
    service: Optional[str] = None  # "api", "database", "rasa", "translation"
    endpoint: Optional[str] = None
    error_type: Optional[str] = None
    
    # Additional Data
    metadata: Dict[str, Any] = {}
    
    class Settings:
        name = "system_metrics"
        indexes = [
            "metric_id",
            "timestamp",
            "metric_type",
            "service"
        ]