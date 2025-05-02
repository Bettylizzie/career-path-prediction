import PyPDF2
import re
from collections import defaultdict

def extract_academic_data(filepath):
    # This is a simplified version. In a real app, you'd use more sophisticated parsing
    if filepath.endswith('.pdf'):
        return extract_from_pdf(filepath)
    else:
        # Handle image-based transcripts with OCR (would need pytesseract)
        return extract_from_image(filepath)

def extract_from_pdf(filepath):
    academic_data = {
        'subjects': {},
        'overall_performance': '',
        'institution': '',
        'qualification': ''
    }
    
    with open(filepath, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        # Extract institution
        institution_match = re.search(r'(University|College|School|Institute)\s+of?\s+([^\n]+)', text, re.I)
        if institution_match:
            academic_data['institution'] = institution_match.group(0)
        
        # Extract qualification
        qual_match = re.search(r'(Bachelor|Diploma|Certificate)\s+of?\s+([^\n]+)', text, re.I)
        if qual_match:
            academic_data['qualification'] = qual_match.group(0)
        
        # Extract subjects and grades
        grade_pattern = re.compile(r'([A-Za-z\s]+)\s+([A-F]|\d{2,3})')
        matches = grade_pattern.finditer(text)
        
        for match in matches:
            subject = match.group(1).strip()
            grade = match.group(2).strip()
            
            # Convert letter grades to numerical
            if grade.isalpha():
                grade = convert_letter_grade(grade)
            
            if grade.isdigit():
                academic_data['subjects'][subject] = int(grade)
        
        # Calculate overall performance
        if academic_data['subjects']:
            avg_grade = sum(academic_data['subjects'].values()) / len(academic_data['subjects'])
            academic_data['overall_performance'] = classify_performance(avg_grade)
    
    return academic_data

def convert_letter_grade(letter):
    grade_map = {'A': 85, 'B': 75, 'C': 65, 'D': 55, 'E': 45, 'F': 35}
    return grade_map.get(letter.upper(), 0)

def classify_performance(average):
    if average >= 80:
        return 'Excellent'
    elif average >= 70:
        return 'Good'
    elif average >= 60:
        return 'Average'
    elif average >= 50:
        return 'Below Average'
    else:
        return 'Poor'

def extract_from_image(filepath):
    # This would use pytesseract for OCR
    # For now, return dummy data
    return {
        'subjects': {
            'Mathematics': 85,
            'Physics': 78,
            'Chemistry': 82,
            'English': 75
        },
        'overall_performance': 'Good',
        'institution': 'Sample University',
        'qualification': 'Bachelor of Science'
    }