from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import List, Optional
from datetime import datetime
import uuid
from app.core.database import get_database
from app.models.chat import ChatSession, Message, MessageType, MessageRole
from app.models.user import User
from app.schemas.chat import (
    ChatSessionCreate, ChatSessionResponse, MessageCreate, 
    MessageResponse, ChatResponse, VoiceMessageCreate, VoiceMessageResponse
)
from app.schemas.common import SuccessResponse, PaginatedResponse, PaginationParams
from app.core.exceptions import NotFoundException, ValidationException
from app.services.chat_service import ChatService
from app.services.nlp_service import NLPService
from app.services.translation_service import TranslationService

router = APIRouter()

# Initialize services
chat_service = ChatService()
nlp_service = NLPService()
translation_service = TranslationService()

@router.post("/sessions", response_model=ChatSessionResponse)
async def create_chat_session(session_data: ChatSessionCreate):
    """Create a new chat session"""
    try:
        session_id = str(uuid.uuid4())
        
        session = ChatSession(
            session_id=session_id,
            language=session_data.language,
            user_location=session_data.user_location,
            device_info=session_data.device_info
        )
        
        await session.insert()
        
        return ChatSessionResponse(
            session_id=session.session_id,
            language=session.language,
            is_active=session.is_active,
            started_at=session.started_at,
            last_activity=session.last_activity,
            message_count=session.message_count,
            average_response_time=session.average_response_time,
            satisfaction_score=session.satisfaction_score
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create chat session: {str(e)}"
        )

@router.get("/sessions/{session_id}", response_model=ChatResponse)
async def get_chat_session(session_id: str):
    """Get chat session with messages"""
    try:
        # Get session
        session = await ChatSession.find_one(ChatSession.session_id == session_id)
        if not session:
            raise NotFoundException("Chat session not found")
        
        # Get messages
        messages = await Message.find(
            Message.session_id == session_id
        ).sort("timestamp").to_list()
        
        # Convert to response format
        message_responses = []
        for msg in messages:
            message_responses.append(MessageResponse(
                message_id=msg.message_id,
                session_id=msg.session_id,
                content=msg.content,
                message_type=msg.message_type,
                role=msg.role,
                original_language=msg.original_language,
                detected_language=msg.detected_language,
                translated_content=msg.translated_content,
                timestamp=msg.timestamp,
                processing_time=msg.processing_time,
                intent=msg.intent,
                entities=msg.entities,
                confidence=msg.confidence,
                sentiment=msg.sentiment,
                response_type=msg.response_type,
                quick_replies=msg.quick_replies,
                attachments=msg.attachments,
                is_read=msg.is_read,
                user_feedback=msg.user_feedback
            ))
        
        session_response = ChatSessionResponse(
            session_id=session.session_id,
            language=session.language,
            is_active=session.is_active,
            started_at=session.started_at,
            last_activity=session.last_activity,
            message_count=session.message_count,
            average_response_time=session.average_response_time,
            satisfaction_score=session.satisfaction_score
        )
        
        return ChatResponse(
            session=session_response,
            messages=message_responses
        )
        
    except NotFoundException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get chat session: {str(e)}"
        )

@router.post("/sessions/{session_id}/messages", response_model=MessageResponse)
async def send_message(
    session_id: str, 
    message_data: MessageCreate,
    background_tasks: BackgroundTasks
):
    """Send a message in a chat session"""
    try:
        # Get session
        session = await ChatSession.find_one(ChatSession.session_id == session_id)
        if not session:
            raise NotFoundException("Chat session not found")
        
        # Detect language if not provided
        detected_language = message_data.language
        if not detected_language:
            detected_language = await nlp_service.detect_language(message_data.content)
        
        # Process message with NLP
        nlp_result = await nlp_service.process_message(
            message_data.content,
            detected_language,
            session.language
        )
        
        # Create user message
        user_message = Message(
            message_id=str(uuid.uuid4()),
            session_id=session_id,
            content=message_data.content,
            message_type=message_data.message_type,
            role=MessageRole.USER,
            original_language=detected_language,
            detected_language=detected_language,
            intent=nlp_result.get("intent"),
            entities=nlp_result.get("entities", []),
            confidence=nlp_result.get("confidence"),
            sentiment=nlp_result.get("sentiment"),
            attachments=message_data.attachments
        )
        
        await user_message.insert()
        
        # Generate AI response
        ai_response = await chat_service.generate_response(
            session_id=session_id,
            user_message=message_data.content,
            intent=nlp_result.get("intent"),
            entities=nlp_result.get("entities", []),
            language=session.language
        )
        
        # Create AI message
        ai_message = Message(
            message_id=str(uuid.uuid4()),
            session_id=session_id,
            content=ai_response["content"],
            message_type=MessageType.TEXT,
            role=MessageRole.ASSISTANT,
            original_language=session.language,
            response_type=ai_response.get("response_type"),
            quick_replies=ai_response.get("quick_replies"),
            attachments=ai_response.get("attachments")
        )
        
        await ai_message.insert()
        
        # Update session
        session.message_count += 2
        session.last_activity = datetime.utcnow()
        await session.save()
        
        # Process background tasks
        background_tasks.add_task(
            chat_service.update_session_analytics,
            session_id
        )
        
        return MessageResponse(
            message_id=ai_message.message_id,
            session_id=ai_message.session_id,
            content=ai_message.content,
            message_type=ai_message.message_type,
            role=ai_message.role,
            original_language=ai_message.original_language,
            response_type=ai_message.response_type,
            quick_replies=ai_message.quick_replies,
            attachments=ai_message.attachments,
            timestamp=ai_message.timestamp,
            is_read=False
        )
        
    except NotFoundException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send message: {str(e)}"
        )

