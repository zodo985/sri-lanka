from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Dict, Any
from app.models.tourism import TouristAttraction, Restaurant, Accommodation, Transportation, EmergencyService, CulturalEvent
from app.schemas.tourism import (
    TouristAttractionResponse, RestaurantResponse, AccommodationResponse,
    TransportationResponse, EmergencyServiceResponse, CulturalEventResponse,
    AttractionSearchRequest, RestaurantSearchRequest, AccommodationSearchRequest
)
from app.schemas.common import SuccessResponse, PaginatedResponse, PaginationParams
from app.core.exceptions import NotFoundException, ValidationException
from app.services.recommendation_service import RecommendationService
from app.services.translation_service import TranslationService

router = APIRouter()

# Initialize services
recommendation_service = RecommendationService()
translation_service = TranslationService()

@router.get("/attractions", response_model=PaginatedResponse)
async def get_attractions(
    search_request: AttractionSearchRequest = Depends(),
    pagination: PaginationParams = Depends()
):
    """Get tourist attractions with search and pagination"""
    try:
        # Build query
        query = {"is_active": True}
        
        if search_request.query:
            query["$or"] = [
                {"name": {"$regex": search_request.query, "$options": "i"}},
                {"description": {"$regex": search_request.query, "$options": "i"}}
            ]
        
        if search_request.attraction_type:
            query["attraction_type"] = search_request.attraction_type
        
        if search_request.district:
            query["district"] = search_request.district
        
        if search_request.province:
            query["province"] = search_request.province
        
        if search_request.tags:
            query["tags"] = {"$in": search_request.tags}
        
        if search_request.difficulty_level:
            query["difficulty_level"] = search_request.difficulty_level
        
        if search_request.wheelchair_accessible is not None:
            query["wheelchair_accessible"] = search_request.wheelchair_accessible
        
        if search_request.is_featured is not None:
            query["is_featured"] = search_request.is_featured
        
        if search_request.min_rating:
            query["average_rating"] = {"$gte": search_request.min_rating}
        
        # Get attractions with pagination
        skip = (pagination.page - 1) * pagination.limit
        attractions = await TouristAttraction.find(query).skip(skip).limit(pagination.limit).to_list()
        
        # Get total count
        total_count = await TouristAttraction.find(query).count()
        
        # Convert to response format
        attraction_responses = []
        for attraction in attractions:
            attraction_responses.append(TouristAttractionResponse(
                attraction_id=str(attraction.id),
                name=attraction.name,
                name_sinhala=attraction.name_sinhala,
                name_tamil=attraction.name_tamil,
                description=attraction.description,
                description_sinhala=attraction.description_sinhala,
                description_tamil=attraction.description_tamil,
                location=attraction.location,
                address=attraction.address,
                district=attraction.district,
                province=attraction.province,
                attraction_type=attraction.attraction_type,
                tags=attraction.tags,
                difficulty_level=attraction.difficulty_level,
                opening_hours=attraction.opening_hours,
                entrance_fee=attraction.entrance_fee,
                best_time_to_visit=attraction.best_time_to_visit,
                duration_visit=attraction.duration_visit,
                images=attraction.images,
                videos=attraction.videos,
                virtual_tour_url=attraction.virtual_tour_url,
                wheelchair_accessible=attraction.wheelchair_accessible,
                parking_available=attraction.parking_available,
                public_transport=attraction.public_transport,
                contact_phone=attraction.contact_phone,
                contact_email=attraction.contact_email,
                website=attraction.website,
                average_rating=attraction.average_rating,
                total_reviews=attraction.total_reviews,
                popularity_score=attraction.popularity_score,
                is_active=attraction.is_active,
                is_featured=attraction.is_featured,
                created_at=attraction.created_at,
                updated_at=attraction.updated_at
            ))
        
        # Calculate pagination info
        total_pages = (total_count + pagination.limit - 1) // pagination.limit
        has_next = pagination.page < total_pages
        has_prev = pagination.page > 1
        
        return PaginatedResponse(
            data=attraction_responses,
            pagination={
                "page": pagination.page,
                "limit": pagination.limit,
                "total": total_count,
                "pages": total_pages,
                "has_next": has_next,
                "has_prev": has_prev
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get attractions: {str(e)}"
        )

@router.get("/attractions/{attraction_id}", response_model=TouristAttractionResponse)
async def get_attraction(attraction_id: str):
    """Get specific tourist attraction by ID"""
    try:
        attraction = await TouristAttraction.get(attraction_id)
        if not attraction:
            raise NotFoundException("Attraction not found")
        
        return TouristAttractionResponse(
            attraction_id=str(attraction.id),
            name=attraction.name,
            name_sinhala=attraction.name_sinhala,
            name_tamil=attraction.name_tamil,
            description=attraction.description,
            description_sinhala=attraction.description_sinhala,
            description_tamil=attraction.description_tamil,
            location=attraction.location,
            address=attraction.address,
            district=attraction.district,
            province=attraction.province,
            attraction_type=attraction.attraction_type,
            tags=attraction.tags,
            difficulty_level=attraction.difficulty_level,
            opening_hours=attraction.opening_hours,
            entrance_fee=attraction.entrance_fee,
            best_time_to_visit=attraction.best_time_to_visit,
            duration_visit=attraction.duration_visit,
            images=attraction.images,
            videos=attraction.videos,
            virtual_tour_url=attraction.virtual_tour_url,
            wheelchair_accessible=attraction.wheelchair_accessible,
            parking_available=attraction.parking_available,
            public_transport=attraction.public_transport,
            contact_phone=attraction.contact_phone,
            contact_email=attraction.contact_email,
            website=attraction.website,
            average_rating=attraction.average_rating,
            total_reviews=attraction.total_reviews,
            popularity_score=attraction.popularity_score,
            is_active=attraction.is_active,
            is_featured=attraction.is_featured,
            created_at=attraction.created_at,
            updated_at=attraction.updated_at
        )
        
    except NotFoundException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get attraction: {str(e)}"
        )

