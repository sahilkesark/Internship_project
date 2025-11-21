#!/usr/bin/env python3
"""
Script to load demo users into the database
"""
import sys
import os
import json
from datetime import date, datetime

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.models.database import SessionLocal, init_db
from app.models.models import User, Assessment
from app.models.schemas import Gender, EducationLevel, Stream

def load_demo_users():
    """Load demo users with various profiles"""
    
    # Initialize database
    init_db()
    db = SessionLocal()
    
    demo_users = [
        {
            "user": {
                "full_name": "Rajesh Kumar",
                "email": "rajesh.kumar@example.com",
                "phone": "+919876543210",
                "date_of_birth": date(2002, 5, 15),
                "gender": Gender.MALE,
                "nationality": "Indian",
                "state": "Uttar Pradesh",
                "city": "Lucknow"
            },
            "assessment": {
                "height_cm": 175.0,
                "weight_kg": 70.0,
                "eyesight_left": 6.0,
                "eyesight_right": 6.0,
                "has_medical_conditions": False,
                "tattoos": False,
                "previous_injuries": False,
                "highest_education": EducationLevel.BACHELORS,
                "stream": Stream.ENGINEERING,
                "university": "IIT Delhi",
                "graduation_year": 2024,
                "percentage_or_cgpa": 82.0,
                "additional_qualifications": ["Debate Winner", "Sports Certificate"],
                "has_ncc": True,
                "ncc_certificate": "B Certificate",
                "olq_score": 78.0,
                "completed": True
            },
            "description": "High OLQ Officer Candidate - Engineering graduate with NCC, excellent for officer entries"
        },
        {
            "user": {
                "full_name": "Priya Sharma",
                "email": "priya.sharma@example.com",
                "phone": "+919876543211",
                "date_of_birth": date(2003, 8, 22),
                "gender": Gender.FEMALE,
                "nationality": "Indian",
                "state": "Maharashtra",
                "city": "Mumbai"
            },
            "assessment": {
                "height_cm": 160.0,
                "weight_kg": 55.0,
                "eyesight_left": 6.0,
                "eyesight_right": 6.0,
                "has_medical_conditions": False,
                "tattoos": False,
                "previous_injuries": False,
                "highest_education": EducationLevel.BACHELORS,
                "stream": Stream.ARTS,
                "university": "Delhi University",
                "graduation_year": 2024,
                "percentage_or_cgpa": 68.0,
                "additional_qualifications": ["Volunteer Work"],
                "has_ncc": False,
                "ncc_certificate": None,
                "olq_score": 52.0,
                "completed": True
            },
            "description": "Medium OLQ Mixed Candidate - Good academic record, suitable for both officer and technical entries"
        },
        {
            "user": {
                "full_name": "Amit Singh",
                "email": "amit.singh@example.com",
                "phone": "+919876543212",
                "date_of_birth": date(2004, 12, 10),
                "gender": Gender.MALE,
                "nationality": "Indian",
                "state": "Punjab",
                "city": "Amritsar"
            },
            "assessment": {
                "height_cm": 168.0,
                "weight_kg": 65.0,
                "eyesight_left": 6.0,
                "eyesight_right": 6.0,
                "has_medical_conditions": False,
                "tattoos": False,
                "previous_injuries": False,
                "highest_education": EducationLevel.INTERMEDIATE,
                "stream": Stream.SCIENCE,
                "university": "Punjab State Board",
                "graduation_year": 2022,
                "percentage_or_cgpa": 58.0,
                "additional_qualifications": [],
                "has_ncc": False,
                "ncc_certificate": None,
                "olq_score": 35.0,
                "completed": True
            },
            "description": "Low OLQ Enlisted Candidate - Best suited for Agniveer, Army GD, and enlisted roles"
        }
    ]
    
    print("Loading demo users...")
    print("=" * 60)
    
    for idx, demo in enumerate(demo_users, 1):
        print(f"\n{idx}. Creating user: {demo['user']['full_name']}")
        print(f"   Description: {demo['description']}")
        
        # Check if user exists
        existing_user = db.query(User).filter(User.email == demo['user']['email']).first()
        if existing_user:
            print(f"   User already exists, skipping...")
            continue
        
        # Create user
        user = User(**demo['user'])
        db.add(user)
        db.flush()
        
        # Create assessment
        assessment_data = demo['assessment'].copy()
        assessment_data['user_id'] = user.user_id
        
        # Mock OLQ responses based on score
        olq_score = assessment_data['olq_score']
        num_correct = int((olq_score / 100) * 10)
        olq_responses = []
        for i in range(10):
            olq_responses.append({
                "question_id": i + 1,
                "selected_option": 1 if i < num_correct else 0  # 1 is typically correct
            })
        assessment_data['olq_responses'] = olq_responses
        
        assessment = Assessment(**assessment_data)
        db.add(assessment)
        
        print(f"   User ID: {user.user_id}")
        print(f"   Assessment ID: {assessment.assessment_id}")
        print(f"   OLQ Score: {olq_score}%")
    
    db.commit()
    print("\n" + "=" * 60)
    print("Demo users loaded successfully!")
    print("\nYou can now test the API with these demo users.")
    
    # Save demo user info to file
    demo_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample', 'demo_users.json')
    os.makedirs(os.path.dirname(demo_file), exist_ok=True)
    
    demo_info = []
    for demo in demo_users:
        user = db.query(User).filter(User.email == demo['user']['email']).first()
        if user:
            assessment = db.query(Assessment).filter(Assessment.user_id == user.user_id).first()
            demo_info.append({
                "name": user.full_name,
                "email": user.email,
                "user_id": user.user_id,
                "assessment_id": assessment.assessment_id if assessment else None,
                "olq_score": demo['assessment']['olq_score'],
                "description": demo['description']
            })
    
    with open(demo_file, 'w') as f:
        json.dump(demo_info, f, indent=2)
    
    print(f"\nDemo user info saved to: {demo_file}")
    
    db.close()

if __name__ == "__main__":
    load_demo_users()
