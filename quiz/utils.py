from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from django.core.files.base import ContentFile
from django.conf import settings
import os
from datetime import datetime
import uuid
from .models import Certificate

def generate_certificate(quiz_attempt):
    if not quiz_attempt.passed:
        return None
    
    certificate_number = str(uuid.uuid4())[:8].upper()
    pdf_filename = f"certificate_{quiz_attempt.id}_{certificate_number}.pdf"
    pdf_filepath = os.path.join(settings.MEDIA_ROOT, 'certificates', pdf_filename)
    
    os.makedirs(os.path.dirname(pdf_filepath), exist_ok=True)
    
    doc = SimpleDocTemplate(pdf_filepath, pagesize=A4)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=36,
        textColor=colors.HexColor('#1a73e8'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=24,
        textColor=colors.HexColor('#34a853'),
        spaceAfter=20,
        alignment=TA_CENTER,
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=14,
        alignment=TA_CENTER,
        spaceAfter=12,
    )
    
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("Certificate of Achievement", title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    elements.append(Paragraph("This is to certify that", normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    student_name = Paragraph(
        f"<b>{quiz_attempt.student.get_full_name() or quiz_attempt.student.username}</b>",
        subtitle_style
    )
    elements.append(student_name)
    elements.append(Spacer(1, 0.2*inch))
    
    quiz_info = Paragraph(
        f"has successfully completed the quiz: <b>{quiz_attempt.quiz.title}</b>",
        normal_style
    )
    elements.append(quiz_info)
    elements.append(Spacer(1, 0.2*inch))
    
    score_info = Paragraph(
        f"with a score of <b>{quiz_attempt.obtained_score}/{quiz_attempt.total_score} ({quiz_attempt.percentage:.2f}%)</b>",
        normal_style
    )
    elements.append(score_info)
    elements.append(Spacer(1, 0.3*inch))
    
    date_str = quiz_attempt.submitted_at.strftime("%B %d, %Y")
    date_para = Paragraph(
        f"Date: <b>{date_str}</b>",
        normal_style
    )
    elements.append(date_para)
    elements.append(Spacer(1, 0.1*inch))
    
    cert_num = Paragraph(
        f"Certificate No: <b>{certificate_number}</b>",
        normal_style
    )
    elements.append(cert_num)
    
    doc.build(elements)
    
    with open(pdf_filepath, 'rb') as pdf_file:
        pdf_content = ContentFile(pdf_file.read())
        
        certificate = Certificate.objects.create(
            quiz_attempt=quiz_attempt,
            certificate_number=certificate_number,
        )
        certificate.pdf_file.save(pdf_filename, pdf_content, save=True)
    
    return certificate
