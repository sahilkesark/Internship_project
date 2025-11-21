from typing import List
from app.models.schemas import OLQResponse, OLQ_QUESTIONS
from app.services.question_bank_service import QUESTION_BANK

def calculate_olq_score(responses: List[OLQResponse]) -> float:
    """
    Calculate OLQ score based on responses
    Returns a score between 0-100
    """
    if not responses:
        return 0.0
    
    total_score = 0
    max_score = 0
    
    for response in responses:
        # Handle both dict and OLQResponse object
        if isinstance(response, dict):
            question_id = response.get("question_id")
            selected_option = response.get("selected_option")
        else:
            question_id = response.question_id
            selected_option = response.selected_option
        
        # Find the question in the new question bank
        question = next(
            (q for q in QUESTION_BANK if q["question_id"] == question_id),
            None
        )
        
        if question:
            # Award points based on how close to optimal answer
            correct_option = question["correct_option"]
            weight = question.get("weight", 10)  # Default weight of 10 for new questions
            
            # Calculate points: full points for correct, partial for close answers
            if selected_option == correct_option:
                points = weight
            elif abs(selected_option - correct_option) == 1:
                points = weight * 0.5  # 50% for adjacent answer
            else:
                points = 0
            
            total_score += points
            max_score += weight
    
    # Convert to percentage
    if max_score > 0:
        return (total_score / max_score) * 100
    
    return 0.0

def get_olq_analysis(responses: List[OLQResponse]) -> dict:
    """
    Analyze OLQ responses and provide insights
    """
    score = calculate_olq_score(responses)
    
    # Categorize performance
    if score >= 80:
        category = "Excellent"
        description = "Outstanding leadership potential with strong decision-making and interpersonal skills."
    elif score >= 65:
        category = "Very Good"
        description = "Strong leadership qualities with good situational awareness and problem-solving ability."
    elif score >= 50:
        category = "Good"
        description = "Demonstrated leadership potential with room for development in specific areas."
    elif score >= 35:
        category = "Average"
        description = "Basic leadership understanding but requires significant development and training."
    else:
        category = "Below Average"
        description = "Limited demonstration of leadership qualities. Consider enlisted roles or further development."
    
    # Analyze strengths and weaknesses
    strengths = []
    weaknesses = []
    
    for response in responses:
        # Handle both dict and OLQResponse object
        if isinstance(response, dict):
            question_id = response.get("question_id")
            selected_option = response.get("selected_option")
        else:
            question_id = response.question_id
            selected_option = response.selected_option
        
        question = next(
            (q for q in QUESTION_BANK if q["question_id"] == question_id),
            None
        )
        
        if question:
            if selected_option == question["correct_option"]:
                # Map question to trait
                trait = _map_question_to_trait(question_id)
                strengths.append(trait)
            else:
                trait = _map_question_to_trait(question_id)
                weaknesses.append(trait)
    
    return {
        "score": score,
        "category": category,
        "description": description,
        "strengths": strengths[:3] if strengths else ["Basic awareness"],
        "weaknesses": weaknesses[:3] if weaknesses else ["None identified"]
    }

def _map_question_to_trait(question_id: int) -> str:
    """Map question ID to leadership trait - uses category from question bank"""
    # Find the question in the question bank
    question = next(
        (q for q in QUESTION_BANK if q["question_id"] == question_id),
        None
    )
    
    if question and "category" in question:
        return question["category"]
    
    # Fallback for old questions
    trait_map = {
        1: "Leadership",
        2: "Decision Making",
        3: "Integrity",
        4: "Adaptability",
        5: "Innovation",
        6: "Crisis Management",
        7: "Risk Taking",
        8: "Decision Under Pressure",
        9: "Self-Awareness",
        10: "Strategic Thinking"
    }
    return trait_map.get(question_id, "General Leadership")
