import asyncio
from typing import Dict, List, Any, Optional
from app.models.tourism import TouristAttraction, Restaurant, Accommodation
from app.models.user import UserPreference
from app.models.planning import Recommendation
import uuid
from datetime import datetime

class RecommendationService:
    """AI-powered recommendation service"""
    
    def __init__(self):
        self.attraction_weights = {
            "historical": 0.3,
            "natural": 0.25,
            "cultural": 0.2,
            "adventure": 0.15,
            "beach": 0.1
        }
        
        self.restaurant_weights = {
            "sri_lankan": 0.4,
            "indian": 0.2,
            "chinese": 0.15,
            "western": 0.15,
            "seafood": 0.1
        }
        
        self.accommodation_weights = {
            "hotel": 0.3,
            "resort": 0.25,
            "guesthouse": 0.2,
            "villa": 0.15,
            "hostel": 0.1
        }
    
    async def get_attraction_recommendations(
        self,
        user_id: Optional[str] = None,
        preferences: Optional[Dict[str, Any]] = None,
        location: Optional[Dict[str, float]] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Get personalized attraction recommendations"""
        try:
            # Get user preferences if user_id provided
            user_preferences = None
            if user_id:
                user_preferences = await UserPreference.find_one(UserPreference.user_id == user_id)
            
            # Build query based on preferences
            query = {"is_active": True}
            
            if preferences:
                if preferences.get("interests"):
                    # Map interests to attraction types
                    attraction_types = []
                    for interest in preferences["interests"]:
                        if interest in ["culture", "history"]:
                            attraction_types.extend(["historical", "cultural", "religious"])
                        elif interest in ["nature", "wildlife"]:
                            attraction_types.extend(["natural", "wildlife", "national_park"])
                        elif interest in ["adventure", "sports"]:
                            attraction_types.extend(["adventure", "hiking", "water_sports"])
                        elif interest in ["beach", "relaxation"]:
                            attraction_types.extend(["beach", "resort"])
                    
                    if attraction_types:
                        query["attraction_type"] = {"$in": attraction_types}
                
                if preferences.get("difficulty_level"):
                    difficulty_mapping = {
                        "beginner": "easy",
                        "intermediate": "moderate",
                        "advanced": "challenging"
                    }
                    query["difficulty_level"] = difficulty_mapping.get(
                        preferences["difficulty_level"], "easy"
                    )
                
                if preferences.get("accessibility_needs"):
                    if "wheelchair" in preferences["accessibility_needs"]:
                        query["wheelchair_accessible"] = True
            
            # Get attractions
            attractions = await TouristAttraction.find(query).limit(limit * 2).to_list()
            
            # Score and rank attractions
            scored_attractions = []
            for attraction in attractions:
                score = await self._calculate_attraction_score(
                    attraction, user_preferences, location
                )
                scored_attractions.append({
                    "attraction": attraction,
                    "score": score
                })
            
            # Sort by score and return top recommendations
            scored_attractions.sort(key=lambda x: x["score"], reverse=True)
            
            recommendations = []
            for item in scored_attractions[:limit]:
                attraction = item["attraction"]
                recommendations.append({
                    "id": str(attraction.id),
                    "name": attraction.name,
                    "type": attraction.attraction_type,
                    "district": attraction.district,
                    "rating": attraction.average_rating,
                    "score": item["score"],
                    "description": attraction.description[:200] + "..." if len(attraction.description) > 200 else attraction.description,
                    "image": attraction.images[0] if attraction.images else None,
                    "location": attraction.location
                })
            
            return recommendations
            
        except Exception as e:
            return []
    
    async def get_restaurant_recommendations(
        self,
        user_id: Optional[str] = None,
        preferences: Optional[Dict[str, Any]] = None,
        location: Optional[Dict[str, float]] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Get personalized restaurant recommendations"""
        try:
            # Get user preferences
            user_preferences = None
            if user_id:
                user_preferences = await UserPreference.find_one(UserPreference.user_id == user_id)
            
            # Build query
            query = {"is_active": True}
            
            if preferences:
                if preferences.get("cuisine_preferences"):
                    query["cuisine_types"] = {"$in": preferences["cuisine_preferences"]}
                
                if preferences.get("dietary_restrictions"):
                    # Filter based on dietary restrictions
                    if "vegetarian" in preferences["dietary_restrictions"]:
                        query["specialties"] = {"$in": ["vegetarian", "rice_and_curry"]}
                    if "halal" in preferences["dietary_restrictions"]:
                        query["specialties"] = {"$in": ["halal", "muslim_food"]}
            
            # Get restaurants
            restaurants = await Restaurant.find(query).limit(limit * 2).to_list()
            
            # Score and rank
            scored_restaurants = []
            for restaurant in restaurants:
                score = await self._calculate_restaurant_score(
                    restaurant, user_preferences, location
                )
                scored_restaurants.append({
                    "restaurant": restaurant,
                    "score": score
                })
            
            scored_restaurants.sort(key=lambda x: x["score"], reverse=True)
            
            recommendations = []
            for item in scored_restaurants[:limit]:
                restaurant = item["restaurant"]
                recommendations.append({
                    "id": str(restaurant.id),
                    "name": restaurant.name,
                    "cuisine_types": restaurant.cuisine_types,
                    "district": restaurant.district,
                    "rating": restaurant.average_rating,
                    "score": item["score"],
                    "price_range": restaurant.price_range,
                    "specialties": restaurant.specialties,
                    "image": restaurant.images[0] if restaurant.images else None,
                    "location": restaurant.location
                })
            
            return recommendations
            
        except Exception as e:
            return []
    
    async def get_accommodation_recommendations(
        self,
        user_id: Optional[str] = None,
        preferences: Optional[Dict[str, Any]] = None,
        location: Optional[Dict[str, float]] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Get personalized accommodation recommendations"""
        try:
            # Get user preferences
            user_preferences = None
            if user_id:
                user_preferences = await UserPreference.find_one(UserPreference.user_id == user_id)
            
            # Build query
            query = {"is_active": True}
            
            if preferences:
                if preferences.get("accommodation_types"):
                    query["accommodation_type"] = {"$in": preferences["accommodation_types"]}
                
                if preferences.get("budget_range"):
                    budget = preferences["budget_range"]
                    if budget.get("min"):
                        query["price_range.min"] = {"$gte": budget["min"]}
                    if budget.get("max"):
                        query["price_range.max"] = {"$lte": budget["max"]}
            
            # Get accommodations
            accommodations = await Accommodation.find(query).limit(limit * 2).to_list()
            
            # Score and rank
            scored_accommodations = []
            for accommodation in accommodations:
                score = await self._calculate_accommodation_score(
                    accommodation, user_preferences, location
                )
                scored_accommodations.append({
                    "accommodation": accommodation,
                    "score": score
                })
            
            scored_accommodations.sort(key=lambda x: x["score"], reverse=True)
            
            recommendations = []
            for item in scored_accommodations[:limit]:
                accommodation = item["accommodation"]
                recommendations.append({
                    "id": str(accommodation.id),
                    "name": accommodation.name,
                    "type": accommodation.accommodation_type,
                    "district": accommodation.district,
                    "rating": accommodation.average_rating,
                    "score": item["score"],
                    "price_range": accommodation.price_range,
                    "amenities": accommodation.amenities,
                    "image": accommodation.images[0] if accommodation.images else None,
                    "location": accommodation.location
                })
            
            return recommendations
            
        except Exception as e:
            return []
    
    async def _calculate_attraction_score(
        self,
        attraction: TouristAttraction,
        user_preferences: Optional[UserPreference],
        location: Optional[Dict[str, float]]
    ) -> float:
        """Calculate recommendation score for attraction"""
        try:
            score = 0.0
            
            # Base score from popularity and rating
            score += attraction.popularity_score * 0.3
            score += attraction.average_rating * 0.2
            
            # User preference matching
            if user_preferences:
                # Interest matching
                if user_preferences.interests:
                    interest_score = 0.0
                    for interest in user_preferences.interests:
                        if interest in ["culture", "history"] and attraction.attraction_type in ["historical", "cultural", "religious"]:
                            interest_score += 0.3
                        elif interest in ["nature", "wildlife"] and attraction.attraction_type in ["natural", "wildlife"]:
                            interest_score += 0.3
                        elif interest in ["adventure"] and attraction.attraction_type in ["adventure"]:
                            interest_score += 0.3
                        elif interest in ["beach", "relaxation"] and attraction.attraction_type in ["beach"]:
                            interest_score += 0.3
                    
                    score += min(interest_score, 0.3)
                
                # Accessibility matching
                if user_preferences.accessibility_needs and "wheelchair" in user_preferences.accessibility_needs:
                    if attraction.wheelchair_accessible:
                        score += 0.2
                
                # Difficulty level matching
                if user_preferences.difficulty_level:
                    difficulty_mapping = {
                        "beginner": "easy",
                        "intermediate": "moderate",
                        "advanced": "challenging"
                    }
                    if attraction.difficulty_level == difficulty_mapping.get(user_preferences.difficulty_level):
                        score += 0.1
            
            # Location proximity (if location provided)
            if location and attraction.location:
                distance = self._calculate_distance(location, attraction.location)
                if distance < 10:  # Within 10km
                    score += 0.2
                elif distance < 50:  # Within 50km
                    score += 0.1
            
            # Featured attractions get bonus
            if attraction.is_featured:
                score += 0.1
            
            return min(score, 1.0)
            
        except Exception:
            return 0.0
    
    async def _calculate_restaurant_score(
        self,
        restaurant: Restaurant,
        user_preferences: Optional[UserPreference],
        location: Optional[Dict[str, float]]
    ) -> float:
        """Calculate recommendation score for restaurant"""
        try:
            score = 0.0
            
            # Base score from rating
            score += restaurant.average_rating * 0.3
            
            # User preference matching
            if user_preferences:
                # Cuisine preference matching
                if user_preferences.interests and "food" in user_preferences.interests:
                    score += 0.2
                
                # Dietary restrictions matching
                if user_preferences.dietary_restrictions:
                    for restriction in user_preferences.dietary_restrictions:
                        if restriction in restaurant.specialties:
                            score += 0.2
            
            # Location proximity
            if location and restaurant.location:
                distance = self._calculate_distance(location, restaurant.location)
                if distance < 5:  # Within 5km
                    score += 0.3
                elif distance < 20:  # Within 20km
                    score += 0.1
            
            return min(score, 1.0)
            
        except Exception:
            return 0.0
    
    async def _calculate_accommodation_score(
        self,
        accommodation: Accommodation,
        user_preferences: Optional[UserPreference],
        location: Optional[Dict[str, float]]
    ) -> float:
        """Calculate recommendation score for accommodation"""
        try:
            score = 0.0
            
            # Base score from rating
            score += accommodation.average_rating * 0.3
            
            # User preference matching
            if user_preferences:
                # Travel style matching
                if user_preferences.travel_style:
                    for style in user_preferences.travel_style:
                        if style == "luxury" and accommodation.accommodation_type in ["hotel", "resort", "villa"]:
                            score += 0.2
                        elif style == "budget" and accommodation.accommodation_type in ["hostel", "guesthouse"]:
                            score += 0.2
                        elif style == "adventure" and accommodation.accommodation_type in ["camping", "hostel"]:
                            score += 0.2
                
                # Budget matching
                if user_preferences.budget_range and accommodation.price_range:
                    user_min = user_preferences.budget_range.get("min", 0)
                    user_max = user_preferences.budget_range.get("max", float('inf'))
                    acc_min = accommodation.price_range.get("min", 0)
                    acc_max = accommodation.price_range.get("max", float('inf'))
                    
                    if user_min <= acc_max and user_max >= acc_min:
                        score += 0.2
            
            # Location proximity
            if location and accommodation.location:
                distance = self._calculate_distance(location, accommodation.location)
                if distance < 10:  # Within 10km
                    score += 0.2
                elif distance < 50:  # Within 50km
                    score += 0.1
            
            return min(score, 1.0)
            
        except Exception:
            return 0.0
    
    def _calculate_distance(self, loc1: Dict[str, float], loc2: Dict[str, float]) -> float:
        """Calculate distance between two locations in kilometers"""
        try:
            import math
            
            lat1, lon1 = loc1["latitude"], loc1["longitude"]
            lat2, lon2 = loc2["latitude"], loc2["longitude"]
            
            # Haversine formula
            R = 6371  # Earth's radius in kilometers
            
            dlat = math.radians(lat2 - lat1)
            dlon = math.radians(lon2 - lon1)
            
            a = (math.sin(dlat/2) * math.sin(dlat/2) +
                 math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
                 math.sin(dlon/2) * math.sin(dlon/2))
            
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            distance = R * c
            
            return distance
            
        except Exception:
            return float('inf')
    
    async def save_recommendation(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
        recommendation_type: str,
        item_id: str,
        item_type: str,
        title: str,
        description: str,
        reason: str,
        confidence_score: float,
        context: Dict[str, Any]
    ) -> str:
        """Save recommendation to database"""
        try:
            recommendation_id = str(uuid.uuid4())
            
            recommendation = Recommendation(
                recommendation_id=recommendation_id,
                user_id=user_id,
                session_id=session_id,
                recommendation_type=recommendation_type,
                item_id=item_id,
                item_type=item_type,
                title=title,
                description=description,
                reason=reason,
                confidence_score=confidence_score,
                context=context,
                algorithm_version="1.0",
                features_used=["collaborative", "content_based", "location"]
            )
            
            await recommendation.insert()
            return recommendation_id
            
        except Exception:
            return ""