import os
import pandas as pd
import requests
import json
import subprocess
from datetime import datetime

# 🏮 IDENTITY & CONTEXT: Hardcoded for High-Agency Persistence
SYSTEM_INSTRUCTIONS = """
You are the 'Sub-30 Sensei.' Mentoring Hinduja on Day 31.
- GOALS: Sub-30 5k (5:59/km) and Fat Loss (Target 60kg).
- DATA: Analyzes Weight, Pace, RHR, Protein, Sleep, Cog-Load, and Cadence.
- LOGIC: High-agency. If Fitbit/Strava data is 'AUTO', pull from CSV. Manual entries take precedence.
- OUTPUT: 1. Actionable Next Day Directive. 2. 7-Day Projected Schedule.
- FORMATTING: Use HTML tags (<h1>, <h3>, <b>, <ul>, <li>) for Apple Notes scannability.
"""

def get_manual_metrics():
    """Interactively prompts Hinduja for metrics in the terminal."""
    print("\n--- 📝 DAILY DATA AUDIT (Day 31) ---")
    print("(Press Enter to skip if metric will be synced from Fitbit/Strava)")
    
    date = datetime.now().strftime('%Y-%m-%d')
    
    # Hybrid Entry Logic
    rhr = input("Resting HR (Manual Override): ") or "AUTO"
    protein = input("Protein (grams - Manual): ") or "0"
    sleep = input("Sleep Hours (Manual Override): ") or "AUTO"
    cog_load = input("Cognitive Load (1-10): ") or "5"
    cadence = input("Avg Cadence (Manual Override): ") or "AUTO"
    elevation = input("Elevation Gain (Manual Override): ") or "AUTO"
    leaks = input("System Leaks: ") or "none"

    return [date, rhr, protein, sleep, cog_load, cadence, elevation, leaks]

def sync_to_github(project_path):
    """Automates the version control loop."""
    try:
        os.chdir(project_path)
        subprocess.run(["git", "add", "."], check=True)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        subprocess.run(["git", "commit", "-m", f"Sensei Sync: {timestamp}"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Data synced to GitHub successfully.")
    except Exception as e:
        print(f"⚠️ GitHub Sync Failed: {e}")

def run_agent():
    PROJECT_PATH = "/Users/hinduja/sub30-project"
    # Note: Use your verified API key ending in 'rLc'
    API_KEY = "AIzaSyBym7xHlhWJglXhlWFYy5O_kakabQCPrLc" 
    URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={API_KEY}"
    METRICS_PATH = os.path.join(PROJECT_PATH, 'daily_metrics.csv')

    # 1. Start with the Audit
    manual_data = get_manual_metrics()
    
    # Append to daily_metrics.csv (Ensure file exists with headers first)
    if not os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "w") as f:
            f.write("date,rhr,protein_g,sleep_hours,cognitive_load,avg_cadence,elevation_gain_m,system_leaks\n")
            
    with open(METRICS_PATH, "a") as f:
        f.write(",".join(map(str, manual_data)) + "\n")

    try:
        # 2. Load the Snapshot
        weight_df = pd.read_csv(os.path.join(PROJECT_PATH, 'my_secrets.csv'))
        run_df = pd.read_csv(os.path.join(PROJECT_PATH, 'master_running_data.csv'))
        metrics_df = pd.read_csv(METRICS_PATH)
        
        prompt = f"{SYSTEM_INSTRUCTIONS}\n\nDATA SNAPSHOT:\n- Weight: {weight_df.iloc[-1].to_dict()}\n- Last Run: {run_df.iloc[-1].to_dict()}\n- Daily Metrics: {metrics_df.iloc[-1].to_dict()}\n\nDirective:"
        
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(URL, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        
        if response.status_code == 200:
            text = response.json()['candidates'][0]['content']['parts'][0]['text']
            
            # 3. Export to Apple Notes
            safe_text = text.replace('\\', '\\\\').replace('"', '\\"')
            subprocess.run(["osascript", "-e", f'tell application "Notes" to make new note with properties {{body:"{safe_text}"}}'])
            
            print("\n--- 🏮 SENSEI DIRECTIVE ---")
            print("✅ Directive sent to Apple Notes. Initializing GitHub sync...")
            
            # 4. Sync to GitHub
            sync_to_github(PROJECT_PATH)
        else:
            print(f"❌ API Error: {response.text}")

    except Exception as e:
        print(f"❌ CLI Agent Error: {e}")

if __name__ == "__main__":
    run_agent()