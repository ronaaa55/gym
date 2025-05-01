import joblib
import pandas as pd
import numpy as np

class FitnessRecommendationSystem:
    def __init__(self):
        # Load models
        self.exercise_model = joblib.load("models/exercise_plan_model.pkl")
        self.diet_model = joblib.load("models/diet_plan_model.pkl")
        
        # Load encoders
        self.gender_encoder = joblib.load("models/gender_encoder.pkl")
        self.bmi_encoder = joblib.load("models/bmi_encoder.pkl")
    
    def calculate_bmi(self, weight, height):
        """Calculate BMI from weight (kg) and height (cm)"""
        height_m = height / 100
        return weight / (height_m ** 2)
    
    def get_bmi_category(self, bmi):
        """Categorize BMI into different categories"""
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    def calculate_max_heart_rate(self, age):
        """Calculate maximum heart rate"""
        return 220 - age
    
    def get_heart_rate_zones(self, max_hr):
        """Calculate heart rate training zones"""
        return {
            'Zone 1 (Recovery)': (0.5 * max_hr, 0.6 * max_hr),
            'Zone 2 (Endurance)': (0.6 * max_hr, 0.7 * max_hr),
            'Zone 3 (Aerobic)': (0.7 * max_hr, 0.8 * max_hr),
            'Zone 4 (Anaerobic)': (0.8 * max_hr, 0.9 * max_hr),
            'Zone 5 (Max Effort)': (0.9 * max_hr, max_hr)
        }
    
    def get_recommendations(self, weight, height, gender, age, goal="Muscle Building"):
        """Get comprehensive fitness recommendations"""
        # Calculate BMI
        bmi = self.calculate_bmi(weight, height)
        bmi_category = self.get_bmi_category(bmi)
        
        # Calculate heart rate zones
        max_hr = self.calculate_max_heart_rate(age)
        hr_zones = self.get_heart_rate_zones(max_hr)
        
        # Prepare input data
        input_data = pd.DataFrame({
            'Weight': [weight],
            'Height': [height],
            'BMI': [bmi],
            'Gender': [gender],
            'Age': [age],
            'BMIcase': [bmi_category],
            'Goal': [goal]
        })
        
        # Encode categorical variables
        input_data['Gender'] = self.gender_encoder.transform(input_data['Gender'])
        input_data['BMIcase'] = self.bmi_encoder.transform(input_data['BMIcase'])
        
        # Get recommendations
        exercise_plan = self.exercise_model.predict(input_data)[0]
        diet_plan = self.diet_model.predict(input_data)[0]
        
        # Calculate personalized macronutrients based on goal
        if goal == "Muscle Building":
            protein_per_kg = 2.2
            carbs_per_kg = 3.5
            fats_per_kg = 0.8
        elif goal == "Fat Loss":
            protein_per_kg = 2.0
            carbs_per_kg = 2.0
            fats_per_kg = 0.6
        else:  # General Fitness
            protein_per_kg = 1.8
            carbs_per_kg = 2.5
            fats_per_kg = 0.7
        
        return {
            'exercise_plan': exercise_plan,
            'diet_plan': diet_plan,
            'bmi': round(bmi, 2),
            'bmi_category': bmi_category,
            'macronutrients': {
                'protein': round(weight * protein_per_kg, 1),
                'carbs': round(weight * carbs_per_kg, 1),
                'fats': round(weight * fats_per_kg, 1)
            },
            'heart_rate_zones': hr_zones,
            'progress_tracking': {
                'weekly_measurements': ['Weight', 'Waist', 'Hips', 'Chest', 'Arms', 'Thighs'],
                'monthly_photos': True,
                'strength_log': True,
                'body_composition': 'Every 4 weeks'
            }
        }

def get_user_input():
    """Get user input for fitness recommendations"""
    print("\nWelcome to the Fitness Recommendation System!")
    print("Please enter your details:")
    
    while True:
        try:
            weight = float(input("Weight (kg): "))
            if weight <= 0:
                print("Weight must be positive. Please try again.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    while True:
        try:
            height = float(input("Height (cm): "))
            if height <= 0:
                print("Height must be positive. Please try again.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    while True:
        gender = input("Gender (Male/Female): ").capitalize()
        if gender not in ["Male", "Female"]:
            print("Please enter either 'Male' or 'Female'.")
            continue
        break
    
    while True:
        try:
            age = int(input("Age: "))
            if age <= 0 or age > 120:
                print("Please enter a valid age.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    while True:
        goal = input("Goal (Muscle Building/Fat Loss/General Fitness): ").title()
        if goal not in ["Muscle Building", "Fat Loss", "General Fitness"]:
            print("Please enter a valid goal.")
            continue
        break
    
    return {
        'weight': weight,
        'height': height,
        'gender': gender,
        'age': age,
        'goal': goal
    }

# Main program
if __name__ == "__main__":
    # Initialize the recommendation system
    recommender = FitnessRecommendationSystem()
    
    # Get user input
    user_data = get_user_input()
    
    # Get recommendations
    recommendations = recommender.get_recommendations(
        user_data['weight'],
        user_data['height'],
        user_data['gender'],
        user_data['age'],
        user_data['goal']
    )
    
    # Print recommendations
    print("\nFitness Recommendations:")
    print(f"BMI: {recommendations['bmi']} ({recommendations['bmi_category']})")
    print(f"Goal: {user_data['goal']}")
    
    print("\nExercise Plan:")
    print(recommendations['exercise_plan'])
    
    print("\nDiet Plan:")
    print(recommendations['diet_plan'])
    
    print("\nDaily Macronutrient Targets:")
    print(f"Protein: {recommendations['macronutrients']['protein']}g")
    print(f"Carbohydrates: {recommendations['macronutrients']['carbs']}g")
    print(f"Fats: {recommendations['macronutrients']['fats']}g")
    
    print("\nHeart Rate Training Zones:")
    for zone, (min_hr, max_hr) in recommendations['heart_rate_zones'].items():
        print(f"{zone}: {int(min_hr)}-{int(max_hr)} BPM")
    
    print("\nProgress Tracking:")
    print("Weekly Measurements:", ", ".join(recommendations['progress_tracking']['weekly_measurements']))
    print("Monthly Progress Photos: Yes")
    print("Strength Log: Yes")
    print("Body Composition Assessment:", recommendations['progress_tracking']['body_composition']) 