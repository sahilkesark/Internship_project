let currentStep = 1;
const totalSteps = 3;

// Date of Birth formatting helper
document.addEventListener('DOMContentLoaded', function() {
    const dobInput = document.getElementById('dob');
    if (dobInput) {
        // Allow manual entry and format as user types
        dobInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, ''); // Remove non-digits
            
            // Format as YYYY-MM-DD
            if (value.length >= 4) {
                value = value.substring(0, 4) + '-' + value.substring(4);
            }
            if (value.length >= 7) {
                value = value.substring(0, 7) + '-' + value.substring(7, 9);
            }
            
            e.target.value = value;
        });
        
        // Validate on blur
        dobInput.addEventListener('blur', function(e) {
            const value = e.target.value;
            const datePattern = /^\d{4}-\d{2}-\d{2}$/;
            if (value && !datePattern.test(value)) {
                e.target.setCustomValidity('Please enter date in YYYY-MM-DD format');
            } else {
                // Check if date is valid
                const date = new Date(value);
                if (value && (isNaN(date.getTime()) || date.toISOString().split('T')[0] !== value)) {
                    e.target.setCustomValidity('Please enter a valid date');
                } else {
                    e.target.setCustomValidity('');
                }
            }
        });
    }
});

function updateProgress() {
    document.querySelectorAll('.progress-step').forEach((step, index) => {
        if (index + 1 <= currentStep) {
            step.classList.add('active');
        } else {
            step.classList.remove('active');
        }
    });
}

function toggleGraduationFields() {
    const highestQual = document.getElementById('highest_qualification').value;
    const graduationSection = document.getElementById('graduation-section');
    const graduationFields = graduationSection.querySelectorAll('input, select');
    
    if (highestQual && highestQual !== '12th') {
        // Show graduation section
        graduationSection.classList.remove('hidden');
        // Make graduation fields required (except cgpa_type which is handled separately)
        graduationFields.forEach(field => {
            if (field.id !== 'cgpa_type' && field.id !== 'degree_cgpa') {
                field.required = true;
            }
        });
        // Make cgpa_type and degree_cgpa required
        document.getElementById('cgpa_type').required = true;
        document.getElementById('degree_cgpa').required = true;
    } else {
        // Hide graduation section
        graduationSection.classList.add('hidden');
        // Remove required and clear values
        graduationFields.forEach(field => {
            field.required = false;
            field.value = '';
        });
    }
}

function updateCGPAField() {
    const cgpaType = document.getElementById('cgpa_type').value;
    const cgpaInput = document.getElementById('degree_cgpa');
    const cgpaLabel = document.getElementById('degree_cgpa_label');
    
    if (cgpaType === 'CGPA') {
        cgpaInput.max = 10;
        cgpaInput.placeholder = 'e.g., 8.5';
        cgpaLabel.textContent = 'CGPA (out of 10) *';
    } else if (cgpaType === 'Percentage') {
        cgpaInput.max = 100;
        cgpaInput.placeholder = 'e.g., 85.5';
        cgpaLabel.textContent = 'Percentage (%) *';
    } else {
        cgpaInput.max = '';
        cgpaInput.placeholder = 'Enter value';
        cgpaLabel.textContent = 'Value *';
    }
    cgpaInput.value = ''; // Clear value when type changes
}

function showStep(step) {
    document.querySelectorAll('.form-step').forEach(s => s.classList.remove('active'));
    document.getElementById(`step${step}`).classList.add('active');
    updateProgress();
}

function nextStep() {
    const currentStepElement = document.getElementById(`step${currentStep}`);
    // Only check visible required fields
    const visibleInputs = Array.from(currentStepElement.querySelectorAll('input[required], select[required]'))
        .filter(input => {
            const section = input.closest('.education-section, .form-grid');
            return !section || !section.classList.contains('hidden');
        });
    
    let isValid = true;

    visibleInputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('error');
        } else {
            input.classList.remove('error');
        }
    });

    if (isValid && currentStep < totalSteps) {
        currentStep++;
        showStep(currentStep);
    } else if (!isValid) {
        alert('Please fill in all required fields');
    }
}

function prevStep() {
    if (currentStep > 1) {
        currentStep--;
        showStep(currentStep);
    }
}

// Form submission
document.getElementById('manualForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);
    
    // Calculate age from DOB
    const dob = new Date(data.dob);
    const today = new Date();
    const age = today.getFullYear() - dob.getFullYear();
    const monthDiff = today.getMonth() - dob.getMonth();
    const ageInYears = monthDiff < 0 || (monthDiff === 0 && today.getDate() < dob.getDate()) ? age - 1 : age;
    
    // Prepare profile data
    const highestQual = data.highest_qualification;
    let degreeType = highestQual;
    let degreePercentage = 0;
    
    // If graduation is filled, get those values
    if (highestQual && highestQual !== '12th') {
        degreeType = highestQual;
        const cgpaValue = parseFloat(data.degree_cgpa) || 0;
        if (data.cgpa_type === 'CGPA') {
            // Convert CGPA to percentage (assuming 10 point scale)
            degreePercentage = cgpaValue * 10;
        } else {
            degreePercentage = cgpaValue;
        }
    }
    
    const profile = {
        dob: data.dob,
        age: ageInYears,
        gender: data.gender,
        marital_status: data.marital,
        nationality: data.nationality,
        highest_qualification: highestQual,
        twelfth_stream: data.twelfth_stream || '',
        twelfth_percentage: parseFloat(data.twelfth_percentage) || 0,
        twelfth_passing_year: data.twelfth_passing_year || '',
        degree_type: degreeType,
        degree_stream: data.degree_stream || '',
        degree_cgpa: parseFloat(data.degree_cgpa) || 0,
        cgpa_type: data.cgpa_type || 'Percentage',
        degree_percentage: degreePercentage,
        degree_passing_year: data.degree_passing_year || '',
        height: parseFloat(data.height) || 0,
        weight: parseFloat(data.weight) || 0,
        medical_problems: data.medical_problems || '',
        ncc_certificate: data.ncc_certificate === 'true',
        education: highestQual === '12th' ? ['12th'] : [degreeType]
    };

    // Show loading
    const submitBtn = e.target.querySelector('.action-btn');
    const originalText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span>Processing...</span>';

    try {
        const response = await fetch('/api/recommend', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({profile: profile})
        });

        const result = await response.json();
        
        // Store results in sessionStorage and redirect
        sessionStorage.setItem('recommendations', JSON.stringify(result));
        window.location.href = '/results';
    } catch (error) {
        alert('Error getting recommendations. Please try again.');
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    }
});

// Initialize
updateProgress();

