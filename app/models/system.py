from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class NotificationType(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"
    REMINDER = "reminder"
    PROMOTION = "promotion"

class NotificationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Notification(Document):
    """System and user notifications"""
    notification_id: str = Indexed(unique=True)
    user_id: Optional[str] = Indexed()  # None for system-wide notifications
    
    # Notification Content
    title: str
    message: str
    notification_type: NotificationType = NotificationType.INFO
    priority: NotificationPriority = NotificationPriority.MEDIUM
    
    # Language and Localization
    language: str = "en"
    localized_content: Dict[str, Dict[str, str]] = {}  # {language: {title, message}}
    
    # Action and Interaction
    action_url: Optional[str] = None
    action_text: Optional[str] = None
    is_actionable: bool = False
    
    # Delivery
    delivery_methods: List[str] = ["in_app"]  # ["in_app", "email", "push", "sms"]
    is_sent: bool = False
    sent_at: Optional[datetime] = None
    
    # User Interaction
    is_read: bool = False
    read_at: Optional[datetime] = None
    is_dismissed: bool = False
    dismissed_at: Optional[datetime] = None
    
    # Scheduling
    scheduled_for: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    
    # Context
    context: Dict[str, Any] = {}
    category: Optional[str] = None  # "weather", "event", "promotion", "system"
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "notifications"
        indexes = [
            "notification_id",
            "user_id",
            "notification_type",
            "is_sent",
            "is_read",
            "scheduled_for"
        ]

class WeatherData(Document):
    """Weather information and forecasts"""
    weather_id: str = Indexed(unique=True)
    location: Dict[str, float] = Indexed()  # {lat, lng}
    city: str = Indexed()
    district: str = Indexed()
    
    # Weather Information
    temperature: float  # Celsius
    humidity: float  # Percentage
    pressure: float  # hPa
    wind_speed: float  # km/h
    wind_direction: float  # Degrees
    visibility: float  # km
    
    # Weather Conditions
    condition: str  # "sunny", "cloudy", "rainy", "stormy"
    description: str
    icon_code: str
    
    # Forecast Data
    forecast_data: List[Dict[str, Any]] = []  # Hourly/daily forecasts
    
    # UV Index and Safety
    uv_index: Optional[float] = None
    air_quality_index: Optional[float] = None
    safety_warnings: List[str] = []
    
    # Data Source
    source: str = "openweather"  # "openweather", "weather_api", "local"
    data_quality: str = "good"  # "good", "fair", "poor"
    
    # Timestamps
    recorded_at: datetime = Indexed()
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "weather_data"
        indexes = [
            "weather_id",
            "location",
            "city",
            "district",
            "recorded_at"
        ]

class CurrencyRate(Document):
    """Currency exchange rates"""
    currency_pair: str = Indexed()  # "USD_LKR", "EUR_LKR", "GBP_LKR"
    base_currency: str  # "USD", "EUR", "GBP"
    target_currency: str  # "LKR"
    
    # Exchange Rate
    rate: float
    inverse_rate: float  # 1/rate
    
    # Rate Information
    rate_type: str = "spot"  # "spot", "buy", "sell", "interbank"
    source: str = "currencylayer"  # "currencylayer", "fixer", "manual"
    
    # Market Data
    bid_rate: Optional[float] = None
    ask_rate: Optional[float] = None
    spread: Optional[float] = None
    
    # Timestamps
    recorded_at: datetime = Indexed()
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "currency_rates"
        indexes = [
            "currency_pair",
            "base_currency",
            "target_currency",
            "recorded_at"
        ]

class Location(Document):
    """Geographic locations and places"""
    location_id: str = Indexed(unique=True)
    name: str = Indexed()
    
    # Geographic Information
    coordinates: Dict[str, float] = Field(..., description="Latitude and longitude")
    address: str
    city: str = Indexed()
    district: str = Indexed()
    province: str = Indexed()
    country: str = "Sri Lanka"
    
    # Location Details
    location_type: str  # "city", "district", "attraction", "landmark"
    administrative_level: int  # 1=country, 2=province, 3=district, 4=city
    
    # Geographic Boundaries
    bounds: Optional[Dict[str, Dict[str, float]]] = None  # {northeast: {lat, lng}, southwest: {lat, lng}}
    area: Optional[float] = None  # Square kilometers
    
    # Additional Information
    population: Optional[int] = None
    timezone: str = "Asia/Colombo"
    postal_codes: List[str] = []
    
    # Status
    is_active: bool = True
    is_verified: bool = False
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "locations"
        indexes = [
            "location_id",
            "name",
            "city",
            "district",
            "province",
            "location_type"
        ]

class SystemConfiguration(Document):
    """System configuration and settings"""
    config_key: str = Indexed(unique=True)
    config_value: Any
    config_type: str  # "string", "number", "boolean", "json"
    
    # Configuration Details
    description: str
    category: str  # "api", "security", "features", "limits"
    is_public: bool = False  # Can be accessed by frontend
    
    # Validation
    validation_rules: Optional[Dict[str, Any]] = None
    allowed_values: Optional[List[Any]] = None
    
    # Environment
    environment: str = "all"  # "development", "staging", "production", "all"
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "system_configurations"
        indexes = [
            "config_key",
            "category",
            "environment"
        ]

class APILog(Document):
    """API request and response logging"""
    log_id: str = Indexed(unique=True)
    
    # Request Information
    method: str
    endpoint: str
    user_id: Optional[str] = Indexed()
    session_id: Optional[str] = Indexed()
    
    # Request Details
    request_headers: Dict[str, str] = {}
    request_body: Optional[Dict[str, Any]] = None
    query_params: Dict[str, str] = {}
    
    # Response Information
    status_code: int
    response_time: float  # milliseconds
    response_size: int  # bytes
    
    # Error Information
    error_message: Optional[str] = None
    error_type: Optional[str] = None
    
    # Client Information
    ip_address: str
    user_agent: str
    country: Optional[str] = None
    city: Optional[str] = None
    
    # Timestamps
    timestamp: datetime = Indexed()
    
    class Settings:
        name = "api_logs"
        indexes = [
            "log_id",
            "user_id",
            "session_id",
            "endpoint",
            "status_code",
            "timestamp"
        ]