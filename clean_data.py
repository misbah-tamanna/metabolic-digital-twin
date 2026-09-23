import pandas as pd
import numpy as np

def process_fitness_data(csv_path="fitness_data.csv"):
    # 1. Load data and bulletproof the column names
    df = pd.read_csv(csv_path)
    
    # Force all headers to lowercase, remove accidental spaces, and strip hidden Excel characters
    df.columns = [str(col).strip().strip('\ufeff').lower() for col in df.columns]
    
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # 2. Ensure continuous daily timeline (Jan 21 -> Sep 21)
    # ... (keep the rest of the script exactly the same from here down)

    # 2. Ensure continuous daily timeline (Jan 21 -> Sep 21)
    full_date_range = pd.date_range(start=df["date"].min(), end=df["date"].max(), freq="D")
    df = df.set_index("date").reindex(full_date_range)
    df.index.name = "date"
    df = df.reset_index()

    # 3. Track original missing status for database flags
    df["weight_missing"] = df["weight"].isna()
    df["calories_missing"] = df["calories"].isna()

    # 4. Weight processing: Linear interpolation + Rolling smoothing
    df["weight_interpolated"] = df["weight"].interpolate(method="linear")
    df["weight_7d_avg"] = df["weight_interpolated"].rolling(window=7, min_periods=1).mean().round(2)
    df["weight_14d_avg"] = df["weight_interpolated"].rolling(window=14, min_periods=1).mean().round(2)

    # 5. Daily weight change (1-day delta and smoothed 7-day rate of change)
    df["weight_change_daily"] = df["weight_interpolated"].diff().round(3)
    df["weight_change_7d"] = (df["weight_7d_avg"] - df["weight_7d_avg"].shift(7)).round(3)

    # 6. Calorie processing: Fill short gaps with rolling median, flag large gaps
    # Identify gaps longer than 4 consecutive days
    calorie_gap_size = df["calories"].isna().astype(int).groupby(df["calories"].notna().cumsum()).cumsum()
    df["large_calorie_gap"] = calorie_gap_size > 4

    # Rolling 7-day intake proxy for scattered missing single days
    rolling_cal_mean = df["calories"].rolling(window=7, min_periods=1, center=True).mean()
    df["calories_cleaned"] = df["calories"].fillna(rolling_cal_mean).round(0)

    # 7. Composite interpolation flag for the SQLite database
    df["is_interpolated"] = df["weight_missing"] | df["calories_missing"]

    # 8. Save cleaned dataset
    cleaned_filename = "fitness_data_cleaned.csv"
    df.to_csv(cleaned_filename, index=False)
    
    print(f"Data pipeline executed successfully. Saved to {cleaned_filename}")
    print(f"Total days: {len(df)}")
    print(f"Recorded weight entries: {(~df['weight_missing']).sum()} / {len(df)}")
    print(f"Recorded calorie entries: {(~df['calories_missing']).sum()} / {len(df)}")
    print(f"Large calorie gap days flagged: {df['large_calorie_gap'].sum()}")
    
    return df

if __name__ == "__main__":
    df = process_fitness_data()
    print("\nPreview of processed rows:")
    print(df[["date", "weight_interpolated", "weight_7d_avg", "calories_cleaned", "is_interpolated"]].head(10))
