from datetime import datetime
from typing import Dict, List, Any
from sqlalchemy.orm import Session
import json
import os

from app.models.models import Assessment, User
from app.models.schemas import RoleCategory
from app.services.olq_service import get_olq_analysis

# Role definitions with eligibility criteria
DEFENCE_ROLES = {
    "officer": [
        {
            "role_name": "Indian Army - NDA Entry",
            "entry_scheme": "National Defence Academy",
            "min_age": 16.5,
            "max_age": 19.5,
            "education": "12th Standard",
            "min_olq": 60,
            "physical_standards": {
                "height_male": 157,
                "height_female": 152,
                "weight": "Proportionate",
                "eyesight": "6/6 or correctable"
            },
            "selection_process": [
                "Written Examination (UPSC)",
                "SSB Interview (5 days)",
                "Medical Examination",
                "Final Merit List"
            ],
            "priority": 1
        },
        {
            "role_name": "Indian Army - CDS Entry",
            "entry_scheme": "Combined Defence Services",
            "min_age": 19,
            "max_age": 24,
            "education": "Graduation",
            "min_olq": 60,
            "physical_standards": {
                "height_male": 157,
                "height_female": 152,
                "weight": "Proportionate",
                "eyesight": "6/6 or correctable"
            },
            "selection_process": [
                "Written Examination (UPSC)",
                "SSB Interview (5 days)",
                "Medical Examination",
                "Final Merit List"
            ],
            "priority": 2
        },
        {
            "role_name": "Indian Army - TGC Entry",
            "entry_scheme": "Technical Graduate Course",
            "min_age": 20,
            "max_age": 27,
            "education": "B.E/B.Tech",
            "min_olq": 55,
            "physical_standards": {
                "height_male": 157,
                "height_female": 152,
                "weight": "Proportionate",
                "eyesight": "6/6 or correctable"
            },
            "selection_process": [
                "SSB Interview (5 days)",
                "Medical Examination",
                "Final Merit List"
            ],
            "priority": 3
        },
        {
            "role_name": "Indian Navy - NDA Entry",
            "entry_scheme": "National Defence Academy (Navy)",
            "min_age": 16.5,
            "max_age": 19.5,
            "education": "12th Standard (PCM)",
            "min_olq": 60,
            "physical_standards": {
                "height_male": 157,
                "height_female": 152,
                "weight": "Proportionate",
                "eyesight": "6/6 or correctable"
            },
            "selection_process": [
                "Written Examination (UPSC)",
                "SSB Interview (5 days)",
                "Medical Examination",
                "Final Merit List"
            ],
            "priority": 1
        },
        {
            "role_name": "Indian Air Force - NDA Entry",
            "entry_scheme": "National Defence Academy (Air Force)",
            "min_age": 16.5,
            "max_age": 19.5,
            "education": "12th Standard (PCM)",
            "min_olq": 65,
            "physical_standards": {
                "height_male": 162.5,
                "height_female": 152,
                "weight": "Proportionate",
                "eyesight": "6/6 (Flying Branch)"
            },
            "selection_process": [
                "Written Examination (UPSC)",
                "SSB Interview (5 days)",
                "PABT (Pilot Aptitude Battery Test)",
                "Medical Examination",
                "Final Merit List"
            ],
            "priority": 1
        },
        {
            "role_name": "Indian Air Force - AFCAT",
            "entry_scheme": "Air Force Common Admission Test",
            "min_age": 20,
            "max_age": 24,
            "education": "Graduation (Any Stream)",
            "min_olq": 60,
            "physical_standards": {
                "height_male": 162.5,
                "height_female": 152,
                "weight": "Proportionate",
                "eyesight": "6/6 or correctable"
            },
            "selection_process": [
                "AFCAT Written Exam",
                "EKT (Engineering Knowledge Test) for Technical",
                "SSB Interview (5 days)",
                "Medical Examination",
                "Final Merit List"
            ],
            "priority": 2
        }
    ],
    "enlisted": [
        {
            "role_name": "Indian Army - Soldier General Duty",
            "entry_scheme": "Army Bharti Rally",
            "min_age": 17.5,
            "max_age": 21,
            "education": "10th Pass",
            "min_olq": 0,
            "physical_standards": {
                "height_male": 163,
                "height_female": 157,
                "weight": "50 kg minimum",
                "chest": "77-82 cm",
                "eyesight": "6/9 or correctable"
            },
            "selection_process": [
                "Physical Fitness Test",
                "Physical Measurement Test",
                "Written Examination",
                "Medical Examination"
            ],
            "priority": 1
        },
        {
            "role_name": "Indian Army - Agniveer",
            "entry_scheme": "Agnipath Scheme",
            "min_age": 17.5,
            "max_age": 21,
            "education": "10th/12th Pass",
            "min_olq": 0,
            "physical_standards": {
                "height_male": 163,
                "height_female": 157,
                "weight": "Proportionate",
                "chest": "77-82 cm",
                "eyesight": "6/9 or correctable"
            },
            "selection_process": [
                "Physical Fitness Test",
                "Physical Measurement Test",
                "Written Examination",
                "Medical Examination"
            ],
            "priority": 1
        },
        {
            "role_name": "Indian Army - Soldier Technical",
            "entry_scheme": "Army Technical Entry",
            "min_age": 17.5,
            "max_age": 23,
            "education": "12th Pass (PCM) with 50%",
            "min_olq": 30,
            "physical_standards": {
                "height_male": 163,
                "height_female": 157,
                "weight": "50 kg minimum",
                "chest": "77-82 cm",
                "eyesight": "6/9 or correctable"
            },
            "selection_process": [
                "Physical Fitness Test",
                "Physical Measurement Test",
                "Written Examination",
                "Medical Examination"
            ],
            "priority": 2
        },
        {
            "role_name": "Indian Army - Soldier Clerk/SKT",
            "entry_scheme": "Army Clerical Entry",
            "min_age": 17.5,
            "max_age": 23,
            "education": "12th Pass with 60%",
            "min_olq": 25,
            "physical_standards": {
                "height_male": 163,
                "height_female": 157,
                "weight": "50 kg minimum",
                "chest": "77-82 cm",
                "eyesight": "6/9 or correctable"
            },
            "selection_process": [
                "Physical Fitness Test",
                "Physical Measurement Test",
                "Written Examination",
                "Typing Test",
                "Medical Examination"
            ],
            "priority": 2
        },
        {
            "role_name": "Indian Navy - Sailor Entry",
            "entry_scheme": "Indian Navy MR/NMR Entry",
            "min_age": 17,
            "max_age": 20,
            "education": "10th/12th Pass",
            "min_olq": 0,
            "physical_standards": {
                "height_male": 157,
                "height_female": 152,
                "weight": "Proportionate",
                "eyesight": "6/9 or correctable"
            },
            "selection_process": [
                "Written Examination",
                "Physical Fitness Test",
                "Medical Examination"
            ],
            "priority": 1
        },
        {
            "role_name": "Indian Air Force - Airman",
            "entry_scheme": "Airman Selection Test",
            "min_age": 17,
            "max_age": 21,
            "education": "10th/12th Pass",
            "min_olq": 0,
            "physical_standards": {
                "height_male": 152.5,
                "height_female": 152,
                "weight": "Proportionate",
                "eyesight": "6/9 or correctable"
            },
            "selection_process": [
                "Online Test (Phase 1)",
                "Adaptability Test (Phase 2)",
                "Medical Examination"
            ],
            "priority": 1
        }
    ],
    "civil_services": [
        {
            "role_name": "IAS/IPS/IFS - UPSC CSE",
            "entry_scheme": "Civil Services Examination",
            "min_age": 21,
            "max_age": 32,
            "education": "Graduation (Any Stream)",
            "min_olq": 70,
            "physical_standards": {
                "height_male": 165,
                "height_female": 150,
                "weight": "Proportionate",
                "eyesight": "Varies by service"
            },
            "selection_process": [
                "Preliminary Examination",
                "Main Examination",
                "Personality Test (Interview)",
                "Medical Examination",
                "Final Merit List"
            ],
            "priority": 1
        },
        {
            "role_name": "State Civil Services",
            "entry_scheme": "State PSC Examination",
            "min_age": 21,
            "max_age": 35,
            "education": "Graduation",
            "min_olq": 60,
            "physical_standards": {
                "height_male": 165,
                "height_female": 150,
                "weight": "Proportionate",
                "eyesight": "Normal"
            },
            "selection_process": [
                "Preliminary Examination",
                "Main Examination",
                "Interview",
                "Document Verification"
            ],
            "priority": 2
        }
    ]
}

