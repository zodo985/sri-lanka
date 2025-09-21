from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models import *
import asyncio
from app.core.config import settings

class Database:
    client: AsyncIOMotorClient = None
    database = None

db = Database()

async def connect_to_mongo():
    """Create database connection"""
    db.client = AsyncIOMotorClient(settings.mongodb_url)
    db.database = db.client[settings.database_name]
    
    # Initialize Beanie with all document models
    await init_beanie(
        database=db.database,
        document_models=[
            User,
            ChatSession,
            Message,
            TouristAttraction,
            Accommodation,
            Restaurant,
            Transportation,
            EmergencyService,
            CulturalEvent,
            Language,
            UserPreference,
            Feedback,
            Notification,
            Itinerary,
            Review,
            Location,
            WeatherData,
            CurrencyRate,
            Translation,
            VoiceMessage,
            ImageRecognition,
            Recommendation,
            Analytics
        ]
    )

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()

async def get_database():
    """Get database instance"""
    return db.database