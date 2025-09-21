from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class AttractionType(str, Enum):
    HISTORICAL = "historical"
    NATURAL = "natural"
    CULTURAL = "cultural"
    RELIGIOUS = "religious"
    ADVENTURE = "adventure"
    BEACH = "beach"
    WILDLIFE = "wildlife"
    HILL_STATION = "hill_station"
    WATERFALL = "waterfall"
    MUSEUM = "museum"
    GARDEN = "garden"
    MARKET = "market"

class DifficultyLevel(str, Enum):
    EASY = "easy"
    MODERATE = "moderate"
    CHALLENGING = "challenging"

class TouristAttraction(Document):
    """Tourist attractions and destinations"""
    name: str = Indexed()
    name_sinhala: Optional[str] = None
    name_tamil: Optional[str] = None
    
    # Basic Information
    description: str
    description_sinhala: Optional[str] = None
    description_tamil: Optional[str] = None
    
    # Location
    location: Dict[str, float] = Field(..., description="Latitude and longitude")
    address: str
    district: str = Indexed()
    province: str = Indexed()
    
    # Categorization
    attraction_type: AttractionType = Indexed()
    tags: List[str] = []  # ["unesco", "national_park", "temple", "beach"]
    difficulty_level: DifficultyLevel = DifficultyLevel.EASY
    
    # Details
    opening_hours: Optional[Dict[str, str]] = None  # {"monday": "9:00-17:00"}
    entrance_fee: Optional[Dict[str, float]] = None  # {"adult": 1000, "child": 500}
    best_time_to_visit: List[str] = []  # ["morning", "evening", "sunset"]
    duration_visit: int = 60  # minutes
    
    # Media
    images: List[str] = []  # URLs
    videos: List[str] = []  # URLs
    virtual_tour_url: Optional[str] = None
    
    # Accessibility
    wheelchair_accessible: bool = False
    parking_available: bool = False
    public_transport: bool = False
    
    # Contact & Services
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    website: Optional[str] = None
    
    # Ratings & Reviews
    average_rating: float = 0.0
    total_reviews: int = 0
    popularity_score: float = 0.0
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Status
    is_active: bool = True
    is_featured: bool = False
    
    class Settings:
        name = "tourist_attractions"
        indexes = [
            "name",
            "district",
            "province",
            "attraction_type",
            "is_active",
            "is_featured"
        ]

class AccommodationType(str, Enum):
    HOTEL = "hotel"
    GUESTHOUSE = "guesthouse"
    HOSTEL = "hostel"
    RESORT = "resort"
    VILLA = "villa"
    HOMESTAY = "homestay"
    CAMPING = "camping"

class Accommodation(Document):
    """Accommodation options"""
    name: str = Indexed()
    accommodation_type: AccommodationType = Indexed()
    
    # Location
    location: Dict[str, float] = Field(..., description="Latitude and longitude")
    address: str
    district: str = Indexed()
    city: str
    
    # Details
    description: str
    amenities: List[str] = []  # ["wifi", "pool", "restaurant", "spa"]
    room_types: List[Dict[str, Any]] = []  # [{"type": "deluxe", "price": 15000, "capacity": 2}]
    
    # Pricing
    price_range: Dict[str, float] = {}  # {"min": 5000, "max": 25000}
    currency: str = "LKR"
    
    # Contact
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    
    # Ratings
    average_rating: float = 0.0
    total_reviews: int = 0
    
    # Media
    images: List[str] = []
    
    # Status
    is_active: bool = True
    is_verified: bool = False
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "accommodations"
        indexes = [
            "name",
            "accommodation_type",
            "district",
            "is_active"
        ]

class Restaurant(Document):
    """Restaurants and food establishments"""
    name: str = Indexed()
    
    # Location
    location: Dict[str, float] = Field(..., description="Latitude and longitude")
    address: str
    district: str = Indexed()
    city: str
    
    # Cuisine & Details
    cuisine_types: List[str] = []  # ["sri_lankan", "indian", "chinese", "western"]
    specialties: List[str] = []  # ["rice_and_curry", "kottu", "hoppers"]
    price_range: str = "$$"  # $, $$, $$$, $$$$
    
    # Services
    delivery_available: bool = False
    takeaway_available: bool = True
    dine_in_available: bool = True
    outdoor_seating: bool = False
    
    # Contact
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    
    # Hours
    opening_hours: Optional[Dict[str, str]] = None
    
    # Ratings
    average_rating: float = 0.0
    total_reviews: int = 0
    
    # Media
    images: List[str] = []
    menu_images: List[str] = []
    
    # Status
    is_active: bool = True
    is_verified: bool = False
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "restaurants"
        indexes = [
            "name",
            "district",
            "cuisine_types",
            "is_active"
        ]

class TransportationType(str, Enum):
    BUS = "bus"
    TRAIN = "train"
    TAXI = "taxi"
    TUK_TUK = "tuk_tuk"
    RENTAL_CAR = "rental_car"
    AIRPORT_TRANSFER = "airport_transfer"
    PRIVATE_DRIVER = "private_driver"

class Transportation(Document):
    """Transportation options and services"""
    name: str = Indexed()
    transport_type: TransportationType = Indexed()
    
    # Route Information
    from_location: str
    to_location: str
    route_description: Optional[str] = None
    
    # Schedule
    departure_times: List[str] = []  # ["06:00", "12:00", "18:00"]
    duration_minutes: int
    frequency: str = "daily"  # daily, weekly, hourly
    
    # Pricing
    price_range: Dict[str, float] = {}  # {"adult": 100, "child": 50}
    currency: str = "LKR"
    
    # Contact
    phone: Optional[str] = None
    website: Optional[str] = None
    
    # Features
    features: List[str] = []  # ["ac", "wifi", "charging", "wheelchair_accessible"]
    
    # Status
    is_active: bool = True
    is_operational: bool = True
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "transportation"
        indexes = [
            "name",
            "transport_type",
            "is_active"
        ]

class EmergencyService(Document):
    """Emergency services and contacts"""
    service_name: str = Indexed()
    service_type: str  # "police", "hospital", "fire", "embassy", "tourist_police"
    
    # Contact Information
    phone: str
    emergency_phone: Optional[str] = None
    email: Optional[str] = None
    
    # Location
    location: Optional[Dict[str, float]] = None
    address: Optional[str] = None
    district: Optional[str] = None
    
    # Details
    description: str
    operating_hours: Optional[str] = None
    languages_supported: List[str] = ["en", "si", "ta"]
    
    # Status
    is_active: bool = True
    is_24_hours: bool = False
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "emergency_services"
        indexes = [
            "service_name",
            "service_type",
            "is_active"
        ]

class CulturalEvent(Document):
    """Cultural events and festivals"""
    name: str = Indexed()
    name_sinhala: Optional[str] = None
    name_tamil: Optional[str] = None
    
    # Event Details
    description: str
    event_type: str  # "festival", "ceremony", "celebration", "religious"
    
    # Dates
    start_date: datetime
    end_date: Optional[datetime] = None
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None  # "yearly", "monthly", "weekly"
    
    # Location
    location: Optional[Dict[str, float]] = None
    venue: str
    district: str = Indexed()
    
    # Details
    entry_fee: Optional[float] = None
    currency: str = "LKR"
    age_restriction: Optional[str] = None
    dress_code: Optional[str] = None
    
    # Media
    images: List[str] = []
    videos: List[str] = []
    
    # Status
    is_active: bool = True
    is_featured: bool = False
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "cultural_events"
        indexes = [
            "name",
            "district",
            "start_date",
            "is_active"
        ]