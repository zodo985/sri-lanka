from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class Language(Document):
    """Supported languages configuration"""
    code: str = Indexed(unique=True)  # "en", "si", "ta", "de", "fr", "zh", "ja"
    name: str  # "English", "සිංහල", "தமிழ்"
    native_name: str  # "English", "සිංහල", "தமிழ்"
    
    # Language Properties
    is_rtl: bool = False  # Right-to-left
    script: str = "latin"  # "latin", "sinhala", "tamil", "chinese", "japanese"
    locale: str  # "en_US", "si_LK", "ta_LK"
    
    # Support Status
    is_active: bool = True
    is_fully_supported: bool = True
    translation_available: bool = True
    voice_support: bool = True
    
    # Language Resources
    model_name: Optional[str] = None  # spaCy model name
    dictionary_url: Optional[str] = None
    grammar_rules: Optional[Dict[str, Any]] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "languages"
        indexes = ["code", "is_active"]

class Translation(Document):
    """Translation cache and management"""
    source_text: str = Indexed()
    source_language: str = Indexed()
    target_language: str = Indexed()
    translated_text: str
    
    # Translation Metadata
    translation_provider: str  # "google", "microsoft", "custom", "cached"
    confidence_score: Optional[float] = None
    is_verified: bool = False
    verified_by: Optional[str] = None  # User ID
    
    # Context
    context: Optional[str] = None  # "tourism", "general", "emergency"
    domain: Optional[str] = None  # "attractions", "food", "transport"
    
    # Usage Statistics
    usage_count: int = 0
    last_used: Optional[datetime] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "translations"
        indexes = [
            "source_text",
            "source_language",
            "target_language",
            "translation_provider"
        ]

class ImageRecognition(Document):
    """Image recognition and analysis results"""
    image_url: str = Indexed()
    image_hash: str = Indexed(unique=True)
    
    # Recognition Results
    recognized_objects: List[Dict[str, Any]] = []  # [{"object": "temple", "confidence": 0.95, "bbox": [x, y, w, h]}]
    landmarks: List[Dict[str, Any]] = []  # [{"landmark": "Sigiriya", "confidence": 0.88, "location": {"lat": 7.9569, "lng": 80.7597}}]
    
    # Image Analysis
    dominant_colors: List[str] = []
    image_tags: List[str] = []  # ["architecture", "historical", "outdoor"]
    scene_description: Optional[str] = None
    
    # Location Information
    detected_location: Optional[Dict[str, float]] = None
    location_confidence: Optional[float] = None
    
    # Processing Information
    processing_status: str = "completed"  # pending, processing, completed, failed
    processing_time: Optional[float] = None  # seconds
    model_version: Optional[str] = None
    
    # User Information
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    processed_at: Optional[datetime] = None
    
    class Settings:
        name = "image_recognitions"
        indexes = [
            "image_url",
            "image_hash",
            "processing_status",
            "user_id"
        ]

class ContentTemplate(Document):
    """Reusable content templates for responses"""
    template_id: str = Indexed(unique=True)
    template_name: str
    category: str  # "greeting", "attraction_info", "directions", "emergency"
    
    # Template Content
    content: Dict[str, str] = {}  # {language: template_text}
    variables: List[str] = []  # ["{attraction_name}", "{distance}", "{price}"]
    
    # Usage Context
    context: Optional[str] = None
    intent: Optional[str] = None
    entity_types: List[str] = []
    
    # Template Properties
    is_active: bool = True
    priority: int = 0  # Higher priority templates are used first
    usage_count: int = 0
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "content_templates"
        indexes = [
            "template_id",
            "category",
            "is_active",
            "priority"
        ]

class FAQ(Document):
    """Frequently Asked Questions and answers"""
    question_id: str = Indexed(unique=True)
    category: str = Indexed()  # "general", "attractions", "transport", "accommodation"
    
    # Question Content
    question: Dict[str, str] = {}  # {language: question_text}
    answer: Dict[str, str] = {}  # {language: answer_text}
    
    # Question Variations
    question_variations: Dict[str, List[str]] = {}  # {language: [variation1, variation2]}
    keywords: List[str] = []
    
    # Usage Statistics
    view_count: int = 0
    helpful_count: int = 0
    not_helpful_count: int = 0
    
    # Status
    is_active: bool = True
    is_featured: bool = False
    priority: int = 0
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "faqs"
        indexes = [
            "question_id",
            "category",
            "is_active",
            "priority"
        ]