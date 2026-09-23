import pandas as pd
import sqlite3

def build_dynamic_model():
    print("Loading cleaned data...")
    df = pd.read_csv("fitness_data_cleaned.csv")
    
    # 1. Aggressively smooth the weight input (14-day rolling average)
    df['weight_14d_avg'] = df['weight_interpolated'].rolling(window=14, min_periods=7).mean()
    df['weight_change_daily'] = df['weight_14d_avg'].diff()
    
    # Smooth calories to match the 14-day window
    df['calories_14d_avg'] = df['calories_cleaned'].rolling(window=14, min_periods=7).mean()
    
    # 2. Thermodynamics Equation
    df['implied_tdee'] = df['calories_14d_avg'] - (df['weight_change_daily'] * 7700)
    
    # MASKING: Isolate good data
    valid_data = df[(df['large_calorie_gap'] == False) & (df['is_interpolated'] == False)].copy()
    
    # 3. Widen the window: 21-day Exponential Moving Average
    valid_data['dynamic_tdee'] = valid_data['implied_tdee'].ewm(span=21, min_periods=14).mean()
    
    # Merge back and forward-fill
    df = df.merge(valid_data[['date', 'dynamic_tdee']], on='date', how='left')
    df['dynamic_tdee'] = df['dynamic_tdee'].ffill()
    
    conn = sqlite3.connect("metabolic_twin.db")
    df.to_sql("daily_logs", conn, if_exists="replace", index=False)
    conn.close()
    print("✅ Aggressively smoothed TDEE calculated and saved!")

if __name__ == "__main__":
    build_dynamic_model()