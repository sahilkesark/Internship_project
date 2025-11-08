from flask import Flask, render_template, request, jsonify
import spacy
import re
import json
from datetime import datetime
import os
from werkzeug.utils import secure_filename

# Try to import PDF libraries at module level
try:
    import PyPDF2
    PDF_LIBRARY = 'PyPDF2'
    PDF_AVAILABLE = True
except ImportError:
    try:
        import pdfplumber
        PDF_LIBRARY = 'pdfplumber'
        PDF_AVAILABLE = True
    except ImportError:
        PDF_LIBRARY = None
        PDF_AVAILABLE = False

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- 1. SETUP ---
try:
    nlp = spacy.load("en_core_web_sm")
except IOError:
    print("ERROR: SpaCy model not found. Run: python -m spacy download en_core_web_sm")
    exit()

# Check for PDF libraries
if PDF_AVAILABLE:
    print(f"{PDF_LIBRARY} is available for PDF processing")
else:
    print("WARNING: Neither PyPDF2 nor pdfplumber is installed.")
    print("  PDF resume parsing will not work. Install one with:")
    print("  pip install PyPDF2")
    print("  or")
    print("  pip install pdfplumber")

def load_careers():
    try:
        with open("careers.json", 'r') as f: 
            return json.load(f)
    except FileNotFoundError: 
        return []

all_careers = load_careers()

# --- 2. HELPER FUNCTIONS ---

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def calculate_age_from_dob(dob_str):
    """Calculate age from date of birth string (YYYY-MM-DD)"""
    try:
        dob = datetime.strptime(dob_str, '%Y-%m-%d')
        today = datetime.now()
        age = today.year - dob.year
        if today.month < dob.month or (today.month == dob.month and today.day < dob.day):
            age -= 1
        return age
    except:
        return None

def check_education(user_edu, req_edu):
    """Check if user education meets requirements"""
    if not user_edu or not req_edu:
        return False
    
    # Convert to set for easier comparison
    user_quals = set(user_edu) if isinstance(user_edu, list) else {user_edu}
    req_quals = set(req_edu) if isinstance(req_edu, list) else {req_edu}
    
    # Handle 12th education
    if "12th" in user_quals:
        # 12th qualifies for 12th requirements
        if "12th" in req_quals:
            return True
    
    # Engineering also qualifies as Graduate and Graduate_PM
    if "Engineering" in user_quals: 
        user_quals.update(["Graduate", "Graduate_PM"])
    
    # Graduate_PM also qualifies as Graduate
    if "Graduate_PM" in user_quals: 
        user_quals.add("Graduate")
    
    # Check if any required education matches user education
    return bool(user_quals.intersection(req_quals))

def get_degree_type_from_qualification(highest_qual, degree_type=None):
    """Convert highest qualification to degree type for compatibility"""
    if highest_qual == '12th':
        return '12th'
    elif highest_qual == 'Graduation' and degree_type:
        # If highest_qual is "Graduation", use the actual degree_type
        return degree_type
    return highest_qual

def check_education_percentage(profile, career):
    """Check education percentage requirements"""
    rules = career.get('eligibility', {})
    
    # Check 12th percentage if required
    if 'education_percentage_min' in rules:
        twelfth_pct = profile.get('twelfth_percentage', 0)
        if twelfth_pct < rules['education_percentage_min']:
            return False, f"12th percentage too low (Req: {rules['education_percentage_min']}%)"
    
    # Check degree percentage if required (only if user has graduation)
    highest_qual = profile.get('highest_qualification')
    if highest_qual and highest_qual != '12th':
        if 'degree_percentage_min' in rules:
            degree_pct = profile.get('degree_percentage', 0)
            if degree_pct < rules['degree_percentage_min']:
                return False, f"Degree percentage too low (Req: {rules['degree_percentage_min']}%, Found: {degree_pct}%)"
    
    return True, ""

def check_physical_requirements(profile, career):
    """Check height and weight requirements"""
    rules = career.get('eligibility', {})
    reasons = []
    
    height = profile.get('height', 0)
    weight = profile.get('weight', 0)
    
    if 'height_min_cm' in rules and rules['height_min_cm'] > 0:
        if height < rules['height_min_cm']:
            reasons.append(f"Height too short (Req: {rules['height_min_cm']}cm)")
    
    if 'weight_min_kg' in rules and rules['weight_min_kg'] > 0:
        if weight < rules['weight_min_kg']:
            reasons.append(f"Weight too low (Req: {rules['weight_min_kg']}kg)")
    
    return (True, "") if not reasons else (False, " | ".join(reasons))

