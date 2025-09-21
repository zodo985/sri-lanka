import asyncio
from typing import Dict, Optional
from app.core.config import settings

class TranslationService:
    """Translation service for multilingual support"""
    
    def __init__(self):
        self.supported_languages = settings.supported_languages
        self.language_names = settings.language_names
        
        # Simple translation dictionaries (in production, use proper translation APIs)
        self.translations = {
            "greetings": {
                "en": "Hello! Welcome to Sri Lanka Tourism Assistant. How can I help you today?",
                "si": "ආයුබෝවන්! ශ්‍රී ලංකා සංචාරක සහායකයට සාදරයෙන් පිළිගනිමු. අද මට ඔබට කෙසේ උදව් කළ හැකිද?",
                "ta": "வணக்கம்! இலங்கை சுற்றுலா உதவியாளருக்கு வரவேற்கிறோம். இன்று உங்களுக்கு எவ்வாறு உதவ முடியும்?",
                "de": "Hallo! Willkommen beim Sri Lanka Tourism Assistant. Wie kann ich Ihnen heute helfen?",
                "fr": "Bonjour! Bienvenue à l'Assistant Tourisme du Sri Lanka. Comment puis-je vous aider aujourd'hui?",
                "zh": "你好！欢迎来到斯里兰卡旅游助手。今天我能为您做些什么？",
                "ja": "こんにちは！スリランカ観光アシスタントへようこそ。今日はどのようにお手伝いできますか？"
            },
            "attractions": {
                "en": "Here are some tourist attractions I found for you:",
                "si": "මම ඔබට සොයාගත් සංචාරක ස්ථාන කිහිපයක්:",
                "ta": "உங்களுக்காக நான் கண்டுபிடித்த சில சுற்றுலா இடங்கள்:",
                "de": "Hier sind einige Touristenattraktionen, die ich für Sie gefunden habe:",
                "fr": "Voici quelques attractions touristiques que j'ai trouvées pour vous:",
                "zh": "我为您找到的一些旅游景点：",
                "ja": "あなたのために見つけた観光スポットをいくつか紹介します："
            },
            "restaurants": {
                "en": "Here are some restaurants I found for you:",
                "si": "මම ඔබට සොයාගත් ආහාරශාලා කිහිපයක්:",
                "ta": "உங்களுக்காக நான் கண்டுபிடித்த சில உணவகங்கள்:",
                "de": "Hier sind einige Restaurants, die ich für Sie gefunden habe:",
                "fr": "Voici quelques restaurants que j'ai trouvés pour vous:",
                "zh": "我为您找到的一些餐厅：",
                "ja": "あなたのために見つけたレストランをいくつか紹介します："
            },
            "accommodation": {
                "en": "Here are some accommodations I found for you:",
                "si": "මම ඔබට සොයාගත් නවාතැන් ස්ථාන කිහිපයක්:",
                "ta": "உங்களுக்காக நான் கண்டுபிடித்த சில விடுதிகள்:",
                "de": "Hier sind einige Unterkünfte, die ich für Sie gefunden habe:",
                "fr": "Voici quelques hébergements que j'ai trouvés pour vous:",
                "zh": "我为您找到的一些住宿：",
                "ja": "あなたのために見つけた宿泊施設をいくつか紹介します："
            },
            "transportation": {
                "en": "Here's information about transportation in Sri Lanka:",
                "si": "ශ්‍රී ලංකාවේ ප්‍රවාහනය පිළිබඳ තොරතුරු:",
                "ta": "இலங்கையில் போக்குவரத்து பற்றிய தகவல்கள்:",
                "de": "Hier sind Informationen über den Transport in Sri Lanka:",
                "fr": "Voici des informations sur les transports au Sri Lanka:",
                "zh": "以下是斯里兰卡交通信息：",
                "ja": "スリランカの交通機関についての情報です："
            },
            "emergency": {
                "en": "Emergency Contacts in Sri Lanka:",
                "si": "ශ්‍රී ලංකාවේ හදිසි සම්බන්ධතා:",
                "ta": "இலங்கையில் அவசர தொடர்புகள்:",
                "de": "Notfallkontakte in Sri Lanka:",
                "fr": "Contacts d'urgence au Sri Lanka:",
                "zh": "斯里兰卡紧急联系方式：",
                "ja": "スリランカの緊急連絡先："
            },
            "weather": {
                "en": "Weather Information:",
                "si": "කාලගුණ තොරතුරු:",
                "ta": "வானிலை தகவல்கள்:",
                "de": "Wetterinformationen:",
                "fr": "Informations météorologiques:",
                "zh": "天气信息：",
                "ja": "天気情報："
            },
            "currency": {
                "en": "Currency Information:",
                "si": "මුදල් තොරතුරු:",
                "ta": "நாணய தகவல்கள்:",
                "de": "Währungsinformationen:",
                "fr": "Informations sur la monnaie:",
                "zh": "货币信息：",
                "ja": "通貨情報："
            },
            "culture": {
                "en": "Sri Lankan Culture & Customs:",
                "si": "ශ්‍රී ලාංකික සංස්කෘතිය හා පරිපාටි:",
                "ta": "இலங்கை கலாச்சாரம் மற்றும் பழக்கவழக்கங்கள்:",
                "de": "Sri Lankische Kultur & Bräuche:",
                "fr": "Culture et coutumes du Sri Lanka:",
                "zh": "斯里兰卡文化与习俗：",
                "ja": "スリランカの文化と習慣："
            }
        }
    
    async def translate(self, text: str, source_language: str, target_language: str) -> str:
        """Translate text from source to target language"""
        try:
            if source_language == target_language:
                return text
            
            # Check if we have a translation for this text
            for category, translations in self.translations.items():
                if text in translations.get(source_language, ""):
                    return translations.get(target_language, text)
            
            # If no specific translation found, return original text
            # In production, you would call a translation API here
            return text
            
        except Exception:
            return text
    
    async def translate_attraction_info(self, attraction_data: Dict, target_language: str) -> Dict:
        """Translate attraction information to target language"""
        try:
            translated_data = attraction_data.copy()
            
            # Translate name
            if target_language == "si" and attraction_data.get("name_sinhala"):
                translated_data["name"] = attraction_data["name_sinhala"]
            elif target_language == "ta" and attraction_data.get("name_tamil"):
                translated_data["name"] = attraction_data["name_tamil"]
            
            # Translate description
            if target_language == "si" and attraction_data.get("description_sinhala"):
                translated_data["description"] = attraction_data["description_sinhala"]
            elif target_language == "ta" and attraction_data.get("description_tamil"):
                translated_data["description"] = attraction_data["description_tamil"]
            
            return translated_data
            
        except Exception:
            return attraction_data
    
    async def translate_restaurant_info(self, restaurant_data: Dict, target_language: str) -> Dict:
        """Translate restaurant information to target language"""
        try:
            # For now, return original data
            # In production, you would translate cuisine types, specialties, etc.
            return restaurant_data
            
        except Exception:
            return restaurant_data
    
    async def translate_accommodation_info(self, accommodation_data: Dict, target_language: str) -> Dict:
        """Translate accommodation information to target language"""
        try:
            # For now, return original data
            # In production, you would translate room types, amenities, etc.
            return accommodation_data
            
        except Exception:
            return accommodation_data
    
    async def get_quick_replies(self, category: str, language: str) -> list:
        """Get quick replies for a category in the specified language"""
        try:
            quick_replies = {
                "main_menu": {
                    "en": [
                        {"title": "Tourist Attractions", "payload": "attractions"},
                        {"title": "Food & Restaurants", "payload": "restaurants"},
                        {"title": "Accommodation", "payload": "accommodation"},
                        {"title": "Transportation", "payload": "transportation"},
                        {"title": "Emergency Help", "payload": "emergency"},
                        {"title": "Weather Info", "payload": "weather"}
                    ],
                    "si": [
                        {"title": "සංචාරක ස්ථාන", "payload": "attractions"},
                        {"title": "ආහාර හා ආහාරශාලා", "payload": "restaurants"},
                        {"title": "නවාතැන්", "payload": "accommodation"},
                        {"title": "ප්‍රවාහන", "payload": "transportation"},
                        {"title": "හදිසි උදව්", "payload": "emergency"},
                        {"title": "කාලගුණ තොරතුරු", "payload": "weather"}
                    ],
                    "ta": [
                        {"title": "சுற்றுலா இடங்கள்", "payload": "attractions"},
                        {"title": "உணவு மற்றும் உணவகங்கள்", "payload": "restaurants"},
                        {"title": "விடுதிகள்", "payload": "accommodation"},
                        {"title": "போக்குவரத்து", "payload": "transportation"},
                        {"title": "அவசர உதவி", "payload": "emergency"},
                        {"title": "வானிலை தகவல்கள்", "payload": "weather"}
                    ]
                },
                "attractions": {
                    "en": [
                        {"title": "Historical Sites", "payload": "historical"},
                        {"title": "Beaches", "payload": "beaches"},
                        {"title": "Mountains", "payload": "mountains"},
                        {"title": "Wildlife", "payload": "wildlife"},
                        {"title": "Temples", "payload": "temples"},
                        {"title": "Back to Main Menu", "payload": "main_menu"}
                    ],
                    "si": [
                        {"title": "ඓතිහාසික ස්ථාන", "payload": "historical"},
                        {"title": "කොරල්", "payload": "beaches"},
                        {"title": "පර්වත", "payload": "mountains"},
                        {"title": "වනජීවී", "payload": "wildlife"},
                        {"title": "විහාර", "payload": "temples"},
                        {"title": "ප්‍රධාන මෙනුවට", "payload": "main_menu"}
                    ],
                    "ta": [
                        {"title": "வரலாற்று இடங்கள்", "payload": "historical"},
                        {"title": "கடற்கரைகள்", "payload": "beaches"},
                        {"title": "மலைகள்", "payload": "mountains"},
                        {"title": "வனவிலங்குகள்", "payload": "wildlife"},
                        {"title": "கோவில்கள்", "payload": "temples"},
                        {"title": "முதன்மை மெனுவுக்கு", "payload": "main_menu"}
                    ]
                }
            }
            
            return quick_replies.get(category, {}).get(language, [])
            
        except Exception:
            return []
    
    async def detect_language_from_text(self, text: str) -> str:
        """Detect language from text"""
        try:
            # Simple language detection based on character sets
            if any('\u0D80' <= char <= '\u0DFF' for char in text):
                return "si"  # Sinhala
            elif any('\u0B80' <= char <= '\u0BFF' for char in text):
                return "ta"  # Tamil
            elif any('\u4e00' <= char <= '\u9fff' for char in text):
                return "zh"  # Chinese
            elif any('\u3040' <= char <= '\u309F' or '\u30A0' <= char <= '\u30FF' for char in text):
                return "ja"  # Japanese
            else:
                return "en"  # Default to English
                
        except Exception:
            return "en"