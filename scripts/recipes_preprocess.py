import pandas as pd

# Load dataset
df = pd.read_csv("data/recipes.csv")
df =df.iloc[0:3000]

# Define non-vegetarian ingredients
non_veg_ingredients = set([
    # Meat & Poultry
    "chicken", "beef", "pork", "mutton", "lamb", "turkey", "duck", "quail", "goat", "veal",
    "rabbit", "boar", "venison", "bison", "kangaroo", "goose", "pheasant", "pigeon", "elk",
    
    # Processed Meat Products
    "bacon", "ham", "sausage", "pepperoni", "salami", "chorizo", "pastrami", "prosciutto",
    "mortadella", "hot dog", "jerky", "liverwurst", "blood sausage", "scrapple",
    
    # Seafood
    "fish", "tuna", "salmon", "trout", "cod", "haddock", "mackerel", "sardine", "anchovy",
    "herring", "catfish", "bass", "snapper", "grouper", "halibut", "swordfish", "mahi mahi",
    "flounder", "eel", "shark", "sturgeon", "tilapia", "tuna steaks", "swordfish steaks",
    
    # Shellfish
    "shrimp", "prawns", "crab", "lobster", "crawfish", "squid", "octopus", "scallops",
    "mussels", "clams", "oysters", "abalone", "conch",
    
    # Animal-Based Ingredients
    "eggs", "gelatin", "lard", "suet", "tallow", "bone broth", "fish sauce", "oyster sauce",
    "shrimp paste", "anchovy paste", "worcestershire sauce", "caviar", "roe", "squid ink",
    
    # Organ Meats (Offal)
    "liver", "kidney", "heart", "brain", "tripe", "sweetbreads", "tongue", "gizzards"
])

# Function to classify recipes correctly
def classify_recipe(ingredients):
    # Step 1: Clean string formatting issues
    ingredients = str(ingredients).lower().replace('"', '').replace("c(", "").replace(")", "")

    # Step 2: Convert to a list of ingredients
    ingredient_list = [ing.strip() for ing in ingredients.split(",")]

    # Step 3: Check for partial matches
    if any(any(non_veg in ingredient for non_veg in non_veg_ingredients) for ingredient in ingredient_list):
        return "Non-veg" #Non-Vegetarian to Non-veg
    return "Veg" #Vegetarian to Veg

# Apply classification
df["DietaryCategory"] = df["RecipeIngredientParts"].apply(classify_recipe)

# Save processed data
df.to_csv("data/preprocessed/recipes.csv", index=False)
