from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Date, JSON, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base
from app.models.schemas import Gender, EducationLevel, Stream, RoleCategory
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, default=generate_uuid)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(20))
    date_of_birth = Column(Date)
    gender = Column(SQLEnum(Gender))
    nationality = Column(String(50))
    state = Column(String(50))
    city = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    assessments = relationship("Assessment", back_populates="user")

class Assessment(Base):
    __tablename__ = "assessments"

    assessment_id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    
    # Physical details
    height_cm = Column(Float)
    weight_kg = Column(Float)
    eyesight_left = Column(Float)
    eyesight_right = Column(Float)
    has_medical_conditions = Column(Boolean, default=False)
    medical_conditions_description = Column(Text)
    tattoos = Column(Boolean, default=False)
    previous_injuries = Column(Boolean, default=False)
    
    # Education details
    highest_education = Column(SQLEnum(EducationLevel))
    stream = Column(SQLEnum(Stream))
    university = Column(String(200))
    graduation_year = Column(Integer)
    percentage_or_cgpa = Column(Float)
    additional_qualifications = Column(JSON)
    has_ncc = Column(Boolean, default=False)
    ncc_certificate = Column(String(50))
    
    # OLQ details
    olq_responses = Column(JSON)
    olq_score = Column(Float)  # 0-100
    
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="assessments")
    recommendations = relationship("Recommendation", back_populates="assessment")

class Recommendation(Base):
    __tablename__ = "recommendations"

    recommendation_id = Column(String, primary_key=True, default=generate_uuid)
    assessment_id = Column(String, ForeignKey("assessments.assessment_id"), nullable=False)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    
    olq_score = Column(Float, nullable=False)
    primary_category = Column(SQLEnum(RoleCategory), nullable=False)
    recommendations_data = Column(JSON, nullable=False)  # List of role recommendations
    explanation = Column(Text)
    ml_model_version = Column(String(50))
    
    generated_at = Column(DateTime(timezone=True), server_default=func.now())

    assessment = relationship("Assessment", back_populates="recommendations")
    study_plans = relationship("StudyPlan", back_populates="recommendation")

class StudyPlan(Base):
    __tablename__ = "study_plans"

    plan_id = Column(String, primary_key=True, default=generate_uuid)
    recommendation_id = Column(String, ForeignKey("recommendations.recommendation_id"), nullable=False)
    
    target_date = Column(Date, nullable=False)
    total_days = Column(Integer, nullable=False)
    hours_per_day = Column(Float, nullable=False)
    total_hours = Column(Float, nullable=False)
    
    modules_data = Column(JSON, nullable=False)  # List of study modules
    daily_schedule_data = Column(JSON, nullable=False)  # Daily schedule
    milestones_data = Column(JSON)  # Key milestones
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    recommendation = relationship("Recommendation", back_populates="study_plans")
