"""
Script to create a properly formatted resume PDF with hyperlinks.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER

def create_resume_pdf():
    """Create Jerry's resume PDF with GitHub repository links."""
    
    filename = "JerrySanjuJoanes_Resume.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                            rightMargin=0.75*inch, leftMargin=0.75*inch,
                            topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor='#000000',
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    contact_style = ParagraphStyle(
        'Contact',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        spaceAfter=12
    )
    
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor='#000000',
        spaceAfter=6,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        leftIndent=0
    )
    
    # Name
    elements.append(Paragraph("Jerry Sanju Joanes", title_style))
    
    # Contact Info
    contact_info = """
    Alappuzha, Kerala, India<br/>
    +91 97447 37096<br/>
    <a href="mailto:jerrysanjujoanes000@gmail.com">jerrysanjujoanes000@gmail.com</a> | 
    <a href="https://linkedin.com/in/jerrysanjujoanes">LinkedIn</a> | 
    <a href="https://github.com/JerrySanjuJoanes">GitHub</a>
    """
    elements.append(Paragraph(contact_info, contact_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # SKILLS
    elements.append(Paragraph("SKILLS", section_heading))
    skills_text = """
    <b>Frontend:</b> HTML, CSS, JS (ES6+), React.js, Next.js, Tailwind CSS<br/>
    <b>Backend &amp; DB:</b> Firebase, Sanity CMS, Flask<br/>
    <b>Tools:</b> Git, GitHub, VS Code, Vercel, Vite, Postman, Figma<br/>
    <b>Soft Skills:</b> Leadership, Collaboration, Communication, Marketing
    """
    elements.append(Paragraph(skills_text, body_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # EXPERIENCE
    elements.append(Paragraph("EXPERIENCE", section_heading))
    
    exp1 = """
    <b>Front-End Development Intern</b> - Zilicon Technologies Pvt Ltd (Remote)<br/>
    <i>Jul 2024 – Oct 2024</i><br/>
    • Developed responsive frontend components for Riglabs Collective.<br/>
    • Built a private NPM UI library for design consistency and faster development.<br/>
    • Created a scalable Tailwind CSS theme system for consistent branding.
    """
    elements.append(Paragraph(exp1, body_style))
    elements.append(Spacer(1, 0.05*inch))
    
    exp2 = """
    <b>FOCES &amp; IEDC Bootcamp CEC</b>, College of Engineering Chengannur<br/>
    <i>Mar 2023 – Present</i><br/>
    • <b>Frontend Developer (FOCES):</b> Maintained FOCES website and CS Department site with performance and accessibility improvements.<br/>
    • <b>Web Developer (IEDC Bootcamp):</b> Managed Bootcamp website, implementing responsive layouts, SEO, and performance optimization.
    """
    elements.append(Paragraph(exp2, body_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # LEADERSHIP EXPERIENCE
    elements.append(Paragraph("LEADERSHIP EXPERIENCE", section_heading))
    
    lead1 = """
    <b>FOCES - Chairperson</b><br/>
    <i>Mar 2024 – Present</i><br/>
    • Lead technical, marketing, and event operations.<br/>
    • Guided 40+ members in hackathons, workshops, and outreach initiatives.
    """
    elements.append(Paragraph(lead1, body_style))
    elements.append(Spacer(1, 0.05*inch))
    
    lead2 = """
    <b>IEDC Bootcamp CEC - Chief Finance Officer</b><br/>
    <i>Sep 2023 – Present</i><br/>
    • Managed finances, sponsorships, and partnerships.<br/>
    • Oversaw web marketing teams.
    """
    elements.append(Paragraph(lead2, body_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # EDUCATION
    elements.append(Paragraph("EDUCATION", section_heading))
    edu = """
    <b>B.Tech, Computer Science and Engineering</b><br/>
    College of Engineering Chengannur (CEC), Kerala<br/>
    <i>2022 – 2026</i>
    """
    elements.append(Paragraph(edu, body_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # PROJECTS
    elements.append(Paragraph("PROJECTS", section_heading))
    
    proj1 = """
    <b>IEEE R10-140 Health and Wellness Campaign</b> — React.js, Firebase<br/>
    Developed leaderboard and activity tracking for 1000+ participants.
    """
    elements.append(Paragraph(proj1, body_style))
    elements.append(Spacer(1, 0.05*inch))
    
    proj2 = """
    <b>4Wayanad Relief Platform</b> — React.js, Firebase<br/>
    Built and deployed a real-time relief platform in 2 days for Wayanad landslides, streamlining aid distribution.<br/>
    <a href="https://github.com/Shijin-GitH/4Wayanad">https://github.com/Shijin-GitH/4Wayanad</a>
    """
    elements.append(Paragraph(proj2, body_style))
    elements.append(Spacer(1, 0.05*inch))
    
    proj3 = """
    <b>Digital Vehicle Assistant (DVA)</b> — React.js, Flask, PostgreSQL, LeafletJS, OpenStreetMap API<br/>
    Open-source platform for fuel-efficient route planning, real-time vehicle management, maintenance reminders, and SOS alerts.<br/>
    <a href="https://github.com/JerrySanjuJoanes/dvabetta">https://github.com/JerrySanjuJoanes/dvabetta</a>
    """
    elements.append(Paragraph(proj3, body_style))
    elements.append(Spacer(1, 0.05*inch))
    
    proj4 = """
    <b>Exodia 2025 Website</b> — React.js, Tailwind CSS<br/>
    Created a dynamic site for event schedules and participant registration.<br/>
    <a href="https://github.com/JerrySanjuJoanes/Exodia">https://github.com/JerrySanjuJoanes/Exodia</a>
    """
    elements.append(Paragraph(proj4, body_style))
    
    # Build PDF
    doc.build(elements)
    print(f"✅ Created {filename}")
    return filename

if __name__ == "__main__":
    create_resume_pdf()
