from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from firebase_config import db, auth
from firebase_admin import firestore
import career_matcher
import cv_analyzer
import personality_assessor
import os
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            # Verify user with Firebase Auth
            user = auth.get_user_by_email(email)
            
            # In a production app, verify password with Firebase client SDK
            # For now, we'll just set the session
            session['user_id'] = user.uid
            session['user_email'] = email
            
            # Update last login time
            db.collection('users').document(user.uid).update({
                'last_login': firestore.SERVER_TIMESTAMP
            })
            
            return redirect(url_for('dashboard'))
            
        except auth.UserNotFoundError:
            flash('User not found', 'error')
        except Exception as e:
            flash('Login failed. Please try again.', 'error')
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        
        try:
            # Create user in Firebase Authentication
            user = auth.create_user(
                email=email,
                password=password,
                display_name=name
            )
            
            # Store additional user data in Firestore
            user_data = {
                'name': name,
                'email': email,
                'created_at': firestore.SERVER_TIMESTAMP,
                'last_login': firestore.SERVER_TIMESTAMP
            }
            
            db.collection('users').document(user.uid).set(user_data)
            
            # Set session variables
            session['user_id'] = user.uid
            session['user_email'] = email
            session['user_name'] = name
            
            return redirect(url_for('dashboard'))
            
        except auth.EmailAlreadyExistsError:
            flash('Email already exists', 'error')
        except Exception as e:
            flash('Registration failed. Please try again.', 'error')
    
    return render_template('auth/register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    user_ref = db.collection('users').document(user_id)
    
    # Check assessment completion more robustly
    assessments = {
        'personality': user_ref.collection('assessments').document('personality').get().exists,
        'academic': user_ref.collection('assessments').document('academic').get().exists,
        'interests': user_ref.collection('assessments').document('interests').get().exists
    }
    
    # Get personality type if exists
    personality_data = user_ref.collection('assessments').document('personality').get().to_dict()
    personality_type = personality_data.get('type', 'Not started') if personality_data else 'Not started'
    
    return render_template('dashboard.html',
                         assessments=assessments,
                         personality_type=personality_type,
                         user=user_ref.get().to_dict())

@app.route('/assessment/personality', methods=['GET', 'POST'])
@login_required
def personality_assessment():
    # Initialize the assessor
    assessor = personality_assessor.PersonalityAssessor()
    
    if request.method == 'POST':
        try:
            answers = {k: int(v) for k, v in request.form.items() if k.startswith('q')}
            personality_type = assessor.assess_personality(answers)
            
            db.collection('users').document(session['user_id']).collection('assessments').document('personality').set({
                'type': personality_type,
                'answers': answers,
                'completed_at': firestore.SERVER_TIMESTAMP
            })
            
            return redirect(url_for('assessment_results'))
            
        except Exception as e:
            flash(f'Assessment failed: {str(e)}', 'error')
    
    # Pass both assessor and questions to template
    return render_template('assessment/personality.html', 
                         assessor=assessor,
                         questions=assessor.questions)


@app.route('/assessment/academic', methods=['GET', 'POST'])
@login_required
def academic_assessment():
    if request.method == 'POST':
        try:
            # Check if files were uploaded
            if 'files' not in request.files:
                flash('No files selected', 'error')
                return redirect(request.url)
            
            files = request.files.getlist('files')
            if not files or all(file.filename == '' for file in files):
                flash('Please select at least one file', 'error')
                return redirect(request.url)
            
            academic_data = {'subjects': {}, 'documents': []}
            
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    academic_data['documents'].append(filename)
                    
                    # Process academic data
                    file_data = cv_analyzer.extract_academic_data(filepath)
                    if 'subjects' in file_data:
                        academic_data['subjects'].update(file_data['subjects'])
            
            if not academic_data['subjects']:
                flash('No valid academic data found in the documents', 'warning')
                return redirect(request.url)
            
            # Save to Firestore
            academic_data['completed_at'] = firestore.SERVER_TIMESTAMP
            db.collection('users').document(session['user_id']).collection('assessments').document('academic').set(academic_data)
            
            flash('Academic records processed successfully!', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            flash(f'Error processing files: {str(e)}', 'error')
            return redirect(request.url)
    
    return render_template('assessment/academic.html')


@app.route('/assessment/interests', methods=['GET', 'POST'])
@login_required
def interests_assessment():
    if request.method == 'POST':
        try:
            interests = request.form.getlist('interests')
            additional = request.form.get('additional_interests', '')
            
            if additional:
                interests.extend([i.strip() for i in additional.split(',') if i.strip()])
                
            if not interests:
                raise ValueError("Please select at least one interest")
                
            db.collection('users').document(session['user_id']).collection('assessments').document('interests').set({
                'interests': interests,
                'completed_at': firestore.SERVER_TIMESTAMP
            })
            
            flash('Interests saved!', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            print(f"Interest Assessment Error: {str(e)}")
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('assessment/interests.html')

@app.route('/results')
@login_required
def assessment_results():
    user_id = session['user_id']
    user_ref = db.collection('users').document(user_id)
    
    # Get all assessment data
    assessments = {
        'personality': user_ref.collection('assessments').document('personality').get().to_dict(),
        'academic': user_ref.collection('assessments').document('academic').get().to_dict(),
        'interests': user_ref.collection('assessments').document('interests').get().to_dict()
    }
    
    # Check if all assessments exist and have data
    if not all(assessments.values()):
        missing = [name for name, data in assessments.items() if not data]
        flash(f'Please complete: {", ".join(missing)} assessments', 'warning')
        return redirect(url_for('dashboard'))
    
    # Generate recommendations
    recommendations = career_matcher.get_recommendations(
        personality_type=assessments['personality']['type'],
        academic_data=assessments['academic'],
        interests=assessments['interests']['interests']
    )
    
    return render_template('results.html', 
                         recommendations=recommendations,
                         assessments=assessments)
@app.route('/chatbot')
@login_required
def chatbot():
    return render_template('chatbot.html')

if __name__ == '__main__':
    app.run(debug=True)