def check_medical_conditions(profile, career):
    """Check medical conditions"""
    rules = career.get('eligibility', {})
    medical_problems = profile.get('medical_problems', '').strip().lower()
    
    if not medical_problems:
        return True, ""
    
    # If career has specific medical restrictions, check them
    restricted_conditions = rules.get('medical_conditions', [])
    if restricted_conditions:
        # Simple check - if user has any medical problems and career restricts them
        # This is a simplified version - you can make it more sophisticated
        return False, "Medical conditions may affect eligibility"
    
    return True, ""

def check_eligibility(profile, career):
    """Comprehensive eligibility check"""
    rules = career.get('eligibility', {})
    reasons = []
    
    # Age check - handle both int and float ages
    age = float(profile.get('age', 0))
    age_min = float(rules.get('age_min', 0))
    age_max = float(rules.get('age_max', 100))
    if not (age_min <= age <= age_max):
        reasons.append(f"Age mismatch (Req: {age_min}-{age_max} years, Found: {age})")
    
    # Marital status
    if profile.get('marital_status') not in rules.get('marital_status', []):
        reasons.append(f"Marital status: Must be {', '.join(rules.get('marital_status', []))}")
    
    # Education type - check highest qualification or degree type
    highest_qual = profile.get('highest_qualification')
    degree_type = profile.get('degree_type')
    
    # Build user_education list
    if highest_qual:
        mapped_degree_type = get_degree_type_from_qualification(highest_qual, degree_type)
        user_education = [mapped_degree_type] if mapped_degree_type else []
    else:
        user_education = [degree_type] if degree_type else []
    
    # Debug logging
    if not user_education:
        reasons.append(f"Education type not specified in profile")
    elif not check_education(user_education, rules.get('education', [])):
        user_edu_str = highest_qual or profile.get('degree_type', 'Not specified')
        req_edu_str = ', '.join(rules.get('education', []))
        reasons.append(f"Education type not met (Have: {user_edu_str}, Need: {req_edu_str})")
    
    # Education percentage
    edu_check, edu_reason = check_education_percentage(profile, career)
    if not edu_check:
        reasons.append(edu_reason)
    
    # Nationality
    if profile.get('nationality') != rules.get('nationality'):
        reasons.append("Nationality mismatch")
    
    # Physical requirements
    phys_check, phys_reason = check_physical_requirements(profile, career)
    if not phys_check:
        reasons.append(phys_reason)
    
    # Medical conditions
    med_check, med_reason = check_medical_conditions(profile, career)
    if not med_check:
        reasons.append(med_reason)
    
    # NCC certificate (if required)
    if rules.get('ncc_certificate') and not profile.get('ncc_certificate', False):
        reasons.append("NCC certificate required")
    
    if not reasons:
        return (True, "Eligible")
    else:
        reason_str = " | ".join(reasons) if reasons else "Eligibility criteria not met"
        return (False, reason_str)

def calculate_suitability(text, career_keywords):
    """Calculate suitability score based on text and keywords"""
    if not text or not career_keywords:
        return 50  # Default score
    
    doc = nlp(text.lower())
    user_kws = set([t.lemma_ for t in doc if not t.is_stop and t.is_alpha and len(t.lemma_) > 2])
    career_kws = set([k.lower() for k in career_keywords])
    
    if not career_kws:
        return 50
    
    match = user_kws.intersection(career_kws)
    base_score = int((len(match) / len(career_kws)) * 100)
    
    # Boost score based on degree course match
    return min(100, base_score + 10)

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    if not PDF_AVAILABLE:
        raise ImportError("Neither PyPDF2 nor pdfplumber is installed. Please install one: pip install PyPDF2 or pip install pdfplumber")
    
    # Use the available library
    if PDF_LIBRARY == 'PyPDF2':
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                return text
            else:
                raise Exception("Could not extract any text from the PDF. The file might be corrupted or image-based.")
        except Exception as e:
            if isinstance(e, ImportError):
                raise
            raise Exception(f"Error extracting text from PDF using PyPDF2: {str(e)}")
    
    elif PDF_LIBRARY == 'pdfplumber':
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                return text
            else:
                raise Exception("Could not extract any text from the PDF. The file might be corrupted or image-based.")
        except Exception as e:
            if isinstance(e, ImportError):
                raise
            raise Exception(f"Error extracting text from PDF using pdfplumber: {str(e)}")
    
    # Should not reach here, but just in case
    raise ImportError("PDF library not properly initialized")

