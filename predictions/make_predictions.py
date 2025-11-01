#!/usr/bin/env python3
"""
Activity B: Load ML model and make attrition predictions
"""
import joblib
import json
import os

def load_model():
    """Load the trained ML model"""
    try:
        model_path = os.path.join(os.path.dirname(__file__), 'model', 'attrition_model.pkl')
        features_path = os.path.join(os.path.dirname(__file__), 'model', 'feature_names.pkl')
        
        model = joblib.load(model_path)
        feature_names = joblib.load(features_path)
        
        print("Model loaded successfully")
        return model, feature_names
        
    except FileNotFoundError:
        print("Error: Model file not found. Run train_model.py first.")
        return None, None
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None

def make_prediction(model, feature_names, employee_features):
    """Make attrition prediction for employee"""
    try:
        # Prepare input data in correct order
        input_data = []
        for feature in feature_names:
            # Handle different feature name formats
            key = feature.strip()
            if key not in employee_features:
                # Try alternative key formats
                alt_keys = [feature, feature.replace(' ', ''), feature.lower().replace(' ', '_')]
                for alt_key in alt_keys:
                    if alt_key in employee_features:
                        key = alt_key
                        break
            
            input_data.append(employee_features.get(key, 0))
        
        # Make prediction
        input_array = [input_data]
        prediction = model.predict(input_array)[0]
        probability = model.predict_proba(input_array)[0]
        
        return {
            'prediction': 'Yes' if prediction == 1 else 'No',
            'confidence': float(max(probability)),
            'probability_no': float(probability[0]),
            'probability_yes': float(probability[1])
        }
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return None

def main():
    # Load model
    model, feature_names = load_model()
    if not model:
        return
    
    # Load employee data
    try:
        with open('latest_employee_data.json', 'r') as f:
            data = json.load(f)
        
        employee_id = data['employee_id']
        features = data['features']
        
        print(f"\nMaking prediction for Employee ID: {employee_id}")
        print(f"Input features: {features}")
        
        # Make prediction
        result = make_prediction(model, feature_names, features)
        
        if result:
            print(f"\n--- ATTRITION PREDICTION ---")
            print(f"Employee ID: {employee_id}")
            print(f"Prediction: {result['prediction']}")
            print(f"Confidence: {result['confidence']:.3f}")
            print(f"Probability of Attrition: {result['probability_yes']:.3f}")
            print(f"Probability of Retention: {result['probability_no']:.3f}")
            
            # Save results
            with open('prediction_results.json', 'w') as f:
                json.dump({
                    'employee_id': employee_id,
                    'prediction_results': result,
                    'input_features': features
                }, f, indent=2)
            
            print("\nResults saved to 'prediction_results.json'")
        
    except FileNotFoundError:
        print("Error: No employee data found. Run fetch_latest_data.py first.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
