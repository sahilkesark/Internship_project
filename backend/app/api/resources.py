from fastapi import APIRouter, HTTPException

from app.models.schemas import ResourcesResponse
from app.services.resources_service import get_role_resources

router = APIRouter()

@router.get("/{role}", response_model=ResourcesResponse)
async def get_resources(role: str):
    """Get curated resources for a specific role"""
    
    resources = get_role_resources(role)
    
    if not resources:
        raise HTTPException(status_code=404, detail=f"Resources not found for role: {role}")
    
    return resources