def generate_recommendations(assessment: Assessment, db: Session) -> Dict[str, Any]:
    """
    Generate career recommendations using hybrid deterministic + ML approach
    """
    olq_score = assessment.olq_score
    user = db.query(User).filter(User.user_id == assessment.user_id).first()
    
    # Calculate age
    age = _calculate_age(user.date_of_birth)
    
    # Get OLQ analysis
    olq_analysis = get_olq_analysis(assessment.olq_responses) if assessment.olq_responses else {}
    
    # Determine primary category based on OLQ score
    if olq_score < 50:
        primary_category = RoleCategory.ENLISTED
        explanation = f"Based on your OLQ score of {olq_score:.1f}%, enlisted roles are recommended. " \
                     f"These positions focus on operational excellence and provide structured career growth. " \
                     f"You can develop leadership skills and potentially transition to officer roles later."
    elif olq_score >= 70:
        primary_category = RoleCategory.CIVIL_SERVICES
        explanation = f"Your OLQ score of {olq_score:.1f}% indicates strong leadership potential. " \
                     f"You are well-suited for both defence officer entries and civil services. " \
                     f"Civil services are prioritized based on your excellent analytical and decision-making abilities."
    else:
        primary_category = RoleCategory.OFFICER
        explanation = f"Your OLQ score of {olq_score:.1f}% demonstrates good leadership qualities. " \
                     f"Officer entries in defence forces are recommended based on your profile. " \
                     f"Continue developing your leadership skills for optimal success."
    
    # Get eligible roles
    recommendations = []
    
    # Always check officer roles if OLQ >= 50
    if olq_score >= 50:
        officer_roles = _filter_eligible_roles(
            DEFENCE_ROLES["officer"],
            assessment,
            age,
            olq_score
        )
        recommendations.extend(officer_roles)
        
        # Add civil services if OLQ >= 60
        if olq_score >= 60:
            civil_roles = _filter_eligible_roles(
                DEFENCE_ROLES["civil_services"],
                assessment,
                age,
                olq_score
            )
            recommendations.extend(civil_roles)
    
    # Add enlisted roles if OLQ < 50 or as backup
    if olq_score < 50 or len(recommendations) < 3:
        enlisted_roles = _filter_eligible_roles(
            DEFENCE_ROLES["enlisted"],
            assessment,
            age,
            olq_score
        )
        recommendations.extend(enlisted_roles)
    
    # Use ML for scoring if model exists
    recommendations = _apply_ml_scoring(recommendations, assessment, olq_score)
    
    # Sort by match score and limit to top 5
    recommendations.sort(key=lambda x: x["match_score"], reverse=True)
    recommendations = recommendations[:5]
    
    # Add feature importance for explainability
    for rec in recommendations:
        rec["feature_importance"] = _calculate_feature_importance(
            rec,
            assessment,
            olq_score
        )
    
    return {
        "primary_category": primary_category,
        "recommendations": recommendations,
        "explanation": explanation,
        "olq_analysis": olq_analysis
    }

