from datetime import datetime, date, timedelta
import random
from typing import Dict, List
from app.services.exam_config_service import get_exam_details
from typing import Dict, List, Any
from sqlalchemy.orm import Session

from app.models.models import Recommendation

# Syllabus templates for different roles
SYLLABUS_TEMPLATES = {
    "NDA": {
        "modules": [
            {
                "name": "Mathematics",
                "topics": [
                    "Algebra", "Matrices and Determinants", "Trigonometry",
                    "Analytical Geometry (2D & 3D)", "Differential Calculus",
                    "Integral Calculus", "Vector Algebra", "Statistics & Probability"
                ],
                "hours_per_topic": 15,
                "priority": 1
            },
            {
                "name": "General Ability Test",
                "topics": [
                    "English Grammar & Comprehension", "General Knowledge",
                    "Physics", "Chemistry", "General Science",
                    "History", "Geography", "Current Affairs"
                ],
                "hours_per_topic": 12,
                "priority": 1
            },
            {
                "name": "SSB Preparation",
                "topics": [
                    "Psychological Tests (TAT, WAT, SRT)",
                    "Group Testing (GD, GPE, PGT, HGT)",
                    "Interview Techniques", "Current Affairs & General Awareness"
                ],
                "hours_per_topic": 10,
                "priority": 2
            }
        ]
    },
    "CDS": {
        "modules": [
            {
                "name": "English",
                "topics": [
                    "Grammar", "Vocabulary", "Comprehension",
                    "Spotting Errors", "Sentence Improvement", "Synonyms & Antonyms"
                ],
                "hours_per_topic": 8,
                "priority": 1
            },
            {
                "name": "General Knowledge",
                "topics": [
                    "Indian History", "Geography", "Indian Polity",
                    "Economics", "General Science", "Current Affairs",
                    "Defence Related Topics"
                ],
                "hours_per_topic": 10,
                "priority": 1
            },
            {
                "name": "Elementary Mathematics",
                "topics": [
                    "Arithmetic", "Algebra", "Trigonometry",
                    "Geometry", "Mensuration", "Statistics"
                ],
                "hours_per_topic": 12,
                "priority": 1
            },
            {
                "name": "SSB Preparation",
                "topics": [
                    "Psychological Tests", "Group Testing",
                    "Interview Skills", "Personal Development"
                ],
                "hours_per_topic": 10,
                "priority": 2
            }
        ]
    },
    "AFCAT": {
        "modules": [
            {
                "name": "General Awareness",
                "topics": [
                    "Current Affairs", "History", "Geography",
                    "Polity", "Economics", "Sports", "Defence",
                    "Art & Culture"
                ],
                "hours_per_topic": 8,
                "priority": 1
            },
            {
                "name": "Verbal Ability",
                "topics": [
                    "Comprehension", "Error Detection", "Sentence Completion",
                    "Synonyms & Antonyms", "Idioms & Phrases"
                ],
                "hours_per_topic": 7,
                "priority": 1
            },
            {
                "name": "Numerical Ability",
                "topics": [
                    "Number System", "Percentage", "Ratio & Proportion",
                    "Average", "Time & Work", "Speed & Distance",
                    "Profit & Loss", "Data Interpretation"
                ],
                "hours_per_topic": 8,
                "priority": 1
            },
            {
                "name": "Reasoning & Military Aptitude",
                "topics": [
                    "Verbal Reasoning", "Non-Verbal Reasoning",
                    "Spatial Ability", "Defence Terminology"
                ],
                "hours_per_topic": 8,
                "priority": 1
            },
            {
                "name": "SSB Preparation",
                "topics": [
                    "Psychological Tests", "Group Tasks",
                    "Interview Preparation", "PABT (for Flying)"
                ],
                "hours_per_topic": 10,
                "priority": 2
            }
        ]
    },
    "UPSC_CSE": {
        "modules": [
            {
                "name": "Preliminary Exam - GS Paper I",
                "topics": [
                    "History", "Geography", "Polity", "Economics",
                    "Environment", "Science & Technology", "Current Affairs"
                ],
                "hours_per_topic": 20,
                "priority": 1
            },
            {
                "name": "Preliminary Exam - CSAT",
                "topics": [
                    "Comprehension", "Logical Reasoning", "Analytical Ability",
                    "Decision Making", "Problem Solving", "Basic Numeracy"
                ],
                "hours_per_topic": 12,
                "priority": 1
            },
            {
                "name": "Optional Subject",
                "topics": [
                    "Paper I - Fundamentals", "Paper I - Advanced Topics",
                    "Paper II - Core Concepts", "Paper II - Applied Topics"
                ],
                "hours_per_topic": 30,
                "priority": 2
            },
            {
                "name": "Essay Writing",
                "topics": [
                    "Essay Structure", "Content Development",
                    "Philosophical Essays", "Social Issues", "Practice"
                ],
                "hours_per_topic": 10,
                "priority": 2
            },
            {
                "name": "Interview Preparation",
                "topics": [
                    "Current Affairs", "DAF Analysis", "Mock Interviews",
                    "Personality Development"
                ],
                "hours_per_topic": 15,
                "priority": 3
            }
        ]
    },
    "ARMY_GD": {
        "modules": [
            {
                "name": "General Knowledge",
                "topics": [
                    "Indian History", "Geography", "Current Affairs",
                    "Indian Armed Forces", "Sports", "General Science"
                ],
                "hours_per_topic": 6,
                "priority": 1
            },
            {
                "name": "General Science",
                "topics": [
                    "Physics Basics", "Chemistry Basics", "Biology Basics",
                    "Scientific Phenomena"
                ],
                "hours_per_topic": 5,
                "priority": 1
            },
            {
                "name": "Mathematics",
                "topics": [
                    "Arithmetic", "Basic Algebra", "Percentage",
                    "Ratio & Proportion", "Simple Interest"
                ],
                "hours_per_topic": 6,
                "priority": 1
            },
            {
                "name": "Physical Fitness",
                "topics": [
                    "Running (1.6 km)", "Pull-ups", "9 feet Ditch",
                    "Zig-zag Balance", "Strength Training"
                ],
                "hours_per_topic": 15,
                "priority": 1
            }
        ]
    },
    "AGNIVEER": {
        "modules": [
            {
                "name": "General Knowledge",
                "topics": [
                    "Indian History", "Geography", "Current Affairs",
                    "Indian Armed Forces", "Sports"
                ],
                "hours_per_topic": 5,
                "priority": 1
            },
            {
                "name": "Mathematics",
                "topics": [
                    "Arithmetic", "Algebra", "Geometry",
                    "Mensuration", "Statistics"
                ],
                "hours_per_topic": 8,
                "priority": 1
            },
            {
                "name": "Physical & Medical Fitness",
                "topics": [
                    "Running Practice", "Fitness Training",
                    "Medical Standards Preparation"
                ],
                "hours_per_topic": 12,
                "priority": 1
            }
        ]
    },
    "DEFAULT": {
        "modules": [
            {
                "name": "General Knowledge & Current Affairs",
                "topics": [
                    "Indian History", "Geography", "Polity",
                    "Economics", "Current Affairs", "Defence Topics"
                ],
                "hours_per_topic": 10,
                "priority": 1
            },
            {
                "name": "Quantitative Aptitude",
                "topics": [
                    "Arithmetic", "Algebra", "Geometry",
                    "Data Interpretation"
                ],
                "hours_per_topic": 10,
                "priority": 1
            },
            {
                "name": "Reasoning Ability",
                "topics": [
                    "Logical Reasoning", "Analytical Reasoning",
                    "Verbal Reasoning"
                ],
                "hours_per_topic": 8,
                "priority": 1
            },
            {
                "name": "English Language",
                "topics": [
                    "Grammar", "Vocabulary", "Comprehension"
                ],
                "hours_per_topic": 8,
                "priority": 1
            }
        ]
    }
}

