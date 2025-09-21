import asyncio
import re
from typing import Dict, List, Any, Optional
from app.core.config import settings

class NLPService:
    """Natural Language Processing service"""
    
    def __init__(self):
        self.supported_languages = settings.supported_languages
        self.language_patterns = {
            "en": r"[a-zA-Z]",
            "si": r"[\u0D80-\u0DFF]",
            "ta": r"[\u0B80-\u0BFF]",
            "de": r"[a-zA-ZäöüßÄÖÜ]",
            "fr": r"[a-zA-ZàâäéèêëïîôöùûüÿçÀÂÄÉÈÊËÏÎÔÖÙÛÜŸÇ]",
            "zh": r"[\u4e00-\u9fff]",
            "ja": r"[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff]"
        }
        
        # Intent patterns
        self.intent_patterns = {
            "greeting": [
                r"\b(hello|hi|hey|good morning|good afternoon|good evening)\b",
                r"\b(ආයුබෝවන්|වාඩි|කොහොමද)\b",  # Sinhala
                r"\b(வணக்கம்|ஹலோ|எப்படி)\b"  # Tamil
            ],
            "attraction_search": [
                r"\b(attractions?|places? to visit|sights?|monuments?|temples?|beaches?|mountains?)\b",
                r"\b(දර්ශන|ස්ථාන|විහාර|කොරල්|පර්වත)\b",  # Sinhala
                r"\b(இடங்கள்|கோவில்கள்|கடற்கரைகள்|மலைகள்)\b"  # Tamil
            ],
            "restaurant_search": [
                r"\b(restaurants?|food|eat|dining|cuisine|meals?)\b",
                r"\b(ආහාර|රෙස්ටෝරන්ට්|කෑම|බොජුන්)\b",  # Sinhala
                r"\b(உணவகங்கள்|உணவு|சாப்பாடு|விருந்தினர்)\b"  # Tamil
            ],
            "accommodation_search": [
                r"\b(hotels?|accommodation|stay|lodging|guesthouse|hostel)\b",
                r"\b(හෝටල්|විඩාර|නවාතැන්|ඉන්න|බැඳි)\b",  # Sinhala
                r"\b(ஹோட்டல்கள்|விடுதிகள்|தங்குதல்|விருந்தினர்)\b"  # Tamil
            ],
            "transportation_info": [
                r"\b(transport|bus|train|taxi|tuk tuk|how to get|directions?)\b",
                r"\b(ප්‍රවාහන|බස්|දුම්රිය|ටැක්සි|කොහොමද|මාර්ගය)\b",  # Sinhala
                r"\b(போக்குவரத்து|பஸ்|ரயில்|டாக்ஸி|எப்படி|வழி)\b"  # Tamil
            ],
            "emergency_help": [
                r"\b(emergency|help|police|hospital|ambulance|danger|urgent)\b",
                r"\b(හදිසි|උදව්|පොලිස්|රෝහල්|අම්බුලන්ස්|අනතුර|අත්තනෝමතික)\b",  # Sinhala
                r"\b(அவசர|உதவி|காவல்துறை|மருத்துவமனை|அம்புலன்ஸ்|அபாயம்|அவசரமான)\b"  # Tamil
            ],
            "weather_info": [
                r"\b(weather|temperature|rain|sunny|cloudy|forecast)\b",
                r"\b(කාලගුණය|උෂ්ණත්වය|වැසි|හිරු|වලාකුළු|පුරෝකථනය)\b",  # Sinhala
                r"\b(வானிலை|வெப்பநிலை|மழை|வெயில்|மேகம்|முன்னறிவிப்பு)\b"  # Tamil
            ],
            "currency_info": [
                r"\b(currency|money|exchange|rupee|dollar|euro|price|cost)\b",
                r"\b(මුදල්|විනිමය|රුපියල්|ඩොලර්|යුරෝ|මිල|වටිනාකම)\b",  # Sinhala
                r"\b(நாணயம்|பணம்|பரிமாற்றம்|ரூபாய்|டாலர்|யூரோ|விலை|செலவு)\b"  # Tamil
            ],
            "cultural_info": [
                r"\b(culture|customs|traditions|festivals|religion|temple|monk)\b",
                r"\b(සංස්කෘතිය|පරිපාටි|ප්‍රථිපත්ති|පෙරහැර|ආගම|විහාර|භික්ෂු)\b",  # Sinhala
                r"\b(கலாச்சாரம்|பழக்கவழக்கங்கள்|மரபுகள்|திருவிழாக்கள்|மதம்|கோவில்|துறவி)\b"  # Tamil
            ]
        }
        
        # Entity patterns
        self.entity_patterns = {
            "attraction_type": [
                r"\b(temple|beach|mountain|waterfall|garden|museum|fort|palace)\b",
                r"\b(විහාර|කොරල්|පර්වත|ජලපාත|උද්යාන|කෞතුකාගාර|කොට|ප්‍රාසාද)\b",  # Sinhala
                r"\b(கோவில்|கடற்கரை|மலை|அருவி|தோட்டம்|அருங்காட்சியகம்|கோட்டை|அரண்மனை)\b"  # Tamil
            ],
            "cuisine_type": [
                r"\b(sri lankan|indian|chinese|western|seafood|vegetarian|spicy)\b",
                r"\b(ශ්‍රී ලාංකික|ඉන්දියානු|චීන|බටහිර|මුහුදු ආහාර|ශාක|කඩල)\b",  # Sinhala
                r"\b(இலங்கை|இந்திய|சீன|மேற்கத்திய|கடல் உணவு|சைவ|காரமான)\b"  # Tamil
            ],
            "accommodation_type": [
                r"\b(hotel|guesthouse|hostel|resort|villa|homestay|camping)\b",
                r"\b(හෝටල්|ගෙස්ට්හවුස්|හෝස්ටල්|රිසෝට්|විලා|ගෙදර|කෑම්පිං)\b",  # Sinhala
                r"\b(ஹோட்டல்|விருந்தினர்|விடுதி|ரிசார்ட்|வில்லா|வீடு|முகாம்)\b"  # Tamil
            ],
            "location": [
                r"\b(colombo|kandy|galle|anuradhapura|polonnaruwa|nuwara eliya|negombo|bentota)\b",
                r"\b(කොළඹ|මහනුවර|ගාල්ල|අනුරාධපුර|පොළොන්නරුව|නුවරඑළිය|නේගොම්බෝ|බෙන්තොට)\b",  # Sinhala
                r"\b(கொழும்பு|கண்டி|காலி|அனுராதபுரம்|பொலன்னறுவை|நுவரெலியா|நெகொம்போ|பென்டோட்டா)\b"  # Tamil
            ],
            "district": [
                r"\b(colombo|gampaha|kalutara|kandy|matale|nuwara eliya|galle|matara|hambantota)\b",
                r"\b(කොළඹ|ගම්පහ|කළුතර|මහනුවර|මාතලේ|නුවරඑළිය|ගාල්ල|මාතර|හම්බන්තොට)\b",  # Sinhala
                r"\b(கொழும்பு|கம்பஹா|கலுத்தரா|கண்டி|மாதலே|நுவரெலியா|காலி|மாதரா|ஹம்பன்தோட்டா)\b"  # Tamil
            ]
        }
    
    async def detect_language(self, text: str) -> str:
        """Detect language of the input text"""
        try:
            text = text.lower().strip()
            
            # Check each language pattern
            for lang_code, pattern in self.language_patterns.items():
                if re.search(pattern, text):
                    return lang_code
            
            # Default to English if no pattern matches
            return "en"
            
        except Exception:
            return "en"
    
    async def extract_intent(self, text: str, language: str = "en") -> Optional[str]:
        """Extract intent from text"""
        try:
            text = text.lower().strip()
            
            # Check each intent pattern
            for intent, patterns in self.intent_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, text, re.IGNORECASE):
                        return intent
            
            return None
            
        except Exception:
            return None
    
    async def extract_entities(self, text: str, language: str = "en") -> List[Dict[str, Any]]:
        """Extract entities from text"""
        try:
            text = text.lower().strip()
            entities = []
            
            # Check each entity pattern
            for entity_type, patterns in self.entity_patterns.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, text, re.IGNORECASE)
                    for match in matches:
                        entities.append({
                            "entity": entity_type,
                            "value": match.group().strip(),
                            "start": match.start(),
                            "end": match.end(),
                            "confidence": 0.8
                        })
            
            return entities
            
        except Exception:
            return []
    
    async def analyze_sentiment(self, text: str, language: str = "en") -> str:
        """Analyze sentiment of text"""
        try:
            text = text.lower().strip()
            
            # Positive sentiment indicators
            positive_words = [
                "good", "great", "excellent", "amazing", "wonderful", "fantastic",
                "beautiful", "nice", "love", "like", "enjoy", "happy", "pleased"
            ]
            
            # Negative sentiment indicators
            negative_words = [
                "bad", "terrible", "awful", "horrible", "hate", "dislike",
                "angry", "frustrated", "disappointed", "sad", "upset"
            ]
            
            # Count positive and negative words
            positive_count = sum(1 for word in positive_words if word in text)
            negative_count = sum(1 for word in negative_words if word in text)
            
            if positive_count > negative_count:
                return "positive"
            elif negative_count > positive_count:
                return "negative"
            else:
                return "neutral"
                
        except Exception:
            return "neutral"
    
    async def process_message(
        self,
        text: str,
        detected_language: str,
        target_language: str = "en"
    ) -> Dict[str, Any]:
        """Process message and extract all NLP information"""
        try:
            # Extract intent
            intent = await self.extract_intent(text, detected_language)
            
            # Extract entities
            entities = await self.extract_entities(text, detected_language)
            
            # Analyze sentiment
            sentiment = await self.analyze_sentiment(text, detected_language)
            
            # Calculate confidence based on pattern matches
            confidence = 0.0
            if intent:
                confidence += 0.6
            if entities:
                confidence += 0.3
            if sentiment != "neutral":
                confidence += 0.1
            
            confidence = min(confidence, 1.0)
            
            return {
                "intent": intent,
                "entities": entities,
                "sentiment": sentiment,
                "confidence": confidence,
                "detected_language": detected_language,
                "target_language": target_language
            }
            
        except Exception as e:
            return {
                "intent": None,
                "entities": [],
                "sentiment": "neutral",
                "confidence": 0.0,
                "detected_language": detected_language,
                "target_language": target_language,
                "error": str(e)
            }
    
    async def translate_text(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text from source to target language"""
        try:
            # In a real implementation, you would use a translation service
            # For now, return the original text
            if source_lang == target_lang:
                return text
            
            # Simple placeholder translations
            translations = {
                "en": {
                    "si": "සිංහල පරිවර්තනය",  # Placeholder
                    "ta": "தமிழ் மொழிபெயர்ப்பு"  # Placeholder
                },
                "si": {
                    "en": "English translation",  # Placeholder
                    "ta": "தமிழ் மொழிபெயர்ப்பு"  # Placeholder
                },
                "ta": {
                    "en": "English translation",  # Placeholder
                    "si": "සිංහල පරිවර්තනය"  # Placeholder
                }
            }
            
            return translations.get(source_lang, {}).get(target_lang, text)
            
        except Exception:
            return text