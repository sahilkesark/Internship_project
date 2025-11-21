"""
Exam-Specific Configuration Service
Contains detailed information for different defence and civil service exams
"""

from typing import Dict, List
from datetime import datetime, timedelta

# Comprehensive Exam Configurations
EXAM_CONFIGS = {
    "NDA": {
        "exam_name": "National Defence Academy & Naval Academy Examination",
        "exam_code": "NDA",
        "conducting_body": "UPSC",
        "exam_frequency": "Twice a year (April & September)",
        "age_limit": {"min": 16.5, "max": 19.5},
        "education_requirement": "12th Pass",
        "exam_pattern": {
            "papers": [
                {
                    "name": "Mathematics",
                    "duration_minutes": 150,
                    "max_marks": 300,
                    "sections": ["Algebra", "Matrices", "Trigonometry", "Analytical Geometry", "Differential Calculus", "Integral Calculus", "Vectors", "Statistics", "Probability"]
                },
                {
                    "name": "General Ability Test (GAT)",
                    "duration_minutes": 150,
                    "max_marks": 600,
                    "sections": ["English", "Physics", "Chemistry", "General Science", "History", "Geography", "Current Affairs"]
                }
            ],
            "total_marks": 900,
            "ssb_interview": "Stage 2 - 5 days",
            "medical_exam": "Stage 3",
            "negative_marking": "1/3rd marks for each wrong answer"
        },
        "syllabus": {
            "Mathematics": {
                "topics": [
                    "Algebra: Sets, Relations, Functions, Complex Numbers, Quadratic Equations",
                    "Matrices & Determinants: Types, Operations, Inverse, Cramer's Rule",
                    "Trigonometry: Angles, Ratios, Identities, Equations, Heights & Distances",
                    "Analytical Geometry 2D & 3D: Straight Lines, Circles, Parabola, Ellipse, Hyperbola",
                    "Differential Calculus: Limits, Continuity, Differentiation, Applications",
                    "Integral Calculus: Integration methods, Definite Integrals, Applications",
                    "Vector Algebra: Vector operations, Scalar & Vector products",
                    "Statistics & Probability: Mean, Median, Mode, Variance, Probability theory"
                ],
                "study_hours": 200,
                "difficulty": "High"
            },
            "English": {
                "topics": [
                    "Grammar: Tenses, Articles, Prepositions, Conjunctions",
                    "Vocabulary: Synonyms, Antonyms, One-word substitution",
                    "Comprehension: Paragraph reading and analysis",
                    "Sentence Correction & Improvement",
                    "Spotting Errors",
                    "Ordering of Sentences"
                ],
                "study_hours": 80,
                "difficulty": "Medium"
            },
            "Physics": {
                "topics": [
                    "Physical Properties of Matter",
                    "Motion of Objects, Force, Momentum",
                    "Work, Power, Energy",
                    "Heat & Temperature",
                    "Light: Reflection, Refraction",
                    "Electricity & Magnetism",
                    "Modern Physics basics"
                ],
                "study_hours": 100,
                "difficulty": "High"
            },
            "Chemistry": {
                "topics": [
                    "Physical & Chemical changes",
                    "Elements, Mixtures, Compounds",
                    "Atomic Structure",
                    "Periodic Table",
                    "Chemical Bonding",
                    "Acids, Bases, Salts",
                    "Oxidation & Reduction"
                ],
                "study_hours": 80,
                "difficulty": "Medium"
            },
            "General Knowledge": {
                "topics": [
                    "Indian History: Ancient, Medieval, Modern",
                    "Geography: Physical, Economic, Social",
                    "Indian Polity & Constitution",
                    "Economics: Basic concepts",
                    "General Science",
                    "Current Affairs: National & International"
                ],
                "study_hours": 120,
                "difficulty": "Medium"
            }
        },
        "study_plan_template": {
            "total_recommended_hours": 600,
            "phase_1": {"name": "Foundation", "duration_weeks": 8, "focus": "Basic concepts and theory"},
            "phase_2": {"name": "Practice", "duration_weeks": 8, "focus": "Problem solving and mock tests"},
            "phase_3": {"name": "Revision", "duration_weeks": 4, "focus": "Quick revision and test series"}
        },
        "recommended_books": [
            "R.S. Aggarwal - Objective General English",
            "Pathfinder for NDA/NA Entrance Examination",
            "Lucent's General Knowledge",
            "NCERT Class 11-12 Physics, Chemistry, Maths"
        ],
        "important_websites": [
            "https://upsc.gov.in",
            "https://www.ndaindia.edu.in"
        ]
    },
    
    "CDS": {
        "exam_name": "Combined Defence Services Examination",
        "exam_code": "CDS",
        "conducting_body": "UPSC",
        "exam_frequency": "Twice a year (February & November)",
        "age_limit": {"IMA": {"min": 19, "max": 24}, "INA": {"min": 19, "max": 24}, "AFA": {"min": 20, "max": 24}, "OTA": {"min": 19, "max": 25}},
        "education_requirement": "Graduation (IMA/INA/AFA), Graduation or equivalent (OTA)",
        "exam_pattern": {
            "papers": [
                {
                    "name": "English",
                    "duration_minutes": 120,
                    "max_marks": 100,
                    "sections": ["Grammar", "Vocabulary", "Comprehension"]
                },
                {
                    "name": "General Knowledge",
                    "duration_minutes": 120,
                    "max_marks": 100,
                    "sections": ["History", "Geography", "Polity", "Economics", "General Science", "Current Affairs"]
                },
                {
                    "name": "Elementary Mathematics (for IMA/INA/AFA only)",
                    "duration_minutes": 120,
                    "max_marks": 100,
                    "sections": ["Arithmetic", "Algebra", "Trigonometry", "Geometry", "Statistics"]
                }
            ],
            "total_marks": 300,
            "ssb_interview": "Stage 2 - 5 days",
            "medical_exam": "Stage 3",
            "negative_marking": "1/3rd marks for each wrong answer"
        },
        "syllabus": {
            "English": {
                "topics": [
                    "Grammar: Parts of Speech, Tenses, Voice, Narration",
                    "Vocabulary: Synonyms, Antonyms, Idioms, Phrases",
                    "Comprehension: Reading passages and inference",
                    "Sentence Arrangement",
                    "Error Spotting",
                    "Fill in the blanks"
                ],
                "study_hours": 80,
                "difficulty": "Medium"
            },
            "General Knowledge": {
                "topics": [
                    "History: Ancient, Medieval, Modern India, World History",
                    "Geography: Physical, Economic, Social, World Geography",
                    "Indian Polity: Constitution, Governance, Rights",
                    "Economics: Indian Economy, Budget, Banking",
                    "General Science: Physics, Chemistry, Biology, Technology",
                    "Current Affairs: National and International events",
                    "Defence Related Topics: Armed Forces, Weapons, Wars"
                ],
                "study_hours": 150,
                "difficulty": "High"
            },
            "Elementary Mathematics": {
                "topics": [
                    "Arithmetic: Number Systems, HCF/LCM, Percentages, Profit/Loss, SI/CI",
                    "Algebra: Linear equations, Quadratic equations, Progressions",
                    "Trigonometry: Ratios, Identities, Heights & Distances",
                    "Geometry: Lines, Angles, Triangles, Circles, Areas, Volumes",
                    "Mensuration: 2D and 3D figures",
                    "Statistics & Probability: Mean, Median, Mode, Basic probability"
                ],
                "study_hours": 120,
                "difficulty": "Medium"
            }
        },
        "study_plan_template": {
            "total_recommended_hours": 400,
            "phase_1": {"name": "Foundation", "duration_weeks": 6, "focus": "Concept building"},
            "phase_2": {"name": "Practice", "duration_weeks": 6, "focus": "Mock tests and practice"},
            "phase_3": {"name": "Revision", "duration_weeks": 3, "focus": "Quick revision and weak areas"}
        },
        "recommended_books": [
            "Arihant CDS Solved Papers",
            "Pathfinder CDS Examination",
            "Lucent's General Knowledge",
            "Wren & Martin for English"
        ],
        "important_websites": [
            "https://upsc.gov.in",
            "https://joinindianarmy.nic.in"
        ]
    },
    
    "AFCAT": {
        "exam_name": "Air Force Common Admission Test",
        "exam_code": "AFCAT",
        "conducting_body": "Indian Air Force",
        "exam_frequency": "Twice a year (February & August)",
        "age_limit": {"Flying Branch": {"min": 20, "max": 24}, "Ground Duty (Technical)": {"min": 20, "max": 26}, "Ground Duty (Non-Technical)": {"min": 20, "max": 26}},
        "education_requirement": "Graduation in any discipline (specific branches for technical)",
        "exam_pattern": {
            "papers": [
                {
                    "name": "AFCAT",
                    "duration_minutes": 120,
                    "max_marks": 300,
                    "total_questions": 100,
                    "sections": [
                        "General Awareness - 20 questions",
                        "Verbal Ability in English - 30 questions",
                        "Numerical Ability - 15 questions",
                        "Reasoning and Military Aptitude Test - 35 questions"
                    ]
                },
                {
                    "name": "EKT (For Technical Branch)",
                    "duration_minutes": 45,
                    "max_marks": 150,
                    "sections": ["Mechanical/Computer Science/Electronics based on graduation"]
                }
            ],
            "afsb_interview": "Stage 2 - 5 days",
            "medical_exam": "Stage 3",
            "negative_marking": "1 mark deducted for each wrong answer"
        },
        "syllabus": {
            "General Awareness": {
                "topics": [
                    "History: Indian and World",
                    "Geography: Physical, Economic",
                    "Polity: Indian Constitution, Governance",
                    "Current Affairs: National & International",
                    "Defence and Sports",
                    "Art and Culture",
                    "Environment and Ecology"
                ],
                "study_hours": 100,
                "difficulty": "Medium"
            },
            "Verbal Ability": {
                "topics": [
                    "Comprehension",
                    "Error Detection",
                    "Sentence Completion",
                    "Synonyms & Antonyms",
                    "Testing of Vocabulary",
                    "Idioms and Phrases"
                ],
                "study_hours": 60,
                "difficulty": "Medium"
            },
            "Numerical Ability": {
                "topics": [
                    "Decimal Fractions",
                    "Simplification",
                    "Average, Percentage",
                    "Profit & Loss",
                    "Ratio & Proportion",
                    "Time & Work",
                    "Time & Distance"
                ],
                "study_hours": 80,
                "difficulty": "Medium"
            },
            "Reasoning & Military Aptitude": {
                "topics": [
                    "Verbal and Non-Verbal Reasoning",
                    "Spatial Ability",
                    "Numerical Reasoning",
                    "Military Aptitude Test topics"
                ],
                "study_hours": 80,
                "difficulty": "High"
            }
        },
        "study_plan_template": {
            "total_recommended_hours": 350,
            "phase_1": {"name": "Foundation", "duration_weeks": 5, "focus": "Basic concepts"},
            "phase_2": {"name": "Practice", "duration_weeks": 5, "focus": "Mock tests"},
            "phase_3": {"name": "Revision", "duration_weeks": 2, "focus": "Quick revision"}
        },
        "recommended_books": [
            "Arihant AFCAT Topic-wise Solved Papers",
            "Pathfinder AFCAT",
            "R.S. Aggarwal Quantitative Aptitude",
            "Lucent's General Knowledge"
        ],
        "important_websites": [
            "https://afcat.cdac.in",
            "https://indianairforce.nic.in"
        ]
    },
    
    "UPSC_CSE": {
        "exam_name": "Union Public Service Commission - Civil Services Examination",
        "exam_code": "UPSC_CSE",
        "conducting_body": "UPSC",
        "exam_frequency": "Once a year (Prelims in June, Mains in September)",
        "age_limit": {"General": {"min": 21, "max": 32}, "OBC": {"min": 21, "max": 35}, "SC/ST": {"min": 21, "max": 37}},
        "education_requirement": "Graduation in any discipline",
        "exam_pattern": {
            "prelims": {
                "papers": [
                    {"name": "GS Paper I", "duration_minutes": 120, "max_marks": 200, "qualifying": False},
                    {"name": "GS Paper II (CSAT)", "duration_minutes": 120, "max_marks": 200, "qualifying": True, "min_qualifying": 33}
                ]
            },
            "mains": {
                "papers": [
                    {"name": "Essay", "max_marks": 250},
                    {"name": "GS Paper I", "max_marks": 250},
                    {"name": "GS Paper II", "max_marks": 250},
                    {"name": "GS Paper III", "max_marks": 250},
                    {"name": "GS Paper IV (Ethics)", "max_marks": 250},
                    {"name": "Optional Paper I", "max_marks": 250},
                    {"name": "Optional Paper II", "max_marks": 250},
                    {"name": "Language Paper I", "max_marks": 300, "qualifying": True},
                    {"name": "Language Paper II", "max_marks": 300, "qualifying": True}
                ],
                "total_marks": 1750
            },
            "interview": {
                "marks": 275
            },
            "negative_marking": "1/3rd marks for wrong answers in Prelims"
        },
        "syllabus": {
            "Prelims_GS1": {
                "topics": [
                    "History of India and Indian National Movement",
                    "Indian and World Geography",
                    "Indian Polity and Governance",
                    "Economic and Social Development",
                    "Environmental Ecology, Biodiversity and Climate Change",
                    "General Science"
                ],
                "study_hours": 400,
                "difficulty": "Very High"
            },
            "Prelims_CSAT": {
                "topics": [
                    "Comprehension",
                    "Interpersonal skills",
                    "Logical reasoning and analytical ability",
                    "Decision making and problem solving",
                    "General mental ability",
                    "Basic numeracy",
                    "Data interpretation"
                ],
                "study_hours": 150,
                "difficulty": "Medium"
            },
            "Mains_GS": {
                "topics": [
                    "Essay Writing",
                    "Indian Heritage and Culture, History and Geography",
                    "Governance, Constitution, Polity, Social Justice",
                    "Technology, Economic Development, Biodiversity, Environment",
                    "Ethics, Integrity, and Aptitude"
                ],
                "study_hours": 800,
                "difficulty": "Very High"
            },
            "Optional_Subject": {
                "topics": ["Choose from 48 optional subjects"],
                "study_hours": 400,
                "difficulty": "Very High"
            }
        },
        "study_plan_template": {
            "total_recommended_hours": 2000,
            "phase_1": {"name": "Foundation", "duration_weeks": 20, "focus": "NCERT and Basic books"},
            "phase_2": {"name": "Advanced", "duration_weeks": 20, "focus": "Standard books and current affairs"},
            "phase_3": {"name": "Test Series", "duration_weeks": 12, "focus": "Mock tests and practice"},
            "phase_4": {"name": "Revision", "duration_weeks": 8, "focus": "Revision and weak areas"}
        },
        "recommended_books": [
            "NCERTs (Class 6-12)",
            "Indian Polity by M. Laxmikanth",
            "Indian Economy by Ramesh Singh",
            "Certificate Physical and Human Geography by G.C. Leong",
            "India's Struggle for Independence by Bipan Chandra",
            "The Hindu/Indian Express (Daily newspaper)"
        ],
        "important_websites": [
            "https://upsc.gov.in",
            "https://www.pib.gov.in",
            "https://www.thehindu.com"
        ]
    },
    
    "SSC_CGL": {
        "exam_name": "Staff Selection Commission - Combined Graduate Level",
        "exam_code": "SSC_CGL",
        "conducting_body": "Staff Selection Commission",
        "exam_frequency": "Once a year",
        "age_limit": {"min": 18, "max": 32},
        "education_requirement": "Graduation",
        "exam_pattern": {
            "tier_1": {
                "duration_minutes": 60,
                "sections": [
                    {"name": "General Intelligence & Reasoning", "questions": 25, "marks": 50},
                    {"name": "General Awareness", "questions": 25, "marks": 50},
                    {"name": "Quantitative Aptitude", "questions": 25, "marks": 50},
                    {"name": "English Comprehension", "questions": 25, "marks": 50}
                ],
                "total_marks": 200,
                "negative_marking": "0.50 marks for each wrong answer"
            },
            "tier_2": {
                "papers": [
                    {"name": "Quantitative Abilities", "duration_minutes": 120, "marks": 200},
                    {"name": "English Language", "duration_minutes": 120, "marks": 200},
                    {"name": "Statistics (for specific posts)", "duration_minutes": 120, "marks": 200},
                    {"name": "General Studies", "duration_minutes": 120, "marks": 200}
                ]
            }
        },
        "syllabus": {
            "Reasoning": {
                "topics": [
                    "Analogies", "Similarities", "Differences",
                    "Space visualization", "Problem solving",
                    "Analysis", "Judgment", "Decision making",
                    "Visual memory", "Discrimination", "Observation",
                    "Relationship concepts", "Verbal and figure classification"
                ],
                "study_hours": 100,
                "difficulty": "Medium"
            },
            "Quantitative_Aptitude": {
                "topics": [
                    "Number Systems", "Computation of whole numbers",
                    "Decimals and fractions", "Percentages",
                    "Ratio and Proportion", "Averages",
                    "Interest", "Profit and Loss", "Discount",
                    "Time and Distance", "Time and Work",
                    "Basic algebra", "Geometry", "Trigonometry"
                ],
                "study_hours": 150,
                "difficulty": "Medium"
            }
        },
        "study_plan_template": {
            "total_recommended_hours": 500,
            "phase_1": {"name": "Foundation", "duration_weeks": 10, "focus": "Basics"},
            "phase_2": {"name": "Practice", "duration_weeks": 10, "focus": "Speed and accuracy"},
            "phase_3": {"name": "Mocks", "duration_weeks": 4, "focus": "Test series"}
        },
        "recommended_books": [
            "Quantitative Aptitude by R.S. Aggarwal",
            "English by S.P. Bakshi",
            "General Awareness by Lucent",
            "Reasoning by M.K. Pandey"
        ],
        "important_websites": [
            "https://ssc.nic.in"
        ]
    },

    "State_PSC": {
        "exam_name": "State Public Service Commission Examinations",
        "exam_code": "State_PSC",
        "conducting_body": "Respective State PSCs",
        "exam_frequency": "Varies by state (Usually annually)",
        "age_limit": {"min": 21, "max": 40},
        "education_requirement": "Graduation",
        "exam_pattern": {
            "prelims": {
                "papers": [
                    {"name": "General Studies", "duration_minutes": 120, "max_marks": 200}
                ]
            },
            "mains": {
                "papers": [
                    {"name": "General Essays", "max_marks": 150},
                    {"name": "General Studies I", "max_marks": 200},
                    {"name": "General Studies II", "max_marks": 200},
                    {"name": "General Studies III", "max_marks": 200},
                    {"name": "Optional Paper I", "max_marks": 200},
                    {"name": "Optional Paper II", "max_marks": 200}
                ],
                "total_marks": 1150
            },
            "interview": {"marks": 100}
        },
        "syllabus": {
            "General_Studies": {
                "topics": [
                    "State History and Culture",
                    "State Geography and Resources",
                    "State Polity and Administration",
                    "State Economy and Development",
                    "Current Affairs - State and National",
                    "Indian History, Geography, Polity",
                    "General Science and Environment"
                ],
                "study_hours": 600,
                "difficulty": "High"
            }
        },
        "study_plan_template": {
            "total_recommended_hours": 1200,
            "phase_1": {"name": "Foundation", "duration_weeks": 16, "focus": "State-specific syllabus"},
            "phase_2": {"name": "Practice", "duration_weeks": 12, "focus": "Test series"},
            "phase_3": {"name": "Revision", "duration_weeks": 6, "focus": "Quick revision"}
        },
        "recommended_books": [
            "State-specific GK books",
            "NCERTs",
            "Indian Polity by M. Laxmikanth",
            "State PSC Previous Years Papers"
        ],
        "important_websites": [
            "Respective State PSC websites"
        ]
    }
}