def generate_study_plan(
    recommendation: Recommendation,
    target_date: date,
    hours_per_day: float,
    db: Session,
    exam_type: str = None
) -> Dict[str, Any]:
    """
    Generate personalized study plan with syllabus and timetable
    Now supports exam-specific study plans with AI-powered insights
    """
    # Calculate total days available
    today = datetime.now().date()
    total_days = (target_date - today).days
    
    if total_days <= 0:
        raise ValueError("Target date must be in the future")
    
    # Get primary recommended role
    recommendations = recommendation.recommendations_data
    if not recommendations:
        raise ValueError("No recommendations found")
    
    primary_role = recommendations[0]
    role_name = primary_role.get("role_name", "")
    
    # Use exam_type if provided, otherwise determine from role
    if exam_type:
        syllabus_key = exam_type
        # Get exam-specific configuration
        exam_config = get_exam_details(exam_type)
        if exam_config:
            # Use exam config to build comprehensive study plan
            syllabus = _build_syllabus_from_exam_config(exam_config)
        else:
            syllabus_key = _determine_syllabus_key(role_name)
            syllabus = SYLLABUS_TEMPLATES.get(syllabus_key, SYLLABUS_TEMPLATES["DEFAULT"])
    else:
        # Determine syllabus template from role
        syllabus_key = _determine_syllabus_key(role_name)
        syllabus = SYLLABUS_TEMPLATES.get(syllabus_key, SYLLABUS_TEMPLATES["DEFAULT"])
    
    # Calculate total hours available
    total_hours = total_days * hours_per_day
    
    # Prepare modules with time allocation
    modules = _allocate_time_to_modules(syllabus["modules"], total_hours, total_days)
    
    # Generate daily schedule
    daily_schedule = _generate_daily_schedule(modules, today, target_date, hours_per_day)
    
    # Generate milestones
    milestones = _generate_milestones(modules, today, target_date)
    
    return {
        "total_days": total_days,
        "total_hours": total_hours,
        "modules": modules,
        "daily_schedule": daily_schedule,
        "milestones": milestones
    }

