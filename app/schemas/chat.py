from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.chat import MessageType, MessageRole

class ChatSessionCreate(BaseModel):
    """Chat session creation schema"""
    language: str = "en"
    user_location: Optional[Dict[str, float]] = None
    device_info: Optional[Dict[str, str]] = None

class ChatSessionResponse(BaseModel):
    """Chat session response schema"""
    session_id: str
    user_id: Optional[str] = None
    language: str
    is_active: bool
    started_at: datetime
    last_activity: datetime
    message_count: int
    average_response_time: float
    satisfaction_score: Optional[float] = None

class MessageCreate(BaseModel):
    """Message creation schema"""
    content: str = Field(..., min_length=1, max_length=2000)
    message_type: MessageType = MessageType.TEXT
    language: Optional[str] = None
    location: Optional[Dict[str, float]] = None
    attachments: Optional[List[Dict[str, Any]]] = None

class MessageResponse(BaseModel):
    """Message response schema"""
    message_id: str
    session_id: str
    content: str
    message_type: MessageType
    role: MessageRole
    original_language: str
    detected_language: Optional[str] = None
    translated_content: Optional[Dict[str, str]] = None
    timestamp: datetime
    processing_time: Optional[float] = None
    intent: Optional[str] = None
    entities: List[Dict[str, Any]] = []
    confidence: Optional[float] = None
    sentiment: Optional[str] = None
    response_type: Optional[str] = None
    quick_replies: Optional[List[Dict[str, str]]] = None
    attachments: Optional[List[Dict[str, Any]]] = None
    is_read: bool
    user_feedback: Optional[str] = None

class ChatResponse(BaseModel):
    """Complete chat response schema"""
    session: ChatSessionResponse
    messages: List[MessageResponse]
    suggestions: Optional[List[str]] = None
    quick_replies: Optional[List[Dict[str, str]]] = None

class VoiceMessageCreate(BaseModel):
    """Voice message creation schema"""
    audio_data: str  # Base64 encoded audio
    audio_format: str = "wav"
    language: Optional[str] = None

class VoiceMessageResponse(BaseModel):
    """Voice message response schema"""
    message_id: str
    session_id: str
    transcription: str
    transcription_confidence: float
    language_detected: str
    processing_status: str
    audio_url: Optional[str] = None
    created_at: datetime
    processed_at: Optional[datetime] = None

class QuickReply(BaseModel):
    """Quick reply schema"""
    title: str
    payload: str
    image_url: Optional[str] = None

class CarouselItem(BaseModel):
    """Carousel item schema"""
    title: str
    subtitle: str
    image_url: Optional[str] = None
    buttons: List[Dict[str, str]] = []

class ChatSuggestion(BaseModel):
    """Chat suggestion schema"""
    text: str
    type: str = "text"  # "text", "location", "quick_reply"
    payload: Optional[str] = None