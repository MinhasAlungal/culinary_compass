import pandas as pd
import streamlit as st
from datetime import date
import requests

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
                    food_name = food['food_name']
                    nutrients = food['nutrients']
            
                    # Format nutrient values as a comma-separated string
                    nutrient_str = ", ".join([f"{key}: {value}" for key, value in nutrients.items()])
            
                    # Append food name with its nutrients
                    recommendation_str += f"  - {food_name} ({nutrient_str})\n"
                    #recommendation_str += f"  - {food}\n"
                    
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
    
    # Clear session state when the page is loaded
    if 'user_data' not in st.session_state:
        st.session_state['user_data'] = None
    if 'recommendation' not in st.session_state:
        st.session_state['recommendation'] = None
    if 'selected_foods' not in st.session_state:
        st.session_state['selected_foods'] = set()
    if 'previous_preference' not in st.session_state:
        st.session_state['previous_preference'] = None
    if 'previous_deficiencies' not in st.session_state:
        st.session_state['previous_deficiencies'] = []

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

    # Get current food preference selection
    food_preference = st.sidebar.selectbox("Diet Preference:", categories)
    
    # Check if food preference changed
    if food_preference != st.session_state['previous_preference']:
        # Clear session state values
        st.session_state['user_data'] = None
        st.session_state['recommendation'] = None
        st.session_state['selected_foods'] = set()
        # Update the previous preference
        st.session_state['previous_preference'] = food_preference
        # Force a rerun to update the UI
        st.rerun()

    st.sidebar.write("Select Deficiencies:")
    cols = st.sidebar.columns(2)
    
    # Check if any deficiency checkbox was clicked
    any_deficiency_clicked = False
    selected_deficiencies = []
    
    # Handle deficiency selection and detect changes
    for i, d in enumerate(deficiencies):
        # Create checkbox in appropriate column
        was_selected = d in st.session_state.get('previous_deficiencies', [])
        is_selected = cols[i % 2].checkbox(d, key=f"def_{d}", value=was_selected)
        
        # Check if this deficiency's state changed
        if is_selected != was_selected:
            any_deficiency_clicked = True
        
        # Add to selected deficiencies if checked
        if is_selected:
            selected_deficiencies.append(d)
    
    # Clear session state if any deficiency was clicked
    if any_deficiency_clicked:
        # Store current deficiency selection before clearing
        st.session_state['previous_deficiencies'] = selected_deficiencies
        
        # Clear other session state values
        st.session_state['user_data'] = None
        st.session_state['recommendation'] = None
        st.session_state['selected_foods'] = set()
        
        # Force a rerun to update the UI
        st.rerun()

    if st.sidebar.button("Get Recommendation"):
        if not name:
            st.warning("Please enter your name before proceeding.")
            return

        # Clear session state when the "Get Recommendation" button is clicked
        clear_session()

        bmi, bmi_category = calculate_bmi(weight, height)
        recommendation = get_recommendation(food_preference, selected_deficiencies)

        # Save user data and recommendation to session state
        st.session_state['user_data'] = {
            "name": name,
            "age": age,
            "gender": gender,
            "weight": weight,
            "height": height,
            "bmi": bmi,
            "bmi_category": bmi_category,
            "food_preference": food_preference,
            "deficiencies": selected_deficiencies
        }
        st.session_state['recommendation'] = recommendation

        # Save to API
        save_to_api(st.session_state['user_data'], recommendation)

    # Display User Info and Recommendations if available
    if st.session_state['user_data']:
        user_data = st.session_state['user_data']
        st.subheader(f"Hello, {user_data['name']}!")
        st.write(f"**Age:** {user_data['age']}  |  **Gender:** {user_data['gender']}")
        st.write(f"**BMI:** {user_data['bmi']}  |  **Category:** {user_data['bmi_category']}")

        if user_data['deficiencies']:
            st.write(f"**Selected Deficiencies:** {', '.join(user_data['deficiencies'])}")


        if st.session_state['recommendation']:
            st.subheader("Here's your food recommendation:")
            for category in st.session_state['recommendation']:
                st.markdown(f"### {category['main_category']}")  # Main category as header
                for sub_cat in category['sub_categories']:
                    with st.expander(f"**{sub_cat['name']}** ({len(sub_cat['foods'])} items)"):
                    # Split into two columns    
                        col1, col2 = st.columns(2)
                        unique_foods = list(set(food["food_name"] for food in sub_cat["foods"]))

                        # Display food items with nutrients and checkbox in the same loop
                        for i, food_name in enumerate(unique_foods):
                            col = col1 if i % 2 == 0 else col2  

                        # Now display the food name and its nutrients
                            for food in sub_cat["foods"]:
                                if food["food_name"] == food_name:
                                    nutrient_values = food["nutrients"]
                                    nutrient_str = ", ".join([f"{nutrient}: {value}" for nutrient, value in nutrient_values.items()])
                                    # Display food name and nutrients **before the checkbox**
                                    #st.write(f"**{food_name}:** {nutrient_str}")

                        # Display checkbox for selecting food
                            selected = col.checkbox(food_name + ' ' + nutrient_str,key=f"food_{food_name}", value=food_name in st.session_state["selected_foods"])

                    # Update session state based on user selection
                            if selected:
                                st.session_state["selected_foods"].add(food_name)
                            else:
                                st.session_state["selected_foods"].discard(food_name)

        
                            
            # Show selected foods
            st.subheader("Your Selected Foods:")
            if st.session_state["selected_foods"]:
                st.write(", ".join(st.session_state["selected_foods"]))
            else:
                st.write("No foods selected yet.")

        # Navigation to recipe selection
        if st.session_state["selected_foods"]:
            st.page_link("pages/recipes_recommendation.py", label="Select Recipes For These Foods :arrow_right:")

    # Footer
    st.markdown("---")
    st.caption(f"Food Recommendation System | {date.today().year}")

def clear_session():
    st.session_state['user_data'] = None
    st.session_state['recommendation'] = None
    st.session_state['selected_foods'] = set()

if __name__ == "__main__":
    main()