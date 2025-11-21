from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os

from app.models.database import get_db
from app.models.models import Assessment, Recommendation
from app.models.schemas import RecommendationRequest, RecommendationResponse
from app.services.recommendation_service import generate_recommendations
from app.services.pdf_service import generate_recommendation_pdf

router = APIRouter()

@router.post("/generate", response_model=RecommendationResponse, status_code=201)
async def create_recommendation(
    request: RecommendationRequest,
    db: Session = Depends(get_db)
):
    """Generate career recommendations based on assessment"""
    
    # Get assessment
    assessment = db.query(Assessment).filter(
        Assessment.assessment_id == request.assessment_id
    ).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    if not assessment.completed:
        raise HTTPException(status_code=400, detail="Assessment not completed")
    
    # Generate recommendations
    recommendation_data = generate_recommendations(assessment, db)
    
    # Save recommendation
    recommendation = Recommendation(
        assessment_id=assessment.assessment_id,
        user_id=assessment.user_id,
        olq_score=assessment.olq_score,
        primary_category=recommendation_data["primary_category"],
        recommendations_data=recommendation_data["recommendations"],
        explanation=recommendation_data["explanation"],
        ml_model_version="1.0"
    )
    
    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)
    
    # Format response
    response = {
        "recommendation_id": recommendation.recommendation_id,
        "assessment_id": recommendation.assessment_id,
        "user_id": recommendation.user_id,
        "olq_score": recommendation.olq_score,
        "primary_category": recommendation.primary_category,
        "recommendations": recommendation.recommendations_data,
        "explanation": recommendation.explanation,
        "generated_at": recommendation.generated_at
    }
    
    return response

@router.get("/{recommendation_id}", response_model=RecommendationResponse)
async def get_recommendation(recommendation_id: str, db: Session = Depends(get_db)):
    """Get recommendation details"""
    
    recommendation = db.query(Recommendation).filter(
        Recommendation.recommendation_id == recommendation_id
    ).first()
    
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    response = {
        "recommendation_id": recommendation.recommendation_id,
        "assessment_id": recommendation.assessment_id,
        "user_id": recommendation.user_id,
        "olq_score": recommendation.olq_score,
        "primary_category": recommendation.primary_category,
        "recommendations": recommendation.recommendations_data,
        "explanation": recommendation.explanation,
        "generated_at": recommendation.generated_at
    }
    
    return response

@router.get("/{recommendation_id}/export")
async def export_recommendation(recommendation_id: str, db: Session = Depends(get_db)):
    """Export recommendation as PDF"""
    
    recommendation = db.query(Recommendation).filter(
        Recommendation.recommendation_id == recommendation_id
    ).first()
    
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    # Get assessment and user details
    assessment = db.query(Assessment).filter(
        Assessment.assessment_id == recommendation.assessment_id
    ).first()
    
    # Generate PDF
    pdf_path = generate_recommendation_pdf(recommendation, assessment)
    
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"career_recommendation_{recommendation_id}.pdf"
    )
