import json
from collections import defaultdict

class CareerMatcher:
    def __init__(self):
        # Load career data (in a real app, this would come from a database)
        with open('career_data.json') as f:
            self.career_data = json.load(f)
        
        # Personality to career mapping
        self.personality_map = {
            'Analyst': ['Data Scientist', 'Software Engineer', 'Financial Analyst', 'AI Specialist'],
            'Diplomat': ['HR Manager', 'Teacher', 'Psychologist', 'Social Worker'],
            'Sentinel': ['Accountant', 'Project Manager', 'Logistics Coordinator', 'Quality Assurance'],
            'Explorer': ['Entrepreneur', 'Marketing Specialist', 'Graphic Designer', 'Tour Guide']
        }
        
        # Subject to career mapping
        self.subject_map = {
            'Mathematics': ['Data Scientist', 'Financial Analyst', 'Engineer', 'Statistician'],
            'Sciences': ['Doctor', 'Biotechnologist', 'Chemist', 'Environmental Scientist'],
            'Languages': ['Journalist', 'Content Writer', 'Translator', 'Public Relations'],
            'Technical': ['Electrician', 'Plumber', 'Mechanic', 'Carpenter'],
            'Arts': ['Graphic Designer', 'Musician', 'Actor', 'Interior Designer']
        }
        
        # Interest to career mapping
        self.interest_map = {
            'Technology': ['Software Developer', 'Cybersecurity Expert', 'IT Support'],
            'Business': ['Entrepreneur', 'Business Analyst', 'Sales Manager'],
            'Healthcare': ['Nurse', 'Doctor', 'Pharmacist', 'Nutritionist'],
            'Creative': ['Graphic Designer', 'Writer', 'Photographer'],
            'Social': ['Teacher', 'Counselor', 'Community Worker']
        }
        
        # Load job market trends
        with open('market_trends.json') as f:
            self.market_trends = json.load(f)
    
    def get_recommendations(self, personality_type, academic_data, interests):
        # Get personality-based recommendations
        personality_careers = self.personality_map.get(personality_type, [])
        
        # Get academic-based recommendations
        academic_careers = []
        for subject, grade in academic_data.get('subjects', {}).items():
            if grade >= 70:  # Only consider subjects with good grades
                academic_careers.extend(self.subject_map.get(subject, []))
        
        # Get interest-based recommendations
        interest_careers = []
        for interest in interests:
            interest_careers.extend(self.interest_map.get(interest, []))
        
        # Combine all recommendations with weights
        recommendations = defaultdict(int)
        for career in personality_careers:
            recommendations[career] += 3  # Personality match is weighted higher
        
        for career in academic_careers:
            recommendations[career] += 2  # Academic match is medium weight
        
        for career in interest_careers:
            recommendations[career] += 1  # Interest match is lower weight
        
        # Sort by weight and get top 3
        sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        top_careers = [career for career, score in sorted_recommendations[:3]]
        
        # Add market data to recommendations
        final_recommendations = []
        for career in top_careers:
            trend_data = self.market_trends.get(career, {})
            final_recommendations.append({
                'career': career,
                'description': self.career_data.get(career, {}).get('description', ''),
                'growth': trend_data.get('growth', 'Moderate'),
                'salary_range': trend_data.get('salary_range', 'Varies'),
                'required_skills': self.career_data.get(career, {}).get('skills', []),
                'courses': self.career_data.get(career, {}).get('courses', [])
            })
        
        return final_recommendations

def get_recommendations(personality_type, academic_data, interests):
    matcher = CareerMatcher()
    return matcher.get_recommendations(personality_type, academic_data, interests)