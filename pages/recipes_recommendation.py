import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from scripts.recipes_recommend import recommend_recipes

# Set page config
st.set_page_config(page_title="Recipe Recommendations", layout="wide")

def extract_image_urls(image_str):
    """Extract image URLs from the 'c(\"...\")' format."""
    if isinstance(image_str, str):
        image_urls = re.findall(r'"(https?://[^\s]+)"', image_str)
        return image_urls
    return []

def show_nutrition_chart(recipe):
    """Generate a bar chart for nutritional content."""
    nutrients = {
        "Calories": recipe.get("Calories", 0),
        "Protein": recipe.get("ProteinContent", 0),
        "Fat": recipe.get("FatContent", 0),
        "Carbs": recipe.get("CarbohydrateContent", 0),
        "Saturated Fat": recipe.get("SaturatedFatContent", 0),
        "Cholesterol": recipe.get("CholesterolContent", 0),
        "Sodium": recipe.get("FatContent", 0),
        "Carbs": recipe.get("SodiumContent", 0),
        "Fiber": recipe.get("FiberContent", 0),
        "Sugar": recipe.get("SugarContent", 0)            
    }
                        
    
    fig, ax = plt.subplots()
    ax.bar(nutrients.keys(), nutrients.values(), color=["red", "green", "blue", "orange", "purple"])
    ax.set_ylabel("Amount")
    ax.set_title(f"{recipe['Name']} - Nutrition Breakdown")
    
    # Rotate x-axis labels by 45 degrees
    ax.set_xticklabels(nutrients.keys(), rotation=45, ha="right")

    st.pyplot(fig)

def recipes_recommendation_sidebar():
    """Display recipe recommendations based on user preferences."""
    try:
        st.title(" 🍽️ Discover Your Personalized Recipes")

        if "user_data" not in st.session_state or "selected_foods" not in st.session_state:
            st.warning("Please get food recommendations first!")
            st.image("assets/wellness.jpg", caption="Flavor meets wellness!", use_container_width=True)
            if st.button("Go to Food Recommendations"):
                st.switch_page("pages/food_recommendation.py")
            return
        
        # Load dataset for slider min-max values
        df = pd.read_csv("data/preprocessed/recipes.csv")

        user_data = st.session_state['user_data']
        diet_preference = user_data.get('food_preference', None)
        selected_foods = st.session_state['selected_foods']

        # Nutrient sliders
        user_nutrients = {
            "Calories": st.sidebar.slider('Calories', float(df['Calories'].min()), float(df['Calories'].max()), float(df['Calories'].mean()), step=0.1),
            "FatContent": st.sidebar.slider('Fat', float(df['FatContent'].min()), float(df['FatContent'].max()), float(df['FatContent'].mean()), step=0.1),
            "SaturatedFatContent": st.sidebar.slider('Saturated Fat', float(df['SaturatedFatContent'].min()), float(df['SaturatedFatContent'].max()), float(df['SaturatedFatContent'].mean()), step=0.1),
            "CholesterolContent": st.sidebar.slider('Cholesterol', float(df['CholesterolContent'].min()), float(df['CholesterolContent'].max()), float(df['CholesterolContent'].mean()), step=0.1),
            "SodiumContent": st.sidebar.slider('Sodium', float(df['SodiumContent'].min()), float(df['SodiumContent'].max()), float(df['SodiumContent'].mean()), step=0.1),
            "CarbohydrateContent": st.sidebar.slider('Carbohydrate', float(df['CarbohydrateContent'].min()), float(df['CarbohydrateContent'].max()), float(df['CarbohydrateContent'].mean()), step=0.1),
            "FiberContent": st.sidebar.slider('Fiber', float(df['FiberContent'].min()), float(df['FiberContent'].max()), float(df['FiberContent'].mean()), step=0.1),
            "SugarContent": st.sidebar.slider('Sugar', float(df['SugarContent'].min()), float(df['SugarContent'].max()), float(df['SugarContent'].mean()), step=0.1),
            "ProteinContent": st.sidebar.slider('Protein', float(df['ProteinContent'].min()), float(df['ProteinContent'].max()), float(df['ProteinContent'].mean()), step=0.1),
        }

        if st.sidebar.button("Find Recipes"):
            if not diet_preference or any(value is None for value in user_nutrients.values()):
                st.warning("Please select your dietary preferences and adjust the sliders before proceeding.")
                return

            if not selected_foods:
                st.error("No ingredients found. Please get food recommendations first.")
                return

            st.session_state["recommended_recipes"] = recommend_recipes(user_nutrients, selected_foods, diet_preference)

        # Ensure recipes persist across reruns
        recommended_recipes = st.session_state.get("recommended_recipes", [])
        # Show a reminder message when no recipes are recommended yet
        if not st.session_state.get("recommended_recipes"):
            st.markdown(
                """
                <div style="
                    padding: 10px; 
                    background-color: #ffebcc; 
                    border-radius: 5px;
                    border-left: 5px solid #ff9800;
                    font-size: 18px;
                    font-weight: bold;
                    color: #8a6d3b;">
                    Please select your dietary preference, adjust the sliders, and click <b>'Find Recipes'</b> to get recommendations.
                </div>
                """,
                unsafe_allow_html=True,
            )
            # Display an image below the warning
            st.image("assets/wellness.jpg", caption="Choose your preferences & find the best recipes!", use_container_width=True)

            
            #st.info("ℹ️ Please select your dietary preference - adjust the sliders, and click 'Find Recipes' to see recommendations.")
        else:
            for idx, recipe in enumerate(recommended_recipes):
                with st.expander(f"🍽️ {recipe.get('Name', 'Unknown Recipe')}"):
                    col1, col2 = st.columns([3, 2])

                    with col1:
                        #st.write("**Dietary Category**: " + str(recipe.get('DietaryCategory', 'N/A')))
                        #st.write("**Cook Time**: " + str(recipe.get('CookTime', 'N/A')))
                        st.write("**Recipe Category**: " + str(recipe.get('RecipeCategory', 'N/A')))
                        st.write("**Ingredients**: " + str(recipe.get('RecipeIngredientParts', 'N/A')))
                        #st.write("**Keywords**: " + str(recipe.get('Keywords', 'N/A')))
                        #st.write("**Calories**: " + str(recipe.get('Calories', 'N/A')))
                        #st.write("**Fat Content**: " + str(recipe.get('FatContent', 'N/A')))
                        #st.write("**Saturated Fat**: " + str(recipe.get('SaturatedFatContent', 'N/A')))
                        #st.write("**Cholesterol**: " + str(recipe.get('CholesterolContent', 'N/A')))
                        #st.write("**Sodium**: " + str(recipe.get('SodiumContent', 'N/A')))
                        #st.write("**Carbohydrates**: " + str(recipe.get('CarbohydrateContent', 'N/A')))
                        #st.write("**Fiber**: " + str(recipe.get('FiberContent', 'N/A')))
                        #st.write("**Sugar**: " + str(recipe.get('SugarContent', 'N/A')))
                        #st.write("**Protein**: " + str(recipe.get('ProteinContent', 'N/A')))
                        st.write("**Instructions**: " + str(recipe.get('RecipeInstructions', 'N/A')))

                        # Checkbox for nutrition chart
                        show_chart = st.checkbox(f"📊 View Nutrition Chart for {recipe['Name']}", key=f"chart_{idx}")

                    with col2:
                        if show_chart:
                            show_nutrition_chart(recipe)

        if st.button("← Back to Food Recommendations"):
            st.switch_page("pages/food_recommendation.py")

    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    recipes_recommendation_sidebar()
