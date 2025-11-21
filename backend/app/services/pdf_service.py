from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os
import tempfile

from app.models.models import Recommendation, Assessment, User

def generate_recommendation_pdf(recommendation: Recommendation, assessment: Assessment) -> str:
    """
    Generate a PDF report for career recommendation
    """
    # Create temporary file
    temp_dir = tempfile.gettempdir()
    pdf_filename = f"recommendation_{recommendation.recommendation_id}.pdf"
    pdf_path = os.path.join(temp_dir, pdf_filename)
    
    # Create PDF document
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a237e'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#283593'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#3949ab'),
        spaceAfter=8,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=8
    )
    
    # Title
    story.append(Paragraph("Career Recommendation Report", title_style))
    story.append(Paragraph("Defence & Civil Services", styles['Heading3']))
    story.append(Spacer(1, 0.3*inch))
    
    # Header info
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y')}", normal_style))
    story.append(Paragraph(f"Recommendation ID: {recommendation.recommendation_id}", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    # OLQ Score Section
    story.append(Paragraph("Officer Like Qualities (OLQ) Assessment", heading_style))
    olq_score = recommendation.olq_score
    story.append(Paragraph(f"Your OLQ Score: <b>{olq_score:.1f}%</b>", normal_style))
    
    # OLQ interpretation
    if olq_score >= 80:
        interpretation = "Excellent - Outstanding leadership potential"
    elif olq_score >= 65:
        interpretation = "Very Good - Strong leadership qualities"
    elif olq_score >= 50:
        interpretation = "Good - Demonstrated leadership potential"
    elif olq_score >= 35:
        interpretation = "Average - Basic leadership understanding"
    else:
        interpretation = "Below Average - Consider enlisted roles"
    
    story.append(Paragraph(f"Assessment: <b>{interpretation}</b>", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Explanation
    story.append(Paragraph("Career Path Recommendation", heading_style))
    story.append(Paragraph(recommendation.explanation, normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Recommended Roles
    story.append(Paragraph("Recommended Career Opportunities", heading_style))
    
    recommendations_data = recommendation.recommendations_data
    for idx, rec in enumerate(recommendations_data, 1):
        story.append(Paragraph(f"{idx}. {rec['role_name']}", subheading_style))
        
        # Role details table
        role_data = [
            ["Entry Scheme:", rec['entry_scheme']],
            ["Match Score:", f"{rec['match_score']:.1f}%"],
            ["Age Range:", f"{rec['min_age']} - {rec['max_age']} years"],
            ["Education:", rec['education_requirement']],
        ]
        
        role_table = Table(role_data, colWidths=[2*inch, 4*inch])
        role_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8eaf6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        story.append(role_table)
        story.append(Spacer(1, 0.1*inch))
        
        # Selection Process
        story.append(Paragraph("<b>Selection Process:</b>", normal_style))
        for step in rec['selection_process']:
            story.append(Paragraph(f"• {step}", normal_style))
        story.append(Spacer(1, 0.1*inch))
        
        # Reasoning
        story.append(Paragraph("<b>Why This Role:</b>", normal_style))
        story.append(Paragraph(rec['reasoning'], normal_style))
        
        # Feature Importance
        if rec.get('feature_importance'):
            story.append(Paragraph("<b>Key Factors:</b>", normal_style))
            for feature, importance in rec['feature_importance'].items():
                story.append(Paragraph(f"• {feature}: {importance*100:.1f}%", normal_style))
        
        story.append(Spacer(1, 0.2*inch))
    
    # Next Steps
    story.append(PageBreak())
    story.append(Paragraph("Next Steps", heading_style))
    next_steps = [
        "Review the recommended roles and research each in detail",
        "Check age and education eligibility for your preferred roles",
        "Start preparing according to the exam syllabus",
        "Maintain physical fitness as per required standards",
        "Stay updated with official notifications",
        "Consider joining coaching or study groups",
        "Practice previous year question papers",
        "Prepare for SSB interview (for officer entries)",
        "Keep all documents ready for application"
    ]
    
    for step in next_steps:
        story.append(Paragraph(f"• {step}", normal_style))
    
    story.append(Spacer(1, 0.3*inch))
    
    # Footer
    story.append(Paragraph("Important Notes", heading_style))
    notes = [
        "All information is based on current recruitment patterns and may change",
        "Please verify eligibility criteria from official sources",
        "Physical and medical standards must be met as per official requirements",
        "This recommendation is generated based on your assessment and should be used as guidance",
        "For official information, always refer to respective organization websites"
    ]
    
    for note in notes:
        story.append(Paragraph(f"• {note}", normal_style))
    
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Best wishes for your career!", styles['Heading3']))
    
    # Build PDF
    doc.build(story)
    
    return pdf_path
