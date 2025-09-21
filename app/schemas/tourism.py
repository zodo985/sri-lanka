from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.tourism import AttractionType, DifficultyLevel, AccommodationType, TransportationType

class TouristAttractionResponse(BaseModel):
    """Tourist attraction response schema"""
    attraction_id: str
    name: str
    name_sinhala: Optional[str] = None
    name_tamil: Optional[str] = None
    description: str
    description_sinhala: Optional[str] = None
    description_tamil: Optional[str] = None
    location: Dict[str, float]
    address: str
    district: str
    province: str
    attraction_type: AttractionType
    tags: List[str]
    difficulty_level: DifficultyLevel
    opening_hours: Optional[Dict[str, str]] = None
    entrance_fee: Optional[Dict[str, float]] = None
    best_time_to_visit: List[str]
    duration_visit: int
    images: List[str]
    videos: List[str] = []
    virtual_tour_url: Optional[str] = None
    wheelchair_accessible: bool
    parking_available: bool
    public_transport: bool
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    website: Optional[str] = None
    average_rating: float
    total_reviews: int
    popularity_score: float
    is_active: bool
    is_featured: bool
    created_at: datetime
    updated_at: datetime

class AccommodationResponse(BaseModel):
    """Accommodation response schema"""
    accommodation_id: str
    name: str
    accommodation_type: AccommodationType
    location: Dict[str, float]
    address: str
    district: str
    city: str
    description: str
    amenities: List[str]
    room_types: List[Dict[str, Any]]
    price_range: Dict[str, float]
    currency: str
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    average_rating: float
    total_reviews: int
    images: List[str]
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

class RestaurantResponse(BaseModel):
    """Restaurant response schema"""
    restaurant_id: str
    name: str
    location: Dict[str, float]
    address: str
    district: str
    city: str
    cuisine_types: List[str]
    specialties: List[str]
    price_range: str
    delivery_available: bool
    takeaway_available: bool
    dine_in_available: bool
    outdoor_seating: bool
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    opening_hours: Optional[Dict[str, str]] = None
    average_rating: float
    total_reviews: int
    images: List[str]
    menu_images: List[str] = []
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

class TransportationResponse(BaseModel):
    """Transportation response schema"""
    transportation_id: str
    name: str
    transport_type: TransportationType
    from_location: str
    to_location: str
    route_description: Optional[str] = None
    departure_times: List[str]
    duration_minutes: int
    frequency: str
    price_range: Dict[str, float]
    currency: str
    phone: Optional[str] = None
    website: Optional[str] = None
    features: List[str]
    is_active: bool
    is_operational: bool
    created_at: datetime
    updated_at: datetime

class EmergencyServiceResponse(BaseModel):
    """Emergency service response schema"""
    service_id: str
    service_name: str
    service_type: str
    phone: str
    emergency_phone: Optional[str] = None
    email: Optional[str] = None
    location: Optional[Dict[str, float]] = None
    address: Optional[str] = None
    district: Optional[str] = None
    description: str
    operating_hours: Optional[str] = None
    languages_supported: List[str]
    is_active: bool
    is_24_hours: bool
    created_at: datetime
    updated_at: datetime

class CulturalEventResponse(BaseModel):
    """Cultural event response schema"""
    event_id: str
    name: str
    name_sinhala: Optional[str] = None
    name_tamil: Optional[str] = None
    description: str
    event_type: str
    start_date: datetime
    end_date: Optional[datetime] = None
    is_recurring: bool
    recurrence_pattern: Optional[str] = None
    location: Optional[Dict[str, float]] = None
    venue: str
    district: str
    entry_fee: Optional[float] = None
    currency: str
    age_restriction: Optional[str] = None
    dress_code: Optional[str] = None
    images: List[str]
    videos: List[str] = []
    is_active: bool
    is_featured: bool
    created_at: datetime
    updated_at: datetime

class AttractionSearchRequest(BaseModel):
    """Attraction search request schema"""
    query: Optional[str] = None
    attraction_type: Optional[AttractionType] = None
    district: Optional[str] = None
    province: Optional[str] = None
    tags: Optional[List[str]] = None
    difficulty_level: Optional[DifficultyLevel] = None
    wheelchair_accessible: Optional[bool] = None
    location: Optional[Dict[str, float]] = None
    radius: Optional[float] = None  # kilometers
    min_rating: Optional[float] = None
    is_featured: Optional[bool] = None
    page: int = 1
    limit: int = 10

class RestaurantSearchRequest(BaseModel):
    """Restaurant search request schema"""
    query: Optional[str] = None
    cuisine_types: Optional[List[str]] = None
    district: Optional[str] = None
    city: Optional[str] = None
    price_range: Optional[str] = None
    delivery_available: Optional[bool] = None
    outdoor_seating: Optional[bool] = None
    location: Optional[Dict[str, float]] = None
    radius: Optional[float] = None
    min_rating: Optional[float] = None
    page: int = 1
    limit: int = 10

class AccommodationSearchRequest(BaseModel):
    """Accommodation search request schema"""
    query: Optional[str] = None
    accommodation_type: Optional[AccommodationType] = None
    district: Optional[str] = None
    city: Optional[str] = None
    amenities: Optional[List[str]] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    currency: str = "LKR"
    location: Optional[Dict[str, float]] = None
    radius: Optional[float] = None
    min_rating: Optional[float] = None
    page: int = 1
    limit: int = 10