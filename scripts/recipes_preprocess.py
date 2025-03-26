import pandas as pd

# Load dataset
df = pd.read_csv("data/recipes.csv")
#df =df.iloc[0:3000]

# Define non-vegetarian keywords
non_veg_keywords = set([
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

# Function to classify recipes
def classify_recipe(row):
    """
    Classifies a recipe as 'Vegetarian' or 'Non-Vegetarian' based on:
    - `RecipeIngredientParts`
    - `RecipeCategory`
    """
    # Extract ingredient list
    ingredients = str(row["RecipeIngredientParts"]).lower().replace('"', '').replace("c(", "").replace(")", "")
    ingredient_list = [ing.strip() for ing in ingredients.split(",")]

    # Extract category list
    categories = str(row["RecipeCategory"]).lower().replace('"', '').replace("c(", "").replace(")", "")
    category_list = [cat.strip() for cat in categories.split(",")]

    # Check for non-veg keywords in ingredients or category
    if any(any(non_veg in item for non_veg in non_veg_keywords) for item in ingredient_list + category_list):
        return "Non-Veg"

    return "Veg"

# Apply classification
df["DietaryCategory"] = df.apply(classify_recipe, axis=1)

# Save processed data
df.to_csv("data/preprocessed/recipes.csv", index=False)