def _calculate_age(date_of_birth) -> float:
    """Calculate age from date of birth"""
    today = datetime.now().date()
    age = today.year - date_of_birth.year
    if today.month < date_of_birth.month or (today.month == date_of_birth.month and today.day < date_of_birth.day):
        age -= 1
    return age

def _filter_eligible_roles(roles: List[Dict], assessment: Assessment, age: float, olq_score: float) -> List[Dict]:
    """Filter roles based on eligibility criteria"""
    eligible = []
    
    for role in roles:
        # Check age
        if age < role["min_age"] or age > role["max_age"]:
            continue
        
        # Check OLQ
        if olq_score < role["min_olq"]:
            continue
        
        # Check physical standards (basic)
        height_req = role["physical_standards"].get("height_male", 0)
        if assessment.height_cm and assessment.height_cm < height_req:
            continue
        
        # Check education level
        if not _check_education_eligibility(role["education"], assessment.highest_education.value):
            continue
        
        # Calculate initial match score
        match_score = _calculate_deterministic_score(role, assessment, olq_score, age)
        
        # Determine category
        if "Soldier" in role["role_name"] or "Sailor" in role["role_name"] or "Airman" in role["role_name"] or "Agniveer" in role["role_name"]:
            category = RoleCategory.ENLISTED
        elif "IAS" in role["role_name"] or "State Civil" in role["role_name"]:
            category = RoleCategory.CIVIL_SERVICES
        else:
            category = RoleCategory.OFFICER
        
        eligible.append({
            "role_name": role["role_name"],
            "role_category": category,
            "entry_scheme": role["entry_scheme"],
            "match_score": match_score,
            "min_age": role["min_age"],
            "max_age": role["max_age"],
            "education_requirement": role["education"],
            "physical_standards": role["physical_standards"],
            "selection_process": role["selection_process"],
            "reasoning": _generate_reasoning(role, assessment, olq_score, match_score),
            "feature_importance": {}
        })
    
    return eligible

