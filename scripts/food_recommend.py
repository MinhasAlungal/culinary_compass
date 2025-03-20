import pandas as pd
import numpy as np
import pickle

def load_data():
    """Load processed food data and trained KNN model."""
    df = pd.read_csv("data/preprocessed/food.csv")
    with open("models/knn_model.pkl", "rb") as model_file:
        knn = pickle.load(model_file)
    return df, knn

def format_recommendations(recommended_items):
    """
    Format the recommendations into a structured list of categories and food items.
    Args:
        recommended_items (DataFrame): DataFrame containing food recommendations
    Returns:
        list: Formatted list of recommendations grouped by main and sub categories
    """
    # Create a dictionary to store the structured data
    formatted_data = {}
    
    # Iterate through each row in the DataFrame
    for _, row in recommended_items.iterrows():
        main_cat = row['main_category']
        sub_cat = row['sub_category']
        food_name = row['description']
        
        # Create main category if it doesn't exist
        if main_cat not in formatted_data:
            formatted_data[main_cat] = {}
            
        # Create sub category if it doesn't exist
        if sub_cat not in formatted_data[main_cat]:
            formatted_data[main_cat][sub_cat] = []
            
        # Add food item to appropriate sub category
        formatted_data[main_cat][sub_cat].append(food_name)
    
    # Convert the nested dictionary to a formatted list
    formatted_list = []
    for main_cat, sub_cats in formatted_data.items():
        main_category = {
            "main_category": main_cat,
            "sub_categories": []
        }
        
        for sub_cat, foods in sub_cats.items():
            sub_category = {
                "name": sub_cat,
                "foods": foods
            }
            main_category["sub_categories"].append(sub_category)
        
        formatted_list.append(main_category)
    
    return formatted_list

def recommend_food(deficiencies, category=None):
    """Recommend food items based on a user's nutrient deficiencies, with optional category filtering."""
    df, knn = load_data()
    print("from recommend_food: deficiencies: ", deficiencies, "category: ", category)
    # Define nutrients inside the function
    nutrients = ['calcium', 'potassium', 'zinc', 'vitamin_C', 'iron', 'magnesium', 'phosphorus', 'sodium', 'copper',
                 'vitamin_E', 'thiamin', 'riboflavin', 'cholesterol', 'Niacin', 'vitamin_B_6', 'choline_total',
                 'vitamin_A', 'vitamin_K', 'folate_total', 'vitamin_B_12', 'selenium', 'vitamin_D']
    
    if not isinstance(deficiencies, list):
        return "Invalid input. Provide a list of deficiencies."
    
    # Check for invalid deficiencies
    invalid_nutrients = [d for d in deficiencies if d not in nutrients]
    if invalid_nutrients:
        return f"Invalid deficiencies: {', '.join(invalid_nutrients)}. Choose from: {', '.join(nutrients)}"
       
    # Create a query vector: 1 for deficient nutrients, 0 for others
    sample = np.zeros(len(nutrients))
    for deficiency in deficiencies:
        sample[nutrients.index(deficiency)] = 1
    
    # Use KNN to get recommendations
    distances, indices = knn.kneighbors([sample])
    
    # Extract recommendations from the full dataset first
    recommended_items = df.iloc[indices[0] % len(df)]  # Ensure valid indices
    
    # If category is 'Veg', filter the recommendations
    if category == 'Veg':
        recommended_items = recommended_items[recommended_items['main_category'] == category]
    
    if recommended_items.empty:
        return {"error": f"No valid food recommendations available for the selected category: {category}"}
    
    formatted_recommendations = format_recommendations(recommended_items)
    return formatted_recommendations