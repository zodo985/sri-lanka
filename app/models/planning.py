from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum

class ItineraryStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ItineraryItemType(str, Enum):
    ATTRACTION = "attraction"
    RESTAURANT = "restaurant"
    ACCOMMODATION = "accommodation"
    TRANSPORTATION = "transportation"
    ACTIVITY = "activity"
    BREAK = "break"

class Itinerary(Document):
    """Travel itinerary planning and management"""
    itinerary_id: str = Indexed(unique=True)
    user_id: str = Indexed()
    
    # Basic Information
    title: str
    description: Optional[str] = None
    status: ItineraryStatus = ItineraryStatus.DRAFT
    
    # Trip Details
    start_date: date
    end_date: date
    duration_days: int
    budget: Optional[Dict[str, float]] = None  # {"total": 50000, "currency": "LKR"}
    
    # Travel Information
    travelers_count: int = 1
    traveler_types: List[str] = []  # ["adult", "child", "senior"]
    travel_style: List[str] = []  # ["budget", "luxury", "adventure", "cultural"]
    
    # Itinerary Items
    items: List[Dict[str, Any]] = []  # Detailed itinerary items
    
    # Preferences
    preferences: Dict[str, Any] = {
        "interests": [],
        "accessibility_needs": [],
        "dietary_restrictions": [],
        "transportation_preference": [],
        "accommodation_type": []
    }
    
    # Optimization
    is_optimized: bool = False
    optimization_score: Optional[float] = None
    total_distance: Optional[float] = None  # kilometers
    total_estimated_cost: Optional[float] = None
    
    # Sharing
    is_public: bool = False
    share_token: Optional[str] = None
    shared_with: List[str] = []  # User IDs
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "itineraries"
        indexes = [
            "itinerary_id",
            "user_id",
            "status",
            "start_date",
            "is_public"
        ]

class Recommendation(Document):
    """AI-powered recommendations for users"""
    recommendation_id: str = Indexed(unique=True)
    user_id: Optional[str] = Indexed()
    session_id: Optional[str] = Indexed()
    
    # Recommendation Details
    recommendation_type: str  # "attraction", "restaurant", "accommodation", "activity"
    item_id: str  # ID of the recommended item
    item_type: str  # "tourist_attraction", "restaurant", "accommodation"
    
    # Recommendation Content
    title: str
    description: str
    reason: str  # Why this was recommended
    confidence_score: float  # 0.0 to 1.0
    
    # Context
    context: Dict[str, Any] = {}  # User preferences, location, time, etc.
    filters_applied: List[str] = []  # ["budget", "location", "interests"]
    
    # User Interaction
    is_viewed: bool = False
    is_clicked: bool = False
    is_saved: bool = False
    is_dismissed: bool = False
    user_rating: Optional[int] = None  # 1-5 stars
    
    # Recommendation Algorithm
    algorithm_version: str = "1.0"
    features_used: List[str] = []  # ["collaborative", "content_based", "location"]
    model_confidence: float = 0.0
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    
    class Settings:
        name = "recommendations"
        indexes = [
            "recommendation_id",
            "user_id",
            "session_id",
            "recommendation_type",
            "created_at"
        ]

class TripPlan(Document):
    """Detailed trip planning with day-by-day breakdown"""
    plan_id: str = Indexed(unique=True)
    itinerary_id: str = Indexed()
    user_id: str = Indexed()
    
    # Plan Details
    day_number: int
    date: date
    location: Optional[Dict[str, float]] = None  # {lat, lng}
    city: Optional[str] = None
    district: Optional[str] = None
    
    # Daily Schedule
    morning_activities: List[Dict[str, Any]] = []
    afternoon_activities: List[Dict[str, Any]] = []
    evening_activities: List[Dict[str, Any]] = []
    
    # Daily Summary
    total_distance: Optional[float] = None
    estimated_cost: Optional[float] = None
    weather_forecast: Optional[Dict[str, Any]] = None
    
    # Notes
    notes: Optional[str] = None
    tips: List[str] = []
    warnings: List[str] = []
    
    # Status
    is_completed: bool = False
    completion_percentage: float = 0.0
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "trip_plans"
        indexes = [
            "plan_id",
            "itinerary_id",
            "user_id",
            "day_number",
            "date"
        ]

class RouteOptimization(Document):
    """Route optimization results and algorithms"""
    optimization_id: str = Indexed(unique=True)
    itinerary_id: str = Indexed()
    
    # Optimization Parameters
    algorithm: str  # "nearest_neighbor", "genetic", "simulated_annealing"
    constraints: Dict[str, Any] = {}  # {"max_driving_time": 8, "prefer_highways": true}
    
    # Results
    original_route: List[Dict[str, Any]] = []
    optimized_route: List[Dict[str, Any]] = []
    optimization_score: float = 0.0
    
    # Metrics
    total_distance: float = 0.0
    total_driving_time: float = 0.0
    total_walking_time: float = 0.0
    fuel_cost: Optional[float] = None
    
    # Processing Information
    processing_time: float = 0.0  # seconds
    iterations: int = 0
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "route_optimizations"
        indexes = [
            "optimization_id",
            "itinerary_id",
            "algorithm"
        ]