def _check_education_eligibility(required: str, completed: str) -> bool:
    """Check if education requirement is met"""
    education_hierarchy = {
        "10th Pass": 1,
        "10th/12th Pass": 1,
        "12th Standard": 2,
        "12th Standard (PCM)": 2,
        "12th Pass": 2,
        "12th Pass (PCM) with 50%": 2,
        "12th Pass with 60%": 2,
        "Graduation": 3,
        "Graduation (Any Stream)": 3,
        "B.E/B.Tech": 3,
        "Masters": 4,
        "Doctorate": 5
    }
    
    completed_hierarchy = {
        "high_school": 1,
        "intermediate": 2,
        "bachelors": 3,
        "masters": 4,
        "doctorate": 5
    }
    
    req_level = education_hierarchy.get(required, 0)
    comp_level = completed_hierarchy.get(completed, 0)
    
    return comp_level >= req_level

def _calculate_deterministic_score(role: Dict, assessment: Assessment, olq_score: float, age: float) -> float:
    """Calculate deterministic match score"""
    score = 0.0
    
    # OLQ score component (40%)
    olq_component = (olq_score - role["min_olq"]) / (100 - role["min_olq"]) if role["min_olq"] < 100 else 1.0
    score += olq_component * 0.4
    
    # Age component (20%) - prefer middle of age range
    age_range = role["max_age"] - role["min_age"]
    ideal_age = role["min_age"] + (age_range * 0.3)  # 30% into the range is ideal
    age_diff = abs(age - ideal_age)
    age_component = max(0, 1 - (age_diff / age_range))
    score += age_component * 0.2
    
    # Education component (20%)
    education_component = 0.8  # Base score for meeting requirement
    if assessment.percentage_or_cgpa >= 75:
        education_component = 1.0
    elif assessment.percentage_or_cgpa >= 60:
        education_component = 0.9
    score += education_component * 0.2
    
    # Physical fitness component (10%)
    physical_component = 0.8  # Base score
    if assessment.height_cm and assessment.weight_kg:
        bmi = assessment.weight_kg / ((assessment.height_cm / 100) ** 2)
        if 18.5 <= bmi <= 24.9:
            physical_component = 1.0
        elif 17 <= bmi <= 27:
            physical_component = 0.9
    score += physical_component * 0.1
    
    # Additional qualifications (10%)
    additional_component = 0.5
    if assessment.has_ncc:
        additional_component += 0.3
    if assessment.additional_qualifications:
        additional_component += 0.2
    additional_component = min(additional_component, 1.0)
    score += additional_component * 0.1
    
    # Convert to percentage
    return score * 100

