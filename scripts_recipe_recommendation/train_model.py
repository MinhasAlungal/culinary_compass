import pandas as pd
import torch
from sentence_transformers import SentenceTransformer

# Load dataset
df = pd.read_csv("/home/minhas/cgn-dp-24-1/culinary_compass/data/recipes_processed.csv")

# Initialize model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Compute embeddings
df["IngredientEmbedding"] = df["RecipeIngredientParts"].apply(lambda x: model.encode(str(x), convert_to_tensor=True).tolist())

# Save embeddings
df.to_csv("/home/minhas/cgn-dp-24-1/culinary_compass/data/recipes_with_embeddings.csv", index=False)
