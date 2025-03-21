import streamlit as st
import pandas as pd
import re
from sentence_transformers import SentenceTransformer
import torch
from scripts.recipes_recommend import load_data, recommend_recipes

# Set page config
st.set_page_config(page_title="Recipe Recommendations", layout="wide")

def extract_image_urls(image_str):
    """Extract image URLs from the 'c("...")' format."""
    if isinstance(image_str, str):
        # Remove 'c("...")' and split the URLs by '", "'
        image_urls = re.findall(r'"(https?://[^\s]+)"', image_str)
        return image_urls
    return []

def recipes_recommendation_sidebar():
    """Display recipe recommendations based on user preferences."""
    try:
        st.title("Recipe Recommendations")

        # Display default message to remind users to select preferences and sliders
        st.write("### Please select your dietary preferences and adjust the sliders for nutritional values before clicking 'Find Recipes'.")

        # Ensure session state has necessary data
        if "user_data" not in st.session_state or "selected_foods" not in st.session_state:
            st.warning("Please get food recommendations first!")
            if st.button("Go to Food Recommendations"):
                st.switch_page("pages/food_recommendation.py")
            return
        
        # Load dataset for slider min-max values
        df = pd.read_csv("data/preprocessed/recipes.csv")

        # Diet Preference from previous page input
        user_data = st.session_state['user_data']
        st.write(user_data)
        diet_preference = user_data.get('food_preference', None)

        ############ to be deleted
        selected_foods= st.session_state['selected_foods']
        st.write(selected_foods)

        # Nutrient sliders
        user_nutrients = {
            "Calories": st.sidebar.slider('Calories', min_value=float(df['Calories'].min()), max_value=float(df['Calories'].max()), value=float(df['Calories'].mean()), step=0.1),
            "FatContent": st.sidebar.slider('Fat', min_value=float(df['FatContent'].min()), max_value=float(df['FatContent'].max()), value=float(df['FatContent'].mean()), step=0.1),
            "SaturatedFatContent": st.sidebar.slider('Saturated Fat', min_value=float(df['SaturatedFatContent'].min()), max_value=float(df['SaturatedFatContent'].max()), value=float(df['SaturatedFatContent'].mean()), step=0.1),
            "CholesterolContent": st.sidebar.slider('Cholesterol', min_value=float(df['CholesterolContent'].min()), max_value=float(df['CholesterolContent'].max()), value=float(df['CholesterolContent'].mean()), step=0.1),
            "SodiumContent": st.sidebar.slider('Sodium', min_value=float(df['SodiumContent'].min()), max_value=float(df['SodiumContent'].max()), value=float(df['SodiumContent'].mean()), step=0.1),
            "CarbohydrateContent": st.sidebar.slider('Carbohydrate', min_value=float(df['CarbohydrateContent'].min()), max_value=float(df['CarbohydrateContent'].max()), value=float(df['CarbohydrateContent'].mean()), step=0.1),
            "FiberContent": st.sidebar.slider('Fiber', min_value=float(df['FiberContent'].min()), max_value=float(df['FiberContent'].max()), value=float(df['FiberContent'].mean()), step=0.1),
            "SugarContent": st.sidebar.slider('Sugar', min_value=float(df['SugarContent'].min()), max_value=float(df['SugarContent'].max()), value=float(df['SugarContent'].mean()), step=0.1),
            "ProteinContent": st.sidebar.slider('Protein', min_value=float(df['ProteinContent'].min()), max_value=float(df['ProteinContent'].max()), value=float(df['ProteinContent'].mean()), step=0.1),
        }

        # Get user ingredients from session state
        user_ingredients = st.session_state.selected_foods
       
        # Print out the ingredients for debugging purposes
        st.write("### User Ingredients:")
        st.write(user_ingredients)

        # Recommend recipes when button is clicked
        if st.button("Find Recipes"):
            # Ensure user has selected preferences and set slider values
            if not diet_preference or any(value is None for value in user_nutrients.values()):
                st.warning("Please select your dietary preferences and adjust the sliders before proceeding.")
                return

            if not user_ingredients:
                st.error("No ingredients found. Please get food recommendations first.")
                return

            st.write("### Recommended Recipes")
            recommendations = recommend_recipes(user_nutrients, user_ingredients, diet_preference)

            for recipe in recommendations:
                # Display metadata for each recipe
                st.subheader(str(recipe.get('Name', 'Unknown Recipe')))
                st.write("**Dietary Category**: " + str(recipe.get('DietaryCategory', 'N/A')))
                st.write("**Cook Time**: " + str(recipe.get('CookTime', 'N/A')))
                st.write("**Recipe Category**: " + str(recipe.get('RecipeCategory', 'N/A')))
                st.write("**Keywords**: " + str(recipe.get('Keywords', 'N/A')))

                # Clean and format ingredients
                st.write("**Ingredients**: " + recipe.get('RecipeIngredientParts', 'N/A'))
                st.write("**Quantities**: " + recipe.get('RecipeIngredientQuantities', 'N/A'))

                # Numeric values as strings
                st.write("**Calories**: " + str(recipe.get('Calories', 'N/A')))
                st.write("**Fat Content**: " + str(recipe.get('FatContent', 'N/A')))
                st.write("**Saturated Fat**: " + str(recipe.get('SaturatedFatContent', 'N/A')))
                st.write("**Cholesterol**: " + str(recipe.get('CholesterolContent', 'N/A')))
                st.write("**Sodium**: " + str(recipe.get('SodiumContent', 'N/A')))
                st.write("**Carbohydrates**: " + str(recipe.get('CarbohydrateContent', 'N/A')))
                st.write("**Fiber**: " + str(recipe.get('FiberContent', 'N/A')))
                st.write("**Sugar**: " + str(recipe.get('SugarContent', 'N/A')))
                st.write("**Protein**: " + str(recipe.get('ProteinContent', 'N/A')))

                st.write("**Instructions**: " + str(recipe.get('RecipeInstructions', 'N/A')))

                # Handle image URLs
                # image_url = recipe.get('Images', '')
                # if image_url:
                #     # If the image URL is a string and it starts with c("...), we need to split it
                #     if isinstance(image_url, str):
                #         if image_url.startswith('c("'):
                #             image_urls = extract_image_urls(image_url)
                #             for img_url in image_urls:
                #                 if img_url:
                #                     st.image(img_url, use_container_width=True)
                #         elif image_url.startswith("http"):
                #             # If it's a valid URL
                #             st.image(image_url, use_container_width=True)
                #         else:
                #             st.warning("Invalid image URL format.")
                #     elif isinstance(image_url, list):
                #         for img_url in image_url:
                #             if img_url:
                #                 st.image(img_url, use_container_width=True)
                #     else:
                #         st.warning("No valid image found.")
                # else:
                #     st.warning("No image available for this recipe.")

                st.markdown("---")

        # Navigation
        if st.button("← Back to Food Recommendations"):
            st.switch_page("pages/food_recommendation.py")

    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    recipes_recommendation_sidebar()
