# 🧠 Dynamic Metabolic Digital Twin

A full-stack web application that acts as a thermodynamic digital twin, analyzing longitudinal health data to calculate dynamic True Daily Energy Expenditure (TDEE) and predict future weight trends. 

**Live Demo:** https://metabolic-digital-twin-six.vercel.app/

<img width="2228" height="1352" alt="image" src="https://github.com/user-attachments/assets/b0980132-1cb7-4ecf-81a7-bb6203a01c01" />

<img width="2234" height="1502" alt="image" src="https://github.com/user-attachments/assets/fe9407e0-beb3-4c82-b951-958e24d8b3c2" />



## 🏆 The Story & Real-World Application
This engine was applied to my own 8-month, 25kg weight loss journey. By processing 240+ days of my personal daily weigh-ins and calorie logs, the model successfully tracked my metabolic adaptation in real-time, mapping a clear, physiological drop in maintenance calories as my body mass decreased.

## 🏗️ Tech Stack
*   **Frontend:** React, Vite, Recharts (Hosted on Vercel)
*   **Backend:** Python, FastAPI, SQLite (Hosted on Render)
*   **Data Science:** Pandas, NumPy

## 🔬 Methodology & Data Engineering

Calculating a highly accurate, dynamic TDEE from real-world human data presents significant challenges due to biological noise (water weight, digestion, etc.) and inconsistent tracking. This project overcomes those challenges using a custom physics engine:

### 1. Thermodynamic Equation over Machine Learning
Standard linear regression models fail on this type of data due to collinearity (highly consistent calorie intake) and low variance. Instead, this engine uses the strict laws of energy balance:
`TDEE = Calories Consumed - (Daily Weight Change × 7700)`

### 2. Aggressive Time-Series Smoothing
To prevent daily water weight fluctuations from creating erratic TDEE spikes, the pipeline applies:
*   A **14-day rolling average** to the raw weight input before it enters the regression.
*   A **21-day Exponential Moving Average (EMA)** to the final calculated TDEE, acting as a mathematical shock absorber that reveals the true underlying metabolic adaptation.

### 3. Masking & Data Gap Handling
Real-world data contains tracking gaps. In this dataset, there were significant missing periods. Standard linear interpolation across these gaps creates artificial "straight lines" that poison the EMA math. 
*   **Solution:** The data pipeline utilizes boolean masking to explicitly flag multi-week gaps. The EMA calculation completely ignores these flagged periods, "freezing" the last known valid TDEE until consistent, real-world data resumes, preventing mathematical hallucinations.

## 🚀 Local Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/misbah-tamanna/metabolic-digital-twin.git](https://github.com/misbah-tamanna/metabolic-digital-twin.git)
2. Install backend dependencies and run the FastAPI server:
   ```bash
   pip install -r requirements.txt
   uvicorn main:app --reload
4. In a new terminal, install frontend dependencies and run Vite:
   ```bash
   cd frontend
   npm install
   npm run dev
