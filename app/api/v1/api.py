from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    users,
    chat,
    tourism,
    recommendations,
    feedback,
    admin
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(tourism.router, prefix="/tourism", tags=["Tourism"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
api_router.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])