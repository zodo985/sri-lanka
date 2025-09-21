#!/usr/bin/env python3
"""
Seed data script for Sri Lanka Tourism Chatbot
This script populates the database with initial data for attractions, restaurants, accommodations, etc.
"""

import asyncio
import sys
import os
from datetime import datetime, date
from typing import List, Dict, Any

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.core.database import connect_to_mongo
from app.models import *

async def seed_languages():
    """Seed supported languages"""
    print("Seeding languages...")
    
    languages = [
        {
            "code": "en",
            "name": "English",
            "native_name": "English",
            "is_rtl": False,
            "script": "latin",
            "locale": "en_US",
            "is_active": True,
            "is_fully_supported": True,
            "translation_available": True,
            "voice_support": True
        },
        {
            "code": "si",
            "name": "Sinhala",
            "native_name": "සිංහල",
            "is_rtl": False,
            "script": "sinhala",
            "locale": "si_LK",
            "is_active": True,
            "is_fully_supported": True,
            "translation_available": True,
            "voice_support": True
        },
        {
            "code": "ta",
            "name": "Tamil",
            "native_name": "தமிழ்",
            "is_rtl": False,
            "script": "tamil",
            "locale": "ta_LK",
            "is_active": True,
            "is_fully_supported": True,
            "translation_available": True,
            "voice_support": True
        },
        {
            "code": "de",
            "name": "German",
            "native_name": "Deutsch",
            "is_rtl": False,
            "script": "latin",
            "locale": "de_DE",
            "is_active": True,
            "is_fully_supported": True,
            "translation_available": True,
            "voice_support": True
        },
        {
            "code": "fr",
            "name": "French",
            "native_name": "Français",
            "is_rtl": False,
            "script": "latin",
            "locale": "fr_FR",
            "is_active": True,
            "is_fully_supported": True,
            "translation_available": True,
            "voice_support": True
        },
        {
            "code": "zh",
            "name": "Chinese",
            "native_name": "中文",
            "is_rtl": False,
            "script": "chinese",
            "locale": "zh_CN",
            "is_active": True,
            "is_fully_supported": True,
            "translation_available": True,
            "voice_support": True
        },
        {
            "code": "ja",
            "name": "Japanese",
            "native_name": "日本語",
            "is_rtl": False,
            "script": "japanese",
            "locale": "ja_JP",
            "is_active": True,
            "is_fully_supported": True,
            "translation_available": True,
            "voice_support": True
        }
    ]
    
    for lang_data in languages:
        existing = await Language.find_one(Language.code == lang_data["code"])
        if not existing:
            language = Language(**lang_data)
            await language.insert()
            print(f"  ✓ Added language: {lang_data['name']}")

