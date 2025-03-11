import pandas as pd
import numpy as np
import pickle

# Load the processed data and the trained KNN model
df = pd.read_csv("data/processed_food_data.csv")
with open("models/knn_model.pkl", "rb") as model_file:
    knn = pickle.load(model_file)


def recommend_food(deficiencies, category=None):
    """Recommend food items based on a user's nutrient deficiencies, with optional category filtering."""
    
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

    # Filter by category (if specified)
    if category == 'Veg':
        # Filter the dataframe based on the main category (e.g., 'Veg')
        df_filtered = df[df['main_category'] == category]
        if df_filtered.empty:
            return f"No data found for the category: {category}."
    else:
        df_filtered = df  # If no category is selected, use the whole dataframe

    # Check if df_filtered contains data
    if df_filtered.shape[0] == 0:
        return "No data available for the selected category."

    # Create a query vector: 1 for deficient nutrients, 0 for others
    sample = np.zeros(len(nutrients))
    for deficiency in deficiencies:
        sample[nutrients.index(deficiency)] = 1  # Targeting deficient nutrients

    # Use the pre-trained KNN model to get recommendations
    distances, indices = knn.kneighbors([sample])

    # Debugging: Check the values of indices
    print(f"Indices from KNN: {indices}")

    # Ensure indices are valid and within bounds
    valid_indices = [idx for idx in indices[0] if idx < len(df_filtered)]
    
    if len(valid_indices) == 0:
        return "No valid food recommendations available."

    # Now use the valid indices for recommendation
    recommendations = df_filtered.iloc[valid_indices][['description'] + deficiencies]

    # Format recommendations as a list of strings
    recommendation_list = [f"\nRecommendations for {' and '.join(deficiencies)} Deficiency:"]
    for i, row in recommendations.iterrows():
        recommendation_list.append(f"Food: {row['description']}, {', '.join([f'{d.capitalize()}: {row[d]} mg' for d in deficiencies])}")

    return "\n".join(recommendation_list)
