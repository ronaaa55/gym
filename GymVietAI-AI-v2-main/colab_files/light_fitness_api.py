from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

def get_exercise_plan(bmi_category, goal):
    plans = {
        "Underweight": {
            "Muscle Building": "Focus on compound exercises: squats, deadlifts, bench press. 3-4 sets of 8-12 reps. Train 3-4 times per week.",
            "Fat Loss": "Light cardio 2-3 times per week, focus on strength training to build muscle.",
            "General Fitness": "Mix of bodyweight exercises and light weights. 2-3 sessions per week."
        },
        "Normal": {
            "Muscle Building": "Progressive overload with compound exercises. 4-5 sets of 6-10 reps. Train 4-5 times per week.",
            "Fat Loss": "HIIT training 3 times per week, strength training 2-3 times per week.",
            "General Fitness": "Balanced mix of cardio and strength training, 3-4 times per week."
        },
        "Overweight": {
            "Muscle Building": "Start with bodyweight exercises, gradually add weights. 3-4 sets of 10-15 reps.",
            "Fat Loss": "Cardio 4-5 times per week, strength training 2-3 times per week.",
            "General Fitness": "Focus on mobility and cardio, gradually add strength training."
        },
        "Obese": {
            "Muscle Building": "Start with walking and bodyweight exercises. Focus on form and consistency.",
            "Fat Loss": "Daily walking, swimming or low-impact cardio. Gradually add resistance training.",
            "General Fitness": "Focus on daily movement, walking, and basic mobility exercises."
        }
    }
    return plans.get(bmi_category, {}).get(goal, "General fitness plan with mixed exercises.")

def get_diet_plan(bmi_category, goal):
    plans = {
        "Underweight": {
            "Muscle Building": "High-calorie, protein-rich diet. Aim for 3000+ calories with 2g protein per kg bodyweight.",
            "Fat Loss": "Focus on nutrient-dense foods while maintaining current calories.",
            "General Fitness": "Balanced diet with slight caloric surplus."
        },
        "Normal": {
            "Muscle Building": "Moderate caloric surplus with high protein intake.",
            "Fat Loss": "Small caloric deficit with high protein to preserve muscle.",
            "General Fitness": "Balanced macronutrients, maintenance calories."
        },
        "Overweight": {
            "Muscle Building": "Slight caloric deficit with high protein intake.",
            "Fat Loss": "Moderate caloric deficit, high protein and fiber.",
            "General Fitness": "Focus on whole foods, moderate portions."
        },
        "Obese": {
            "Muscle Building": "Focus on protein intake while maintaining caloric deficit.",
            "Fat Loss": "Significant caloric deficit with balanced nutrients.",
            "General Fitness": "Focus on whole foods, portion control."
        }
    }
    return plans.get(bmi_category, {}).get(goal, "Balanced diet with whole foods.")

@app.route('/recommend', methods=['POST'])
def get_recommendation():
    try:
        data = request.json
        
        # Extract user data
        weight = float(data['weight'])
        height = float(data['height'])
        gender = data['gender']
        age = int(data['age'])
        goal = data.get('goal', 'General Fitness')
        
        # Calculate BMI
        bmi = calculate_bmi(weight, height)
        bmi_category = get_bmi_category(bmi)
        
        # Get plans
        exercise_plan = get_exercise_plan(bmi_category, goal)
        diet_plan = get_diet_plan(bmi_category, goal)
        
        # Calculate heart rate zones
        max_hr = 220 - age
        
        # Prepare response
        response = {
            'exercise_plan': exercise_plan,
            'diet_plan': diet_plan,
            'bmi': round(bmi, 2),
            'bmi_category': bmi_category,
            'heart_rate_zones': {
                'fat_burning': f"{int(0.6 * max_hr)}-{int(0.7 * max_hr)}",
                'cardio': f"{int(0.7 * max_hr)}-{int(0.8 * max_hr)}",
                'peak': f"{int(0.8 * max_hr)}-{int(0.9 * max_hr)}"
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True) 