import pyarrow.parquet as pq
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity

table = pq.ParquetFile("data/raw/recipes.parquet")

batch = next(table.iter_batches (
    batch_size = 100,
    columns=["RecipeId", "Name", "RecipeIngredientParts"]
))

recipe_df = batch.to_pandas()

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

recipe_df["CleanedIngredients"] = recipe_df["RecipeIngredientParts"].apply(clean_recipe)

mlb = MultiLabelBinarizer()

ingredient_vectors = mlb.fit_transform(
    recipe_df["CleanedIngredients"]
)

def recommend_recipes(user_ingredients):
    user_vector = mlb.transform([user_ingredients])

    user_similarities = cosine_similarity(
        user_vector,
        ingredient_vectors
    )

    top_matches = user_similarities[0].argsort()[::-1][:5]

    return recipe_df.iloc[top_matches]["Name"].tolist()