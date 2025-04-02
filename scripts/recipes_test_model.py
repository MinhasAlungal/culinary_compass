from recipes_recommend import recommend_recipes_minilm, recommend_recipes_mpnet, recommend_recipes_paraphrase
import pickle

# Step 7: User input for testing
user_nutrients = {
    "Calories": 500, "FatContent": 20, "SaturatedFatContent": 5,
    "CholesterolContent": 10, "SodiumContent": 500, "CarbohydrateContent": 50,
    "FiberContent": 10, "SugarContent": 10, "ProteinContent": 30
}

user_ingredients = [ "Egg, whole, raw, frozen, salted, pasteurized", "Cheese, American, restaurant",
                    "Cheese, cotija, solid", "Crustaceans, crab, alaska king, raw",
                      "Mollusks, clam, mixed species, raw",  "Seaweed, wakame, raw",
                    "Cream cheese, full fat, block"]
# Define the diet preference
diet_preference = "Non-veg"# You can set this to "Vegetarian", "Non-Vegetarian", or "Any" based on user input

# Get recommendations from all models
print("\n=== Recommendations from MiniLM Model ===")
recommendations_minilm = recommend_recipes_minilm(user_nutrients, user_ingredients, diet_preference)
for recipe in recommendations_minilm:
    print(f"Name: {recipe['Name']}\nImage: {recipe['Images']}\nInstructions: {recipe['RecipeInstructions']}\n{'-'*50}")

print("\n=== Recommendations from MPNet Model ===")
recommendations_mpnet = recommend_recipes_mpnet(user_nutrients, user_ingredients, diet_preference)
for recipe in recommendations_mpnet:
    print(f"Name: {recipe['Name']}\nImage: {recipe['Images']}\nInstructions: {recipe['RecipeInstructions']}\n{'-'*50}")

print("\n=== Recommendations from Paraphrase Model ===")
recommendations_paraphrase = recommend_recipes_paraphrase(user_nutrients, user_ingredients, diet_preference)
for recipe in recommendations_paraphrase:
    print(f"Name: {recipe['Name']}\nImage: {recipe['Images']}\nInstructions: {recipe['RecipeInstructions']}\n{'-'*50}")