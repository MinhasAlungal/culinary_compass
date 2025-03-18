import pandas as pd
import streamlit as st
from datetime import date
import requests
import os
from scripts.food_recommend import recommend_food
import json

API_BASE_URL = "http://127.0.0.1:8000"
SAVE_HISTORY_URL = f"{API_BASE_URL}/save-history/"
GET_RECOMMENDATION_URL = f"{API_BASE_URL}/get-recommendation/"

def load_data():
    """Load processed food data and extract unique categories."""
    df = pd.read_csv("data/preprocessed/food.csv")
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
        response = requests.get(
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

def save_to_session(user_data: dict, recommendation: list):
    """Save user data and recommendations to session state."""
    try:
        # Save user data and recommendations to session state
        st.session_state['user_data'] = user_data
        st.session_state['recommended_foods'] = recommendation
        print("Successfully saved to session state:", st.session_state)
    except Exception as e:
        print(f"Error saving to session state: {str(e)}")
        st.error("Failed to save data to session. Please try again.")

def save_to_api(user_data: dict, recommendation: list):
    """Save user data and recommendations to API."""
    try:
        # Convert recommendation list to formatted string
        recommendation_str = ""
        for main_cat in recommendation:
            recommendation_str += f"\n{main_cat['main_category']}\n"
            for sub_cat in main_cat['sub_categories']:
                recommendation_str += f"{sub_cat['name']}\n"
                for food in sub_cat['foods']:
                    recommendation_str += f"  - {food}\n"
        
        # Prepare data to match UserHistory model
        history_data = {
            "name": str(user_data['name']),
            "age": int(user_data['age']),
            "gender": str(user_data['gender']),
            "height": float(user_data['height']),
            "weight": float(user_data['weight']),
            "bmi": float(user_data['bmi']),
            "bmi_category": str(user_data['bmi_category']),
            "food_preference": str(user_data['food_preference']),
            "deficiencies": list(user_data['deficiencies']),
            "recommendations": recommendation_str
        }
        
        # Make API call to save history
        response = requests.post(SAVE_HISTORY_URL, json=history_data)
        if response.status_code == 200:
            print("History saved successfully!")
        else:
            print(f"Failed to save history. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            st.error("Failed to save history.")
            
    except Exception as e:
        print(f"Error saving to API: {str(e)}")
        st.error("Failed to save data to API. Please try again.")

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

        # Display User Info
        st.subheader(f"Hello, {name}! Here's your food recommendation:")
        st.write(f"**Age:** {age}  |  **Gender:** {gender}")
        st.write(f"**BMI:** {bmi}  |  **Category:** {bmi_category}")

        if selected_deficiencies:
            st.write(f"**Selected Deficiencies:** {', '.join(selected_deficiencies)}")

        if recommendation:
            st.subheader("Recommended Foods:")
            
            # Show full JSON (collapsible) response from API -- for debugging
            with st.expander("View Raw JSON Response"):
                st.json(recommendation)

            # Display in a structured way for the user
            for category in recommendation:
                st.markdown(f"### {category['main_category']}")  # Main category as header
                for sub_cat in category['sub_categories']:
                    with st.expander(f"**{sub_cat['name']}** ({len(sub_cat['foods'])} items)"):
                        st.write(", ".join(sub_cat["foods"]))

        else:
            st.error("No recommendations found. Try selecting different preferences or deficiencies.")

        # Save user history
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

        # Save to user log file
        save_to_api(user_data, recommendation)

        # Save to session state
        save_to_session(user_data, recommendation)

        # Navigation to recipe selection
        if st.button("Select Recipes for These Foods"):
            st.page_link("pages/recipe_recommendation.py", label="Go to recipe recommendation")

    # Footer
    st.markdown("---")
    st.caption(f"Food Recommendation System | {date.today().year}")

if __name__ == "__main__":
    main()
