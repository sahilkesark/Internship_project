import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
import json

def generate_synthetic_data(n_samples=1000):
    """
    Generate synthetic training data for the recommendation model
    """
    np.random.seed(42)
    
    data = []
    
    for _ in range(n_samples):
        # Generate features
        olq_score = np.random.uniform(0, 100)
        education_level = np.random.choice([1, 2, 3, 4, 5])  # 1=10th, 2=12th, 3=grad, 4=masters, 5=phd
        percentage = np.random.uniform(50, 95)
        age = np.random.uniform(17, 32)
        has_ncc = np.random.choice([0, 1], p=[0.7, 0.3])
        height = np.random.uniform(155, 185)
        weight = np.random.uniform(50, 85)
        bmi = weight / ((height/100) ** 2)
        
        # Additional qualifications
        num_qualifications = np.random.poisson(0.5)
        
        # Determine suitable roles based on rules
        suitable_roles = []
        
        # Officer roles
        if olq_score >= 60 and education_level >= 2 and age >= 16.5 and age <= 24:
            if education_level >= 2 and age <= 19.5:
                suitable_roles.append("NDA")
            if education_level >= 3 and age >= 19:
                suitable_roles.append("CDS")
            if education_level >= 3:
                suitable_roles.append("AFCAT")
        
        # Civil Services
        if olq_score >= 70 and education_level >= 3 and age >= 21 and age <= 32:
            suitable_roles.append("UPSC_CSE")
        
        # Enlisted roles
        if olq_score < 50 or age < 19:
            if education_level >= 1 and age >= 17.5 and age <= 21:
                suitable_roles.append("ARMY_GD")
                suitable_roles.append("AGNIVEER")
        
        # If no roles, add default
        if not suitable_roles:
            if education_level >= 2:
                suitable_roles.append("ARMY_TECHNICAL")
            else:
                suitable_roles.append("ARMY_GD")
        
        # Pick primary role
        primary_role = np.random.choice(suitable_roles)
        
        # Calculate success probability
        success_prob = 0.5
        if olq_score >= 70:
            success_prob += 0.2
        if percentage >= 75:
            success_prob += 0.15
        if has_ncc:
            success_prob += 0.1
        if 18.5 <= bmi <= 24.9:
            success_prob += 0.05
        
        success_prob = min(success_prob, 0.95)
        
        data.append({
            'olq_score': olq_score / 100,  # Normalize
            'education_level': education_level / 5,
            'percentage': percentage / 100,
            'age': age / 35,
            'has_ncc': has_ncc,
            'height': height / 190,
            'weight': weight / 100,
            'bmi': bmi / 30,
            'num_qualifications': min(num_qualifications, 5) / 5,
            'primary_role': primary_role,
            'success_probability': success_prob
        })
    
    return pd.DataFrame(data)

def train_models():
    """
    Train ML models for role recommendation
    """
    print("Generating synthetic training data...")
    df = generate_synthetic_data(n_samples=2000)
    
    # Prepare features
    feature_columns = [
        'olq_score', 'education_level', 'percentage', 'age',
        'has_ncc', 'height', 'weight', 'bmi', 'num_qualifications'
    ]
    
    X = df[feature_columns].values
    y_role = df['primary_role'].values
    y_success = df['success_probability'].values
    
    # Encode roles
    le = LabelEncoder()
    y_role_encoded = le.fit_transform(y_role)
    
    # Split data
    X_train, X_test, y_role_train, y_role_test, y_success_train, y_success_test = train_test_split(
        X, y_role_encoded, y_success, test_size=0.2, random_state=42
    )
    
    print("\nTraining Role Classification Model...")
    role_classifier = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight='balanced'
    )
    role_classifier.fit(X_train, y_role_train)
    
    # Evaluate
    y_role_pred = role_classifier.predict(X_test)
    accuracy = accuracy_score(y_role_test, y_role_pred)
    print(f"Role Classification Accuracy: {accuracy:.3f}")
    
    # Cross-validation
    cv_scores = cross_val_score(role_classifier, X_train, y_role_train, cv=5)
    print(f"Cross-validation scores: {cv_scores}")
    print(f"Mean CV score: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
    
    # Feature importance
    feature_importance = dict(zip(feature_columns, role_classifier.feature_importances_))
    print("\nFeature Importance:")
    for feature, importance in sorted(feature_importance.items(), key=lambda x: x[1], reverse=True):
        print(f"  {feature}: {importance:.3f}")
    
    print("\nTraining Success Probability Model...")
    success_predictor = GradientBoostingClassifier(
        n_estimators=100,
        max_depth=5,
        random_state=42
    )
    
    # Convert to binary classification (success > 0.7)
    y_success_binary = (y_success_train > 0.7).astype(int)
    success_predictor.fit(X_train, y_success_binary)
    
    y_success_pred = success_predictor.predict(X_test)
    y_success_test_binary = (y_success_test > 0.7).astype(int)
    success_accuracy = accuracy_score(y_success_test_binary, y_success_pred)
    print(f"Success Prediction Accuracy: {success_accuracy:.3f}")
    
    # Save models
    model_dir = os.path.join(os.path.dirname(__file__), '../../data/models')
    os.makedirs(model_dir, exist_ok=True)
    
    print(f"\nSaving models to {model_dir}...")
    joblib.dump(role_classifier, os.path.join(model_dir, 'role_classifier.pkl'))
    joblib.dump(success_predictor, os.path.join(model_dir, 'success_predictor.pkl'))
    joblib.dump(le, os.path.join(model_dir, 'label_encoder.pkl'))
    
    # Save feature names
    with open(os.path.join(model_dir, 'feature_names.json'), 'w') as f:
        json.dump(feature_columns, f)
    
    # Save model metadata
    metadata = {
        'role_classifier_accuracy': float(accuracy),
        'success_predictor_accuracy': float(success_accuracy),
        'feature_importance': {k: float(v) for k, v in feature_importance.items()},
        'role_classes': le.classes_.tolist(),
        'training_samples': len(X_train),
        'test_samples': len(X_test),
        'trained_on': pd.Timestamp.now().isoformat()
    }
    
    with open(os.path.join(model_dir, 'model_metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("\nModel training completed successfully!")
    print(f"Models saved to: {model_dir}")
    
    return role_classifier, success_predictor, le

if __name__ == "__main__":
    train_models()
