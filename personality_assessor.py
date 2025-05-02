class PersonalityAssessor:
    def __init__(self):
        self.questions = [
            "I enjoy analyzing problems and finding logical solutions.",
            "I prefer working in teams rather than alone.",
            "I like following established routines and procedures.",
            "I'm often described as creative and imaginative.",
            "I make decisions based more on facts than feelings.",
            "I enjoy helping others and making a difference in their lives.",
            "I prefer jobs with clear instructions over open-ended tasks.",
            "I'm always looking for new experiences and adventures.",
            "I trust logic more than intuition when making decisions.",
            "I'm good at understanding how other people are feeling."
        ]
        
        self.traits = {
            'Analyst': ['logical', 'analytical', 'objective'],
            'Diplomat': ['empathetic', 'cooperative', 'idealistic'],
            'Sentinel': ['practical', 'reliable', 'organized'],
            'Explorer': ['spontaneous', 'adaptable', 'curious']
        }
    
    def assess_personality(self, answers):
        """Assess personality based on answers (1-5 scale)"""
        if len(answers) != len(self.questions):
            raise ValueError("Number of answers doesn't match number of questions")
        
        # Calculate scores for each trait
        trait_scores = {
            'Analyst': (answers.get('q1', 0) + answers.get('q5', 0) + answers.get('q9', 0)),
            'Diplomat': (answers.get('q2', 0) + answers.get('q6', 0) + answers.get('q10', 0)),
            'Sentinel': (answers.get('q3', 0) + answers.get('q7', 0)),
            'Explorer': (answers.get('q4', 0) + answers.get('q8', 0))
        }
        
        # Determine the dominant trait
        dominant_trait = max(trait_scores.items(), key=lambda x: x[1])[0]
        
        return dominant_trait

def assess_personality(answers):
    assessor = PersonalityAssessor()
    return assessor.assess_personality(answers)