def _build_syllabus_from_exam_config(exam_config: Dict) -> Dict:
    """Build syllabus structure from exam configuration"""
    modules = []
    
    syllabus_data = exam_config.get("syllabus", {})
    
    for subject_name, subject_data in syllabus_data.items():
        topics = subject_data.get("topics", [])
        study_hours = subject_data.get("study_hours", 50)
        
        # Calculate hours per topic
        hours_per_topic = study_hours / len(topics) if topics else 10
        
        modules.append({
            "name": subject_name.replace("_", " ").title(),
            "topics": topics,
            "hours_per_topic": hours_per_topic,
            "priority": 1
        })
    
    return {"modules": modules}


def _determine_syllabus_key(role_name: str) -> str:
    """Determine which syllabus template to use based on role"""
    role_lower = role_name.lower()
    
    if "nda" in role_lower:
        return "NDA"
    elif "cds" in role_lower:
        return "CDS"
    elif "afcat" in role_lower:
        return "AFCAT"
    elif "upsc" in role_lower or "ias" in role_lower or "ips" in role_lower:
        return "UPSC_CSE"
    elif "general duty" in role_lower or "soldier gd" in role_lower:
        return "ARMY_GD"
    elif "agniveer" in role_lower:
        return "AGNIVEER"
    else:
        return "DEFAULT"

def _allocate_time_to_modules(modules: List[Dict], total_hours: float, total_days: int) -> List[Dict]:
    """Allocate time to each module based on priority and complexity"""
    result_modules = []
    
    # Calculate total required hours
    total_required = sum(
        len(m["topics"]) * m["hours_per_topic"] for m in modules
    )
    
    # Adjust if we have less time than required
    time_factor = min(1.0, total_hours / total_required) if total_required > 0 else 1.0
    
    week_number = 1
    cumulative_days = 0
    
    for module in modules:
        topics = module["topics"]
        hours_per_topic = module["hours_per_topic"] * time_factor
        total_module_hours = len(topics) * hours_per_topic
        
        # Calculate which week this module falls in
        module_days = total_module_hours / (total_hours / total_days)
        cumulative_days += module_days
        week_number = min(int(cumulative_days / 7) + 1, int(total_days / 7) + 1)
        
        result_modules.append({
            "module_name": module["name"],
            "topics": topics,
            "estimated_hours": round(total_module_hours, 1),
            "priority": module["priority"],
            "week_number": week_number
        })
    
    return result_modules

