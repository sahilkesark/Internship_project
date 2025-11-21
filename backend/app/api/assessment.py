from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.models.database import get_db
from app.models.models import User, Assessment
from app.models.schemas import (
    PersonalDetailsRequest, PhysicalDetailsRequest, EducationDetailsRequest,
    OLQSubmissionRequest, AssessmentResponse, OLQQuestion, OLQ_QUESTIONS
)
from app.services.olq_service import calculate_olq_score
from app.services.question_bank_service import get_randomized_questions, validate_answers, get_category_insights

router = APIRouter()

# Store session questions temporarily (in production, use Redis or database)
SESSION_QUESTIONS = {}

@router.post("/start", response_model=AssessmentResponse, status_code=201)
async def start_assessment(personal_data: PersonalDetailsRequest, db: Session = Depends(get_db)):
    """Start a new assessment with personal details"""
    
    # Check if user exists, if not create
    user = db.query(User).filter(User.email == personal_data.email).first()
    if not user:
        user = User(
            full_name=personal_data.full_name,
            email=personal_data.email,
            phone=personal_data.phone,
            date_of_birth=personal_data.date_of_birth,
            gender=personal_data.gender,
            nationality=personal_data.nationality,
            state=personal_data.state,
            city=personal_data.city
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Create new assessment
    assessment = Assessment(
        user_id=user.user_id,
        completed=False
    )
    
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    
    return assessment

@router.put("/{assessment_id}/physical", response_model=AssessmentResponse)
async def update_physical_details(
    assessment_id: str,
    physical_data: PhysicalDetailsRequest,
    db: Session = Depends(get_db)
):
    """Update assessment with physical details"""
    
    assessment = db.query(Assessment).filter(Assessment.assessment_id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Update physical details
    assessment.height_cm = physical_data.height_cm
    assessment.weight_kg = physical_data.weight_kg
    assessment.eyesight_left = physical_data.eyesight_left
    assessment.eyesight_right = physical_data.eyesight_right
    assessment.has_medical_conditions = physical_data.has_medical_conditions
    assessment.medical_conditions_description = physical_data.medical_conditions_description
    assessment.tattoos = physical_data.tattoos
    assessment.previous_injuries = physical_data.previous_injuries
    
    db.commit()
    db.refresh(assessment)
    
    return assessment

@router.put("/{assessment_id}/education", response_model=AssessmentResponse)
async def update_education_details(
    assessment_id: str,
    education_data: EducationDetailsRequest,
    db: Session = Depends(get_db)
):
    """Update assessment with education details"""
    
    assessment = db.query(Assessment).filter(Assessment.assessment_id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Update education details
    assessment.highest_education = education_data.highest_education
    assessment.stream = education_data.stream
    assessment.university = education_data.university
    assessment.graduation_year = education_data.graduation_year
    assessment.percentage_or_cgpa = education_data.percentage_or_cgpa
    assessment.additional_qualifications = education_data.additional_qualifications
    assessment.has_ncc = education_data.has_ncc
    assessment.ncc_certificate = education_data.ncc_certificate
    
    db.commit()
    db.refresh(assessment)
    
    return assessment

@router.get("/olq-questions")
async def get_olq_questions(num_questions: int = 10, difficulty: str = None):
    """Get randomized OLQ questions with varied correct answers"""
    session_id = str(uuid.uuid4())
    questions = get_randomized_questions(num_questions, difficulty)
    
    # Store questions for this session (for validation later)
    SESSION_QUESTIONS[session_id] = questions
    
    # Return only frontend-safe data (no correct answers)
    frontend_questions = [q['frontend'] for q in questions]
    
    return {
        "session_id": session_id,
        "questions": frontend_questions,
        "total_questions": len(frontend_questions),
        "note": "Questions are randomized. Options are shuffled. Answer index varies per question."
    }

@router.get("/olq-questions-legacy", response_model=List[OLQQuestion])
async def get_olq_questions_legacy():
    """Get OLQ questions (legacy endpoint - not randomized)"""
    return OLQ_QUESTIONS

@router.post("/olq", response_model=AssessmentResponse)
async def submit_olq_responses(
    olq_data: OLQSubmissionRequest,
    db: Session = Depends(get_db),
    session_id: str = None
):
    """Submit OLQ responses and calculate score with AI-powered analysis"""
    
    assessment = db.query(Assessment).filter(
        Assessment.assessment_id == olq_data.assessment_id
    ).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Calculate OLQ score
    if session_id and session_id in SESSION_QUESTIONS:
        # Use new validation with randomized questions
        session_questions = SESSION_QUESTIONS[session_id]
        responses_list = [r.dict() for r in olq_data.responses]
        
        validation_result = validate_answers(responses_list, session_questions)
        olq_score = validation_result['total_score']
        
        # Get category-wise insights
        insights = get_category_insights(validation_result['category_analysis'])
        
        # Store detailed analysis
        assessment.olq_responses = responses_list
        assessment.olq_score = olq_score
        
        # Clean up session
        del SESSION_QUESTIONS[session_id]
    else:
        # Fallback to old method for backward compatibility
        olq_score = calculate_olq_score(olq_data.responses)
        assessment.olq_responses = [r.dict() for r in olq_data.responses]
        assessment.olq_score = olq_score
    
    assessment.completed = True
    
    db.commit()
    db.refresh(assessment)
    
    return assessment

@router.get("/{assessment_id}", response_model=AssessmentResponse)
async def get_assessment(assessment_id: str, db: Session = Depends(get_db)):
    """Get assessment details"""
    
    assessment = db.query(Assessment).filter(Assessment.assessment_id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    return assessment