async def seed_tourist_attractions():
    """Seed tourist attractions"""
    print("Seeding tourist attractions...")
    
    attractions = [
        {
            "name": "Sigiriya Rock Fortress",
            "name_sinhala": "සීගිරිය ගල් කොටුව",
            "name_tamil": "சிகிரியா கல் கோட்டை",
            "description": "Ancient rock fortress and UNESCO World Heritage Site with stunning frescoes and panoramic views.",
            "description_sinhala": "පුරාණ ගල් කොටුවක් සහ යුනෙස්කෝ ලෝක උරුම අඩවියක් වන අතර අලංකාර චිත්ර සහ විශ්වීය දර්ශන ඇත.",
            "description_tamil": "பண்டைய கல் கோட்டை மற்றும் யுனெஸ்கோ உலக பாரம்பரிய தளம், அழகிய சித்திரங்கள் மற்றும் பரந்த தோற்றங்களுடன்.",
            "location": {"latitude": 7.9569, "longitude": 80.7597},
            "address": "Sigiriya, Central Province, Sri Lanka",
            "district": "Matale",
            "province": "Central",
            "attraction_type": "historical",
            "tags": ["unesco", "historical", "archaeological", "frescoes"],
            "difficulty_level": "moderate",
            "opening_hours": {
                "monday": "7:00-19:00",
                "tuesday": "7:00-19:00",
                "wednesday": "7:00-19:00",
                "thursday": "7:00-19:00",
                "friday": "7:00-19:00",
                "saturday": "7:00-19:00",
                "sunday": "7:00-19:00"
            },
            "entrance_fee": {"adult": 5000, "child": 2500, "foreign_adult": 30, "foreign_child": 15},
            "best_time_to_visit": ["morning", "evening"],
            "duration_visit": 180,
            "images": [
                "https://example.com/sigiriya1.jpg",
                "https://example.com/sigiriya2.jpg"
            ],
            "wheelchair_accessible": False,
            "parking_available": True,
            "public_transport": True,
            "contact_phone": "+94 66 2 234 226",
            "website": "https://www.sigiriya.lk",
            "average_rating": 4.8,
            "total_reviews": 1250,
            "popularity_score": 0.95,
            "is_active": True,
            "is_featured": True
        },
        {
            "name": "Temple of the Sacred Tooth Relic",
            "name_sinhala": "ශ්‍රී දළදා මාලිගාව",
            "name_tamil": "புனித பல் சின்னம் கோவில்",
            "description": "Sacred Buddhist temple housing the tooth relic of Buddha, located in Kandy.",
            "description_sinhala": "බුදුන්ගේ දළදා වන්දනාව තබා ඇති පූජනීය බෞද්ධ විහාරය, මහනුවර පිහිටා ඇත.",
            "description_tamil": "புத்தரின் புனித பல் சின்னம் வைக்கப்பட்டுள்ள புனித பௌத்த கோவில், கண்டியில் அமைந்துள்ளது.",
            "location": {"latitude": 7.2945, "longitude": 80.6414},
            "address": "Sri Dalada Veediya, Kandy, Sri Lanka",
            "district": "Kandy",
            "province": "Central",
            "attraction_type": "religious",
            "tags": ["temple", "buddhist", "sacred", "unesco"],
            "difficulty_level": "easy",
            "opening_hours": {
                "monday": "5:30-20:00",
                "tuesday": "5:30-20:00",
                "wednesday": "5:30-20:00",
                "thursday": "5:30-20:00",
                "friday": "5:30-20:00",
                "saturday": "5:30-20:00",
                "sunday": "5:30-20:00"
            },
            "entrance_fee": {"adult": 1000, "child": 500},
            "best_time_to_visit": ["morning", "evening"],
            "duration_visit": 120,
            "images": [
                "https://example.com/tooth_temple1.jpg",
                "https://example.com/tooth_temple2.jpg"
            ],
            "wheelchair_accessible": True,
            "parking_available": True,
            "public_transport": True,
            "contact_phone": "+94 81 2 234 226",
            "average_rating": 4.7,
            "total_reviews": 2100,
            "popularity_score": 0.92,
            "is_active": True,
            "is_featured": True
        },
        {
            "name": "Yala National Park",
            "name_sinhala": "යාල ජාතික වනෝද්යානය",
            "name_tamil": "யாலா தேசிய பூங்கா",
            "description": "Famous wildlife sanctuary known for leopards, elephants, and diverse bird species.",
            "description_sinhala": "කොටියන්, අලින් සහ විවිධ පක්ෂි වර්ග සඳහා ප්‍රසිද්ධ වන සතුන් සඳහා ප්‍රසිද්ධ වනෝද්යානය.",
            "description_tamil": "சிறுத்தைகள், யானைகள் மற்றும் பல்வேறு பறவை இனங்களுக்கு பிரபலமான வனவிலங்கு சரணாலயம்.",
            "location": {"latitude": 6.3725, "longitude": 81.5244},
            "address": "Yala National Park, Southern Province, Sri Lanka",
            "district": "Hambantota",
            "province": "Southern",
            "attraction_type": "wildlife",
            "tags": ["national_park", "wildlife", "leopards", "elephants", "safari"],
            "difficulty_level": "easy",
            "opening_hours": {
                "monday": "6:00-18:00",
                "tuesday": "6:00-18:00",
                "wednesday": "6:00-18:00",
                "thursday": "6:00-18:00",
                "friday": "6:00-18:00",
                "saturday": "6:00-18:00",
                "sunday": "6:00-18:00"
            },
            "entrance_fee": {"adult": 2000, "child": 1000, "foreign_adult": 15, "foreign_child": 8},
            "best_time_to_visit": ["morning", "evening"],
            "duration_visit": 240,
            "images": [
                "https://example.com/yala1.jpg",
                "https://example.com/yala2.jpg"
            ],
            "wheelchair_accessible": False,
            "parking_available": True,
            "public_transport": False,
            "contact_phone": "+94 47 2 234 226",
            "average_rating": 4.6,
            "total_reviews": 890,
            "popularity_score": 0.88,
            "is_active": True,
            "is_featured": True
        },
        {
            "name": "Galle Fort",
            "name_sinhala": "ගාල්ල කොටුව",
            "name_tamil": "காலி கோட்டை",
            "description": "Historic Dutch colonial fort with charming streets, cafes, and ocean views.",
            "description_sinhala": "අලංකාර වීදි, කැෆේ සහ සාගර දර්ශන සහිත ඓතිහාසික ලන්දේසි යටත්විජිත කොටුව.",
            "description_tamil": "அழகிய தெருக்கள், கஃபேக்கள் மற்றும் கடல் காட்சிகளுடன் வரலாற்று டச்சு காலனித்துவ கோட்டை.",
            "location": {"latitude": 6.0329, "longitude": 80.2170},
            "address": "Galle Fort, Galle, Sri Lanka",
            "district": "Galle",
            "province": "Southern",
            "attraction_type": "historical",
            "tags": ["fort", "dutch", "colonial", "unesco", "walking"],
            "difficulty_level": "easy",
            "opening_hours": {
                "monday": "24/7",
                "tuesday": "24/7",
                "wednesday": "24/7",
                "thursday": "24/7",
                "friday": "24/7",
                "saturday": "24/7",
                "sunday": "24/7"
            },
            "entrance_fee": {"adult": 0, "child": 0},
            "best_time_to_visit": ["morning", "evening", "sunset"],
            "duration_visit": 180,
            "images": [
                "https://example.com/galle_fort1.jpg",
                "https://example.com/galle_fort2.jpg"
            ],
            "wheelchair_accessible": True,
            "parking_available": True,
            "public_transport": True,
            "contact_phone": "+94 91 2 234 226",
            "average_rating": 4.5,
            "total_reviews": 1650,
            "popularity_score": 0.85,
            "is_active": True,
            "is_featured": True
        },
        {
            "name": "Nuwara Eliya",
            "name_sinhala": "නුවරඑළිය",
            "name_tamil": "நுவரெலியா",
            "description": "Hill station known as 'Little England' with tea plantations, cool climate, and scenic beauty.",
            "description_sinhala": "'කුඩා එංගලන්තය' ලෙස හැඳින්වෙන කඳුකර නගරය, තේ වතු, සිසිල් දේශගුණය සහ සුන්දර දර්ශන සහිත.",
            "description_tamil": "'சிறிய இங்கிலாந்து' என்று அழைக்கப்படும் மலை நிலையம், தேயிலை தோட்டங்கள், குளிர்ந்த காலநிலை மற்றும் அழகிய காட்சிகளுடன்.",
            "location": {"latitude": 6.9497, "longitude": 80.7891},
            "address": "Nuwara Eliya, Central Province, Sri Lanka",
            "district": "Nuwara Eliya",
            "province": "Central",
            "attraction_type": "hill_station",
            "tags": ["hill_station", "tea", "cool_climate", "scenic", "gardens"],
            "difficulty_level": "easy",
            "opening_hours": {"monday": "24/7", "tuesday": "24/7", "wednesday": "24/7", "thursday": "24/7", "friday": "24/7", "saturday": "24/7", "sunday": "24/7"},
            "entrance_fee": {"adult": 0, "child": 0},
            "best_time_to_visit": ["morning", "afternoon"],
            "duration_visit": 300,
            "images": [
                "https://example.com/nuwara_eliya1.jpg",
                "https://example.com/nuwara_eliya2.jpg"
            ],
            "wheelchair_accessible": True,
            "parking_available": True,
            "public_transport": True,
            "contact_phone": "+94 52 2 234 226",
            "average_rating": 4.4,
            "total_reviews": 980,
            "popularity_score": 0.82,
            "is_active": True,
            "is_featured": True
        }
    ]
    
    for attraction_data in attractions:
        existing = await TouristAttraction.find_one(TouristAttraction.name == attraction_data["name"])
        if not existing:
            attraction = TouristAttraction(**attraction_data)
            await attraction.insert()
            print(f"  ✓ Added attraction: {attraction_data['name']}")