@router.get("/restaurants", response_model=PaginatedResponse)
async def get_restaurants(
    search_request: RestaurantSearchRequest = Depends(),
    pagination: PaginationParams = Depends()
):
    """Get restaurants with search and pagination"""
    try:
        # Build query
        query = {"is_active": True}
        
        if search_request.query:
            query["$or"] = [
                {"name": {"$regex": search_request.query, "$options": "i"}},
                {"specialties": {"$regex": search_request.query, "$options": "i"}}
            ]
        
        if search_request.cuisine_types:
            query["cuisine_types"] = {"$in": search_request.cuisine_types}
        
        if search_request.district:
            query["district"] = search_request.district
        
        if search_request.city:
            query["city"] = search_request.city
        
        if search_request.price_range:
            query["price_range"] = search_request.price_range
        
        if search_request.delivery_available is not None:
            query["delivery_available"] = search_request.delivery_available
        
        if search_request.outdoor_seating is not None:
            query["outdoor_seating"] = search_request.outdoor_seating
        
        if search_request.min_rating:
            query["average_rating"] = {"$gte": search_request.min_rating}
        
        # Get restaurants with pagination
        skip = (pagination.page - 1) * pagination.limit
        restaurants = await Restaurant.find(query).skip(skip).limit(pagination.limit).to_list()
        
        # Get total count
        total_count = await Restaurant.find(query).count()
        
        # Convert to response format
        restaurant_responses = []
        for restaurant in restaurants:
            restaurant_responses.append(RestaurantResponse(
                restaurant_id=str(restaurant.id),
                name=restaurant.name,
                location=restaurant.location,
                address=restaurant.address,
                district=restaurant.district,
                city=restaurant.city,
                cuisine_types=restaurant.cuisine_types,
                specialties=restaurant.specialties,
                price_range=restaurant.price_range,
                delivery_available=restaurant.delivery_available,
                takeaway_available=restaurant.takeaway_available,
                dine_in_available=restaurant.dine_in_available,
                outdoor_seating=restaurant.outdoor_seating,
                phone=restaurant.phone,
                email=restaurant.email,
                website=restaurant.website,
                opening_hours=restaurant.opening_hours,
                average_rating=restaurant.average_rating,
                total_reviews=restaurant.total_reviews,
                images=restaurant.images,
                menu_images=restaurant.menu_images,
                is_active=restaurant.is_active,
                is_verified=restaurant.is_verified,
                created_at=restaurant.created_at,
                updated_at=restaurant.updated_at
            ))
        
        # Calculate pagination info
        total_pages = (total_count + pagination.limit - 1) // pagination.limit
        has_next = pagination.page < total_pages
        has_prev = pagination.page > 1
        
        return PaginatedResponse(
            data=restaurant_responses,
            pagination={
                "page": pagination.page,
                "limit": pagination.limit,
                "total": total_count,
                "pages": total_pages,
                "has_next": has_next,
                "has_prev": has_prev
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get restaurants: {str(e)}"
        )

@router.get("/accommodations", response_model=PaginatedResponse)
async def get_accommodations(
    search_request: AccommodationSearchRequest = Depends(),
    pagination: PaginationParams = Depends()
):
    """Get accommodations with search and pagination"""
    try:
        # Build query
        query = {"is_active": True}
        
        if search_request.query:
            query["$or"] = [
                {"name": {"$regex": search_request.query, "$options": "i"}},
                {"description": {"$regex": search_request.query, "$options": "i"}}
            ]
        
        if search_request.accommodation_type:
            query["accommodation_type"] = search_request.accommodation_type
        
        if search_request.district:
            query["district"] = search_request.district
        
        if search_request.city:
            query["city"] = search_request.city
        
        if search_request.amenities:
            query["amenities"] = {"$in": search_request.amenities}
        
        if search_request.min_price:
            query["price_range.min"] = {"$gte": search_request.min_price}
        
        if search_request.max_price:
            query["price_range.max"] = {"$lte": search_request.max_price}
        
        if search_request.min_rating:
            query["average_rating"] = {"$gte": search_request.min_rating}
        
        # Get accommodations with pagination
        skip = (pagination.page - 1) * pagination.limit
        accommodations = await Accommodation.find(query).skip(skip).limit(pagination.limit).to_list()
        
        # Get total count
        total_count = await Accommodation.find(query).count()
        
        # Convert to response format
        accommodation_responses = []
        for accommodation in accommodations:
            accommodation_responses.append(AccommodationResponse(
                accommodation_id=str(accommodation.id),
                name=accommodation.name,
                accommodation_type=accommodation.accommodation_type,
                location=accommodation.location,
                address=accommodation.address,
                district=accommodation.district,
                city=accommodation.city,
                description=accommodation.description,
                amenities=accommodation.amenities,
                room_types=accommodation.room_types,
                price_range=accommodation.price_range,
                currency=accommodation.currency,
                phone=accommodation.phone,
                email=accommodation.email,
                website=accommodation.website,
                average_rating=accommodation.average_rating,
                total_reviews=accommodation.total_reviews,
                images=accommodation.images,
                is_active=accommodation.is_active,
                is_verified=accommodation.is_verified,
                created_at=accommodation.created_at,
                updated_at=accommodation.updated_at
            ))
        
        # Calculate pagination info
        total_pages = (total_count + pagination.limit - 1) // pagination.limit
        has_next = pagination.page < total_pages
        has_prev = pagination.page > 1
        
        return PaginatedResponse(
            data=accommodation_responses,
            pagination={
                "page": pagination.page,
                "limit": pagination.limit,
                "total": total_count,
                "pages": total_pages,
                "has_next": has_next,
                "has_prev": has_prev
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get accommodations: {str(e)}"
        )

@router.get("/transportation", response_model=List[TransportationResponse])
async def get_transportation_options():
    """Get transportation options"""
    try:
        transportation = await Transportation.find({"is_active": True}).to_list()
        
        transportation_responses = []
        for transport in transportation:
            transportation_responses.append(TransportationResponse(
                transportation_id=str(transport.id),
                name=transport.name,
                transport_type=transport.transport_type,
                from_location=transport.from_location,
                to_location=transport.to_location,
                route_description=transport.route_description,
                departure_times=transport.departure_times,
                duration_minutes=transport.duration_minutes,
                frequency=transport.frequency,
                price_range=transport.price_range,
                currency=transport.currency,
                phone=transport.phone,
                website=transport.website,
                features=transport.features,
                is_active=transport.is_active,
                is_operational=transport.is_operational,
                created_at=transport.created_at,
                updated_at=transport.updated_at
            ))
        
        return transportation_responses
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get transportation options: {str(e)}"
        )

@router.get("/emergency-services", response_model=List[EmergencyServiceResponse])
async def get_emergency_services():
    """Get emergency services and contacts"""
    try:
        services = await EmergencyService.find({"is_active": True}).to_list()
        
        service_responses = []
        for service in services:
            service_responses.append(EmergencyServiceResponse(
                service_id=str(service.id),
                service_name=service.service_name,
                service_type=service.service_type,
                phone=service.phone,
                emergency_phone=service.emergency_phone,
                email=service.email,
                location=service.location,
                address=service.address,
                district=service.district,
                description=service.description,
                operating_hours=service.operating_hours,
                languages_supported=service.languages_supported,
                is_active=service.is_active,
                is_24_hours=service.is_24_hours,
                created_at=service.created_at,
                updated_at=service.updated_at
            ))
        
        return service_responses
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get emergency services: {str(e)}"
        )

