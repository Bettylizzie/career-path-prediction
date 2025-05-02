import firebase_admin
from firebase_admin import credentials, firestore, auth  # Added auth import

def initialize_firebase():
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    return firestore.client()

# Initialize Firebase
db = initialize_firebase()
auth = auth  # Make auth available for import

def get_user_data(user_id):
    user_ref = db.collection('users').document(user_id)
    return user_ref.get().to_dict()

def save_assessment_results(user_id, assessment_type, results):
    db.collection('users').document(user_id).collection('assessments').document(assessment_type).set(results)

# Career database initialization
def init_career_data():
    careers_ref = db.collection('careers')
    if not careers_ref.limit(1).get():  # More efficient check if collection exists
        # Sample career data
        careers = [
            {
                'title': 'Software Developer',
                'skills': ['Programming', 'Problem Solving', 'Teamwork'],
                'personality': {'Openness': 80, 'Conscientiousness': 70},
                'education': {'Math': 'B', 'Science': 'B'},
                'image': 'https://images.unsplash.com/photo-1551033406-611cf9a28f67',
                'demand': 'High',
                'salary_range': '$70,000 - $120,000'
            },
            # More careers...
        ]
        batch = db.batch()
        for career in careers:
            new_ref = careers_ref.document()
            batch.set(new_ref, career)
        batch.commit()