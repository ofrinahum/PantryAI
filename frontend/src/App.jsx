import { useState } from 'react'
import './App.css'

function App() {
  const [ingredients, setIngredients] = useState('')
  const findRecipes = async () => {
    const ingredientList = ingredients.split(',').map(item => item.trim())
  
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
  
    console.log(data)
  }

  return (
    <div>
      <h1>PantryAI 🍳</h1>

      <p>Enter the ingredients you have:</p>

      <input
        value={ingredients}
        onChange={(event) => setIngredients(event.target.value)}
        placeholder="chicken, rice, broccoli"
      />

      <button onClick={findRecipes}>Find Recipes</button>
    </div>
  )
}

export default App