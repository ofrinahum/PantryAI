import pandas as pd

df = pd.read_parquet(
    "data/raw/recipes.parquet",
    columns=["RecipeId", "Name", "RecipeIngredientParts"]
)

print(df.head())
print(df.shape)
print(df.iloc[0]) # iloc is a Pandas tool for selecting data by its integer position (i=integer, loc=location).

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
    cleaned_words=[]
    for word in words:
        if word not in PREPARATION_WORDS:
            cleaned_words.append(word)
    return " ".join(cleaned_words)

print(clean_ingredient("  Fresh Chopped Chicken Breast  "))
print(clean_ingredient("  DICED onions  "))
print(clean_ingredient("  shredded cheddar cheese  "))
print(clean_ingredient("  chicken thigh  "))

