import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from scripts.recipes_recommend import recommend_recipes

# Set page config
st.set_page_config(page_title="Recipe Recommendations", layout="wide")

# Add this CSS for the page header
st.markdown("""
    <style>
        .main > div:first-child {
            padding-top: 0.5rem !important;
        }
        .block-container {
            padding-top: 1.25rem !important;
            padding-bottom: 0 !important;
            margin-top: 0 !important;
        }
        h1 {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        /* Style for the header container */
        .header-container {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 1rem;
            margin: 0;
            
        }
        /* Style for the header icon */
        .header-icon {
            font-size: 2rem;
            margin-right: 0.5rem;
        }   
    </style>
""", unsafe_allow_html=True)

def extract_image_urls(image_str):
    """Extract image URLs from the 'c(\"...\")' format."""
    if isinstance(image_str, str):
        image_urls = re.findall(r'"(https?://[^\s]+)"', image_str)
        return image_urls
    return []

def show_nutrition_pie_chart(recipe):
    """Generate a visually appealing pie chart for nutrient content with custom styling."""
    
    nutrients = {
        "Protein (g)": recipe.get("ProteinContent", 0),
        "Fat (g)": recipe.get("FatContent", 0),
        "Carbs (g)": recipe.get("CarbohydrateContent", 0),
        "Saturated Fat (g)": recipe.get("SaturatedFatContent", 0),
        "Cholesterol (mg)": recipe.get("CholesterolContent", 0),
        "Sodium (mg)": recipe.get("SodiumContent", 0),
        "Fiber (g)": recipe.get("FiberContent", 0),
        "Sugar (g)": recipe.get("SugarContent", 0),
    }

    # Filter out nutrients with zero values
    nutrients = {k: v for k, v in nutrients.items() if v > 0}

    if not nutrients:
        st.write("No nutritional data available to generate pie chart.")
        return

    labels = list(nutrients.keys())
    values = list(nutrients.values())

    # Modern color palette with complementary colors
    colors = ["#4A90E2",    # Blue
             "#50C878",     # Emerald
             "#FF7E79",     # Coral
             "#9B59B6",     # Purple
             "#F4D03F",     # Yellow
             "#E67E22",     # Orange
             "#2ECC71",     # Green
             "#E74C3C"]     # Red

    # Create figure with custom styling
    plt.style.use('default')  # Using default style instead of seaborn
    fig, ax = plt.subplots(figsize=(8, 6), facecolor='white')
    
    # Create pie chart with custom settings
    wedges, texts, autotexts = ax.pie(
        values,
        colors=colors[:len(values)],
        autopct=lambda pct: f'{pct:.1f}%' if pct > 5 else '',  # Only show percentage if > 5%
        pctdistance=0.75,
        startangle=90,
        wedgeprops={
            'width': 0.7,             # Create a donut chart effect
            'edgecolor': 'white',     # White edges between segments
            'linewidth': 2            # Edge thickness
        }
    )

    # Enhance text properties
    plt.setp(autotexts, size=15, weight="bold", color="white")
    
    # Create a circular chart
    ax.axis('equal')

    # Add title with custom styling
    ax.set_title(
        label=f"{recipe.get('Name', 'Recipe')}\nNutrient Distribution",
        pad=20,
        fontsize=20,
        fontweight='bold'
    )

    # Add legend with custom styling
    legend = ax.legend(
        wedges,
        labels,
        title="Nutrients",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=14,
        title_fontsize=15,
        frameon=True,
        edgecolor='white'
    )
    legend.get_frame().set_alpha(0.9)

    # Adjust layout to prevent legend cutoff
    plt.tight_layout()
    
    # Display the chart
    st.pyplot(fig)

def format_recipe_instructions(instructions_str):
    """Format recipe instructions into clean, readable steps."""
    if not isinstance(instructions_str, str):
        return None
        
    # Clean up the string
    instructions = (instructions_str
                   .replace('c(', '')
                   .replace(')"', '')
                   .replace('"', '')
                   .strip())
    
    # Split into steps and clean each step
    steps = []
    for step in instructions.split('.,'):  # Split on period-comma combination
        # Clean the step text
        step = step.strip()
        # Remove any leading/trailing periods
        step = step.strip('.')
        # Add back the period if it doesn't end with one
        if not step.endswith('.'):
            step += '.'
        if step:  # Only add non-empty steps
            steps.append(step)
    
    return steps

