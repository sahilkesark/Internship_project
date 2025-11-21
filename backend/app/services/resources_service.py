from typing import Dict, List, Any
from app.models.schemas import Resource, ResourcesResponse

# Curated resources database
RESOURCES_DATABASE = {
    "NDA": {
        "resources": [
            {
                "title": "Pathfinder for NDA & NA Examination",
                "type": "book",
                "url": None,
                "description": "Comprehensive guide covering Mathematics and GAT with previous year papers",
                "relevance_score": 0.95,
                "is_free": False
            },
            {
                "title": "NDA/NA Mathematics by R.S. Aggarwal",
                "type": "book",
                "url": None,
                "description": "Detailed mathematics preparation with solved examples",
                "relevance_score": 0.92,
                "is_free": False
            },
            {
                "title": "Lucent's General Knowledge",
                "type": "book",
                "url": None,
                "description": "Complete GK coverage for competitive exams",
                "relevance_score": 0.88,
                "is_free": False
            },
            {
                "title": "UPSC NDA Official Website",
                "type": "website",
                "url": "https://www.upsc.gov.in",
                "description": "Official notifications, syllabus, and previous papers",
                "relevance_score": 1.0,
                "is_free": True
            },
            {
                "title": "SSBCrack - SSB Interview Preparation",
                "type": "website",
                "url": "https://www.ssbcrack.com",
                "description": "Complete SSB interview guidance and tips",
                "relevance_score": 0.90,
                "is_free": True
            },
            {
                "title": "Major Kalshi Classes - NDA Coaching",
                "type": "course",
                "url": "https://www.majorkalshiclasses.com",
                "description": "Online and offline NDA preparation courses",
                "relevance_score": 0.85,
                "is_free": False
            }
        ],
        "study_tips": [
            "Start with NCERT books for basics in Mathematics and Science",
            "Solve previous 10 years' question papers",
            "Focus on speed and accuracy in Mathematics",
            "Read newspapers daily for current affairs",
            "Practice mock SSB interviews with peers",
            "Maintain physical fitness throughout preparation",
            "Join online study groups for peer learning"
        ],
        "exam_pattern": {
            "total_papers": 2,
            "paper_1": "Mathematics (300 marks, 2.5 hours)",
            "paper_2": "General Ability Test (600 marks, 2.5 hours)",
            "total_marks": 900,
            "ssb_interview": "900 marks over 5 days",
            "negative_marking": "Yes, 1/3rd for each wrong answer"
        },
        "previous_papers": [
            {"year": "2023", "url": "https://www.upsc.gov.in/previous-papers"},
            {"year": "2022", "url": "https://www.upsc.gov.in/previous-papers"},
            {"year": "2021", "url": "https://www.upsc.gov.in/previous-papers"}
        ]
    },
    "CDS": {
        "resources": [
            {
                "title": "Pathfinder CDS Examination",
                "type": "book",
                "url": None,
                "description": "Complete guide for CDS with solved papers",
                "relevance_score": 0.95,
                "is_free": False
            },
            {
                "title": "Arihant CDS Solved Papers",
                "type": "book",
                "url": None,
                "description": "Last 10 years solved question papers",
                "relevance_score": 0.90,
                "is_free": False
            },
            {
                "title": "CDS Elementary Mathematics by R.S. Aggarwal",
                "type": "book",
                "url": None,
                "description": "Mathematics preparation for CDS",
                "relevance_score": 0.88,
                "is_free": False
            },
            {
                "title": "UPSC CDS Official Website",
                "type": "website",
                "url": "https://www.upsc.gov.in",
                "description": "Official notifications and previous papers",
                "relevance_score": 1.0,
                "is_free": True
            },
            {
                "title": "SSBCrack",
                "type": "website",
                "url": "https://www.ssbcrack.com",
                "description": "SSB preparation and guidance",
                "relevance_score": 0.90,
                "is_free": True
            }
        ],
        "study_tips": [
            "Focus on English grammar and vocabulary building",
            "Practice elementary mathematics daily",
            "Read newspapers for GK and current affairs",
            "Attempt mock tests regularly",
            "Prepare for SSB interview alongside written exam",
            "Work on time management",
            "Revise regularly and make notes"
        ],
        "exam_pattern": {
            "total_papers": 3,
            "paper_1": "English (100 marks, 2 hours)",
            "paper_2": "General Knowledge (100 marks, 2 hours)",
            "paper_3": "Elementary Mathematics (100 marks, 2 hours)",
            "total_marks": 300,
            "ssb_interview": "5-day process",
            "negative_marking": "Yes, 1/3rd for each wrong answer"
        },
        "previous_papers": [
            {"year": "2023", "url": "https://www.upsc.gov.in/previous-papers"},
            {"year": "2022", "url": "https://www.upsc.gov.in/previous-papers"}
        ]
    },
    "AFCAT": {
        "resources": [
            {
                "title": "Pathfinder for AFCAT",
                "type": "book",
                "url": None,
                "description": "Complete AFCAT preparation guide",
                "relevance_score": 0.95,
                "is_free": False
            },
            {
                "title": "AFCAT Previous Year Papers",
                "type": "book",
                "url": None,
                "description": "Solved previous year question papers",
                "relevance_score": 0.90,
                "is_free": False
            },
            {
                "title": "Indian Air Force Official Website",
                "type": "website",
                "url": "https://indianairforce.nic.in",
                "description": "Official notifications and information",
                "relevance_score": 1.0,
                "is_free": True
            },
            {
                "title": "CareerDefence AFCAT",
                "type": "website",
                "url": "https://www.careerdefence.in",
                "description": "Online AFCAT preparation and mock tests",
                "relevance_score": 0.85,
                "is_free": False
            }
        ],
        "study_tips": [
            "Focus on current affairs and general awareness",
            "Practice reasoning and numerical ability regularly",
            "Improve English vocabulary and comprehension",
            "Study military terminology and defence knowledge",
            "Attempt full-length mock tests",
            "Work on speed and accuracy",
            "Prepare thoroughly for SSB interview"
        ],
        "exam_pattern": {
            "total_questions": 100,
            "duration": "2 hours",
            "general_awareness": "25 questions",
            "verbal_ability": "25 questions",
            "numerical_ability": "25 questions",
            "reasoning_military_aptitude": "25 questions",
            "ekt": "50 questions for technical branch",
            "negative_marking": "Yes, 1 mark deduction for each wrong answer"
        },
        "previous_papers": [
            {"year": "2023", "url": "https://indianairforce.nic.in"},
            {"year": "2022", "url": "https://indianairforce.nic.in"}
        ]
    },
    "UPSC_CSE": {
        "resources": [
            {
                "title": "NCERT Books (Class 6-12)",
                "type": "book",
                "url": "https://ncert.nic.in/textbook.php",
                "description": "Foundation for all subjects",
                "relevance_score": 1.0,
                "is_free": True
            },
            {
                "title": "Indian Polity by M. Laxmikanth",
                "type": "book",
                "url": None,
                "description": "Complete polity coverage",
                "relevance_score": 0.98,
                "is_free": False
            },
            {
                "title": "India's Struggle for Independence by Bipan Chandra",
                "type": "book",
                "url": None,
                "description": "Modern Indian history",
                "relevance_score": 0.95,
                "is_free": False
            },
            {
                "title": "Certificate Physical and Human Geography by G.C. Leong",
                "type": "book",
                "url": None,
                "description": "Geography fundamentals",
                "relevance_score": 0.93,
                "is_free": False
            },
            {
                "title": "Indian Economy by Ramesh Singh",
                "type": "book",
                "url": None,
                "description": "Comprehensive economics guide",
                "relevance_score": 0.94,
                "is_free": False
            },
            {
                "title": "UPSC Official Website",
                "type": "website",
                "url": "https://www.upsc.gov.in",
                "description": "Official notifications, syllabus, previous papers",
                "relevance_score": 1.0,
                "is_free": True
            },
            {
                "title": "InsightsIAS",
                "type": "website",
                "url": "https://www.insightsonindia.com",
                "description": "Daily current affairs and answer writing",
                "relevance_score": 0.92,
                "is_free": True
            },
            {
                "title": "Vision IAS",
                "type": "course",
                "url": "https://www.visionias.in",
                "description": "Comprehensive UPSC CSE coaching",
                "relevance_score": 0.90,
                "is_free": False
            }
        ],
        "study_tips": [
            "Start with NCERT textbooks as foundation",
            "Read The Hindu or Indian Express daily",
            "Make concise notes for quick revision",
            "Practice answer writing regularly",
            "Join test series for prelims and mains",
            "Select optional subject wisely based on background",
            "Maintain consistency in preparation",
            "Focus on understanding concepts rather than rote learning",
            "Stay updated with current affairs",
            "Practice mock interviews"
        ],
        "exam_pattern": {
            "prelims": "2 papers (GS Paper I - 200 marks, CSAT - 200 marks qualifying)",
            "mains": "9 papers (Essay, GS 1-4, Optional 1-2, Language papers)",
            "interview": "275 marks",
            "total_marks": "2025 (Mains + Interview)",
            "attempts": "6 for General, 9 for OBC, Unlimited for SC/ST",
            "negative_marking": "Yes in Prelims, 1/3rd for each wrong answer"
        },
        "previous_papers": [
            {"year": "2023", "url": "https://www.upsc.gov.in/previous-papers"},
            {"year": "2022", "url": "https://www.upsc.gov.in/previous-papers"},
            {"year": "2021", "url": "https://www.upsc.gov.in/previous-papers"}
        ]
    },
    "ARMY_GD": {
        "resources": [
            {
                "title": "Kiran's Army GD Guide",
                "type": "book",
                "url": None,
                "description": "Complete preparation guide for Army GD",
                "relevance_score": 0.90,
                "is_free": False
            },
            {
                "title": "Lucent's General Knowledge",
                "type": "book",
                "url": None,
                "description": "GK preparation",
                "relevance_score": 0.88,
                "is_free": False
            },
            {
                "title": "Indian Army Official Website",
                "type": "website",
                "url": "https://joinindianarmy.nic.in",
                "description": "Official recruitment notifications",
                "relevance_score": 1.0,
                "is_free": True
            },
            {
                "title": "Defence Direct Education YouTube",
                "type": "video",
                "url": "https://www.youtube.com/@DefenceDirectEducation",
                "description": "Free video lectures for Army exams",
                "relevance_score": 0.85,
                "is_free": True
            }
        ],
        "study_tips": [
            "Focus on physical fitness from day one",
            "Practice running 1.6 km regularly",
            "Master pull-ups and other physical tests",
            "Study GK from newspapers and current affairs",
            "Practice basic mathematics daily",
            "Learn about Indian Army structure and ranks",
            "Maintain discipline and punctuality"
        ],
        "exam_pattern": {
            "physical_test": "1.6 km run, Pull-ups, 9 feet ditch, Zig-zag balance",
            "written_exam": "GK, GS, Mathematics (50 questions, 100 marks)",
            "duration": "1 hour",
            "medical_test": "Height, Weight, Chest, Vision",
            "negative_marking": "No negative marking"
        },
        "previous_papers": [
            {"year": "2023", "url": "https://joinindianarmy.nic.in"},
            {"year": "2022", "url": "https://joinindianarmy.nic.in"}
        ]
    },
    "AGNIVEER": {
        "resources": [
            {
                "title": "Agnipath Scheme Complete Guide",
                "type": "book",
                "url": None,
                "description": "Comprehensive guide for Agniveer recruitment",
                "relevance_score": 0.92,
                "is_free": False
            },
            {
                "title": "Lucent's General Knowledge",
                "type": "book",
                "url": None,
                "description": "GK for competitive exams",
                "relevance_score": 0.88,
                "is_free": False
            },
            {
                "title": "Indian Army Agniveer Portal",
                "type": "website",
                "url": "https://joinindianarmy.nic.in",
                "description": "Official Agniveer recruitment portal",
                "relevance_score": 1.0,
                "is_free": True
            },
            {
                "title": "Study IQ Education",
                "type": "video",
                "url": "https://www.studyiq.com",
                "description": "Free video courses for defence exams",
                "relevance_score": 0.83,
                "is_free": True
            }
        ],
        "study_tips": [
            "Build strong physical fitness",
            "Practice running and endurance exercises",
            "Focus on GK and current affairs",
            "Study basic mathematics and science",
            "Understand Agnipath scheme benefits and terms",
            "Practice previous year papers",
            "Maintain medical fitness standards"
        ],
        "exam_pattern": {
            "common_entrance_exam": "GK, Mathematics, General Science",
            "physical_fitness": "Running, endurance tests",
            "medical_examination": "As per military standards",
            "duration": "4 years of service",
            "negative_marking": "May vary by exam"
        },
        "previous_papers": [
            {"year": "2023", "url": "https://joinindianarmy.nic.in"},
            {"year": "2022", "url": "https://joinindianarmy.nic.in"}
        ]
    }
}

