import pandas as pd
import streamlit as st
from datetime import date
import requests
import os
from scripts.recommend import recommend_food

API_BASE_URL = "http://127.0.0.1:8000"
SAVE_HISTORY_URL = f"{API_BASE_URL}/save-history/"
GET_RECOMMENDATION_URL = f"{API_BASE_URL}/get-recommendation/"

@st.cache_data
def load_data():
    """Load processed food data and extract unique categories."""
    df = pd.read_csv("data/processed_food_data.csv")
    categories = df["main_category"].unique().tolist()
    deficiencies = [
        'calcium', 'potassium', 'zinc', 'vitamin_C', 'iron', 'magnesium', 
        'phosphorus', 'sodium', 'copper', 'vitamin_E', 'thiamin', 'riboflavin', 
        'cholesterol', 'Niacin', 'vitamin_B_6', 'choline_total', 'vitamin_A', 
        'vitamin_K', 'folate_total', 'vitamin_B_12', 'selenium', 'vitamin_D'
    ]
    return df, categories, deficiencies

def calculate_bmi(weight, height):
    """Calculate and categorize BMI."""
    bmi = round(weight / (height ** 2), 2)
    if bmi < 18.5:
        category = "Underweight - Increase nutrient-dense meals."
    elif 18.5 <= bmi < 24.9:
        category = "Normal weight - Maintain a balanced diet and exercise."
    elif 25 <= bmi < 29.9:
        category = "Overweight - Focus on portion control and active lifestyle."
    else:
        category = "Obese - Consider a structured diet and exercise plan."
    return bmi, category

def get_recommendation(preference, deficiencies):
    try:
        response = requests.post(
            GET_RECOMMENDATION_URL,
            json={"food_preference": preference, "deficiencies": deficiencies},
            timeout=5
        )
        if response.status_code == 200:
            return response.json()["recommendation"]
        else:
            st.error(f"API Error: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"API Connection Error: {str(e)}")
        return None

def save_to_api(user_data):
    """Send user data to API and return success status."""
    try:
        response = requests.post(SAVE_HISTORY_URL, json=user_data, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return False

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="Food Recommendation System", layout="wide")
    st.title("Food Recommendation System")
    
    # Load Data
    df, categories, deficiencies = load_data()

    # Sidebar Input
    st.sidebar.header("User Information")
    name = st.sidebar.text_input("Enter your name:")
    age = st.sidebar.number_input("Age:", min_value=1, value=25)
    gender = st.sidebar.radio("Gender:", ("Male", "Female", "Other"))
    
    col1, col2 = st.sidebar.columns(2)
    weight = col1.number_input("Weight (kg):", min_value=1.0, value=50.0)
    height = col2.number_input("Height (m):", min_value=0.5, max_value=2.5, value=1.50)
    
    food_preference = st.sidebar.selectbox("Diet Preference:", categories)
    
    st.sidebar.write("Select Deficiencies:")
    cols = st.sidebar.columns(2)
    selected_deficiencies = [d for i, d in enumerate(deficiencies) if cols[i % 2].checkbox(d, key=f"def_{d}")]
    
    if st.sidebar.button("Get Recommendation"):
        if not name:
            st.warning("Please enter your name before proceeding.")
            return
        
        bmi, bmi_category = calculate_bmi(weight, height)
        recommendation = get_recommendation(food_preference, selected_deficiencies)
        
        # Display Results
        st.subheader(f"Hello, {name}! Here's your food recommendation:")
        st.write(f"**Age:** {age}  |  **Gender:** {gender}")
        st.write(f"**BMI:** {bmi}  |  **Category:** {bmi_category}")
        
        if selected_deficiencies:
            st.write(f"**Selected Deficiencies:** {', '.join(selected_deficiencies)}")
        
        st.success(recommendation)

        # Save to API
        user_data = {
            "name": name,
            "age": age,
            "gender": gender,
            "weight": weight,
            "height": height,
            "bmi": bmi,
            "bmi_category": bmi_category,
            "food_preference": food_preference,
            "deficiencies": selected_deficiencies,
            "recommendation": recommendation
        }
        
        if save_to_api(user_data):
            print("User history saved successfully!")
        else:
            print("Failed to save history.")

    # Footer
    st.markdown("---")
    st.caption(f"Food Recommendation System | {date.today().year}")

if __name__ == "__main__":
    main()
