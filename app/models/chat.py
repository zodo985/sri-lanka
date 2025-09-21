from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class MessageType(str, Enum):
    TEXT = "text"
    VOICE = "voice"
    IMAGE = "image"
    LOCATION = "location"
    QUICK_REPLY = "quick_reply"
    CAROUSEL = "carousel"
    BUTTON = "button"

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatSession(Document):
    """Chat session between user and chatbot"""
    user_id: Optional[str] = Indexed()
    session_id: str = Indexed(unique=True)
    
    # Session Information
    language: str = "en"
    is_active: bool = True
    started_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None
    
    # Context & State
    current_intent: Optional[str] = None
    current_entities: Dict[str, Any] = {}
    conversation_context: Dict[str, Any] = {}
    
    # User Information
    user_location: Optional[Dict[str, float]] = None  # {lat, lng}
    user_preferences: Dict[str, Any] = {}
    
    # Session Metadata
    device_info: Optional[Dict[str, str]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    
    # Analytics
    message_count: int = 0
    average_response_time: float = 0.0
    satisfaction_score: Optional[float] = None
    
    class Settings:
        name = "chat_sessions"
        indexes = [
            "user_id",
            "session_id",
            "is_active",
            "started_at"
        ]

class Message(Document):
    """Individual message in a chat session"""
    session_id: str = Indexed()
    message_id: str = Indexed(unique=True)
    
    # Message Content
    content: str
    message_type: MessageType = MessageType.TEXT
    role: MessageRole
    
    # Language & Translation
    original_language: str = "en"
    detected_language: Optional[str] = None
    translated_content: Optional[Dict[str, str]] = {}  # {language: content}
    
    # Metadata
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    processing_time: Optional[float] = None  # milliseconds
    
    # NLP Information
    intent: Optional[str] = None
    entities: List[Dict[str, Any]] = []
    confidence: Optional[float] = None
    sentiment: Optional[str] = None
    
    # Response Information (for assistant messages)
    response_type: Optional[str] = None  # "text", "quick_reply", "carousel"
    quick_replies: Optional[List[Dict[str, str]]] = None
    attachments: Optional[List[Dict[str, Any]]] = None
    
    # User Interaction
    is_read: bool = False
    user_feedback: Optional[str] = None  # "helpful", "not_helpful", "inaccurate"
    
    # References
    parent_message_id: Optional[str] = None
    referenced_attractions: List[str] = []  # Attraction IDs
    referenced_services: List[str] = []  # Service IDs
    
    class Settings:
        name = "messages"
        indexes = [
            "session_id",
            "message_id",
            "timestamp",
            "role",
            "intent"
        ]

class VoiceMessage(Document):
    """Voice message with audio processing data"""
    message_id: str = Indexed(unique=True)
    session_id: str = Indexed()
    
    # Audio Information
    audio_url: str
    audio_duration: float  # seconds
    audio_format: str  # "wav", "mp3", "ogg"
    sample_rate: int
    channels: int
    
    # Transcription
    transcription: str
    transcription_confidence: float
    language_detected: str
    
    # Processing
    processing_status: str = "pending"  # pending, processing, completed, failed
    error_message: Optional[str] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    processed_at: Optional[datetime] = None
    
    class Settings:
        name = "voice_messages"
        indexes = [
            "message_id",
            "session_id",
            "processing_status"
        ]