from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.models.feedback import Feedback, Review, FeedbackType, FeedbackRating
from app.schemas.common import SuccessResponse, PaginatedResponse, PaginationParams
from app.core.exceptions import ValidationException, NotFoundException
from app.core.security import verify_token
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
import uuid

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/submit")
async def submit_feedback(
    feedback_type: FeedbackType,
    rating: FeedbackRating,
    comment: Optional[str] = None,
    item_id: Optional[str] = None,
    item_type: Optional[str] = None,
    session_id: Optional[str] = None,
    token: Optional[str] = Depends(oauth2_scheme)
):
    """Submit user feedback"""
    try:
        user_id = None
        if token:
            payload = verify_token(token)
            user_id = payload.get("sub")
        
        feedback_id = str(uuid.uuid4())
        
        feedback = Feedback(
            feedback_id=feedback_id,
            user_id=user_id,
            session_id=session_id,
            feedback_type=feedback_type,
            rating=rating,
            comment=comment,
            item_id=item_id,
            item_type=item_type
        )
        
        await feedback.insert()
        
        return SuccessResponse(
            message="Feedback submitted successfully",
            data={"feedback_id": feedback_id}
        )
        
    except ValidationException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit feedback: {str(e)}"
        )

@router.get("/my-feedback", response_model=PaginatedResponse)
async def get_my_feedback(
    pagination: PaginationParams = Depends(),
    token: str = Depends(oauth2_scheme)
):
    """Get current user's feedback"""
    try:
        # Verify token
        payload = verify_token(token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise ValidationException("Invalid token")
        
        # Get feedback with pagination
        skip = (pagination.page - 1) * pagination.limit
        feedback_list = await Feedback.find(
            Feedback.user_id == user_id
        ).sort("created_at", -1).skip(skip).limit(pagination.limit).to_list()
        
        # Get total count
        total_count = await Feedback.find(Feedback.user_id == user_id).count()
        
        # Convert to response format
        feedback_data = []
        for feedback in feedback_list:
            feedback_data.append({
                "feedback_id": feedback.feedback_id,
                "feedback_type": feedback.feedback_type,
                "rating": feedback.rating,
                "comment": feedback.comment,
                "item_id": feedback.item_id,
                "item_type": feedback.item_type,
                "created_at": feedback.created_at,
                "is_processed": feedback.is_processed,
                "admin_response": feedback.admin_response
            })
        
        # Calculate pagination info
        total_pages = (total_count + pagination.limit - 1) // pagination.limit
        has_next = pagination.page < total_pages
        has_prev = pagination.page > 1
        
        return PaginatedResponse(
            data=feedback_data,
            pagination={
                "page": pagination.page,
                "limit": pagination.limit,
                "total": total_count,
                "pages": total_pages,
                "has_next": has_next,
                "has_prev": has_prev
            }
        )
        
    except (ValidationException, NotFoundException):
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get feedback: {str(e)}"
        )

@router.post("/review")
async def submit_review(
    item_id: str,
    item_type: str,
    title: str,
    content: str,
    rating: int,
    visit_date: Optional[str] = None,
    visit_type: Optional[str] = None,
    images: Optional[List[str]] = None,
    token: str = Depends(oauth2_scheme)
):
    """Submit a detailed review"""
    try:
        # Verify token
        payload = verify_token(token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise ValidationException("Invalid token")
        
        if not (1 <= rating <= 5):
            raise ValidationException("Rating must be between 1 and 5")
        
        review_id = str(uuid.uuid4())
        
        review = Review(
            review_id=review_id,
            user_id=user_id,
            item_id=item_id,
            item_type=item_type,
            title=title,
            content=content,
            rating=rating,
            visit_date=datetime.fromisoformat(visit_date) if visit_date else None,
            visit_type=visit_type,
            images=images or []
        )
        
        await review.insert()
        
        return SuccessResponse(
            message="Review submitted successfully",
            data={"review_id": review_id}
        )
        
    except ValidationException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit review: {str(e)}"
        )

@router.get("/reviews/{item_id}")
async def get_item_reviews(
    item_id: str,
    item_type: str,
    pagination: PaginationParams = Depends()
):
    """Get reviews for a specific item"""
    try:
        # Get reviews with pagination
        skip = (pagination.page - 1) * pagination.limit
        reviews = await Review.find(
            Review.item_id == item_id,
            Review.item_type == item_type,
            Review.is_approved == True
        ).sort("created_at", -1).skip(skip).limit(pagination.limit).to_list()
        
        # Get total count
        total_count = await Review.find(
            Review.item_id == item_id,
            Review.item_type == item_type,
            Review.is_approved == True
        ).count()
        
        # Convert to response format
        review_data = []
        for review in reviews:
            review_data.append({
                "review_id": review.review_id,
                "user_id": review.user_id,
                "title": review.title,
                "content": review.content,
                "rating": review.rating,
                "visit_date": review.visit_date,
                "visit_type": review.visit_type,
                "images": review.images,
                "helpful_votes": review.helpful_votes,
                "not_helpful_votes": review.not_helpful_votes,
                "is_featured": review.is_featured,
                "created_at": review.created_at
            })
        
        # Calculate pagination info
        total_pages = (total_count + pagination.limit - 1) // pagination.limit
        has_next = pagination.page < total_pages
        has_prev = pagination.page > 1
        
        return PaginatedResponse(
            data=review_data,
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
            detail=f"Failed to get reviews: {str(e)}"
        )

@router.post("/review/{review_id}/vote")
async def vote_on_review(
    review_id: str,
    helpful: bool,
    token: str = Depends(oauth2_scheme)
):
    """Vote on a review (helpful or not helpful)"""
    try:
        # Verify token
        payload = verify_token(token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise ValidationException("Invalid token")
        
        # Get review
        review = await Review.find_one(Review.review_id == review_id)
        if not review:
            raise NotFoundException("Review not found")
        
        # Update vote counts
        if helpful:
            review.helpful_votes += 1
        else:
            review.not_helpful_votes += 1
        
        await review.save()
        
        return SuccessResponse(
            message="Vote recorded successfully",
            data={
                "helpful_votes": review.helpful_votes,
                "not_helpful_votes": review.not_helpful_votes
            }
        )
        
    except (ValidationException, NotFoundException):
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to vote on review: {str(e)}"
        )