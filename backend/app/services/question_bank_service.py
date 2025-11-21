"""
Enhanced OLQ Question Bank Service with Randomization
Provides diverse questions with varied correct answers
"""

import random
from typing import List, Dict
from datetime import datetime

# Comprehensive OLQ Question Bank (50 questions with diverse correct answers)
QUESTION_BANK = [
    # Leadership & Team Management
    {
        "question_id": 1,
        "category": "Leadership",
        "question": "You are leading a team on a challenging project with a tight deadline. One of your team members is struggling. What do you do?",
        "options": [
            "Take over their work to ensure quality and meet the deadline",
            "Provide guidance, redistribute tasks if needed, and monitor progress closely",
            "Let them figure it out on their own to build independence",
            "Report the issue to higher management immediately"
        ],
        "correct_option": 1,
        "difficulty": "medium"
    },
    {
        "question_id": 2,
        "category": "Decision Making",
        "question": "During a high-pressure situation, your superior gives you an order that you believe might not be the most effective approach. What would you do?",
        "options": [
            "Follow the order without question as they have more experience",
            "Politely present your alternative suggestion with reasoning and follow their final decision",
            "Refuse to follow and implement your own plan",
            "Follow the order but document your concerns for later"
        ],
        "correct_option": 1,
        "difficulty": "hard"
    },
    {
        "question_id": 3,
        "category": "Integrity",
        "question": "You witness a colleague taking credit for work that was actually done by your team. How do you respond?",
        "options": [
            "Confront them publicly in the next meeting",
            "Privately address the issue with them first, then escalate if needed",
            "Ignore it to avoid conflict",
            "Take credit for their work next time"
        ],
        "correct_option": 1,
        "difficulty": "medium"
    },
    {
        "question_id": 4,
        "category": "Adaptability",
        "question": "You are assigned to work in a remote area with limited resources for an extended period. How do you feel about this?",
        "options": [
            "Concerned and would try to get the assignment changed",
            "View it as a challenge and opportunity to prove adaptability and leadership",
            "Accept it reluctantly as part of duty",
            "Would consider it a punishment"
        ],
        "correct_option": 1,
        "difficulty": "easy"
    },
    {
        "question_id": 5,
        "category": "Innovation",
        "question": "You discover a more efficient process that could save time and resources, but it requires changing established procedures. What do you do?",
        "options": [
            "Keep it to yourself to avoid complications",
            "Document the proposal with data and present it through proper channels",
            "Implement it immediately without approval",
            "Share it informally with colleagues but take no formal action"
        ],
        "correct_option": 1,
        "difficulty": "medium"
    },
    
    # More varied questions with different correct answers
    {
        "question_id": 6,
        "category": "Crisis Management",
        "question": "Your team is demoralized after a failed mission. As a leader, what is your priority?",
        "options": [
            "Identify who made mistakes and take disciplinary action",
            "Analyze what went wrong, learn from it, and motivate the team for future success",
            "Move on quickly to the next task without discussion",
            "Blame external factors to protect the team"
        ],
        "correct_option": 1,
        "difficulty": "medium"
    },
    {
        "question_id": 7,
        "category": "Risk Taking",
        "question": "You have to choose between a comfortable desk job with better facilities or a challenging field position with more responsibility. What would you prefer?",
        "options": [
            "Definitely the comfortable desk job",
            "The challenging field position for growth and experience",
            "Whichever pays more",
            "Would try to negotiate for desk job with same responsibility"
        ],
        "correct_option": 1,
        "difficulty": "easy"
    },
    {
        "question_id": 8,
        "category": "Decision Under Pressure",
        "question": "During a crisis, you need to make a quick decision with incomplete information. How do you proceed?",
        "options": [
            "Wait for complete information even if it delays action",
            "Assess available facts, consider risks, make the best possible decision and act",
            "Pass the decision to someone else",
            "Make a random choice and hope for the best"
        ],
        "correct_option": 1,
        "difficulty": "hard"
    },
    {
        "question_id": 9,
        "category": "Self-Awareness",
        "question": "You are given feedback that your communication style is sometimes too direct and affects team morale. How do you respond?",
        "options": [
            "Ignore the feedback as direct communication is effective",
            "Reflect on it, seek specific examples, and work on balancing directness with empathy",
            "Become overly cautious and stop giving honest feedback",
            "Defend your style and explain why it's necessary"
        ],
        "correct_option": 1,
        "difficulty": "medium"
    },
    {
        "question_id": 10,
        "category": "Strategic Thinking",
        "question": "You have limited resources and must choose between two critical tasks. Both are important but you can only prioritize one. How do you decide?",
        "options": [
            "Choose the easier task to ensure completion",
            "Analyze impact, urgency, and long-term consequences, then decide based on overall benefit",
            "Try to do both partially",
            "Seek approval from superior without providing your analysis"
        ],
        "correct_option": 1,
        "difficulty": "hard"
    },
    
    # NEW QUESTIONS WITH VARIED CORRECT ANSWERS
    {
        "question_id": 11,
        "category": "Time Management",
        "question": "You have multiple urgent tasks with conflicting deadlines. What is your approach?",
        "options": [
            "Work on all tasks simultaneously to show multitasking ability",
            "Prioritize based on impact and urgency, delegate where possible",
            "Focus only on your favorite tasks first",
            "Inform everyone you cannot meet any deadline"
        ],
        "correct_option": 1,
        "difficulty": "medium"
    },
    {
        "question_id": 12,
        "category": "Communication",
        "question": "During a briefing, you notice team members are confused but not asking questions. What do you do?",
        "options": [
            "Continue as planned, they should ask if confused",
            "Pause, check understanding, and clarify complex points",
            "Speed up to finish quickly",
            "Ask why they're not paying attention"
        ],
        "correct_option": 1,
        "difficulty": "easy"
    },
    {
        "question_id": 13,
        "category": "Conflict Resolution",
        "question": "Two team members are in a heated argument that is disrupting work. What's your immediate action?",
        "options": [
            "Let them sort it out themselves",
            "Intervene calmly, separate them if needed, and address the issue professionally",
            "Side with the person you like more",
            "Report both to HR immediately"
        ],
        "correct_option": 1,
        "difficulty": "medium"
    },
    {
        "question_id": 14,
        "category": "Initiative",
        "question": "You notice a potential security vulnerability that's not in your area of responsibility. What do you do?",
        "options": [
            "Ignore it as it's not your job",
            "Immediately report it to the relevant authority with your observations",
            "Try to fix it yourself without informing anyone",
            "Tell your friends about it casually"
        ],
        "correct_option": 1,
        "difficulty": "easy"
    },
    {
        "question_id": 15,
        "category": "Accountability",
        "question": "A project you led failed despite your best efforts due to unforeseen circumstances. How do you handle it?",
        "options": [
            "Blame the unforeseen circumstances and team",
            "Take responsibility, analyze failures, and present lessons learned",
            "Downplay the failure and move on",
            "Resign from the leadership position"
        ],
        "correct_option": 1,
        "difficulty": "hard"
    },
    
    # Questions with correct answer at position 0
    {
        "question_id": 16,
        "category": "Ethics",
        "question": "You discover a minor procedural violation that could save significant time but technically breaks rules. What do you do?",
        "options": [
            "Follow the rules strictly regardless of time implications",
            "Use the shortcut as it's minor and saves time",
            "Ask others what they would do",
            "Do it but keep it secret"
        ],
        "correct_option": 0,
        "difficulty": "hard"
    },
    {
        "question_id": 17,
        "category": "Courage",
        "question": "You witness senior officers making a decision you believe is unethical. What should you do?",
        "options": [
            "Report through proper channels despite potential career impact",
            "Stay quiet to protect your career",
            "Anonymously leak the information",
            "Go along with it and forget about it"
        ],
        "correct_option": 0,
        "difficulty": "hard"
    },
    {
        "question_id": 18,
        "category": "Discipline",
        "question": "You're exhausted after a long day but have mandatory physical training early next morning. What do you do?",
        "options": [
            "Attend on time regardless of how you feel",
            "Skip it this once as you're too tired",
            "Attend but arrive late",
            "Ask someone to mark your attendance"
        ],
        "correct_option": 0,
        "difficulty": "easy"
    },
    
    # Questions with correct answer at position 2
    {
        "question_id": 19,
        "category": "Emotional Intelligence",
        "question": "A team member is consistently underperforming. You discover they're going through personal issues. What's your response?",
        "options": [
            "Replace them immediately as performance is priority",
            "Ignore the personal issues and focus only on work",
            "Show empathy, offer support within boundaries, and adjust expectations temporarily",
            "Do their work for them until they recover"
        ],
        "correct_option": 2,
        "difficulty": "medium"
    },
    {
        "question_id": 20,
        "category": "Resource Management",
        "question": "You have limited budget for team welfare activities. How do you utilize it?",
        "options": [
            "Use it for a lavish event for a few people",
            "Save it for your own use",
            "Consult team, prioritize activities that benefit maximum people, and ensure transparency",
            "Don't use it at all to avoid complications"
        ],
        "correct_option": 2,
        "difficulty": "medium"
    },
    
    # Questions with correct answer at position 3
    {
        "question_id": 21,
        "category": "Learning Orientation",
        "question": "You're assigned a task requiring skills you don't have. What's your approach?",
        "options": [
            "Decline the task as you're not qualified",
            "Pretend you know and figure it out somehow",
            "Accept hesitantly and hope for the best",
            "Accept enthusiastically, identify resources, learn quickly, and seek guidance when needed"
        ],
        "correct_option": 3,
        "difficulty": "easy"
    },
    {
        "question_id": 22,
        "category": "Feedback",
        "question": "Your superior asks for honest feedback on their leadership style. What do you do?",
        "options": [
            "Give only compliments to stay safe",
            "Be brutally honest without tact",
            "Avoid giving feedback",
            "Provide balanced, constructive feedback with specific examples in a respectful manner"
        ],
        "correct_option": 3,
        "difficulty": "hard"
    },
    
    # More diverse questions
    {
        "question_id": 23,
        "category": "Teamwork",
        "question": "You're part of a team where one member is not contributing. Others want to exclude them. What do you do?",
        "options": [
            "Agree to exclude them to maintain team harmony",
            "Confront the non-contributing member publicly",
            "Understand the root cause, offer help, set clear expectations, and include them in recovery plan",
            "Report them to management without discussion"
        ],
        "correct_option": 2,
        "difficulty": "medium"
    },
    {
        "question_id": 24,
        "category": "Vision",
        "question": "You're asked to create a long-term strategy for your unit. What's your approach?",
        "options": [
            "Copy what other successful units are doing",
            "Analyze current state, future trends, stakeholder needs, and create data-driven innovative plan",
            "Make quick decisions based on intuition",
            "Ask everyone's opinion and combine all ideas"
        ],
        "correct_option": 1,
        "difficulty": "hard"
    },
    {
        "question_id": 25,
        "category": "Resilience",
        "question": "You've faced three consecutive setbacks in your career. How do you respond?",
        "options": [
            "Consider changing career paths",
            "Analyze patterns, learn from mistakes, strengthen weak areas, and persist with renewed strategy",
            "Blame circumstances and continue same approach",
            "Take extended break and avoid similar challenges"
        ],
        "correct_option": 1,
        "difficulty": "hard"
    },
    {
        "question_id": 26,
        "category": "Mentorship",
        "question": "A junior colleague seeks your mentorship. You're already very busy. What do you do?",
        "options": [
            "Politely decline as you have no time",
            "Make time for regular mentoring sessions, sharing knowledge benefits both",
            "Give generic advice and move on",
            "Direct them to read books instead"
        ],
        "correct_option": 1,
        "difficulty": "medium"
    },
    {
        "question_id": 27,
        "category": "Cultural Sensitivity",
        "question": "You're leading a diverse team with different cultural backgrounds and practices. How do you ensure team cohesion?",
        "options": [
            "Impose one culture for uniformity",
            "Respect diversity, create inclusive environment, and leverage different perspectives",
            "Keep cultural discussions out of workplace",
            "Form sub-groups by culture"
        ],
        "correct_option": 1,
        "difficulty": "medium"
    },
    {
        "question_id": 28,
        "category": "Technology Adoption",
        "question": "New technology is introduced that will change how your team works. Some resist it. What do you do?",
        "options": [
            "Force everyone to adopt it immediately",
            "Understand concerns, provide training, demonstrate benefits, and support transition",
            "Avoid using new technology yourself",
            "Let willing people adopt, ignore resisters"
        ],
        "correct_option": 1,
        "difficulty": "medium"
    },
    {
        "question_id": 29,
        "category": "Work-Life Balance",
        "question": "Your team is consistently working late hours. Productivity is declining. What's your action?",
        "options": [
            "Push them to work harder",
            "Analyze workload, optimize processes, redistribute tasks, and ensure reasonable hours",
            "Ignore it as long as work gets done",
            "Only reduce your own hours"
        ],
        "correct_option": 1,
        "difficulty": "medium"
    },
    {
        "question_id": 30,
        "category": "Recognition",
        "question": "A team member did exceptional work. How do you recognize their contribution?",
        "options": [
            "Don't recognize to avoid jealousy in team",
            "Publicly acknowledge, explain impact, and ensure appropriate rewards/growth opportunities",
            "Take credit yourself and reward them privately",
            "Give generic praise and move on"
        ],
        "correct_option": 1,
        "difficulty": "easy"
    },
    
    # Additional 20 questions for comprehensive coverage
    {
        "question_id": 31,
        "category": "Problem Solving",
        "question": "You face a complex problem with no obvious solution. What's your methodology?",
        "options": [
            "Try random solutions until something works",
            "Break down problem, gather data, brainstorm solutions, test hypotheses systematically",
            "Wait for someone else to solve it",
            "Escalate immediately without attempting"
        ],
        "correct_option": 1,
        "difficulty": "hard"
    },
    {
        "question_id": 32,
        "category": "Change Management",
        "question": "You need to implement an unpopular but necessary policy change. How do you proceed?",
        "options": [
            "Implement it suddenly without explanation",
            "Communicate reasons clearly, address concerns, provide transition support, and monitor impact",
            "Delay implementation hoping situation changes",
            "Modify the policy to make everyone happy"
        ],
        "correct_option": 1,
        "difficulty": "hard"
    },
    {
        "question_id": 33,
        "category": "Delegation",
        "question": "You have a critical task. A capable team member wants to take it on. What do you do?",
        "options": [
            "Do it yourself as it's too critical",
            "Delegate with clear instructions, checkpoints, and support",
            "Delegate and forget about it",
            "Split it equally regardless of capability"
        ],
        "correct_option": 1,
        "difficulty": "medium"
    },
    {
        "question_id": 34,
        "category": "Negotiation",
        "question": "Two departments need the same limited resource. Both have valid requirements. How do you resolve this?",
        "options": [
            "Give it to the department you prefer",
            "Understand both needs, find creative compromise, or alternative solution",
            "Split resource equally making both ineffective",
            "Let them fight it out"
        ],
        "correct_option": 1,
        "difficulty": "hard"
    },
    {
        "question_id": 35,
        "category": "Quality vs Speed",
        "question": "You must choose between delivering on time with acceptable quality or delaying for perfect quality. What do you choose?",
        "options": [
            "Always choose perfect quality regardless of time",
            "Assess criticality, deliver acceptable quality on time, and plan improvements for next iteration",
            "Always choose speed over quality",
            "Randomly decide based on mood"
        ],
        "correct_option": 1,
        "difficulty": "medium"
    },
    {
        "question_id": 36,
        "category": "Innovation vs Tradition",
        "question": "There's a traditional method that works but a newer method promises better results. What do you do?",
        "options": [
            "Always stick with traditional proven methods",
            "Evaluate new method through pilot testing while maintaining current operations, then decide based on data",
            "Immediately switch to new method",
            "Avoid any change"
        ],
        "correct_option": 1,
        "difficulty": "medium"
    },
    {
        "question_id": 37,
        "category": "Transparency",
        "question": "You have information about upcoming organizational changes that will affect your team but you're told to keep it confidential. Team keeps asking. What do you do?",
        "options": [
            "Leak the information to build trust",
            "Maintain confidentiality while acknowledging their concerns and preparing them generally",
            "Lie and say you know nothing",
            "Avoid your team until announcement"
        ],
        "correct_option": 1,
        "difficulty": "hard"
    },
    {
        "question_id": 38,
        "category": "Motivation",
        "question": "Your team has lost motivation after a major organizational change. What's your approach?",
        "options": [
            "Give motivational speeches",
            "Understand individual concerns, provide clarity on future, involve them in planning, and celebrate small wins",
            "Threaten consequences for low performance",
            "Wait for motivation to return naturally"
        ],
        "correct_option": 1,
        "difficulty": "medium"
    },
    {
        "question_id": 39,
        "category": "Crisis Leadership",
        "question": "During an emergency, information is chaotic and everyone is looking to you for direction. What do you do first?",
        "options": [
            "Make immediate decisions with available information",
            "Quickly assess situation, ensure safety, establish command, gather information, and then act decisively",
            "Wait for complete information",
            "Delegate the crisis to someone else"
        ],
        "correct_option": 1,
        "difficulty": "hard"
    },
    {
        "question_id": 40,
        "category": "Continuous Improvement",
        "question": "Your team consistently meets targets but hasn't improved in years. What do you do?",
        "options": [
            "Don't fix what isn't broken",
            "Set stretch goals, encourage innovation, provide learning opportunities, and benchmark against best practices",
            "Increase targets arbitrarily",
            "Replace team members with new people"
        ],
        "correct_option": 1,
        "difficulty": "medium"
    },
    {
        "question_id": 41,
        "category": "Stakeholder Management",
        "question": "You have multiple stakeholders with conflicting priorities. How do you manage them?",
        "options": [
            "Satisfy the most powerful stakeholder",
            "Map stakeholder interests, communicate regularly, find common ground, and manage expectations transparently",
            "Avoid the difficult stakeholders",
            "Promise everyone everything"
        ],
        "correct_option": 1,
        "difficulty": "hard"
    },
    {
        "question_id": 42,
        "category": "Talent Development",
        "question": "You have a high-potential team member who is outgrowing their role. What do you do?",
        "options": [
            "Keep them as they're too valuable to lose",
            "Support their growth through new challenges, training, and career opportunities even if it means losing them",
            "Give them a title change without responsibilities",
            "Ignore their growth needs"
        ],
        "correct_option": 1,
        "difficulty": "medium"
    },
    {
        "question_id": 43,
        "category": "Data-Driven Decisions",
        "question": "You need to make a decision. You have data that contradicts your intuition. What do you do?",
        "options": [
            "Always trust your intuition",
            "Analyze data quality, understand the contradiction, and make informed decision considering both",
            "Always follow data blindly",
            "Flip a coin"
        ],
        "correct_option": 1,
        "difficulty": "hard"
    },
    {
        "question_id": 44,
        "category": "Succession Planning",
        "question": "You're being promoted. You need to identify your replacement. What's your approach?",
        "options": [
            "Choose someone who won't outshine you",
            "Identify capable candidate, mentor them, ensure smooth transition, and set them up for success",
            "Leave it to management to decide",
            "Don't identify anyone to remain indispensable"
        ],
        "correct_option": 1,
        "difficulty": "medium"
    },
    {
        "question_id": 45,
        "category": "Credibility",
        "question": "You made a promise to your team but circumstances changed making it impossible to keep. What do you do?",
        "options": [
            "Break the promise without explanation",
            "Explain the changed circumstances honestly, apologize, and commit to alternative solution",
            "Pretend you never made the promise",
            "Blame others for the change"
        ],
        "correct_option": 1,
        "difficulty": "medium"
    },
    {
        "question_id": 46,
        "category": "Empowerment",
        "question": "Your team can handle decisions independently but keeps asking for your approval on everything. What do you do?",
        "options": [
            "Continue approving everything to maintain control",
            "Empower them by defining decision boundaries, building confidence, and stepping back",
            "Get frustrated and micromanage",
            "Ignore their requests"
        ],
        "correct_option": 1,
        "difficulty": "medium"
    },
    {
        "question_id": 47,
        "category": "Global Mindset",
        "question": "You're working with international partners with different work styles and time zones. How do you ensure effective collaboration?",
        "options": [
            "Insist everyone follows your work style",
            "Understand cultural differences, find common ground, use technology effectively, and be flexible with timing",
            "Only work during your convenient hours",
            "Minimize interaction with international partners"
        ],
        "correct_option": 1,
        "difficulty": "medium"
    },
    {
        "question_id": 48,
        "category": "Compliance",
        "question": "You discover your team has been taking shortcuts that violate safety regulations but save time. What do you do?",
        "options": [
            "Immediately stop all shortcuts, retrain on procedures, and investigate extent",
            "Ignore if no accidents have occurred",
            "Take shortcuts yourself to stay competitive",
            "Report anonymously without addressing team"
        ],
        "correct_option": 0,
        "difficulty": "hard"
    },
    {
        "question_id": 49,
        "category": "Strategic Alignment",
        "question": "Your team's goals are unclear in relation to organizational strategy. What do you do?",
        "options": [
            "Continue with current activities",
            "Seek clarification from leadership, align team goals with strategy, and communicate connection clearly",
            "Set your own goals independently",
            "Wait for someone to tell you"
        ],
        "correct_option": 1,
        "difficulty": "medium"
    },
    {
        "question_id": 50,
        "category": "Legacy",
        "question": "You're approaching the end of your tenure in this role. What's your priority?",
        "options": [
            "Coast through remaining time",
            "Ensure sustainability of your initiatives, document learnings, mentor successors, and finish strong",
            "Start focusing only on your next role",
            "Take credit for everything before leaving"
        ],
        "correct_option": 1,
        "difficulty": "medium"
    }
]


