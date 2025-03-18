import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
import pickle

# Load dataset
df = pd.read_csv("data/preprocessed/recipes.csv")

# Initialize model
st_model = SentenceTransformer("all-MiniLM-L6-v2")

# Save the trained model
with open("models/recipes_st.pkl", "wb") as model_file:
    pickle.dump(st_model, model_file)


# Compute embeddings
df["IngredientEmbedding"] = df["RecipeIngredientParts"].apply(lambda x: st_model.encode(str(x), convert_to_tensor=True).tolist())

# Save embeddings
df.to_csv("data/embeddings/recipes.csv", index=False)
