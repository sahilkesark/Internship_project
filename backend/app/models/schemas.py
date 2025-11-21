from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum

# Enums
class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class EducationLevel(str, Enum):
    HIGH_SCHOOL = "high_school"
    INTERMEDIATE = "intermediate"
    BACHELORS = "bachelors"
    MASTERS = "masters"
    DOCTORATE = "doctorate"

class Stream(str, Enum):
    SCIENCE = "science"
    COMMERCE = "commerce"
    ARTS = "arts"
    ENGINEERING = "engineering"
    MEDICAL = "medical"
    LAW = "law"
    OTHER = "other"

class RoleCategory(str, Enum):
    OFFICER = "officer"
    ENLISTED = "enlisted"
    CIVIL_SERVICES = "civil_services"

# Request Schemas
class PersonalDetailsRequest(BaseModel):
    user_id: Optional[str] = None
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., pattern=r"^\+?[1-9]\d{9,14}$")
    date_of_birth: date
    gender: Gender
    nationality: str = "Indian"
    state: str
    city: str

class PhysicalDetailsRequest(BaseModel):
    height_cm: float = Field(..., ge=140, le=220)
    weight_kg: float = Field(..., ge=40, le=150)
    eyesight_left: float = Field(..., ge=0, le=10)
    eyesight_right: float = Field(..., ge=0, le=10)
    has_medical_conditions: bool = False
    medical_conditions_description: Optional[str] = None
    tattoos: bool = False
    previous_injuries: bool = False

class EducationDetailsRequest(BaseModel):
    highest_education: EducationLevel
    stream: Stream
    university: str
    graduation_year: int = Field(..., ge=1990, le=2030)
    percentage_or_cgpa: float = Field(..., ge=0, le=100)
    additional_qualifications: Optional[List[str]] = []
    has_ncc: bool = False
    ncc_certificate: Optional[str] = None

class OLQQuestion(BaseModel):
    question_id: int
    question: str
    options: List[str]

class OLQResponse(BaseModel):
    question_id: int
    selected_option: int  # 0-based index

class OLQSubmissionRequest(BaseModel):
    assessment_id: str
    responses: List[OLQResponse]

class RecommendationRequest(BaseModel):
    assessment_id: str

class StudyPlanRequest(BaseModel):
    recommendation_id: str
    target_date: date
    hours_per_day: float = Field(..., ge=1, le=16)
    preferred_study_times: Optional[List[str]] = []
    exam_type: Optional[str] = None  # NDA, CDS, AFCAT, UPSC_CSE, SSC_CGL, State_PSC

# Response Schemas
class UserResponse(BaseModel):
    user_id: str
    full_name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class AssessmentResponse(BaseModel):
    assessment_id: str
    user_id: str
    olq_score: Optional[float] = None
    completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RoleRecommendation(BaseModel):
    role_name: str
    role_category: RoleCategory
    entry_scheme: str
    match_score: float
    min_age: float  # Changed to float to support ages like 16.5 years
    max_age: float  # Changed to float to support ages like 19.5 years
    education_requirement: str
    physical_standards: Dict[str, Any]
    selection_process: List[str]
    reasoning: str
    feature_importance: Dict[str, float]

class RecommendationResponse(BaseModel):
    recommendation_id: str
    assessment_id: str
    user_id: str
    olq_score: float
    primary_category: RoleCategory
    recommendations: List[RoleRecommendation]
    explanation: str
    generated_at: datetime

    class Config:
        from_attributes = True

class StudyModule(BaseModel):
    module_name: str
    topics: List[str]
    estimated_hours: float
    priority: int
    week_number: int

class DailySchedule(BaseModel):
    date: date
    modules: List[str]
    hours_allocated: float
    topics_covered: List[str]

