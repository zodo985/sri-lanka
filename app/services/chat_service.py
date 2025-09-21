import asyncio
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from app.models.chat import ChatSession, Message, VoiceMessage
from app.models.tourism import TouristAttraction, Restaurant, Accommodation
from app.services.nlp_service import NLPService
from app.services.translation_service import TranslationService
from app.services.recommendation_service import RecommendationService

class ChatService:
    """Chat service for handling conversations and responses"""
    
    def __init__(self):
        self.nlp_service = NLPService()
        self.translation_service = TranslationService()
        self.recommendation_service = RecommendationService()
    
    async def generate_response(
        self,
        session_id: str,
        user_message: str,
        intent: Optional[str] = None,
        entities: List[Dict[str, Any]] = None,
        language: str = "en"
    ) -> Dict[str, Any]:
        """Generate AI response based on user message"""
        try:
            entities = entities or []
            
            # Handle different intents
            if intent == "greeting":
                return await self._handle_greeting(language)
            elif intent == "attraction_search":
                return await self._handle_attraction_search(entities, language)
            elif intent == "restaurant_search":
                return await self._handle_restaurant_search(entities, language)
            elif intent == "accommodation_search":
                return await self._handle_accommodation_search(entities, language)
            elif intent == "transportation_info":
                return await self._handle_transportation_info(entities, language)
            elif intent == "emergency_help":
                return await self._handle_emergency_help(entities, language)
            elif intent == "weather_info":
                return await self._handle_weather_info(entities, language)
            elif intent == "currency_info":
                return await self._handle_currency_info(entities, language)
            elif intent == "cultural_info":
                return await self._handle_cultural_info(entities, language)
            else:
                return await self._handle_general_query(user_message, language)
                
        except Exception as e:
            return {
                "content": f"I apologize, but I encountered an error processing your request. Please try again.",
                "response_type": "text"
            }
    
    async def _handle_greeting(self, language: str) -> Dict[str, Any]:
        """Handle greeting intent"""
        greetings = {
            "en": "Hello! Welcome to Sri Lanka Tourism Assistant. How can I help you today?",
            "si": "ආයුබෝවන්! ශ්‍රී ලංකා සංචාරක සහායකයට සාදරයෙන් පිළිගනිමු. අද මට ඔබට කෙසේ උදව් කළ හැකිද?",
            "ta": "வணக்கம்! இலங்கை சுற்றுலா உதவியாளருக்கு வரவேற்கிறோம். இன்று உங்களுக்கு எவ்வாறு உதவ முடியும்?"
        }
        
        content = greetings.get(language, greetings["en"])
        
        quick_replies = [
            {"title": "Tourist Attractions", "payload": "attractions"},
            {"title": "Food & Restaurants", "payload": "restaurants"},
            {"title": "Accommodation", "payload": "accommodation"},
            {"title": "Transportation", "payload": "transportation"}
        ]
        
        return {
            "content": content,
            "response_type": "text",
            "quick_replies": quick_replies
        }
    
    async def _handle_attraction_search(self, entities: List[Dict[str, Any]], language: str) -> Dict[str, Any]:
        """Handle attraction search intent"""
        try:
            # Extract search parameters from entities
            attraction_type = None
            location = None
            district = None
            
            for entity in entities:
                if entity.get("entity") == "attraction_type":
                    attraction_type = entity.get("value")
                elif entity.get("entity") == "location":
                    location = entity.get("value")
                elif entity.get("entity") == "district":
                    district = entity.get("value")
            
            # Search attractions
            query = {}
            if attraction_type:
                query["attraction_type"] = attraction_type
            if district:
                query["district"] = district
            
            attractions = await TouristAttraction.find(query).limit(5).to_list()
            
            if not attractions:
                return {
                    "content": "I couldn't find any attractions matching your criteria. Please try a different search.",
                    "response_type": "text"
                }
            
            # Create carousel response
            carousel_items = []
            for attraction in attractions:
                carousel_items.append({
                    "title": attraction.name,
                    "subtitle": f"{attraction.district}, {attraction.province}",
                    "image_url": attraction.images[0] if attraction.images else None,
                    "buttons": [
                        {"title": "View Details", "payload": f"attraction_details_{attraction.id}"},
                        {"title": "Get Directions", "payload": f"directions_{attraction.id}"}
                    ]
                })
            
            return {
                "content": f"Here are some attractions I found for you:",
                "response_type": "carousel",
                "attachments": carousel_items
            }
            
        except Exception as e:
            return {
                "content": "I apologize, but I couldn't search for attractions at the moment. Please try again later.",
                "response_type": "text"
            }
    
    async def _handle_restaurant_search(self, entities: List[Dict[str, Any]], language: str) -> Dict[str, Any]:
        """Handle restaurant search intent"""
        try:
            # Extract search parameters
            cuisine_type = None
            location = None
            district = None
            
            for entity in entities:
                if entity.get("entity") == "cuisine_type":
                    cuisine_type = entity.get("value")
                elif entity.get("entity") == "location":
                    location = entity.get("value")
                elif entity.get("entity") == "district":
                    district = entity.get("value")
            
            # Search restaurants
            query = {}
            if cuisine_type:
                query["cuisine_types"] = cuisine_type
            if district:
                query["district"] = district
            
            restaurants = await Restaurant.find(query).limit(5).to_list()
            
            if not restaurants:
                return {
                    "content": "I couldn't find any restaurants matching your criteria. Please try a different search.",
                    "response_type": "text"
                }
            
            # Create carousel response
            carousel_items = []
            for restaurant in restaurants:
                carousel_items.append({
                    "title": restaurant.name,
                    "subtitle": f"{', '.join(restaurant.cuisine_types)} • {restaurant.price_range}",
                    "image_url": restaurant.images[0] if restaurant.images else None,
                    "buttons": [
                        {"title": "View Menu", "payload": f"restaurant_menu_{restaurant.id}"},
                        {"title": "Get Directions", "payload": f"directions_{restaurant.id}"}
                    ]
                })
            
            return {
                "content": f"Here are some restaurants I found for you:",
                "response_type": "carousel",
                "attachments": carousel_items
            }
            
        except Exception as e:
            return {
                "content": "I apologize, but I couldn't search for restaurants at the moment. Please try again later.",
                "response_type": "text"
            }
    
    async def _handle_accommodation_search(self, entities: List[Dict[str, Any]], language: str) -> Dict[str, Any]:
        """Handle accommodation search intent"""
        try:
            # Extract search parameters
            accommodation_type = None
            location = None
            district = None
            
            for entity in entities:
                if entity.get("entity") == "accommodation_type":
                    accommodation_type = entity.get("value")
                elif entity.get("entity") == "location":
                    location = entity.get("value")
                elif entity.get("entity") == "district":
                    district = entity.get("value")
            
            # Search accommodations
            query = {}
            if accommodation_type:
                query["accommodation_type"] = accommodation_type
            if district:
                query["district"] = district
            
            accommodations = await Accommodation.find(query).limit(5).to_list()
            
            if not accommodations:
                return {
                    "content": "I couldn't find any accommodations matching your criteria. Please try a different search.",
                    "response_type": "text"
                }
            
            # Create carousel response
            carousel_items = []
            for accommodation in accommodations:
                carousel_items.append({
                    "title": accommodation.name,
                    "subtitle": f"{accommodation.accommodation_type.title()} • {accommodation.district}",
                    "image_url": accommodation.images[0] if accommodation.images else None,
                    "buttons": [
                        {"title": "View Details", "payload": f"accommodation_details_{accommodation.id}"},
                        {"title": "Check Availability", "payload": f"availability_{accommodation.id}"}
                    ]
                })
            
            return {
                "content": f"Here are some accommodations I found for you:",
                "response_type": "carousel",
                "attachments": carousel_items
            }
            
        except Exception as e:
            return {
                "content": "I apologize, but I couldn't search for accommodations at the moment. Please try again later.",
                "response_type": "text"
            }
    
    async def _handle_transportation_info(self, entities: List[Dict[str, Any]], language: str) -> Dict[str, Any]:
        """Handle transportation information intent"""
        content = "Here's information about transportation in Sri Lanka:\n\n"
        content += "🚌 **Buses**: Affordable public transport connecting major cities\n"
        content += "🚂 **Trains**: Scenic routes, especially the hill country line\n"
        content += "🚕 **Taxis**: Available in cities, can be booked via apps\n"
        content += "🛺 **Tuk-tuks**: Three-wheelers, great for short distances\n"
        content += "🚗 **Rental Cars**: Available at airports and major cities\n\n"
        content += "Would you like specific information about any of these options?"
        
        quick_replies = [
            {"title": "Bus Routes", "payload": "bus_routes"},
            {"title": "Train Schedules", "payload": "train_schedules"},
            {"title": "Taxi Booking", "payload": "taxi_booking"},
            {"title": "Rental Cars", "payload": "rental_cars"}
        ]
        
        return {
            "content": content,
            "response_type": "text",
            "quick_replies": quick_replies
        }
    
    async def _handle_emergency_help(self, entities: List[Dict[str, Any]], language: str) -> Dict[str, Any]:
        """Handle emergency help intent"""
        content = "🚨 **Emergency Contacts in Sri Lanka:**\n\n"
        content += "**Police**: 119\n"
        content += "**Ambulance**: 110\n"
        content += "**Fire Department**: 110\n"
        content += "**Tourist Police**: +94 11 242 1052\n\n"
        content += "**Tourist Hotline**: 1912\n"
        content += "**Emergency Services**: 1990\n\n"
        content += "Stay safe! Is there anything specific you need help with?"
        
        return {
            "content": content,
            "response_type": "text"
        }
    
    async def _handle_weather_info(self, entities: List[Dict[str, Any]], language: str) -> Dict[str, Any]:
        """Handle weather information intent"""
        content = "I can provide current weather information for any location in Sri Lanka. "
        content += "The weather varies by region - coastal areas are generally warm and humid, "
        content += "while hill stations like Nuwara Eliya can be cooler.\n\n"
        content += "Which city or area would you like weather information for?"
        
        return {
            "content": content,
            "response_type": "text"
        }
    
    async def _handle_currency_info(self, entities: List[Dict[str, Any]], language: str) -> Dict[str, Any]:
        """Handle currency information intent"""
        content = "💰 **Currency Information:**\n\n"
        content += "**Sri Lankan Rupee (LKR)** is the local currency.\n"
        content += "**Exchange Rate**: Approximately 1 USD = 320 LKR (varies)\n\n"
        content += "**Where to Exchange**:\n"
        content += "• Banks (best rates)\n"
        content += "• Licensed money changers\n"
        content += "• Hotels (convenient but lower rates)\n"
        content += "• ATMs (withdrawal in local currency)\n\n"
        content += "**Payment Methods**:\n"
        content += "• Cash is widely accepted\n"
        content += "• Credit cards in major establishments\n"
        content += "• Mobile payments (eZ Cash, FriMi)"
        
        return {
            "content": content,
            "response_type": "text"
        }
    
    async def _handle_cultural_info(self, entities: List[Dict[str, Any]], language: str) -> Dict[str, Any]:
        """Handle cultural information intent"""
        content = "🏛️ **Sri Lankan Culture & Customs:**\n\n"
        content += "**Dress Code**:\n"
        content += "• Modest clothing when visiting temples\n"
        content += "• Remove shoes and hats at religious sites\n"
        content += "• Cover shoulders and knees\n\n"
        content += "**Cultural Etiquette**:\n"
        content += "• Use right hand for eating and giving\n"
        content += "• Remove shoes before entering homes\n"
        content += "• Don't point with your finger\n"
        content += "• Respect local customs and traditions\n\n"
        content += "**Festivals**:\n"
        content += "• Sinhala & Tamil New Year (April)\n"
        content += "• Vesak (May) - Buddhist festival\n"
        content += "• Kandy Esala Perahera (July/August)"
        
        return {
            "content": content,
            "response_type": "text"
        }
    
    async def _handle_general_query(self, user_message: str, language: str) -> Dict[str, Any]:
        """Handle general queries"""
        content = "I understand you're asking about: " + user_message + "\n\n"
        content += "I can help you with:\n"
        content += "• Tourist attractions and places to visit\n"
        content += "• Food and restaurant recommendations\n"
        content += "• Accommodation options\n"
        content += "• Transportation information\n"
        content += "• Cultural information and customs\n"
        content += "• Emergency contacts\n"
        content += "• Weather and currency information\n\n"
        content += "Could you be more specific about what you'd like to know?"
        
        quick_replies = [
            {"title": "Tourist Attractions", "payload": "attractions"},
            {"title": "Food & Restaurants", "payload": "restaurants"},
            {"title": "Accommodation", "payload": "accommodation"},
            {"title": "Transportation", "payload": "transportation"}
        ]
        
        return {
            "content": content,
            "response_type": "text",
            "quick_replies": quick_replies
        }
    
    async def process_voice_message(
        self,
        voice_message_id: str,
        audio_data: str,
        audio_format: str,
        language: str
    ):
        """Process voice message (placeholder implementation)"""
        try:
            # In a real implementation, you would:
            # 1. Save audio file
            # 2. Convert to speech-to-text
            # 3. Process the transcription
            # 4. Update the voice message record
            
            # For now, just update the status
            voice_message = await VoiceMessage.find_one(VoiceMessage.message_id == voice_message_id)
            if voice_message:
                voice_message.processing_status = "completed"
                voice_message.transcription = "Voice message processed successfully"
                voice_message.transcription_confidence = 0.95
                voice_message.processed_at = datetime.utcnow()
                await voice_message.save()
                
        except Exception as e:
            # Update status to failed
            voice_message = await VoiceMessage.find_one(VoiceMessage.message_id == voice_message_id)
            if voice_message:
                voice_message.processing_status = "failed"
                voice_message.error_message = str(e)
                await voice_message.save()
    
    async def update_session_analytics(self, session_id: str):
        """Update session analytics (placeholder implementation)"""
        try:
            # Update session metrics, response times, etc.
            session = await ChatSession.find_one(ChatSession.session_id == session_id)
            if session:
                # Calculate average response time
                messages = await Message.find(
                    Message.session_id == session_id,
                    Message.role == "assistant"
                ).to_list()
                
                if messages:
                    total_time = sum(msg.processing_time or 0 for msg in messages)
                    session.average_response_time = total_time / len(messages)
                    await session.save()
                    
        except Exception as e:
            # Log error but don't raise
            pass