def _generate_daily_schedule(
    modules: List[Dict],
    start_date: date,
    target_date: date,
    hours_per_day: float
) -> List[Dict]:
    """Generate day-by-day study schedule"""
    daily_schedule = []
    current_date = start_date
    
    # Flatten all topics with their modules
    all_items = []
    for module in modules:
        module_hours = module["estimated_hours"]
        topics = module["topics"]
        hours_per_topic = module_hours / len(topics) if topics else 0
        
        for topic in topics:
            all_items.append({
                "module": module["module_name"],
                "topic": topic,
                "hours": hours_per_topic
            })
    
    # Distribute items across days
    item_index = 0
    total_days = (target_date - current_date).days
    
    for day in range(total_days):
        if item_index >= len(all_items):
            break
        
        day_date = current_date + timedelta(days=day)
        hours_remaining = hours_per_day
        modules_covered = []
        topics_covered = []
        
        while hours_remaining > 0 and item_index < len(all_items):
            item = all_items[item_index]
            
            if item["hours"] <= hours_remaining:
                # Can complete this topic today
                if item["module"] not in modules_covered:
                    modules_covered.append(item["module"])
                topics_covered.append(f"{item['module']}: {item['topic']}")
                hours_remaining -= item["hours"]
                item_index += 1
            else:
                # Partial topic completion
                if item["module"] not in modules_covered:
                    modules_covered.append(item["module"])
                topics_covered.append(f"{item['module']}: {item['topic']} (partial)")
                item["hours"] -= hours_remaining
                hours_remaining = 0
        
        # Add revision day every 7th day
        if (day + 1) % 7 == 0:
            daily_schedule.append({
                "date": day_date.isoformat(),
                "modules": ["Revision & Practice"],
                "hours_allocated": hours_per_day,
                "topics_covered": ["Revision of previous week topics", "Practice tests", "Doubt clearing"]
            })
        else:
            daily_schedule.append({
                "date": day_date.isoformat(),
                "modules": modules_covered,
                "hours_allocated": hours_per_day - hours_remaining,
                "topics_covered": topics_covered
            })
    
    return daily_schedule

def _generate_milestones(modules: List[Dict], start_date: date, target_date: date) -> List[Dict]:
    """Generate key milestones for the study plan"""
    milestones = []
    total_days = (target_date - start_date).days
    
    # Calculate module completion dates
    cumulative_days = 0
    total_hours = sum(m["estimated_hours"] for m in modules)
    
    for module in modules:
        module_fraction = module["estimated_hours"] / total_hours if total_hours > 0 else 0
        module_days = int(total_days * module_fraction)
        cumulative_days += module_days
        milestone_date = start_date + timedelta(days=cumulative_days)
        
        milestones.append({
            "title": f"Complete {module['module_name']}",
            "date": milestone_date.isoformat(),
            "description": f"Finish all topics in {module['module_name']}",
            "type": "module_completion"
        })
    
    # Add practice milestones
    quarter_days = total_days // 4
    if quarter_days > 7:
        milestones.append({
            "title": "First Mock Test",
            "date": (start_date + timedelta(days=quarter_days)).isoformat(),
            "description": "Attempt first full-length mock test",
            "type": "assessment"
        })
        
        milestones.append({
            "title": "Mid-Point Assessment",
            "date": (start_date + timedelta(days=total_days // 2)).isoformat(),
            "description": "Comprehensive revision and multiple mock tests",
            "type": "assessment"
        })
        
        milestones.append({
            "title": "Final Preparation Phase",
            "date": (start_date + timedelta(days=total_days - 14)).isoformat(),
            "description": "Intensive revision, daily mock tests, and last-minute tips",
            "type": "final_prep"
        })
    
    # Add exam date
    milestones.append({
        "title": "Exam Day",
        "date": target_date.isoformat(),
        "description": "Final examination - Stay confident!",
        "type": "exam"
    })
    
    # Sort by date
    milestones.sort(key=lambda x: x["date"])
    
    return milestones
