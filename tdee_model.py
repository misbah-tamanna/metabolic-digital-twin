import pandas as pd
import numpy as np

def build_tdee_model():
    print("Loading cleaned data...")
    df = pd.read_csv("fitness_data_cleaned.csv")
    
    # 1. Filter out the noise! Drop days with missing data AND large interpolated gaps
    df = df.dropna(subset=['weight_7d_avg', 'calories_cleaned', 'weight_change_7d'])
    df = df[df['large_calorie_gap'] == False] # EXCLUDE the multi-week flatlines
    
    # 2. Smooth the calories to match the weight smoothing (7-day average)
    df['calories_7d_avg'] = df['calories_cleaned'].rolling(window=7, min_periods=1).mean()
    
    # 3. Regress: Daily Weight Change vs Average Daily Calories
    df['daily_weight_change'] = df['weight_change_7d'] / 7
    df = df.dropna(subset=['calories_7d_avg', 'daily_weight_change'])
    
    X = df['calories_7d_avg'].values
    y = df['daily_weight_change'].values
    
    # Fit the Linear Regression
    slope, intercept = np.polyfit(X, y, 1)
    tdee_estimate = -intercept / slope
    
    correlation_matrix = np.corrcoef(X, y)
    r_squared = correlation_matrix[0, 1] ** 2
    
    print("\n--- 🧠 Metabolic Twin: REFINED Regression Results ---")
    print(f"Calculated Maintenance Calories (TDEE): {tdee_estimate:.0f} kcal/day")
    print(f"Model Coefficient (Slope): {slope:.6f} (Theoretical ideal: ~0.00013)")
    print(f"Model R-squared: {r_squared:.4f}")
    
    return slope, intercept, tdee_estimate

if __name__ == "__main__":
    build_tdee_model()