async def seed_restaurants():
    """Seed restaurants"""
    print("Seeding restaurants...")
    
    restaurants = [
        {
            "name": "Ministry of Crab",
            "location": {"latitude": 6.9271, "longitude": 79.8612},
            "address": "Old Dutch Hospital, Colombo 01, Sri Lanka",
            "district": "Colombo",
            "city": "Colombo",
            "cuisine_types": ["seafood", "sri_lankan", "contemporary"],
            "specialties": ["crab", "prawns", "lobster", "rice_and_curry"],
            "price_range": "$$$$",
            "delivery_available": False,
            "takeaway_available": True,
            "dine_in_available": True,
            "outdoor_seating": True,
            "phone": "+94 11 2 234 272",
            "email": "info@ministryofcrab.com",
            "website": "https://www.ministryofcrab.com",
            "opening_hours": {
                "monday": "12:00-15:00, 18:00-22:30",
                "tuesday": "12:00-15:00, 18:00-22:30",
                "wednesday": "12:00-15:00, 18:00-22:30",
                "thursday": "12:00-15:00, 18:00-22:30",
                "friday": "12:00-15:00, 18:00-22:30",
                "saturday": "12:00-15:00, 18:00-22:30",
                "sunday": "12:00-15:00, 18:00-22:30"
            },
            "average_rating": 4.6,
            "total_reviews": 450,
            "images": ["https://example.com/ministry_crab1.jpg"],
            "is_active": True,
            "is_verified": True
        },
        {
            "name": "Upali's by Nawaloka",
            "location": {"latitude": 6.9147, "longitude": 79.8500},
            "address": "Nawaloka Hospital, Colombo 02, Sri Lanka",
            "district": "Colombo",
            "city": "Colombo",
            "cuisine_types": ["sri_lankan", "traditional"],
            "specialties": ["rice_and_curry", "hoppers", "string_hoppers", "kottu"],
            "price_range": "$$",
            "delivery_available": True,
            "takeaway_available": True,
            "dine_in_available": True,
            "outdoor_seating": False,
            "phone": "+94 11 2 234 272",
            "opening_hours": {
                "monday": "11:00-22:00",
                "tuesday": "11:00-22:00",
                "wednesday": "11:00-22:00",
                "thursday": "11:00-22:00",
                "friday": "11:00-22:00",
                "saturday": "11:00-22:00",
                "sunday": "11:00-22:00"
            },
            "average_rating": 4.3,
            "total_reviews": 320,
            "images": ["https://example.com/upalis1.jpg"],
            "is_active": True,
            "is_verified": True
        },
        {
            "name": "The Empire Cafe",
            "location": {"latitude": 6.0329, "longitude": 80.2170},
            "address": "Galle Fort, Galle, Sri Lanka",
            "district": "Galle",
            "city": "Galle",
            "cuisine_types": ["international", "cafe", "contemporary"],
            "specialties": ["coffee", "brunch", "sandwiches", "desserts"],
            "price_range": "$$$",
            "delivery_available": False,
            "takeaway_available": True,
            "dine_in_available": True,
            "outdoor_seating": True,
            "phone": "+94 91 2 234 272",
            "opening_hours": {
                "monday": "8:00-22:00",
                "tuesday": "8:00-22:00",
                "wednesday": "8:00-22:00",
                "thursday": "8:00-22:00",
                "friday": "8:00-22:00",
                "saturday": "8:00-22:00",
                "sunday": "8:00-22:00"
            },
            "average_rating": 4.4,
            "total_reviews": 280,
            "images": ["https://example.com/empire_cafe1.jpg"],
            "is_active": True,
            "is_verified": True
        }
    ]
    
    for restaurant_data in restaurants:
        existing = await Restaurant.find_one(Restaurant.name == restaurant_data["name"])
        if not existing:
            restaurant = Restaurant(**restaurant_data)
            await restaurant.insert()
            print(f"  ✓ Added restaurant: {restaurant_data['name']}")

