import pandas as pd
import streamlit as st
from datetime import date
from scripts.recommend import recommend_food
import requests
from api import UserHistory


def calculate_bmi(weight, height):
    """Calculate BMI from weight (kg) and height (m)."""
    return round(weight / (height ** 2), 2)

def get_bmi_category(bmi):
    """Categorize BMI into different health categories."""
    if bmi < 18.5:
        return "Underweight - Increase nutrient-dense meals."
    elif 18.5 <= bmi < 24.9:
        return "Normal weight - Maintain a balanced diet and exercise."
    elif 25 <= bmi < 29.9:
        return "Overweight - Focus on portion control and active lifestyle."
    else:
        return "Obese - Consider a structured diet and exercise plan."

def get_food_recommendation(preference, deficiencies):
    """Fetch food recommendations based on diet preference and deficiencies."""
    return recommend_food(deficiencies if deficiencies else 'none', category=preference)

@st.cache_data
def load_data():
    """Load processed food data and extract unique categories."""
    df = pd.read_csv("data/processed_food_data.csv")
    return df, df["main_category"].unique()

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="Food Recommendation System", layout="wide")
    st.title("Food Recommendation System")
    st.sidebar.header("User Information")
    
    # Load data
    df, unique_categories = load_data()
    unique_deficiencies = ['calcium', 'potassium', 'zinc', 'vitamin_C', 'iron', 'magnesium', 'phosphorus', 'sodium', 'copper',
                           'vitamin_E', 'thiamin', 'riboflavin', 'cholesterol', 'Niacin', 'vitamin_B_6', 'choline_total',
                           'vitamin_A', 'vitamin_K', 'folate_total', 'vitamin_B_12', 'selenium', 'vitamin_D']
    
    # User Inputs
    name = st.sidebar.text_input("Enter your name:")
    age = st.sidebar.number_input("Age:", min_value=1, value=25)
    gender = st.sidebar.radio("Gender:", ("Male", "Female", "Other"))
    
    col1, col2 = st.sidebar.columns(2)
    weight = col1.number_input("Weight (kg):", min_value=1.0, value=50.0)
    height = col2.number_input("Height (m):", min_value=0.5, max_value=2.5, value=1.50)
    
    food_preference = st.sidebar.selectbox("Diet Preference:", unique_categories)
    
    st.sidebar.write("Select Deficiencies:")
    cols = st.sidebar.columns(2)
    selected_deficiencies = [d for i, d in enumerate(unique_deficiencies) if cols[i % 2].checkbox(d, key=f"deficiency_{d}")]
    
    # Recommendation Button
    if st.sidebar.button("Get Recommendation"):
        bmi = calculate_bmi(weight, height)
        bmi_category = get_bmi_category(bmi)
        recommendation = get_food_recommendation(food_preference, selected_deficiencies)
        
        # Display Results
        st.subheader(f"Hello, {name}! Here's your food recommendation:")
        st.write(f"**Age:** {age}  |  **Gender:** {gender}")
        st.write(f"**BMI:** {bmi}  |  **Category:** {bmi_category}")
        
        # Display BMI chart 
        # st.image("assets/bmi_chart.gif", caption="BMI Categories", use_container_width=True) 
        # need to check why the file is not loading
        
        if selected_deficiencies:
            st.write(f"**Selected Deficiencies:** {', '.join(selected_deficiencies)}")
        st.success(recommendation)
        
        # Save recommendation to history
        api_url = "http://127.0.0.1:8000/save-history/"
        user_history = UserHistory (
            name=name,
            age=age,
            gender=gender,
            weight=weight,
            height=height,
            bmi=bmi,
            bmi_category=bmi_category,
            food_preference=food_preference,
            deficiencies=selected_deficiencies,
            recommendation=recommendation
        )

        response = requests.post(api_url, json=user_history.model_dump())

        if response.status_code == 200:
            print("User history saved successfully!")
        else:
            print("Failed to save history.")

        
    # Footer
    st.markdown("---")
    st.caption(f"Food Recommendation System | {date.today().year}")

if __name__ == "__main__":
    main()
