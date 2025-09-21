from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional, Dict, Any
from app.schemas.common import SuccessResponse, PaginatedResponse, PaginationParams
from app.core.exceptions import ValidationException, AuthorizationException
from app.core.security import verify_token
from app.models.user import User, UserRole
from app.models.feedback import Feedback, Review
from app.models.analytics import Analytics
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_admin(token: str = Depends(oauth2_scheme)):
    """Get current admin user"""
    payload = verify_token(token)
    user_id = payload.get("sub")
    
    user = await User.get(user_id)
    if not user or user.role not in [UserRole.ADMIN, UserRole.MODERATOR]:
        raise AuthorizationException("Admin access required")
    
    return user

@router.get("/dashboard")
async def get_admin_dashboard(
    admin: User = Depends(get_current_admin)
):
    """Get admin dashboard statistics"""
    try:
        # Get basic statistics
        total_users = await User.find().count()
        active_users = await User.find(User.status == "active").count()
        total_feedback = await Feedback.find().count()
        total_reviews = await Review.find().count()
        
        # Get recent feedback
        recent_feedback = await Feedback.find().sort("created_at", -1).limit(5).to_list()
        
        # Get pending reviews
        pending_reviews = await Review.find(Review.is_approved == False).count()
        
        return SuccessResponse(
            message="Dashboard data retrieved successfully",
            data={
                "statistics": {
                    "total_users": total_users,
                    "active_users": active_users,
                    "total_feedback": total_feedback,
                    "total_reviews": total_reviews,
                    "pending_reviews": pending_reviews
                },
                "recent_feedback": [
                    {
                        "feedback_id": feedback.feedback_id,
                        "feedback_type": feedback.feedback_type,
                        "rating": feedback.rating,
                        "comment": feedback.comment,
                        "created_at": feedback.created_at
                    }
                    for feedback in recent_feedback
                ]
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get dashboard data: {str(e)}"
        )

@router.get("/feedback", response_model=PaginatedResponse)
async def get_all_feedback(
    pagination: PaginationParams = Depends(),
    feedback_type: Optional[str] = None,
    rating: Optional[str] = None,
    admin: User = Depends(get_current_admin)
):
    """Get all feedback with filtering"""
    try:
        # Build query
        query = {}
        if feedback_type:
            query["feedback_type"] = feedback_type
        if rating:
            query["rating"] = rating
        
        # Get feedback with pagination
        skip = (pagination.page - 1) * pagination.limit
        feedback_list = await Feedback.find(query).sort("created_at", -1).skip(skip).limit(pagination.limit).to_list()
        
        # Get total count
        total_count = await Feedback.find(query).count()
        
        # Convert to response format
        feedback_data = []
        for feedback in feedback_list:
            feedback_data.append({
                "feedback_id": feedback.feedback_id,
                "user_id": feedback.user_id,
                "session_id": feedback.session_id,
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
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get feedback: {str(e)}"
        )

@router.put("/feedback/{feedback_id}/process")
async def process_feedback(
    feedback_id: str,
    admin_response: str,
    admin: User = Depends(get_current_admin)
):
    """Process feedback with admin response"""
    try:
        # Get feedback
        feedback = await Feedback.find_one(Feedback.feedback_id == feedback_id)
        if not feedback:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Feedback not found"
            )
        
        # Update feedback
        feedback.is_processed = True
        feedback.is_acknowledged = True
        feedback.admin_response = admin_response
        feedback.admin_user_id = str(admin.id)
        feedback.processed_at = datetime.utcnow()
        
        await feedback.save()
        
        return SuccessResponse(
            message="Feedback processed successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process feedback: {str(e)}"
        )

@router.get("/reviews", response_model=PaginatedResponse)
async def get_all_reviews(
    pagination: PaginationParams = Depends(),
    is_approved: Optional[bool] = None,
    admin: User = Depends(get_current_admin)
):
    """Get all reviews with filtering"""
    try:
        # Build query
        query = {}
        if is_approved is not None:
            query["is_approved"] = is_approved
        
        # Get reviews with pagination
        skip = (pagination.page - 1) * pagination.limit
        reviews = await Review.find(query).sort("created_at", -1).skip(skip).limit(pagination.limit).to_list()
        
        # Get total count
        total_count = await Review.find(query).count()
        
        # Convert to response format
        review_data = []
        for review in reviews:
            review_data.append({
                "review_id": review.review_id,
                "user_id": review.user_id,
                "item_id": review.item_id,
                "item_type": review.item_type,
                "title": review.title,
                "content": review.content,
                "rating": review.rating,
                "is_approved": review.is_approved,
                "is_flagged": review.is_flagged,
                "moderation_notes": review.moderation_notes,
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

@router.put("/reviews/{review_id}/approve")
async def approve_review(
    review_id: str,
    admin: User = Depends(get_current_admin)
):
    """Approve a review"""
    try:
        # Get review
        review = await Review.find_one(Review.review_id == review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found"
            )
        
        # Update review
        review.is_approved = True
        review.moderation_notes = f"Approved by admin {admin.username}"
        
        await review.save()
        
        return SuccessResponse(
            message="Review approved successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to approve review: {str(e)}"
        )

@router.put("/reviews/{review_id}/reject")
async def reject_review(
    review_id: str,
    reason: str,
    admin: User = Depends(get_current_admin)
):
    """Reject a review"""
    try:
        # Get review
        review = await Review.find_one(Review.review_id == review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found"
            )
        
        # Update review
        review.is_approved = False
        review.moderation_notes = f"Rejected by admin {admin.username}: {reason}"
        
        await review.save()
        
        return SuccessResponse(
            message="Review rejected successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reject review: {str(e)}"
        )

@router.get("/analytics")
async def get_analytics(
    days: int = 30,
    admin: User = Depends(get_current_admin)
):
    """Get analytics data"""
    try:
        # Get analytics for the specified number of days
        from datetime import datetime, timedelta
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days)
        
        analytics = await Analytics.find(
            Analytics.date >= start_date,
            Analytics.date <= end_date
        ).sort("date", -1).to_list()
        
        # Process analytics data
        analytics_data = {
            "period": f"{days} days",
            "total_users": sum(a.total_users for a in analytics),
            "active_users": sum(a.active_users for a in analytics),
            "total_messages": sum(a.total_messages for a in analytics),
            "total_sessions": sum(a.total_sessions for a in analytics),
            "average_session_duration": sum(a.average_session_duration for a in analytics) / len(analytics) if analytics else 0,
            "language_usage": {},
            "feature_usage": {},
            "satisfaction_score": sum(a.satisfaction_score for a in analytics) / len(analytics) if analytics else 0
        }
        
        # Aggregate language usage
        for analytics_item in analytics:
            for lang, count in analytics_item.language_usage.items():
                analytics_data["language_usage"][lang] = analytics_data["language_usage"].get(lang, 0) + count
        
        # Aggregate feature usage
        for analytics_item in analytics:
            for feature, count in analytics_item.feature_usage.items():
                analytics_data["feature_usage"][feature] = analytics_data["feature_usage"].get(feature, 0) + count
        
        return SuccessResponse(
            message="Analytics data retrieved successfully",
            data=analytics_data
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get analytics: {str(e)}"
        )