@router.post("/sessions/{session_id}/voice", response_model=VoiceMessageResponse)
async def process_voice_message(
    session_id: str,
    voice_data: VoiceMessageCreate,
    background_tasks: BackgroundTasks
):
    """Process voice message and return transcription"""
    try:
        # Get session
        session = await ChatSession.find_one(ChatSession.session_id == session_id)
        if not session:
            raise NotFoundException("Chat session not found")
        
        # Process voice message in background
        voice_message_id = str(uuid.uuid4())
        
        # Create voice message record
        voice_message = VoiceMessage(
            message_id=voice_message_id,
            session_id=session_id,
            audio_url="",  # Will be updated after processing
            audio_duration=0.0,
            audio_format=voice_data.audio_format,
            sample_rate=16000,  # Default
            channels=1,  # Default
            transcription="",
            transcription_confidence=0.0,
            language_detected=voice_data.language or session.language,
            processing_status="processing"
        )
        
        await voice_message.insert()
        
        # Process in background
        background_tasks.add_task(
            chat_service.process_voice_message,
            voice_message_id,
            voice_data.audio_data,
            voice_data.audio_format,
            voice_data.language or session.language
        )
        
        return VoiceMessageResponse(
            message_id=voice_message_id,
            session_id=session_id,
            transcription="",
            transcription_confidence=0.0,
            language_detected=voice_message.language_detected,
            processing_status="processing",
            created_at=voice_message.created_at
        )
        
    except NotFoundException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process voice message: {str(e)}"
        )

@router.get("/sessions/{session_id}/messages", response_model=PaginatedResponse)
async def get_messages(
    session_id: str,
    pagination: PaginationParams = Depends()
):
    """Get messages for a chat session with pagination"""
    try:
        # Get session
        session = await ChatSession.find_one(ChatSession.session_id == session_id)
        if not session:
            raise NotFoundException("Chat session not found")
        
        # Get messages with pagination
        skip = (pagination.page - 1) * pagination.limit
        messages = await Message.find(
            Message.session_id == session_id
        ).sort("timestamp", -1).skip(skip).limit(pagination.limit).to_list()
        
        # Get total count
        total_count = await Message.find(Message.session_id == session_id).count()
        
        # Convert to response format
        message_responses = []
        for msg in messages:
            message_responses.append(MessageResponse(
                message_id=msg.message_id,
                session_id=msg.session_id,
                content=msg.content,
                message_type=msg.message_type,
                role=msg.role,
                original_language=msg.original_language,
                detected_language=msg.detected_language,
                translated_content=msg.translated_content,
                timestamp=msg.timestamp,
                processing_time=msg.processing_time,
                intent=msg.intent,
                entities=msg.entities,
                confidence=msg.confidence,
                sentiment=msg.sentiment,
                response_type=msg.response_type,
                quick_replies=msg.quick_replies,
                attachments=msg.attachments,
                is_read=msg.is_read,
                user_feedback=msg.user_feedback
            ))
        
        # Calculate pagination info
        total_pages = (total_count + pagination.limit - 1) // pagination.limit
        has_next = pagination.page < total_pages
        has_prev = pagination.page > 1
        
        return PaginatedResponse(
            data=message_responses,
            pagination={
                "page": pagination.page,
                "limit": pagination.limit,
                "total": total_count,
                "pages": total_pages,
                "has_next": has_next,
                "has_prev": has_prev
            }
        )
        
    except NotFoundException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get messages: {str(e)}"
        )

@router.put("/sessions/{session_id}/end", response_model=SuccessResponse)
async def end_chat_session(session_id: str):
    """End a chat session"""
    try:
        # Get session
        session = await ChatSession.find_one(ChatSession.session_id == session_id)
        if not session:
            raise NotFoundException("Chat session not found")
        
        # Update session
        session.is_active = False
        session.ended_at = datetime.utcnow()
        await session.save()
        
        return SuccessResponse(
            message="Chat session ended successfully"
        )
        
    except NotFoundException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to end chat session: {str(e)}"
        )