def get_randomized_questions(num_questions: int = 10, difficulty: str = None) -> List[Dict]:
    """
    Get randomized OLQ questions
    
    Args:
        num_questions: Number of questions to return (default 10)
        difficulty: Filter by difficulty ('easy', 'medium', 'hard', or None for mixed)
    
    Returns:
        List of randomized questions with shuffled options
    """
    # Filter by difficulty if specified
    if difficulty:
        filtered_questions = [q for q in QUESTION_BANK if q.get('difficulty') == difficulty]
    else:
        filtered_questions = QUESTION_BANK.copy()
    
    # Randomly select questions
    selected_questions = random.sample(filtered_questions, min(num_questions, len(filtered_questions)))
    
    # Randomize options for each question
    randomized_questions = []
    for question in selected_questions:
        q_copy = question.copy()
        options = q_copy['options'].copy()
        correct_option = q_copy['correct_option']
        correct_answer_text = options[correct_option]
        
        # Shuffle options
        random.shuffle(options)
        
        # Find new index of correct answer
        new_correct_index = options.index(correct_answer_text)
        
        q_copy['options'] = options
        q_copy['correct_option'] = new_correct_index
        
        # Don't send correct answer to frontend
        frontend_question = {
            'question_id': q_copy['question_id'],
            'question': q_copy['question'],
            'options': q_copy['options'],
            'category': q_copy['category']
        }
        
        randomized_questions.append({
            'frontend': frontend_question,
            'correct_option': new_correct_index  # Store for backend validation
        })
    
    return randomized_questions