def _apply_ml_scoring(recommendations: List[Dict], assessment: Assessment, olq_score: float) -> List[Dict]:
    """Apply ML model scoring if available"""
    # Check if ML model exists
    ml_model_path = os.path.join(os.getenv("ML_MODEL_PATH", "../data/models"), "role_classifier.pkl")
    
    if os.path.exists(ml_model_path):
        try:
            import joblib
            model = joblib.load(ml_model_path)
            
            # Prepare features for each recommendation
            for rec in recommendations:
                features = _prepare_ml_features(assessment, olq_score, rec)
                ml_score = model.predict_proba([features])[0][1] * 100  # Probability * 100
                
                # Blend deterministic and ML scores
                rec["match_score"] = (rec["match_score"] * 0.6) + (ml_score * 0.4)
        except Exception as e:
            # If ML fails, continue with deterministic scores
            print(f"ML scoring failed: {e}")
    
    return recommendations

def _prepare_ml_features(assessment: Assessment, olq_score: float, recommendation: Dict) -> List[float]:
    """Prepare features for ML model"""
    features = [
        olq_score / 100,  # Normalized OLQ score
        assessment.percentage_or_cgpa / 100,  # Normalized education score
        1.0 if assessment.has_ncc else 0.0,  # NCC flag
        len(assessment.additional_qualifications or []) / 5.0,  # Normalized qualifications count
        assessment.height_cm / 180.0 if assessment.height_cm else 0.9,  # Normalized height
        assessment.weight_kg / 80.0 if assessment.weight_kg else 0.8,  # Normalized weight
    ]
    return features

def _calculate_feature_importance(rec: Dict, assessment: Assessment, olq_score: float) -> Dict[str, float]:
    """Calculate feature importance for explainability"""
    importance = {
        "OLQ Score": 0.0,
        "Education Level": 0.0,
        "Physical Fitness": 0.0,
        "Additional Qualifications": 0.0,
        "Age Suitability": 0.0
    }
    
    # OLQ impact
    if olq_score >= rec.get("min_olq", 0) + 20:
        importance["OLQ Score"] = 0.35
    elif olq_score >= rec.get("min_olq", 0) + 10:
        importance["OLQ Score"] = 0.25
    else:
        importance["OLQ Score"] = 0.15
    
    # Education impact
    if assessment.percentage_or_cgpa >= 75:
        importance["Education Level"] = 0.25
    elif assessment.percentage_or_cgpa >= 60:
        importance["Education Level"] = 0.20
    else:
        importance["Education Level"] = 0.15
    
    # Physical fitness
    if assessment.height_cm and assessment.weight_kg:
        importance["Physical Fitness"] = 0.20
    else:
        importance["Physical Fitness"] = 0.10
    
    # Additional qualifications
    if assessment.has_ncc or assessment.additional_qualifications:
        importance["Additional Qualifications"] = 0.15
    else:
        importance["Additional Qualifications"] = 0.05
    
    # Age - calculated as remainder
    total = sum(importance.values())
    importance["Age Suitability"] = max(0.05, 1.0 - total)
    
    # Normalize to sum to 1.0
    total = sum(importance.values())
    importance = {k: v/total for k, v in importance.items()}
    
    return importance

def _generate_reasoning(role: Dict, assessment: Assessment, olq_score: float, match_score: float) -> str:
    """Generate human-readable reasoning for recommendation"""
    reasons = []
    
    # OLQ-based reasoning
    if olq_score >= role["min_olq"] + 20:
        reasons.append(f"Your OLQ score of {olq_score:.1f}% significantly exceeds the minimum requirement")
    elif olq_score >= role["min_olq"] + 10:
        reasons.append(f"Your OLQ score of {olq_score:.1f}% is well above the minimum requirement")
    else:
        reasons.append(f"Your OLQ score of {olq_score:.1f}% meets the minimum requirement")
    
    # Education reasoning
    if assessment.percentage_or_cgpa >= 75:
        reasons.append("Your excellent academic performance strengthens your candidacy")
    elif assessment.percentage_or_cgpa >= 60:
        reasons.append("Your good academic record supports this application")
    
    # NCC advantage
    if assessment.has_ncc:
        reasons.append("Your NCC background provides a significant advantage")
    
    # Match score
    if match_score >= 80:
        reasons.append("This role is an excellent match for your profile")
    elif match_score >= 65:
        reasons.append("This role is a very good fit for your qualifications")
    else:
        reasons.append("This role matches your basic eligibility criteria")
    
    return ". ".join(reasons) + "."
