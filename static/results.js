function displayResults() {
    const recommendations = JSON.parse(sessionStorage.getItem('recommendations'));
    
    if (!recommendations) {
        window.location.href = '/';
        return;
    }

    const loading = document.getElementById('loading');
    const resultsContainer = document.getElementById('resultsContainer');
    
    loading.classList.add('hidden');
    resultsContainer.classList.remove('hidden');

    // Update count
    document.getElementById('eligibleCount').textContent = recommendations.eligible?.length || 0;

    // Display eligible careers only
    displayCareerList(recommendations.eligible || [], 'eligible-list', true);

    // Show preparation plan button for the top recommendation at the bottom
    try {
        const top = (recommendations.eligible || [])[0];
        const actionContainer = document.getElementById('prep-plan-action');
        if (top && actionContainer) {
            const careerParam = encodeURIComponent(top.name || '');
            actionContainer.innerHTML = `
                <a href="/prep-plan?career=${careerParam}" class="primary-btn prep-plan-bottom-btn">
                    <span>View Preparation Plan for Top Recommendation</span>
                    <span class="btn-arrow">→</span>
                </a>
            `;
            actionContainer.style.display = 'block';
        } else if (actionContainer) {
            actionContainer.style.display = 'none';
        }
    } catch (e) {
        console.error('Failed to inject preparation plan action:', e);
    }
}

function formatEligibilityDetails(career) {
    const details = [];
    const eligibility = career.eligibility || {};
    
    // Description - what is this entry (ALWAYS FIRST and ALWAYS SHOWN)
    // This ensures description is always visible for all entries, single or multiple
    if (career.description) {
        details.push(career.description);
    } else {
        // If no description, add a default one based on career name
        details.push(`A career opportunity in ${career.service_branch || 'Defence Services'}.`);
    }
    
    // Role - what you will become
    if (career.role) {
        details.push(`You will become: ${career.role}`);
    }
    
    // Entry Details - detailed information about the entry process
    if (career.entry_details) {
        details.push(`Entry Details: ${career.entry_details}`);
    }
    
    // What it offers - benefits and perks
    if (career.offers) {
        details.push(`What it offers: ${career.offers}`);
    }
    
    // Age requirements
    if (eligibility.age_min && eligibility.age_max) {
        details.push(`Age Requirement: ${eligibility.age_min}-${eligibility.age_max} years`);
    }
    
    // Education requirements
    if (eligibility.education && eligibility.education.length > 0) {
        const eduStr = eligibility.education.join(', ');
        let eduDetail = `Education: ${eduStr}`;
        if (eligibility.education_percentage_min) {
            eduDetail += ` (Minimum ${eligibility.education_percentage_min}%)`;
        } else if (eligibility.degree_percentage_min) {
            eduDetail += ` (Minimum ${eligibility.degree_percentage_min}%)`;
        }
        details.push(eduDetail);
    }
    
    // Physical requirements
    if (eligibility.height_min_cm || eligibility.weight_min_kg) {
        const physDetails = [];
        if (eligibility.height_min_cm) {
            physDetails.push(`Height: ${eligibility.height_min_cm} cm`);
        }
        if (eligibility.weight_min_kg) {
            physDetails.push(`Weight: ${eligibility.weight_min_kg} kg`);
        }
        if (physDetails.length > 0) {
            details.push(`Physical Requirements: ${physDetails.join(', ')}`);
        }
    }
    
    // Marital status requirement
    if (eligibility.marital_status && eligibility.marital_status.length > 0) {
        const maritalStr = eligibility.marital_status.join(' or ');
        details.push(`Marital Status: ${maritalStr}`);
    }
    
    // NCC certificate requirement
    if (eligibility.ncc_certificate) {
        details.push(`Special Requirement: NCC Certificate required`);
    }
    
    return details;
}

function formatIneligibleReason(reason) {
    if (!reason) return ['Not eligible'];
    
    // Split by " | " to show multiple reasons on separate lines
    const reasons = String(reason).split(' | ');
    return reasons.map(r => r.trim()).filter(r => r.length > 0);
}

