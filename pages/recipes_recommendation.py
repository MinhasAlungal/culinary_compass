import streamlit as st
import pandas as pd

# Set page config must be the first Streamlit command
st.set_page_config(page_title="Recipe Recommendations", layout="wide")

def recipes_recommendation_sidebar():
    """Display recipe recommendations based on user preferences."""
    try:
        st.title("Recipe Recommendations")
        
        # Initialize session state if not already done
        if "user_data" not in st.session_state:
            st.session_state.user_data = {}
        if "recommended_foods" not in st.session_state:
            st.session_state.recommended_foods = []
        
        # Load the dataset for sliders
        df = pd.read_csv("data/preprocessed/recipes.csv")
        
        # Recipe preferences in sidebar
        st.sidebar.write('Select Preferences')
        calories = st.sidebar.slider('Calories', 
                                   min_value=df['Calories'].min(), 
                                   max_value=df['Calories'].max())
        fat = st.sidebar.slider('Fat', 
                              min_value=df['FatContent'].min(), 
                              max_value=df['FatContent'].max())
        saturated_fat = st.sidebar.slider('Saturated Fat',
                                        min_value=df['SaturatedFatContent'].min(),
                                        max_value=df['SaturatedFatContent'].max())
        cholesterol = st.sidebar.slider('Cholesterol',
                                      min_value=df['CholesterolContent'].min(),
                                      max_value=df['CholesterolContent'].max())
        sodium = st.sidebar.slider('Sodium',
                                 min_value=df['SodiumContent'].min(),
                                 max_value=df['SodiumContent'].max())
        carbohydrate = st.sidebar.slider('Carbohydrate',
                                       min_value=df['CarbohydrateContent'].min(),
                                       max_value=df['CarbohydrateContent'].max())
        fiber = st.sidebar.slider('Fiber',
                                min_value=df['FiberContent'].min(),
                                max_value=df['FiberContent'].max())
        sugar = st.sidebar.slider('Sugar',
                                min_value=df['SugarContent'].min(),
                                max_value=df['SugarContent'].max())
        protein = st.sidebar.slider('Protein',
                                  min_value=df['ProteinContent'].min(),
                                  max_value=df['ProteinContent'].max())

        # Check if we have valid user data in session state
        if not st.session_state.user_data or not st.session_state.recommended_foods:
            print("Missing session state data")
            print("user_data in session:", bool(st.session_state.user_data))
            print("recommended_foods in session:", bool(st.session_state.recommended_foods))
            st.warning("Please get food recommendations first!")
            if st.button("Go to Food Recommendations"):
                st.switch_page("pages/food_recommendation.py")
            return

        # Display user data
        st.subheader("Your Profile")
        user_data = st.session_state.user_data
        st.write(f"**Name:** {user_data.get('name', 'Not provided')}")
        st.write(f"**BMI:** {user_data.get('bmi', 'Not provided')} ({user_data.get('bmi_category', 'Not provided')})")
        st.write(f"**Diet Preference:** {user_data.get('food_preference', 'Not provided')}")
        if user_data.get('deficiencies'):
            st.write(f"**Deficiencies:** {', '.join(user_data['deficiencies'])}")

        # Display recommended foods
        st.subheader("Recommended Foods")
        recommended_foods = st.session_state.recommended_foods
        
        # Display each main category and its foods
        for main_cat in recommended_foods:
            st.header(f"📍 {main_cat['main_category']}")
            
            for sub_cat in main_cat['sub_categories']:
                with st.expander(f"🔹 {sub_cat['name']} ({len(sub_cat['foods'])} items)"):
                    for food in sub_cat['foods']:
                        st.markdown(f"• {food}")
                st.markdown("---")

        # Navigation
        if st.button("← Back to Food Recommendations"):
            st.switch_page("pages/food_recommendation.py")

    except Exception as e:
        print(f"Error in recipes_recommendation_sidebar: {str(e)}")
        st.error("An unexpected error occurred. Please try again.")

if __name__ == "__main__":
    recipes_recommendation_sidebar()