def parse_resume_text(text):
    """Parse resume text to extract profile information"""
    doc = nlp(text)
    
    # Initialize profile with defaults
    profile = {
        'age': 21,
        'marital_status': 'Unmarried',
        'nationality': 'Indian',
        'degree_type': 'Graduate',
        'degree_course': '',
        'twelfth_percentage': 60,
        'degree_percentage': 60,
        'height': 170,
        'weight': 65,
        'medical_problems': '',
        'ncc_certificate': False
    }
    
    # Extract age - multiple patterns to catch different formats
    age_found = False
    
    # Pattern 1: "age: 19", "age 19", "aged 19"
    age_patterns = [
        r'\bage\s*:?\s*(\d{1,2}(?:\.\d+)?)\s*(?:years?\s*old|yrs?)?\b',
        r'\baged\s+(\d{1,2}(?:\.\d+)?)\s*(?:years?\s*old|yrs?)?\b',
        r'\b(\d{1,2}(?:\.\d+)?)\s*years?\s*old\b',
        r'\b(\d{1,2}(?:\.\d+)?)\s*yrs?\b',
        r'\b(\d{1,2}(?:\.\d+)?)\s*y\.?o\.?\b',
    ]
    
    for pattern in age_patterns:
        age_match = re.search(pattern, text, re.IGNORECASE)
        if age_match:
            try:
                age_value = float(age_match.group(1))
                if 16 <= age_value <= 40:  # Reasonable age range
                    profile['age'] = age_value
                    age_found = True
                    break
            except:
                continue
    
    # Pattern 2: DOB calculation if age not found explicitly
    if not age_found:
        dob_patterns = [
            r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{4})\b',
            r'\b(\d{4}[/-]\d{1,2}[/-]\d{1,2})\b',
            r'\bdate\s+of\s+birth\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{4})\b',
            r'\bdob\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{4})\b',
            r'\bbirth\s+date\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{4})\b',
        ]
        for pattern in dob_patterns:
            dob_match = re.search(pattern, text, re.IGNORECASE)
            if dob_match:
                try:
                    dob_str = dob_match.group(1)
                    # Try different date formats
                    for fmt in ['%d-%m-%Y', '%m-%d-%Y', '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d']:
                        try:
                            dob = datetime.strptime(dob_str.replace('/', '-'), fmt)
                            age = calculate_age_from_dob(dob.strftime('%Y-%m-%d'))
                            if age and 16 <= age <= 40:
                                profile['age'] = age
                                age_found = True
                                break
                        except:
                            continue
                    if age_found:
                        break
                except:
                    pass
    
    # Extract education - check for HIGHER education FIRST, then 12th
    # This is important because resumes often mention both 12th and graduation
    # Check for Engineering degrees first (most specific)
    if re.search(r'\b(b\.?tech|b\.?e\.?|bachelor.*engineering|engineering\s+degree|bachelor\s+of\s+engineering)\b', text, re.IGNORECASE):
        profile['degree_type'] = 'Engineering'
    # Check for Law degrees
    elif re.search(r'\b(llb|law|bachelor.*law|bachelor\s+of\s+law)\b', text, re.IGNORECASE):
        profile['degree_type'] = 'Law'
    # Check for Physics/Maths graduates
    elif re.search(r'\b(physics|maths?|mathematics).*graduate|graduate.*(physics|maths?|mathematics)\b', text, re.IGNORECASE):
        profile['degree_type'] = 'Graduate_PM'
    # Check for other Bachelor's degrees (Science, Arts, Commerce, etc.)
    elif re.search(r'\b(bachelor\s+of\s+science|b\.?sc\.?|bachelor\s+of\s+arts|b\.?a\.?|bachelor\s+of\s+commerce|b\.?com\.?|bachelor\s+degree|bachelor)\b', text, re.IGNORECASE):
        profile['degree_type'] = 'Graduate'
    # Check for generic graduate
    elif re.search(r'\b(graduate|graduation|completed\s+graduation)\b', text, re.IGNORECASE):
        profile['degree_type'] = 'Graduate'
    # Only if no higher education found, check for 12th
    elif re.search(r'\b(12th|12\s*th|12\s*standard|twelfth|intermediate|hsc|higher\s+secondary|senior\s+secondary|class\s+12|xii)\b', text, re.IGNORECASE):
        profile['degree_type'] = '12th'
    
    # Extract course/stream
    course_match = re.search(r'\b(computer science|mechanical|electrical|civil|electronics|aerospace|chemical)\b', text, re.IGNORECASE)
    if course_match:
        profile['degree_course'] = course_match.group(1).title()
    
    # Extract percentages and CGPA
    # First, try to extract CGPA (e.g., "CGPA: 8.5 / 10" or "8.5/10")
    cgpa_patterns = [
        r'cgpa\s*:?\s*(\d+(?:\.\d+)?)\s*/?\s*10',
        r'(\d+(?:\.\d+)?)\s*/?\s*10\s*(?:cgpa|gpa)',
        r'cgpa\s*:?\s*(\d+(?:\.\d+)?)',
    ]
    cgpa_found = False
    for pattern in cgpa_patterns:
        cgpa_match = re.search(pattern, text, re.IGNORECASE)
        if cgpa_match:
            try:
                cgpa_value = float(cgpa_match.group(1))
                if 0 <= cgpa_value <= 10:
                    # Convert CGPA to percentage (assuming 10-point scale)
                    percentage = (cgpa_value / 10) * 100
                    profile['degree_percentage'] = percentage
                    cgpa_found = True
                    break
            except:
                continue
    
    # Extract percentages (if CGPA not found or for 12th)
    pct_pattern = r'(\d+(?:\.\d+)?)\s*%'
    percentages = re.findall(pct_pattern, text)
    if percentages:
        pcts = [float(p) for p in percentages]
        
        # Try to identify which percentage is for 12th and which is for degree
        # Look for context around each percentage
        text_lower = text.lower()
        
        # Find all percentage matches with context
        pct_matches = list(re.finditer(pct_pattern, text))
        twelfth_pcts = []
        degree_pcts = []
        
        for match in pct_matches:
            pct_value = float(match.group(1))
            # Get context around the match (50 chars before and after)
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 50)
            context = text_lower[start:end]
            
            # Check if this percentage is for 12th
            if re.search(r'\b(12th|12\s*th|12\s*standard|twelfth|intermediate|hsc|higher\s+secondary|senior\s+secondary|class\s+12|xii)\b', context):
                twelfth_pcts.append(pct_value)
            # Check if this percentage is for degree/graduation
            elif re.search(r'\b(degree|graduation|bachelor|b\.?tech|b\.?e\.?|b\.?sc\.?|b\.?a\.?|cgpa|gpa)\b', context):
                degree_pcts.append(pct_value)
            # If no clear context, assign based on position and degree type
            elif profile['degree_type'] == '12th':
                twelfth_pcts.append(pct_value)
            else:
                # If we have graduation, assume higher percentage is for degree
                if len(pcts) == 2:
                    if pct_value == max(pcts):
                        degree_pcts.append(pct_value)
                    else:
                        twelfth_pcts.append(pct_value)
                else:
                    degree_pcts.append(pct_value)
        
        # Assign percentages
        if twelfth_pcts:
            profile['twelfth_percentage'] = max(twelfth_pcts)  # Take highest if multiple
        if degree_pcts and not cgpa_found:
            profile['degree_percentage'] = max(degree_pcts)  # Take highest if multiple
        elif not cgpa_found and len(pcts) == 1:
            # Single percentage - assign based on degree type
            if profile['degree_type'] == '12th':
                profile['twelfth_percentage'] = pcts[0]
            else:
                profile['degree_percentage'] = pcts[0]
        elif not cgpa_found and len(pcts) >= 2:
            # Multiple percentages but no clear context - assume first is 12th, second is degree
            profile['twelfth_percentage'] = pcts[0]
            profile['degree_percentage'] = pcts[1]
    
    # Extract height
    height_match = re.search(r'\b(\d{3})\s*(?:cm|centimeters?)\b', text, re.IGNORECASE)
    if height_match:
        profile['height'] = int(height_match.group(1))
    
    # Extract weight
    weight_match = re.search(r'\b(\d{2,3})\s*(?:kg|kilograms?)\b', text, re.IGNORECASE)
    if weight_match:
        profile['weight'] = int(weight_match.group(1))
    
    # Check for NCC
    if re.search(r'\bncc\b', text, re.IGNORECASE):
        profile['ncc_certificate'] = True
    
    # Check marital status
    if re.search(r'\b(married|spouse|wife|husband)\b', text, re.IGNORECASE):
        profile['marital_status'] = 'Married'
    
    # Set highest_qualification based on degree_type
    if profile['degree_type'] == '12th':
        profile['highest_qualification'] = '12th'
    elif profile['degree_type'] in ['Engineering', 'Graduate', 'Graduate_PM', 'Law']:
        profile['highest_qualification'] = 'Graduation'
    else:
        profile['highest_qualification'] = profile['degree_type']
    
    # Add education array for compatibility
    profile['education'] = [profile['degree_type']]
    
    return profile