class StudyPlanResponse(BaseModel):
    plan_id: str
    recommendation_id: str
    target_date: date
    total_days: int
    hours_per_day: float
    total_hours: float
    modules: List[StudyModule]
    daily_schedule: List[DailySchedule]
    milestones: List[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True

class Resource(BaseModel):
    title: str
    type: str  # book, video, website, pdf, course
    url: Optional[str] = None
    description: str
    relevance_score: float
    is_free: bool

class ResourcesResponse(BaseModel):
    role: str
    resources: List[Resource]
    study_tips: List[str]
    exam_pattern: Dict[str, Any]
    previous_papers: List[Dict[str, str]]

# OLQ Questions
OLQ_QUESTIONS = [
    {
        "question_id": 1,
        "question": "You are leading a team on a challenging project with a tight deadline. One of your team members is struggling. What do you do?",
        "options": [
            "Take over their work to ensure quality and meet the deadline",
            "Provide guidance, redistribute tasks if needed, and monitor progress closely",
            "Let them figure it out on their own to build independence",
            "Report the issue to higher management immediately"
        ],
        "correct_option": 1,
        "weight": 10
    },
    {
        "question_id": 2,
        "question": "During a high-pressure situation, your superior gives you an order that you believe might not be the most effective approach. What would you do?",
        "options": [
            "Follow the order without question as they have more experience",
            "Politely present your alternative suggestion with reasoning and follow their final decision",
            "Refuse to follow and implement your own plan",
            "Follow the order but document your concerns for later"
        ],
        "correct_option": 1,
        "weight": 10
    },
    {
        "question_id": 3,
        "question": "You witness a colleague taking credit for work that was actually done by your team. How do you respond?",
        "options": [
            "Confront them publicly in the next meeting",
            "Privately address the issue with them first, then escalate if needed",
            "Ignore it to avoid conflict",
            "Take credit for their work next time"
        ],
        "correct_option": 1,
        "weight": 10
    },
    {
        "question_id": 4,
        "question": "You are assigned to work in a remote area with limited resources for an extended period. How do you feel about this?",
        "options": [
            "Concerned and would try to get the assignment changed",
            "View it as a challenge and opportunity to prove adaptability and leadership",
            "Accept it reluctantly as part of duty",
            "Would consider it a punishment"
        ],
        "correct_option": 1,
        "weight": 10
    },
    {
        "question_id": 5,
        "question": "You discover a more efficient process that could save time and resources, but it requires changing established procedures. What do you do?",
        "options": [
            "Keep it to yourself to avoid complications",
            "Document the proposal with data and present it through proper channels",
            "Implement it immediately without approval",
            "Share it informally with colleagues but take no formal action"
        ],
        "correct_option": 1,
        "weight": 10
    },
    {
        "question_id": 6,
        "question": "Your team is demoralized after a failed mission/project. As a leader, what is your priority?",
        "options": [
            "Identify who made mistakes and take disciplinary action",
            "Analyze what went wrong, learn from it, and motivate the team for future success",
            "Move on quickly to the next task without discussion",
            "Blame external factors to protect the team"
        ],
        "correct_option": 1,
        "weight": 10
    },
    {
        "question_id": 7,
        "question": "You have to choose between a comfortable desk job with better facilities or a challenging field position with more responsibility. What would you prefer?",
        "options": [
            "Definitely the comfortable desk job",
            "The challenging field position for growth and experience",
            "Whichever pays more",
            "Would try to negotiate for desk job with same responsibility"
        ],
        "correct_option": 1,
        "weight": 10
    },
    {
        "question_id": 8,
        "question": "During a crisis, you need to make a quick decision with incomplete information. How do you proceed?",
        "options": [
            "Wait for complete information even if it delays action",
            "Assess available facts, consider risks, make the best possible decision and act",
            "Pass the decision to someone else",
            "Make a random choice and hope for the best"
        ],
        "correct_option": 1,
        "weight": 10
    },
    {
        "question_id": 9,
        "question": "You are given feedback that your communication style is sometimes too direct and affects team morale. How do you respond?",
        "options": [
            "Ignore the feedback as direct communication is effective",
            "Reflect on it, seek specific examples, and work on balancing directness with empathy",
            "Become overly cautious and stop giving honest feedback",
            "Defend your style and explain why it's necessary"
        ],
        "correct_option": 1,
        "weight": 10
    },
    {
        "question_id": 10,
        "question": "You have limited resources and must choose between two critical tasks. Both are important but you can only prioritize one. How do you decide?",
        "options": [
            "Choose the easier task to ensure completion",
            "Analyze impact, urgency, and long-term consequences, then decide based on overall benefit",
            "Try to do both partially",
            "Seek approval from superior without providing your analysis"
        ],
        "correct_option": 1,
        "weight": 10
    }
]