async def seed_accommodations():
    """Seed accommodations"""
    print("Seeding accommodations...")
    
    accommodations = [
        {
            "name": "Galle Face Hotel",
            "accommodation_type": "hotel",
            "location": {"latitude": 6.9271, "longitude": 79.8612},
            "address": "2 Galle Road, Colombo 03, Sri Lanka",
            "district": "Colombo",
            "city": "Colombo",
            "description": "Historic luxury hotel with ocean views and colonial architecture.",
            "amenities": ["wifi", "pool", "spa", "restaurant", "bar", "gym", "parking"],
            "room_types": [
                {"type": "deluxe", "price": 25000, "capacity": 2},
                {"type": "suite", "price": 45000, "capacity": 4},
                {"type": "presidential", "price": 75000, "capacity": 6}
            ],
            "price_range": {"min": 25000, "max": 75000},
            "currency": "LKR",
            "phone": "+94 11 2 234 272",
            "email": "reservations@gallefacehotel.com",
            "website": "https://www.gallefacehotel.com",
            "average_rating": 4.5,
            "total_reviews": 180,
            "images": ["https://example.com/galle_face1.jpg"],
            "is_active": True,
            "is_verified": True
        },
        {
            "name": "Jetwing Lighthouse",
            "accommodation_type": "resort",
            "location": {"latitude": 6.0329, "longitude": 80.2170},
            "address": "Dadella, Galle, Sri Lanka",
            "district": "Galle",
            "city": "Galle",
            "description": "Luxury beachfront resort with stunning ocean views and modern amenities.",
            "amenities": ["wifi", "pool", "spa", "restaurant", "bar", "beach_access", "parking"],
            "room_types": [
                {"type": "standard", "price": 18000, "capacity": 2},
                {"type": "deluxe", "price": 28000, "capacity": 2},
                {"type": "suite", "price": 45000, "capacity": 4}
            ],
            "price_range": {"min": 18000, "max": 45000},
            "currency": "LKR",
            "phone": "+94 91 2 234 272",
            "email": "reservations@jetwinghotels.com",
            "website": "https://www.jetwinghotels.com",
            "average_rating": 4.7,
            "total_reviews": 220,
            "images": ["https://example.com/jetwing_lighthouse1.jpg"],
            "is_active": True,
            "is_verified": True
        }
    ]
    
    for accommodation_data in accommodations:
        existing = await Accommodation.find_one(Accommodation.name == accommodation_data["name"])
        if not existing:
            accommodation = Accommodation(**accommodation_data)
            await accommodation.insert()
            print(f"  ✓ Added accommodation: {accommodation_data['name']}")

