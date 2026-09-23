import pandas as pd
import sqlite3

def setup_database():
    print("Connecting to SQLite database...")
    # This creates the database file locally in your folder
    conn = sqlite3.connect("metabolic_twin.db")
    
    print("Loading cleaned dataset...")
    df = pd.read_csv("fitness_data_cleaned.csv")
    
    print("Building 'daily_logs' SQL table...")
    # This writes the dataframe directly into SQL
    df.to_sql("daily_logs", conn, if_exists="replace", index=False)
    
    print("✅ Database built successfully!")
    conn.close()

if __name__ == "__main__":
    setup_database()