import { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

function App() {
  const [data, setData] = useState([])
  const [predictionData, setPredictionData] = useState([])
  const [targetCalories, setTargetCalories] = useState(2000)
  const [currentTdee, setCurrentTdee] = useState(2628) 
  
  const currentWeight = 75.0 

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/logs')
      .then(res => res.json())
      .then(jsonData => setData(jsonData))
      
    fetchPrediction(targetCalories)
  }, [])

  const fetchPrediction = (calories) => {
    fetch(`http://127.0.0.1:8000/api/predict?target_calories=${calories}&current_weight=${currentWeight}`)
      .then(res => res.json())
      .then(jsonData => {
          setPredictionData(jsonData.predictions)
          setCurrentTdee(jsonData.tdee) // Update the UI with the dynamic backend TDEE
      })
  }

  const handleSliderChange = (e) => {
    const newCalories = parseInt(e.target.value)
    setTargetCalories(newCalories)
    fetchPrediction(newCalories)
  }

  return (
    <div style={{ padding: '40px', fontFamily: 'system-ui, sans-serif', maxWidth: '1000px', margin: '0 auto' }}>
      <h1>🧠 Dynamic Metabolic Twin</h1>
      
      <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
        <div style={{ flex: 1, backgroundColor: '#eff6ff', padding: '20px', borderRadius: '8px', border: '1px solid #bfdbfe' }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#1e40af' }}>Current Dynamic TDEE</h3>
          <p style={{ fontSize: '32px', fontWeight: 'bold', margin: 0, color: '#1d4ed8' }}>{Math.round(currentTdee).toLocaleString()} kcal</p>
          <p style={{ fontSize: '14px', color: '#3b82f6', margin: '5px 0 0 0' }}>Adjusted for your current ~75kg body mass</p>
        </div>

        <div style={{ flex: 1, backgroundColor: '#f0fdf4', padding: '20px', borderRadius: '8px', border: '1px solid #bbf7d0' }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#166534' }}>30-Day Predictor</h3>
          <p style={{ margin: '0 0 10px 0', color: '#15803d' }}>Target Calories: <strong>{targetCalories} kcal</strong></p>
          <input 
            type="range" min="1500" max="3500" step="50" 
            value={targetCalories} onChange={handleSliderChange} style={{ width: '100%' }}
          />
        </div>
      </div>

      {/* --- NEW: Metabolic Adaptation Chart --- */}
      <h3>Metabolic Adaptation (TDEE over time)</h3>
      <div style={{ height: '250px', width: '100%', marginBottom: '40px', backgroundColor: '#fdfdfd', padding: '20px', borderRadius: '8px', border: '1px solid #eee' }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
            <XAxis dataKey="date" tick={{fontSize: 12}} minTickGap={30} />
           <YAxis 
  domain={['dataMin - 100', 'dataMax + 100']} 
  tick={{fontSize: 12}} 
  tickFormatter={(tick) => Math.round(tick)} 
/>
            <Tooltip />
            <Line type="monotone" dataKey="dynamic_tdee" stroke="#f59e0b" name="Dynamic TDEE (kcal)" strokeWidth={2} dot={false} connectNulls={true} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <h3>Historical Weight Trend</h3>
      <div style={{ height: '250px', width: '100%', marginBottom: '40px', backgroundColor: '#fdfdfd', padding: '20px', borderRadius: '8px', border: '1px solid #eee' }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
            <XAxis dataKey="date" tick={{fontSize: 12}} minTickGap={30} />
            <YAxis domain={['dataMin - 1', 'dataMax + 1']} tick={{fontSize: 12}} />
            <Tooltip />
            <Line type="monotone" dataKey="weight_7d_avg" stroke="#64748b" name="7-Day Avg Weight (kg)" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <h3>Future Projection (Next 30 Days)</h3>
      <div style={{ height: '250px', width: '100%', backgroundColor: '#fdfdfd', padding: '20px', borderRadius: '8px', border: '1px solid #eee' }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={predictionData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
            <XAxis dataKey="day" tick={{fontSize: 12}} minTickGap={5} />
            <YAxis domain={['dataMin - 0.5', 'dataMax + 0.5']} tick={{fontSize: 12}} />
            <Tooltip />
            <Line type="monotone" dataKey="projected_weight" stroke="#22c55e" name="Projected Weight (kg)" strokeWidth={3} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

    </div>
  )
}

export default App