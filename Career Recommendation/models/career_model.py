from sklearn import tree
import numpy as np
from .career_data import CAREER_DATA, SKILLS_LIST, INTERESTS_LIST, EDUCATION_LEVELS

class CareerRecommender:
    """A simple AI-based career recommendation system using Decision Trees"""
    
    def __init__(self):
        """Initialize and train the model with predefined career data"""
        self.clf = tree.DecisionTreeClassifier()
        self._train_model()
        
    def _train_model(self):
        """Train the decision tree model with our career dataset"""
        # Extract features and target from our dataset
        X = []  # Features (skills, interests, education level)
        y = []  # Target (career paths)
        
        for career in CAREER_DATA:
            # Generate multiple training examples for each career
            for _ in range(5):  # Create 5 variations per career for better training
                # Features: skills, interests, education level
                features = self._encode_features(
                    np.random.choice(career['relevant_skills'], 
                                    size=min(3, len(career['relevant_skills'])), 
                                    replace=False).tolist(),
                    np.random.choice(career['relevant_interests'], 
                                    size=min(2, len(career['relevant_interests'])), 
                                    replace=False).tolist(),
                    np.random.choice(career['education_levels'], 
                                    size=1)[0]
                )
                
                X.append(features)
                y.append(career['id'])
        
        # Train the model
        self.clf.fit(X, y)
    
    def _encode_features(self, skills, interests, education):
        """Encode input features into a numerical vector"""
        # One-hot encode skills
        skills_vector = [1 if skill in skills else 0 for skill in SKILLS_LIST]
        
        # One-hot encode interests
        interests_vector = [1 if interest in interests else 0 for interest in INTERESTS_LIST]
        
        # One-hot encode education level
        education_index = EDUCATION_LEVELS.index(education)
        education_vector = [0] * len(EDUCATION_LEVELS)
        education_vector[education_index] = 1
        
        # Combine all features
        return skills_vector + interests_vector + education_vector
    
    def get_recommendations(self, skills, interests, education):
        """Get career recommendations based on user input"""
        # Encode the user input
        user_features = self._encode_features(skills, interests, education)
        
        # Use the model to predict the probability for each career
        proba = self.clf.predict_proba([user_features])[0]
        
        # Get top 3 career recommendations (indices)
        top_indices = np.argsort(proba)[::-1][:3]
        
        # Convert to career IDs (class labels)
        top_career_ids = [self.clf.classes_[idx] for idx in top_indices]
        
        # Get career details
        recommendations = []
        for career_id in top_career_ids:
            for career in CAREER_DATA:
                if career['id'] == career_id:
                    # Calculate match percentage (simplified)
                    match_percentage = int(proba[np.where(self.clf.classes_ == career_id)][0] * 100)
                    
                    recommendations.append({
                        'title': career['title'],
                        'description': career['description'],
                        'match_percentage': match_percentage,
                        'skills_needed': career['relevant_skills'],
                        'education': career['education_levels']
                    })
                    break
        
        return recommendations