from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.recommender import recommend_recipes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecommendationRequest(BaseModel):
    ingredients: list[str]

@app.post("/recommend")
def recommend(request: RecommendationRequest):
    recipes = recommend_recipes(request.ingredients)
    return {"recipes": recipes}