function displayCareerList(careers, elementId, isEligible) {
    const container = document.getElementById(elementId);
    container.innerHTML = '';

    if (careers.length === 0) {
        container.innerHTML = '<p class="no-results">No careers found in this category.</p>';
        return;
    }

    careers.forEach((career, index) => {
        const div = document.createElement('div');
        div.className = `career-card ${isEligible ? 'eligible' : 'ineligible'}`;
        div.style.animationDelay = `${index * 0.1}s`;
        
        if (isEligible) {
            // Extract description separately for prominent display
            let description = career.description || '';
            
            // If no description found, create a meaningful one based on career info
            if (!description || description.trim() === '') {
                const serviceBranch = career.service_branch || 'Defence Services';
                const entryType = career.entry_type || 'Entry';
                const careerName = career.name || 'This career';
                description = `${careerName} is a ${entryType} entry scheme in the ${serviceBranch}. This career path offers opportunities to serve the nation and build a distinguished career in ${serviceBranch}.`;
            }
            
            // Ensure description is a string and trim it
            description = String(description).trim();
            
            // Get other details (excluding description)
            const details = formatEligibilityDetails(career);
            // Remove the first item (description) since we're showing it separately
            const otherDetails = details.slice(1);
            const detailsHtml = otherDetails.map(d => `<div class="career-detail">${escapeHtml(d)}</div>`).join('');
            
            // Create prep plan button for each career
            const careerParam = encodeURIComponent(career.name || '');
            const prepPlanBtn = `
                <div class="career-prep-plan-btn">
                    <a href="/prep-plan?career=${careerParam}" class="prep-plan-link">
                        <span>View Preparation Plan</span>
                        <span class="btn-arrow">→</span>
                    </a>
                </div>
            `;
            
            div.innerHTML = `
                <div class="career-name-wrapper">
                    <h4 class="career-name">${career.name}</h4>
                </div>
                <div class="career-meta">
                    <span class="career-branch">${career.service_branch}</span>
                    <span class="career-separator">•</span>
                    <span class="career-entry">${career.entry_type || 'Entry'}</span>
                </div>
                ${description && description.trim() !== '' ? `
                <div class="career-description" style="display: block !important; visibility: visible !important; opacity: 1 !important;">
                    <strong>About this Service:</strong> ${escapeHtml(description)}
                </div>
                ` : `
                <div class="career-description" style="display: block !important; visibility: visible !important; opacity: 1 !important;">
                    <strong>About this Service:</strong> ${escapeHtml(`A ${career.entry_type || 'career'} opportunity in the ${career.service_branch || 'Defence Services'}. This entry scheme offers a path to serve the nation and build a distinguished career.`)}
                </div>
                `}
                <div class="career-details">
                    ${detailsHtml}
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${career.score || 0}%"></div>
                </div>
                <div class="match-score">${career.score || 0}% Match</div>
                ${prepPlanBtn}
            `;
        } else {
            const reason = career.reason || 'Not eligible';
            const reasons = formatIneligibleReason(reason);
            
            // Create reasons HTML with better formatting
            let reasonsHtml = '';
            if (reasons.length > 0) {
                reasonsHtml = `
                    <div class="ineligible-reason-header">Why not eligible:</div>
                    <div class="ineligible-reasons-list">
                        ${reasons.map(r => `<div class="reason-line">${escapeHtml(r)}</div>`).join('')}
                    </div>
                `;
            } else {
                reasonsHtml = '<div class="reason-line">Not eligible</div>';
            }
            
            div.innerHTML = `
                <h4>${career.name}</h4>
                <div class="career-meta">
                    <span class="career-branch">${career.service_branch}</span>
                    <span class="career-separator">•</span>
                    <span class="career-entry">${career.entry_type || 'Entry'}</span>
                </div>
                <div class="ineligible-reason">
                    ${reasonsHtml}
                </div>
            `;
        }
        
        container.appendChild(div);
    });
}

// Helper function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Load results when page loads
window.addEventListener('DOMContentLoaded', displayResults);

