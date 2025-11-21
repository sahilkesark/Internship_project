from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.models import Recommendation, StudyPlan
from app.models.schemas import StudyPlanRequest, StudyPlanResponse
from app.services.study_plan_service import generate_study_plan
from app.services.exam_config_service import get_exam_list, get_exam_details

router = APIRouter()

@router.get("/exams")
async def get_available_exams():
    """Get list of all available exams with their details"""
    return {"exams": get_exam_list()}

@router.get("/exams/{exam_code}")
async def get_exam_info(exam_code: str):
    """Get detailed information about a specific exam"""
    exam_details = get_exam_details(exam_code)
    if not exam_details:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam_details

@router.post("/generate", response_model=StudyPlanResponse, status_code=201)
async def create_study_plan(
    request: StudyPlanRequest,
    db: Session = Depends(get_db)
):
    """Generate personalized study plan"""
    
    # Get recommendation
    recommendation = db.query(Recommendation).filter(
        Recommendation.recommendation_id == request.recommendation_id
    ).first()
    
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    # Generate study plan with exam type
    plan_data = generate_study_plan(
        recommendation,
        request.target_date,
        request.hours_per_day,
        db,
        exam_type=request.exam_type
    )
    
    # Save study plan
    study_plan = StudyPlan(
        recommendation_id=recommendation.recommendation_id,
        target_date=request.target_date,
        total_days=plan_data["total_days"],
        hours_per_day=request.hours_per_day,
        total_hours=plan_data["total_hours"],
        modules_data=plan_data["modules"],
        daily_schedule_data=plan_data["daily_schedule"],
        milestones_data=plan_data["milestones"]
    )
    
    db.add(study_plan)
    db.commit()
    db.refresh(study_plan)
    
    # Format response
    response = {
        "plan_id": study_plan.plan_id,
        "recommendation_id": study_plan.recommendation_id,
        "target_date": study_plan.target_date,
        "total_days": study_plan.total_days,
        "hours_per_day": study_plan.hours_per_day,
        "total_hours": study_plan.total_hours,
        "modules": study_plan.modules_data,
        "daily_schedule": study_plan.daily_schedule_data,
        "milestones": study_plan.milestones_data,
        "created_at": study_plan.created_at
    }
    
    return response

@router.get("/{plan_id}", response_model=StudyPlanResponse)
async def get_study_plan(plan_id: str, db: Session = Depends(get_db)):
    """Get study plan details"""
    
    study_plan = db.query(StudyPlan).filter(StudyPlan.plan_id == plan_id).first()
    
    if not study_plan:
        raise HTTPException(status_code=404, detail="Study plan not found")
    
    response = {
        "plan_id": study_plan.plan_id,
        "recommendation_id": study_plan.recommendation_id,
        "target_date": study_plan.target_date,
        "total_days": study_plan.total_days,
        "hours_per_day": study_plan.hours_per_day,
        "total_hours": study_plan.total_hours,
        "modules": study_plan.modules_data,
        "daily_schedule": study_plan.daily_schedule_data,
        "milestones": study_plan.milestones_data,
        "created_at": study_plan.created_at
    }
    
    return response
