import pandas as pd
import pyarrow.parquet as pq
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity


# Load a small sample of the recipe dataset
table = pq.ParquetFile("data/raw/recipes.parquet")

batch = next(table.iter_batches(
    batch_size=100,
    columns=["RecipeId", "Name", "RecipeIngredientParts"]
))

sample_df = batch.to_pandas()


# Explore unique raw ingredients
INGREDIENT_BANK = set()

for ingredients in sample_df["RecipeIngredientParts"]:
    for ingredient in ingredients:
        INGREDIENT_BANK.add(ingredient)

print("Unique ingredients:", len(INGREDIENT_BANK))

# Words that describe preparation rather than the ingredient itself
PREPARATION_WORDS = {
    "fresh",
    "chopped",
    "diced",
    "whole",
    "sliced",
    "peeled",
    "shredded",
    "skinless",
    "seeded"
}

def singularize(word):
    if word.endswith("s"):
        if word[:-1] in INGREDIENT_BANK:
            return word[:-1]

    return word


def clean_ingredient(ingredient):

    ingredient = ingredient.strip().lower()
    words = ingredient.split()
    cleaned_words = []

    for word in words:
        if word not in PREPARATION_WORDS:
            cleaned_words.append(word)

    return " ".join(cleaned_words)

def clean_recipe(ingredients):
    cleaned_recipe = []
    for ingredient in ingredients:
        cleaned_recipe.append(clean_ingredient(ingredient))
    return cleaned_recipe

sample_df["CleanedIngredients"] = sample_df["RecipeIngredientParts"].apply(clean_recipe)
mlb = MultiLabelBinarizer() # Converts ingredient lists into 0/1 numerical vectors.
ingredient_vectors = mlb.fit_transform(sample_df["CleanedIngredients"])
print(ingredient_vectors.shape)
print(mlb.classes_[:20])
similarities = cosine_similarity(ingredient_vectors) # Calculates how similar each recipe is to every other recipe.
print(similarities.shape)
print(similarities[0].argsort()[::-1]) # Returns the indexes that would sort the similarity scores from smallest to largest.
top_matches = similarities[0].argsort()[::-1][1:6]
print(sample_df.iloc[top_matches]["Name"])