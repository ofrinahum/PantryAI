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

# Clean individual ingredient names
def clean_ingredient(ingredient):
    ingredient = ingredient.strip().lower()
    words = ingredient.split()
    cleaned_words = []

    for word in words:
        if word not in PREPARATION_WORDS:
            cleaned_words.append(word)

    return " ".join(cleaned_words)


# Clean all ingredients belonging to one recipe
def clean_recipe(ingredients):
    cleaned_recipe = []

    for ingredient in ingredients:
        cleaned_recipe.append(clean_ingredient(ingredient))

    return cleaned_recipe


sample_df["CleanedIngredients"] = sample_df["RecipeIngredientParts"].apply(clean_recipe)


# Convert ingredient lists into 0/1 numerical vectors
mlb = MultiLabelBinarizer()
ingredient_vectors = mlb.fit_transform(sample_df["CleanedIngredients"])

def recommend_recipes(user_ingredients):
    user_vector = mlb.transform([user_ingredients])
    user_similarities = cosine_similarity(user_vector, ingredient_vectors)

    top_matches = user_similarities[0].argsort()[::-1][:5]

    return sample_df.iloc[top_matches]["Name"].tolist()

print(recommend_recipes(["chicken", "rice", "broccoli"]))
