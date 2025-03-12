import pandas as pd
import numpy as np
import pickle

def load_data():
    """Load processed food data and trained KNN model."""
    df = pd.read_csv("data/processed_food_data.csv")
    with open("models/knn_model.pkl", "rb") as model_file:
        knn = pickle.load(model_file)
    return df, knn

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
        return f"No valid food recommendations available for the selected category: {category}"
    
    # Format recommendations as a list of strings
    recommendation_list = [f"\nRecommendations for {' and '.join(deficiencies)} Deficiency:"]
    for _, row in recommended_items.iterrows():
        #recommendation_list.append(
        #    f"Food: {row['description']}, {', '.join([f'{d.capitalize()}: {row[d]} mg' for d in deficiencies])}"
        #)
        recommendation_list.append(f"\n{row['description']}")
        
    
    print(recommendation_list)

    return "\n".join(recommendation_list)
