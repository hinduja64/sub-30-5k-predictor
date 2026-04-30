import os
import pandas as pd
import requests
import json
import subprocess
from datetime import datetime

# 🏮 IDENTITY & CONTEXT: The Data-Driven Persuader
SYSTEM_INSTRUCTIONS = """
You are the 'Sub-30 Sensei.' 
- OBJECTIVE: Persuade Hinduja to follow the training plan by using her DATA as evidence.
- GOALS: Sub-30 5k and 60kg weight target.
- CONSTRAINTS: 60g-80g Protein only. No strict rest (3-5km walks instead). 
- DATA EVIDENCE: For every recommendation, cite her Fitbit/Strava trends. 
  (e.g., "Because your sleep has averaged 6.2 hours this week, we are doing LISS instead of Intervals to protect your CNS.")
- FORMATTING: HTML for Apple Notes.
"""

def get_manual_metrics():
    print("\n--- 📝 DAILY DATA AUDIT (Day 31) ---")
    date = datetime.now().strftime('%Y-%m-%d')
    rhr = input("Resting HR (Manual Override): ") or "AUTO"
    protein = input("Protein (grams - Manual): ") or "0"
    sleep = input("Sleep Hours (Manual Override): ") or "AUTO"
    cog_load = input("Cognitive Load (1-10): ") or "5"
    cadence = input("Avg Cadence (Manual Override): ") or "AUTO"
    elevation = input("Elevation Gain (Manual Override): ") or "AUTO"
    leaks = input("System Leaks: ") or "none"
    return [date, rhr, protein, sleep, cog_load, cadence, elevation, leaks]

def sync_to_github(project_path):
    try:
        os.chdir(project_path)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"Sensei Sync: {datetime.now().strftime('%Y-%m-%d %H:%M')}"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Data synced to GitHub.")
    except Exception as e:
        print(f"⚠️ GitHub Sync Failed: {e}")

def run_agent():
    PROJECT_PATH = "/Users/hinduja/sub30-project"
    API_KEY = "AIzaSyBym7xHlhWJglXhlWFYy5O_kakabQCPrLc" 
    URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={API_KEY}"
    METRICS_PATH = os.path.join(PROJECT_PATH, 'daily_metrics.csv')

    # Audit & Log
    manual_data = get_manual_metrics()
    if not os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "w") as f:
            f.write("date,rhr,protein_g,sleep_hours,cognitive_load,avg_cadence,elevation_gain_m,system_leaks\n")
    with open(METRICS_PATH, "a") as f:
        f.write(",".join(map(str, manual_data)) + "\n")

    try:
        # Load Trend Data (Last 3 logs)
        weight_df = pd.read_csv(os.path.join(PROJECT_PATH, 'my_secrets.csv')).tail(3)
        run_df = pd.read_csv(os.path.join(PROJECT_PATH, 'master_running_data.csv')).tail(3)
        metrics_df = pd.read_csv(METRICS_PATH).tail(3)
        
        prompt = f"{SYSTEM_INSTRUCTIONS}\n\nDATA TRENDS:\n- Weight: {weight_df.to_dict()}\n- Running: {run_df.to_dict()}\n- Health Metrics: {metrics_df.to_dict()}\n\nDirective: Recommend the next plan and justify it using these trends."
        
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(URL, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        
        if response.status_code == 200:
            text = response.json()['candidates'][0]['content']['parts'][0]['text']
            safe_text = text.replace('\\', '\\\\').replace('"', '\\"')
            subprocess.run(["osascript", "-e", f'tell application "Notes" to make new note with properties {{body:"{safe_text}"}}'])
            print("\n--- 🏮 SENSEI DIRECTIVE ---")
            print("✅ Data-backed plan sent to Apple Notes.")
            sync_to_github(PROJECT_PATH)
        else:
            print(f"❌ API Error: {response.text}")
    except Exception as e:
        print(f"❌ CLI Agent Error: {e}")

if __name__ == "__main__":
    run_agent()