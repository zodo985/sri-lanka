from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, List
from datetime import datetime

class ErrorResponse(BaseModel):
    """Standard error response format"""
    success: bool = False
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SuccessResponse(BaseModel):
    """Standard success response format"""
    success: bool = True
    message: str
    data: Optional[Any] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = Field(1, ge=1, description="Page number")
    limit: int = Field(10, ge=1, le=100, description="Items per page")
    sort_by: Optional[str] = None
    sort_order: str = "asc"  # "asc" or "desc"

class PaginatedResponse(BaseModel):
    """Paginated response format"""
    success: bool = True
    data: List[Any]
    pagination: Dict[str, Any] = {
        "page": 1,
        "limit": 10,
        "total": 0,
        "pages": 0,
        "has_next": False,
        "has_prev": False
    }
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class LocationData(BaseModel):
    """Location data structure"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    address: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    country: str = "Sri Lanka"

class LanguageData(BaseModel):
    """Language data structure"""
    code: str
    name: str
    native_name: str
    is_rtl: bool = False

class MediaData(BaseModel):
    """Media data structure"""
    url: str
    type: str  # "image", "video", "audio"
    caption: Optional[str] = None
    alt_text: Optional[str] = None