def get_exam_list() -> List[Dict]:
    """Get list of all available exams"""
    exams = []
    for code, config in EXAM_CONFIGS.items():
        exams.append({
            "exam_code": code,
            "exam_name": config["exam_name"],
            "conducting_body": config["conducting_body"],
            "exam_frequency": config["exam_frequency"],
            "difficulty": config["syllabus"][list(config["syllabus"].keys())[0]].get("difficulty", "Medium")
        })
    return exams


def get_exam_details(exam_code: str) -> Dict:
    """Get detailed information about a specific exam"""
    return EXAM_CONFIGS.get(exam_code, None)


def recommend_exam_based_on_profile(education_level: str, age: int, interests: List[str], olq_score: float) -> List[str]:
    """Recommend suitable exams based on user profile"""
    recommendations = []
    
    # Age-based filtering
    for code, config in EXAM_CONFIGS.items():
        age_limit = config.get("age_limit", {})
        
        # Handle different age limit formats
        if isinstance(age_limit, dict):
            if "min" in age_limit and "max" in age_limit:
                if age_limit["min"] <= age <= age_limit["max"]:
                    recommendations.append(code)
            else:
                # Multiple categories with different age limits
                for category, limits in age_limit.items():
                    if isinstance(limits, dict) and limits.get("min", 0) <= age <= limits.get("max", 100):
                        recommendations.append(code)
                        break
    
    # Education-based filtering
    if education_level in ["high_school", "intermediate"]:
        # Only NDA suitable
        recommendations = [code for code in recommendations if code == "NDA"]
    
    # OLQ score based recommendations
    if olq_score >= 80:
        # High scorers suitable for all exams
        pass
    elif olq_score >= 65:
        # Remove very challenging exams for moderate scorers
        recommendations = [code for code in recommendations if code != "UPSC_CSE"]
    else:
        # For lower scorers, recommend less competitive exams
        recommendations = [code for code in recommendations if code in ["SSC_CGL", "State_PSC"]]
    
    return list(set(recommendations))