@router.get("/cultural-events", response_model=List[CulturalEventResponse])
async def get_cultural_events():
    """Get cultural events and festivals"""
    try:
        events = await CulturalEvent.find({"is_active": True}).to_list()
        
        event_responses = []
        for event in events:
            event_responses.append(CulturalEventResponse(
                event_id=str(event.id),
                name=event.name,
                name_sinhala=event.name_sinhala,
                name_tamil=event.name_tamil,
                description=event.description,
                event_type=event.event_type,
                start_date=event.start_date,
                end_date=event.end_date,
                is_recurring=event.is_recurring,
                recurrence_pattern=event.recurrence_pattern,
                location=event.location,
                venue=event.venue,
                district=event.district,
                entry_fee=event.entry_fee,
                currency=event.currency,
                age_restriction=event.age_restriction,
                dress_code=event.dress_code,
                images=event.images,
                videos=event.videos,
                is_active=event.is_active,
                is_featured=event.is_featured,
                created_at=event.created_at,
                updated_at=event.updated_at
            ))
        
        return event_responses
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get cultural events: {str(e)}"
        )

@router.get("/featured", response_model=Dict[str, List[Any]])
async def get_featured_content():
    """Get featured attractions, restaurants, and accommodations"""
    try:
        # Get featured attractions
        featured_attractions = await TouristAttraction.find(
            {"is_featured": True, "is_active": True}
        ).limit(5).to_list()
        
        # Get featured restaurants
        featured_restaurants = await Restaurant.find(
            {"is_featured": True, "is_active": True}
        ).limit(5).to_list()
        
        # Get featured accommodations
        featured_accommodations = await Accommodation.find(
            {"is_featured": True, "is_active": True}
        ).limit(5).to_list()
        
        return {
            "attractions": [
                {
                    "id": str(attraction.id),
                    "name": attraction.name,
                    "type": attraction.attraction_type,
                    "district": attraction.district,
                    "rating": attraction.average_rating,
                    "image": attraction.images[0] if attraction.images else None
                }
                for attraction in featured_attractions
            ],
            "restaurants": [
                {
                    "id": str(restaurant.id),
                    "name": restaurant.name,
                    "cuisine_types": restaurant.cuisine_types,
                    "district": restaurant.district,
                    "rating": restaurant.average_rating,
                    "image": restaurant.images[0] if restaurant.images else None
                }
                for restaurant in featured_restaurants
            ],
            "accommodations": [
                {
                    "id": str(accommodation.id),
                    "name": accommodation.name,
                    "type": accommodation.accommodation_type,
                    "district": accommodation.district,
                    "rating": accommodation.average_rating,
                    "image": accommodation.images[0] if accommodation.images else None
                }
                for accommodation in featured_accommodations
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get featured content: {str(e)}"
        )