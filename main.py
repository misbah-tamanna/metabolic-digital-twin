from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import pandas as pd
import json

# 1. Initialize the FastAPI application
app = FastAPI()

# 2. CORS Middleware (CRITICAL)
# React will run on a different local port (e.g., localhost:3000). 
# By default, web browsers block requests between different ports for security. 
# This tells our API to accept requests from anywhere while we develop.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Health Check Endpoint
# When you visit the base URL, it just returns a success message
@app.get("/")
def read_root():
    return {"message": "Metabolic Twin API is running!"}

# 4. Data Endpoint for React
# When React asks for /api/logs, we query the SQLite database and send JSON back
@app.get("/api/logs")
def get_daily_logs():
    print("React requested data! Querying database...")
    
    # Open connection to our database
    conn = sqlite3.connect("metabolic_twin.db")
    
    # Use Pandas to run a SQL query and grab everything
    df = pd.read_sql_query("SELECT * FROM daily_logs", conn)
    conn.close()
    
    # Convert the Pandas dataframe into standard JSON format for the web
    # .to_json() automatically converts Python NaNs into web-safe 'null' values
    json_data = json.loads(df.to_json(orient="records"))
    
    return json_data

# 5. Prediction Endpoint (DYNAMIC VERSION)
@app.get("/api/predict")
def predict_weight(target_calories: int = 2500, current_weight: float = 75.0):
    
    # 1. Connect to DB to dynamically grab your LATEST calculated TDEE
    conn = sqlite3.connect("metabolic_twin.db")
    cursor = conn.cursor()
    cursor.execute("SELECT dynamic_tdee FROM daily_logs WHERE dynamic_tdee IS NOT NULL ORDER BY date DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    
    # 2. Assign the true dynamic TDEE (fallback to 2628 if the query misses)
    tdee = result[0] if result else 2628 
    
    # 3. Calculate daily deficit & weight loss (1 kg fat = ~7700 kcal)
    daily_deficit = tdee - target_calories
    daily_kg_lost = daily_deficit / 7700
    
    # 4. Generate 30 days of future predictions
    predictions = []
    projected_weight = current_weight
    
    for day in range(1, 31):
        projected_weight -= daily_kg_lost
        predictions.append({
            "day": f"Day {day}",
            "projected_weight": round(projected_weight, 2)
        })
        
    return {"tdee": tdee, "predictions": predictions}