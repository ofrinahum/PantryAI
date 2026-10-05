import { useState } from 'react'
import './App.css'

function App() {
  const [ingredients, setIngredients] = useState('')
  const [recipes, setRecipes] = useState([])

  const findRecipes = async () => {
    const ingredientList = ingredients
      .split(',')
      .map(item => item.trim())

    const response = await fetch('http://127.0.0.1:8000/recommend', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ingredients: ingredientList,
      }),
    })

    const data = await response.json()

    setRecipes(data.recipes)
  }

  return (
    <div className="app">
      <div className="content">

        <h1>PantryAI 🍳</h1>

        <p className="prompt">
          What ingredients do you have?
        </p>

        <p className="subtitle">
          Tell us what's in your pantry and we'll find something delicious.
        </p>

        <input
          className="ingredient-input"
          value={ingredients}
          onChange={(event) => setIngredients(event.target.value)}
          placeholder="chicken, rice, broccoli..."
        />

        <button className="find-button" onClick={findRecipes}>
          Find Recipes ✨
        </button>

        <div className="recipes">
          {recipes.map((recipe) => (
            <div className="recipe-card" key={recipe}>
              🍽️ {recipe}
            </div>
          ))}
        </div>

      </div>
    </div>
  )
}

export default App