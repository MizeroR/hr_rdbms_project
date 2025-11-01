#!/usr/bin/env python3
"""
Train and save ML model for attrition prediction
Run this first to create the model file needed for Task 3
"""
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import os

def train_attrition_model():
    # Load dataset
    data_path = os.path.join(os.path.dirname(__file__), '..', 'databases', 'WA_Fn-UseC_-HR-Employee-Attrition.csv')
    df = pd.read_csv(data_path)
    
    # Select key features for prediction
    features = ['Age', ' Education', ' JobLevel', ' JobSatisfaction', 
               ' MonthlyIncome', ' TotalWorkingYears', ' YearsAtCompany']
    
    X = df[features]
    y = LabelEncoder().fit_transform(df[' Attrition'].str.strip())
    
    # Train model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Save model and feature names
    model_dir = os.path.join(os.path.dirname(__file__), 'model')
    os.makedirs(model_dir, exist_ok=True)
    
    joblib.dump(model, os.path.join(model_dir, 'attrition_model.pkl'))
    joblib.dump(features, os.path.join(model_dir, 'feature_names.pkl'))
    
    print(f"Model trained and saved. Accuracy: {model.score(X_test, y_test):.3f}")
    return model

if __name__ == "__main__":
    train_attrition_model()