from flask import Flask, render_template, request, session, redirect, url_for
import os
from models.career_model import CareerRecommender

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Initialize the AI career recommender model
career_recommender = CareerRecommender()

@app.route('/')
def home():
    """Render the home page"""
    return render_template('index.html')

@app.route('/form')
def form():
    """Render the input form page"""
    return render_template('form.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    """Process form data and generate recommendations"""
    if request.method == 'POST':
        # Get form data
        skills = request.form.getlist('skills')
        interests = request.form.getlist('interests')
        education = request.form.get('education')
        
        # Generate recommendations using the AI model
        recommendations = career_recommender.get_recommendations(
            skills=skills,
            interests=interests,
            education=education
        )
        
        # Store in session (temporary storage)
        session['user_data'] = {
            'skills': skills,
            'interests': interests,
            'education': education
        }
        session['recommendations'] = recommendations
        
        return redirect(url_for('result'))
    
    return redirect(url_for('form'))

@app.route('/result')
def result():
    """Show recommendation results"""
    # Check if we have recommendations in the session
    if 'recommendations' not in session:
        return redirect(url_for('form'))
    
    recommendations = session['recommendations']
    user_data = session.get('user_data', {})
    
    return render_template('result.html', 
                           recommendations=recommendations,
                           user_data=user_data)

if __name__ == '__main__':
    app.run(debug=True)
    
    