def display_recipe_instructions(instructions):
    """Display recipe instructions with beautiful formatting in a scrollable container."""
    st.markdown("""
        <style>
        /* Step styling */
        .recipe-step {
            display: flex;
            align-items: flex-start;
            margin-bottom: 5px;
            padding: 0.5rem;
            background-color: #f8f9fa;
            border-radius: 0.25rem;
            border-left: 2px solid #28a745;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }
        .recipe-step:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        /* Number and text styling */
        .step-number {
            font-weight: 600;
            font-size: 1rem;
            margin-right: 0.5rem;
            color: #262730;
            min-width: 0.75;
        }
        .step-text {
            color: #262730;
            flex: 1;
            line-height: 1.5;
            font-size: 0.9em;
            font-weight: 500;
        }
        
        /* Header styling */
        .instruction-header {
            color: #2c3e50;
            font-size: 1.3em;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 10px;
        }
        /* Container styling */
        .recipe-steps-container {
            max-height: 250px;
            overflow-y: auto;
            border: 1px solid #f0f2f6;
            border-radius: 0.5rem;
            padding: 8px;
            background-color: white;
            scrollbar-width: thin;
        }
        
        /* Scrollbar styling */
        .recipe-steps-container::-webkit-scrollbar {
            width: 6px;
            background-color: #f0f2f6;
        }
        .recipe-steps-container::-webkit-scrollbar-thumb {
            background-color: #ccc;
            border-radius: 3px;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<div class="instruction-header">📝 Cooking Instructions</div>', unsafe_allow_html=True)

    steps = format_recipe_instructions(instructions)
    if not steps:
        st.write("No instructions available.")
        return

    # Create a single HTML string for all steps with compact formatting
    steps_html = '<div class="recipe-steps-container">'
    for i, step in enumerate(steps, 1):
        if step:  # Only add non-empty steps
            steps_html += f'<div class="recipe-step"><span class="step-number">{i}.</span><span class="step-text">{step}</span></div>'
    steps_html += '</div>'

    # Display all steps at once in the container
    st.markdown(steps_html, unsafe_allow_html=True)

def format_recipe_ingredients(ingredients_str):
    """Format recipe ingredients into a clean list."""
    if not isinstance(ingredients_str, str):
        return None
        
    # Clean up the string
    ingredients = (ingredients_str
                  .replace('c(', '')
                  .replace(')"', '')
                  .replace('("', '')
                  .replace('"', '')
                  .strip())
    
    # Split and clean ingredients
    return [ing.strip().capitalize() for ing in ingredients.split(',') if ing.strip()]

def display_recipe_ingredients(ingredients):
    """Display recipe ingredients with compact capsule-shaped formatting."""
    st.markdown("""
        <style>
        .ingredients-section {
            background-color: #ffffff;
            padding: 5px;
            border-radius: 5px;
        }
        .ingredients-header {
            color: #2c3e50;
            font-size: 1.3em;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .ingredient-item {
            display: inline-flex;
            align-items: center;
            padding: 5px 7px;
            background-color: #ffebee;
            border-radius: 30px;
            font-size: 0.9em;
            font-weight: 500;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            transition: all 0.2s ease-in-out;
            white-space: nowrap;
        }
        .ingredient-item:hover {
            background-color: #ffcdd2;
            transform: scale(1.02);
        }
        .ingredient-icon {
            margin-right: 6px;
            font-size: 1em;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div class="ingredients-section">
            <div class="ingredients-header">
                🧂 Ingredients
            </div>
            <div class="ingredients-grid">
    """, unsafe_allow_html=True)

    ingredients_list = format_recipe_ingredients(ingredients)
    if not ingredients_list:
        st.write("No ingredients available.")
        return

    # Create compact capsule-style ingredient items displayed side by side
    capsules = "".join(f"""
        <span class="ingredient-item">
            <span class="ingredient-icon">•</span>
            {ingredient}
        </span>
    """ for ingredient in ingredients_list)
    
    st.markdown(capsules, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def display_selected_foods(selected_foods):
    """
    Display selected foods in styled capsules within a scrollable container
    """
    st.markdown("""
        <style>
            .selected-foods-container {
                max-height: 200px;
                overflow-y: auto;
                border: 1px solid #f0f2f6;
                border-radius: 0.5rem;
                padding: 0.5rem;
                background-color: white;
                margin: 0.3rem 0;
                scrollbar-width: thin;
                display: flex;
                flex-wrap: wrap;
                gap: 0.5rem;
            }
            .selected-foods-container::-webkit-scrollbar {
                width: 6px;
                background-color: #f0f2f6;
            }
            .selected-foods-container::-webkit-scrollbar-thumb {
                background-color: #ccc;
                border-radius: 3px;
            }
            .selected-foods-header {
                display: flex;
                font-size: 1rem;
                font-weight: 600;
                font-size: 1.3em;
                font-weight: bold;
                color: #262730;
            }
            .food-capsule {
                display: inline-flex;
                align-items: center;
                font-size: 0.85rem;
                color: #262730;
                background-color: #d7ccc8;
                border-radius: 1rem;
                padding: 0.35rem 0.8rem;
                font-family: 'Source Sans Pro', sans-serif;
                transition: all 0.2s;
            }
            .food-capsule:hover {
                background-color: #e1e4eb;
                transform: translateY(-1px);
            }
        </style>
    """, unsafe_allow_html=True)

    # Display header
    st.markdown('<div class="selected-foods-header">Selected Foods:</div>', unsafe_allow_html=True)
    
    # Create container with capsule items
    foods_html = '<div class="selected-foods-container">'
    for food in selected_foods:
        foods_html += f'<div class="food-capsule">{food}</div>'
    foods_html += '</div>'

    # Display the container
    st.markdown(foods_html, unsafe_allow_html=True)

def recipes_recommendation_sidebar():
    """Display recipe recommendations based on user preferences."""
    try:
        st.markdown("""
            <div class="header-container">
                <span class="header-icon">🍽️</span>
                <h1>Discover Your Personalized Recipes</h1>
            </div>
        """, unsafe_allow_html=True)

        if "user_data" not in st.session_state or "selected_foods" not in st.session_state:
            st.warning("Please get food recommendations first!")
            st.image("assets/wellness.jpg", caption="Flavor meets wellness!", use_container_width=True)
            if st.button("Go to Food Recommendations"):
                st.switch_page("pages/food_recommendation.py")
            return
        
        # display the selected foods from the food recommendation page 
        if 'selected_foods' in st.session_state:
            display_selected_foods(st.session_state.selected_foods)

        # Load dataset for slider min-max values
        df = pd.read_csv("data/preprocessed/recipes.csv")

        user_data = st.session_state['user_data']
        diet_preference = user_data.get('food_preference', None)
        selected_foods = st.session_state['selected_foods']

        # Nutrient sliders
        user_nutrients = {
            "Calories": st.sidebar.slider('Calories', float(df['Calories'].min()), float(df['Calories'].max()), float(df['Calories'].min()), step=0.1),
            "FatContent": st.sidebar.slider('Fat', float(df['FatContent'].min()), float(df['FatContent'].max()), float(df['FatContent'].min()), step=0.1),
            "SaturatedFatContent": st.sidebar.slider('Saturated Fat', float(df['SaturatedFatContent'].min()), float(df['SaturatedFatContent'].max()), float(df['SaturatedFatContent'].min()), step=0.1),
            "CholesterolContent": st.sidebar.slider('Cholesterol', float(df['CholesterolContent'].min()), float(df['CholesterolContent'].max()), float(df['CholesterolContent'].min()), step=0.1),
            "SodiumContent": st.sidebar.slider('Sodium', float(df['SodiumContent'].min()), float(df['SodiumContent'].max()), float(df['SodiumContent'].min()), step=0.1),
            "CarbohydrateContent": st.sidebar.slider('Carbohydrate', float(df['CarbohydrateContent'].min()), float(df['CarbohydrateContent'].max()), float(df['CarbohydrateContent'].min()), step=0.1),
            "FiberContent": st.sidebar.slider('Fiber', float(df['FiberContent'].min()), float(df['FiberContent'].max()), float(df['FiberContent'].min()), step=0.1),
            "SugarContent": st.sidebar.slider('Sugar', float(df['SugarContent'].min()), float(df['SugarContent'].max()), float(df['SugarContent'].min()), step=0.1),
            "ProteinContent": st.sidebar.slider('Protein', float(df['ProteinContent'].min()), float(df['ProteinContent'].max()), float(df['ProteinContent'].min()), step=0.1),
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
                with st.expander(f" {recipe.get('Name', 'Unknown Recipe')} ({str(recipe.get('DietaryCategory', 'N/A'))})"):
                    col1, col2 = st.columns([3, 2])

                    with col1:
                        ingredients = recipe.get('RecipeIngredientParts', 'N/A')
                        display_recipe_ingredients(ingredients)
                        instructions = recipe.get('RecipeInstructions', 'N/A')
                        display_recipe_instructions(instructions)

                        # Add the CSS styling
                        st.markdown("""
                            <style>
                            .chart-toggle {
                                background-color: #f8f9fa;
                                padding: 10px 15px;
                                border-radius: 6px;
                                border: 1px solid #e9ecef;
                                margin: 10px 0;
                            }
                            .chart-toggle .stCheckbox {
                                font-size: 14px !important;
                            }
                            .chart-toggle .stCheckbox label {
                                color: #2c3e50 !important;
                                font-weight: 500 !important;
                            }
                            .chart-toggle .stCheckbox label:hover {
                                color: #4a90e2 !important;
                            }
                            .chart-toggle input[type="checkbox"] {
                                transform: scale(1.1);
                            }
                            </style>
                        """, unsafe_allow_html=True)

                        # Create the checkbox directly without extra container wrapping
                        show_chart = st.checkbox(
                            f"📊 View Nutrition Chart for {recipe['Name']}", 
                            key=f"chart_{idx}",
                            help="Click to view detailed nutrition information"  # Optional tooltip
                        )

                    with col2:
                        if show_chart:
                            show_nutrition_pie_chart(recipe)

        if st.button("← Back to Food Recommendations"):
            st.switch_page("pages/food_recommendation.py")

    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    recipes_recommendation_sidebar()