# --- 3. ROUTES ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/manual')
def manual_form():
    return render_template('manual_form.html')

@app.route('/ai-parser')
def ai_parser():
    return render_template('ai_parser.html')

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/api/parse-resume', methods=['POST'])
def parse_resume_api():
    """Handle PDF resume upload and parsing"""
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    try:
        filename = secure_filename(file.filename)
        if not filename:
            return jsonify({'error': 'Invalid filename'}), 400
            
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save file
        try:
            file.save(filepath)
        except Exception as e:
            return jsonify({'error': f'Failed to save file: {str(e)}'}), 500
        
        # Extract text from PDF
        try:
            text = extract_text_from_pdf(filepath)
            if not text or not text.strip():
                # Clean up file before returning error
                try:
                    os.remove(filepath)
                except:
                    pass
                return jsonify({'error': 'Could not extract text from PDF. The file might be corrupted, password-protected, or image-based.'}), 400
            
        except ImportError as e:
            # Clean up file before returning error
            try:
                os.remove(filepath)
            except:
                pass
            return jsonify({'error': str(e)}), 500
        except Exception as e:
            # Clean up file before returning error
            try:
                os.remove(filepath)
            except:
                pass
            return jsonify({'error': f'PDF extraction error: {str(e)}'}), 500
        
            # Parse profile from text
        try:
            profile = parse_resume_text(text)
        except Exception as e:
            # Clean up file before returning error
            try:
                os.remove(filepath)
            except:
                pass
            return jsonify({'error': f'Error parsing resume: {str(e)}'}), 500
        
        # Calculate age if DOB is provided
        if 'dob' in request.form and request.form['dob']:
            age = calculate_age_from_dob(request.form['dob'])
            if age:
                profile['age'] = age
        
        # Get recommendations
        eligible = []
        ineligible = []
        
        try:
            for career in all_careers:
                try:
                    is_eligible, reason = check_eligibility(profile, career)
                    if is_eligible:
                        score = calculate_suitability(text, career.get('suitability_keywords', []))
                        eligible.append({**career, 'score': score})
                    else:
                        ineligible.append({**career, 'reason': reason})
                except Exception as e:
                    # If individual career check fails, add to ineligible with error reason
                    ineligible.append({**career, 'reason': f"Error checking eligibility: {str(e)}"})
            
            eligible.sort(key=lambda x: x['score'], reverse=True)
        except Exception as e:
            # Clean up file before returning error
            try:
                os.remove(filepath)
            except:
                pass
            return jsonify({'error': f'Error generating recommendations: {str(e)}'}), 500
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        # Ensure we always return both lists, even if empty
        result = {
            "eligible": eligible if eligible else [],
            "ineligible": ineligible if ineligible else []
        }
        
        return jsonify(result)
    
    except Exception as e:
        # Make sure to clean up file in case of any error
        try:
            if 'filepath' in locals():
                os.remove(filepath)
        except:
            pass
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/api/recommend', methods=['POST'])
def recommend_api():
    """Get career recommendations based on profile"""
    try:
        data = request.json
        profile = data.get('profile', {})
        
        # Calculate age from DOB if provided
        if 'dob' in profile and profile['dob']:
            age = calculate_age_from_dob(profile['dob'])
            if age:
                profile['age'] = age
        
        # Ensure age is set
        if 'age' not in profile or not profile['age']:
            return jsonify({'error': 'Age is required'}), 400
        
        eligible = []
        ineligible = []
        
        # Check if careers are loaded
        if not all_careers:
            return jsonify({'error': 'No careers data available'}), 500
        
        for career in all_careers:
            try:
                is_eligible, reason = check_eligibility(profile, career)
                if is_eligible:
                    # Create text for suitability calculation
                    degree_type = profile.get('degree_type', '')
                    degree_stream = profile.get('degree_stream', '')
                    medical = profile.get('medical_problems', '')
                    text = f"{degree_type} {degree_stream} {medical}"
                    score = calculate_suitability(text, career.get('suitability_keywords', []))
                    eligible.append({**career, 'score': score})
                else:
                    ineligible.append({**career, 'reason': reason})
            except Exception as e:
                # If there's an error checking a specific career, add it to ineligible
                ineligible.append({**career, 'reason': f"Error checking eligibility: {str(e)}"})
        
        eligible.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        return jsonify({"eligible": eligible, "ineligible": ineligible})
    
    except Exception as e:
        import traceback
        print(f"Error in recommend_api: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

###############################
# Preparation Plan Route
###############################

@app.route('/prep-plan')
def prep_plan():
    """Show a detailed preparation plan for a selected career entry.

    Accepts query parameter `career` (career name). If not provided or not found,
    falls back to a generic plan based on common entry types (NDA/CDS/SSC Tech/TGC/AFCAT/NCC/JAG/UPSC).
    """
    from flask import request, render_template

    career_name = request.args.get('career', '')

    # Try to locate the exact career from loaded careers
    selected = None
    for c in all_careers:
        if c.get('name') == career_name:
            selected = c
            break

    # Identify entry category for plan generation
    name_for_category = (selected or {}).get('name', career_name).lower()
    def get_category(name: str):
        n = name.lower()
        if 'nda' in n:
            return 'NDA'
        if 'cds' in n or 'combined defence services' in n:
            return 'CDS'
        if 'ssc tech' in n:
            return 'SSC_Tech'
        if 'tgc' in n:
            return 'TGC'
        if 'afcat' in n:
            return 'AFCAT'
        if 'ncc' in n:
            return 'NCC'
        if 'jag' in n:
            return 'JAG'
        if 'civil services' in n or 'ias' in n or 'ips' in n or 'upsc' in n:
            return 'UPSC'
        # Default to NDA-style plan for defence entries
        return 'Generic'

    category = get_category(name_for_category)

    # Preparation content per category
    prep_content = {
        'NDA': {
            'title': 'National Defence Academy (NDA) Preparation Plan',
            'duration_weeks': 12,
            'syllabus': [
                'Mathematics: Algebra, Trigonometry, Calculus, Coordinate Geometry, Statistics & Probability',
                'General Ability Test (GAT): English, History, Geography, Polity, Economics, General Science',
                'Current Affairs & Defence Awareness',
            ],
            'resources': [
                {'name': 'Official UPSC NDA Syllabus', 'url': 'https://upsc.gov.in/'},
                {'name': 'NDA Previous Year Papers (PDF)', 'url': 'https://ndaexam.com/'},
                {'name': 'NCERT Maths (Class 11-12)', 'url': 'https://ncert.nic.in/textbook.php'},
                {'name': 'Lucent General Knowledge', 'url': 'https://amzn.to/3GKbook'},
            ],
        },
        'CDS': {
            'title': 'Combined Defence Services (CDS) Preparation Plan',
            'duration_weeks': 12,
            'syllabus': [
                'English: Vocabulary, Grammar, Comprehension',
                'General Knowledge: History, Geography, Polity, Economics, Science',
                'Elementary Mathematics: Arithmetic, Algebra, Trigonometry, Geometry, Mensuration, Statistics',
            ],
            'resources': [
                {'name': 'UPSC CDS Notification & Syllabus', 'url': 'https://upsc.gov.in/'},
                {'name': 'CDS Previous Year Papers', 'url': 'https://cdsexam.com/'},
                {'name': 'Pathfinder CDS Guide', 'url': 'https://amzn.to/3CDSbook'},
            ],
        },
        'SSC_Tech': {
            'title': 'SSC Tech Preparation Plan (Engineering Graduates)',
            'duration_weeks': 10,
            'syllabus': [
                'Core Engineering Subjects (as per stream)',
                'Aptitude & Reasoning for SSB',
                'Current Affairs & Defence Technology',
            ],
            'resources': [
                {'name': 'SSC Tech Notification (Join Indian Army)', 'url': 'https://joinindianarmy.nic.in/'},
                {'name': 'Gate/IES Core Concepts (per stream)', 'url': 'https://gate.iitkgp.ac.in/'},
            ],
        },
        'TGC': {
            'title': 'Technical Graduate Course (TGC) Preparation Plan',
            'duration_weeks': 10,
            'syllabus': [
                'Engineering Fundamentals (per stream)',
                'SSB Psychology, GTO Tasks, Interview',
            ],
            'resources': [
                {'name': 'TGC Notification (Join Indian Army)', 'url': 'https://joinindianarmy.nic.in/'},
            ],
        },
        'AFCAT': {
            'title': 'AFCAT Preparation Plan',
            'duration_weeks': 10,
            'syllabus': [
                'General Awareness, Verbal Ability, Numerical Ability, Reasoning & Military Aptitude',
            ],
            'resources': [
                {'name': 'AFCAT Official Site', 'url': 'https://afcat.cdac.in/'},
            ],
        },
        'NCC': {
            'title': 'NCC Special Entry Preparation Plan',
            'duration_weeks': 8,
            'syllabus': [
                'SSB preparation: Psychology, GTO, Interview',
                'Current Affairs & Defence Awareness',
            ],
            'resources': [
                {'name': 'NCC Special Entry (Join Indian Army)', 'url': 'https://joinindianarmy.nic.in/'},
            ],
        },
        'JAG': {
            'title': 'JAG (Judge Advocate General) Preparation Plan',
            'duration_weeks': 12,
            'syllabus': [
                'Constitutional Law, IPC & CrPC, Evidence Act',
                'Contract & Company Law, Administrative Law',
                'SSB: Psych, GTO, Interview',
            ],
            'resources': [
                {'name': 'Bare Acts (India Code)', 'url': 'https://www.indiacode.nic.in/'},
            ],
        },
        'UPSC': {
            'title': 'UPSC Civil Services Preparation Plan',
            'duration_weeks': 24,
            'syllabus': [
                'Prelims: GS Paper I & II (CSAT)',
                'Mains: Essay, GS I-IV, Optional Subject, Language',
                'Interview: Personality Test',
            ],
            'resources': [
                {'name': 'UPSC Official Syllabus', 'url': 'https://upsc.gov.in/'},
                {'name': 'NCERTs (Class 6-12) for GS', 'url': 'https://ncert.nic.in/textbook.php'},
            ],
        },
        'Generic': {
            'title': 'Defence Entry Preparation Plan',
            'duration_weeks': 8,
            'syllabus': [
                'Math & Reasoning fundamentals',
                'English grammar & comprehension',
                'General Knowledge & Current Affairs',
            ],
            'resources': [
                {'name': 'General Defence Awareness', 'url': 'https://mod.gov.in/'},
            ],
        }
    }

    content = prep_content.get(category, prep_content['Generic'])

    # Build a simple week-wise timetable based on duration
    weeks = content['duration_weeks']
    timetable = []
    for w in range(1, weeks + 1):
        timetable.append({
            'week': w,
            'focus': (
                'Mathematics practice' if category in ['NDA', 'CDS'] else
                'Core engineering subject revision' if category in ['SSC_Tech', 'TGC'] else
                'Verbal & reasoning drills' if category in ['AFCAT'] else
                'Law subject consolidation' if category in ['JAG'] else
                'GS + Optional prep' if category in ['UPSC'] else
                'Quant + English + GK mix'
            ),
            'tasks': [
                'Daily: 2 hours core subject',
                'Daily: 1 hour aptitude/SSB prep',
                'Weekly: 1 mock test and analysis'
            ]
        })

    return render_template(
        'prep_plan.html',
        career=selected or {'name': career_name or content['title'], 'service_branch': '', 'entry_type': category},
        category=category,
        title=content['title'],
        syllabus=content['syllabus'],
        resources=content['resources'],
        timetable=timetable
    )

if __name__ == '__main__':
    app.run(debug=True, port=5001)
