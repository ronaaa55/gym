from flask import Flask, request, jsonify
import pandas as pd
import joblib
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load models and encoders
exercise_model = joblib.load('models/exercise_plan_model.pkl')
diet_model = joblib.load('models/diet_plan_model.pkl')
gender_encoder = joblib.load('models/gender_encoder.pkl')
bmi_encoder = joblib.load('models/bmi_encoder.pkl')

def calculate_bmi(weight, height):
    height_m = height / 100
    bmi = weight / (height_m * height_m)
    return bmi

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

@app.route('/recommend', methods=['POST'])
def get_recommendation():
    try:
        data = request.json
        
        # Extract user data
        weight = float(data['weight'])
        height = float(data['height'])
        gender = data['gender']
        age = int(data['age'])
        goal = data['goal']
        
        # Calculate BMI
        bmi = calculate_bmi(weight, height)
        bmi_category = get_bmi_category(bmi)
        
        # Prepare input data
        input_data = pd.DataFrame({
            'Weight': [weight],
            'Height': [height],
            'BMI': [bmi],
            'Gender': [gender],
            'Age': [age],
            'BMIcase': [bmi_category]
        })
        
        # Encode categorical variables
        input_data['Gender'] = gender_encoder.transform(input_data['Gender'])
        input_data['BMIcase'] = bmi_encoder.transform(input_data['BMIcase'])
        
        # Get predictions
        exercise_plan = exercise_model.predict(input_data)[0]
        diet_plan = diet_model.predict(input_data)[0]
        
        # Prepare response
        response = {
            'exercise_plan': exercise_plan,
            'diet_plan': diet_plan,
            'bmi': round(bmi, 2),
            'bmi_category': bmi_category,
            'heart_rate_zones': {
                'fat_burning': f"{int(0.6 * (220 - age))}-{int(0.7 * (220 - age))}",
                'cardio': f"{int(0.7 * (220 - age))}-{int(0.8 * (220 - age))}",
                'peak': f"{int(0.8 * (220 - age))}-{int(0.9 * (220 - age))}"
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True) 