def get_role_resources(role: str) -> ResourcesResponse:
    """
    Get curated resources for a specific role
    """
    # Normalize role name to match database keys
    role_key = _normalize_role_name(role)
    
    # Get resources from database
    role_data = RESOURCES_DATABASE.get(role_key)
    
    if not role_data:
        # Return default resources if specific role not found
        role_data = RESOURCES_DATABASE.get("ARMY_GD", {})
    
    return ResourcesResponse(
        role=role,
        resources=role_data.get("resources", []),
        study_tips=role_data.get("study_tips", []),
        exam_pattern=role_data.get("exam_pattern", {}),
        previous_papers=role_data.get("previous_papers", [])
    )

def _normalize_role_name(role: str) -> str:
    """Normalize role name to match database keys"""
    role_lower = role.lower()
    
    if "nda" in role_lower:
        return "NDA"
    elif "cds" in role_lower:
        return "CDS"
    elif "afcat" in role_lower or "air force" in role_lower:
        return "AFCAT"
    elif "upsc" in role_lower or "ias" in role_lower or "civil service" in role_lower:
        return "UPSC_CSE"
    elif "general duty" in role_lower or "soldier gd" in role_lower:
        return "ARMY_GD"
    elif "agniveer" in role_lower:
        return "AGNIVEER"
    else:
        return "ARMY_GD"  # Default