async def seed_emergency_services():
    """Seed emergency services"""
    print("Seeding emergency services...")
    
    services = [
        {
            "service_name": "Sri Lanka Police",
            "service_type": "police",
            "phone": "119",
            "emergency_phone": "119",
            "email": "info@police.lk",
            "location": {"latitude": 6.9271, "longitude": 79.8612},
            "address": "Police Headquarters, Colombo 01, Sri Lanka",
            "district": "Colombo",
            "description": "National police service for law enforcement and public safety.",
            "operating_hours": "24/7",
            "languages_supported": ["en", "si", "ta"],
            "is_active": True,
            "is_24_hours": True
        },
        {
            "service_name": "Tourist Police",
            "service_type": "tourist_police",
            "phone": "+94 11 242 1052",
            "emergency_phone": "+94 11 242 1052",
            "email": "touristpolice@police.lk",
            "location": {"latitude": 6.9271, "longitude": 79.8612},
            "address": "Tourist Police Division, Colombo 01, Sri Lanka",
            "district": "Colombo",
            "description": "Specialized police service for tourists with multilingual support.",
            "operating_hours": "24/7",
            "languages_supported": ["en", "si", "ta", "de", "fr", "zh", "ja"],
            "is_active": True,
            "is_24_hours": True
        },
        {
            "service_name": "National Hospital of Sri Lanka",
            "service_type": "hospital",
            "phone": "+94 11 2 691 111",
            "emergency_phone": "110",
            "email": "info@nhsl.health.gov.lk",
            "location": {"latitude": 6.9147, "longitude": 79.8500},
            "address": "National Hospital, Colombo 07, Sri Lanka",
            "district": "Colombo",
            "description": "Main public hospital with emergency services and specialized care.",
            "operating_hours": "24/7",
            "languages_supported": ["en", "si", "ta"],
            "is_active": True,
            "is_24_hours": True
        },
        {
            "service_name": "Fire and Rescue Services",
            "service_type": "fire",
            "phone": "110",
            "emergency_phone": "110",
            "email": "info@fire.lk",
            "location": {"latitude": 6.9271, "longitude": 79.8612},
            "address": "Fire Headquarters, Colombo 01, Sri Lanka",
            "district": "Colombo",
            "description": "Fire and rescue services for emergency situations.",
            "operating_hours": "24/7",
            "languages_supported": ["en", "si", "ta"],
            "is_active": True,
            "is_24_hours": True
        }
    ]
    
    for service_data in services:
        existing = await EmergencyService.find_one(EmergencyService.service_name == service_data["service_name"])
        if not existing:
            service = EmergencyService(**service_data)
            await service.insert()
            print(f"  ✓ Added emergency service: {service_data['service_name']}")