def validate_answers(responses: List[Dict], session_questions: List[Dict]) -> Dict:
    """
    Validate user responses against their session questions
    
    Args:
        responses: User's answers
        session_questions: Questions that were presented to this user
    
    Returns:
        Scoring results with detailed analysis
    """
    total_score = 0
    max_score = len(session_questions) * 10  # 10 points per question
    category_scores = {}
    
    for response in responses:
        question_id = response.get('question_id')
        selected_option = response.get('selected_option')
        
        # Find the question in session
        session_q = next((q for q in session_questions if q['frontend']['question_id'] == question_id), None)
        
        if session_q:
            correct_option = session_q['correct_option']
            category = session_q['frontend']['category']
            
            # Calculate points
            if selected_option == correct_option:
                points = 10
            elif abs(selected_option - correct_option) == 1:
                points = 5  # Partial credit for adjacent answer
            else:
                points = 0
            
            total_score += points
            
            # Track category-wise scores
            if category not in category_scores:
                category_scores[category] = {'correct': 0, 'total': 0}
            category_scores[category]['total'] += 1
            if selected_option == correct_option:
                category_scores[category]['correct'] += 1
    
    # Calculate percentage
    percentage = (total_score / max_score * 100) if max_score > 0 else 0
    
    # Category analysis
    category_analysis = {}
    for category, scores in category_scores.items():
        category_analysis[category] = {
            'score': (scores['correct'] / scores['total'] * 100) if scores['total'] > 0 else 0,
            'strength': 'Strong' if (scores['correct'] / scores['total']) >= 0.7 else 
                       'Moderate' if (scores['correct'] / scores['total']) >= 0.5 else 'Needs Development'
        }
    
    return {
        'total_score': percentage,
        'category_analysis': category_analysis,
        'raw_score': total_score,
        'max_score': max_score
    }


def get_category_insights(category_analysis: Dict) -> Dict:
    """Generate insights based on category performance"""
    strengths = []
    weaknesses = []
    recommendations = []
    
    for category, data in category_analysis.items():
        if data['strength'] == 'Strong':
            strengths.append(category)
        elif data['strength'] == 'Needs Development':
            weaknesses.append(category)
    
    # Generate personalized recommendations
    if 'Leadership' in weaknesses:
        recommendations.append("Focus on developing team management and motivational skills")
    if 'Decision Making' in weaknesses:
        recommendations.append("Practice scenario-based decision-making exercises")
    if 'Crisis Management' in weaknesses:
        recommendations.append("Study crisis management frameworks and real-world case studies")
    
    return {
        'strengths': strengths[:5],
        'weaknesses': weaknesses[:5],
        'recommendations': recommendations[:5]
    }
