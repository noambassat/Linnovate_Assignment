
import React, { useState } from 'react'
import ReactDOM from 'react-dom/client'

function App() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])

  const handleSubmit = async (e) => {
      e.preventDefault()

      console.log('Sending query:', query)

      try {
        const response = await fetch('/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query, top_k: 3 })
        })

        console.log('Got response:', response)

        if (!response.ok) {
          throw new Error('Request failed')
        }

        const data = await response.json()
        console.log('Parsed data:', data)
        setResults(data.matches)
      } catch (err) {
        console.error('Error:', err)
        alert('Request failed. See console for details.')
      }
    }


  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial' }}>
      <h1>Ask about the video</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={{ width: '300px', padding: '0.5rem' }}
          placeholder="Enter your question"
        />
        <button type="submit" style={{ marginLeft: '1rem' }}>Submit</button>
      </form>

      <ul>
        {results.map((item, index) => (
          <li key={index} style={{ marginTop: '1rem' }}>
            <strong>{item.segment_path}</strong><br />
            <em>{item.summary}</em>
          </li>
        ))}
      </ul>
    </div>
  )
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />)