async def seed_cultural_events():
    """Seed cultural events"""
    print("Seeding cultural events...")
    
    events = [
        {
            "name": "Kandy Esala Perahera",
            "name_sinhala": "කැන්ද එසල පෙරහැර",
            "name_tamil": "கண்டி ஏசலா பெரஹரா",
            "description": "Grand annual Buddhist festival featuring decorated elephants, traditional dancers, and drummers.",
            "event_type": "festival",
            "start_date": datetime(2024, 8, 15),
            "end_date": datetime(2024, 8, 25),
            "is_recurring": True,
            "recurrence_pattern": "yearly",
            "location": {"latitude": 7.2945, "longitude": 80.6414},
            "venue": "Temple of the Sacred Tooth Relic, Kandy",
            "district": "Kandy",
            "entry_fee": 0,
            "currency": "LKR",
            "age_restriction": None,
            "dress_code": "Modest clothing, remove shoes",
            "images": ["https://example.com/perahera1.jpg"],
            "is_active": True,
            "is_featured": True
        },
        {
            "name": "Sinhala and Tamil New Year",
            "name_sinhala": "සිංහල හා දෙමළ අලුත් අවුරුද්ද",
            "name_tamil": "சிங்கள மற்றும் தமிழ் புத்தாண்டு",
            "description": "Traditional New Year celebration with cultural games, food, and family gatherings.",
            "event_type": "celebration",
            "start_date": datetime(2024, 4, 13),
            "end_date": datetime(2024, 4, 14),
            "is_recurring": True,
            "recurrence_pattern": "yearly",
            "location": {"latitude": 6.9271, "longitude": 79.8612},
            "venue": "Nationwide celebration",
            "district": "Colombo",
            "entry_fee": 0,
            "currency": "LKR",
            "age_restriction": None,
            "dress_code": "Traditional or casual",
            "images": ["https://example.com/new_year1.jpg"],
            "is_active": True,
            "is_featured": True
        }
    ]
    
    for event_data in events:
        existing = await CulturalEvent.find_one(CulturalEvent.name == event_data["name"])
        if not existing:
            event = CulturalEvent(**event_data)
            await event.insert()
            print(f"  ✓ Added cultural event: {event_data['name']}")

async def main():
    """Main seeding function"""
    print("Starting database seeding...")
    
    try:
        # Connect to database
        await connect_to_mongo()
        print("✓ Connected to database")
        
        # Seed data
        await seed_languages()
        await seed_tourist_attractions()
        await seed_restaurants()
        await seed_accommodations()
        await seed_emergency_services()
        await seed_cultural_events()
        
        print("\n✓ Database seeding completed successfully!")
        
    except Exception as e:
        print(f"\n✗ Error during seeding: {str(e)}")
        raise
    finally:
        # Close database connection
        from app.core.database import close_mongo_connection
        await close_mongo_connection()
        print("✓ Database connection closed")

if __name__ == "__main__":
    asyncio.run(main())