import os
import pandas as pd
import requests
import json
import subprocess
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file for security
load_dotenv()

# 🏮 IDENTITY & CONTEXT: The Data-Driven Persuader
SYSTEM_INSTRUCTIONS = """
You are the 'Sub-30 Sensei.' 
- OBJECTIVE: Persuade Hinduja to follow the training plan by using her DATA as evidence.
- GOALS: Sub-30 5k (5:59/km) and Fat Loss (Target 60kg).
- CONSTRAINTS: 60g-80g Protein only. No 'Strict Rest' (3-5km walks instead). 
- DATA EVIDENCE: For every recommendation, cite her Fitbit/Strava trends (e.g., RHR, Sleep, Cadence).
- STRENGTH PROTOCOL: Include 3-4 days/week of bodyweight training (Squats, Lunges, Pushups, Planks).
- FORMATTING: HTML for Apple Notes. Provide 'Next Day Directive' and '7-Day Projection.'
"""

def get_manual_metrics():
    print("\n--- 📝 DAILY DATA AUDIT ---")
    date = datetime.now().strftime('%Y-%m-%d')
    rhr = input("Resting HR (Enter for AUTO): ") or "AUTO"
    protein = input("Protein (grams): ") or "0"
    sleep = input("Sleep Hours (Enter for AUTO): ") or "AUTO"
    cog_load = input("Cognitive Load (1-10): ") or "5"
    cadence = input("Avg Cadence (Enter for AUTO): ") or "AUTO"
    elevation = input("Elevation Gain (Enter for AUTO): ") or "AUTO"
    leaks = input("System Leaks: ") or "none"
    return [date, rhr, protein, sleep, cog_load, cadence, elevation, leaks]

def sync_to_github(project_path):
    try:
        os.chdir(project_path)
        subprocess.run(["git", "add", "."], check=True)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        subprocess.run(["git", "commit", "-m", f"Sensei Sync: {timestamp}"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Data synced to GitHub (secrets excluded via .gitignore).")
    except Exception as e:
        print(f"⚠️ GitHub Sync Failed: {e}")

def run_agent():
    PROJECT_PATH = "/Users/hinduja/sub30-project"
    
    # Securely fetch API key from .env
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        print("❌ Error: GEMINI_API_KEY not found in .env file.")
        return

    URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={API_KEY}"
    METRICS_PATH = os.path.join(PROJECT_PATH, 'daily_metrics.csv')

    # 1. Collect and Save Manual Metrics
    manual_data = get_manual_metrics()
    if not os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "w") as f:
            f.write("date,rhr,protein_g,sleep_hours,cognitive_load,avg_cadence,elevation_gain_m,system_leaks\n")
    with open(METRICS_PATH, "a") as f:
        f.write(",".join(map(str, manual_data)) + "\n")

    try:
        # 2. Load Trend Data for Context (Last 3 entries)
        weight_df = pd.read_csv(os.path.join(PROJECT_PATH, 'my_secrets.csv')).tail(3)
        run_df = pd.read_csv(os.path.join(PROJECT_PATH, 'master_running_data.csv')).tail(3)
        metrics_df = pd.read_csv(METRICS_PATH).tail(3)
        
        # 3. Construct the Prompt with Data Evidence
        prompt = f"""
        {SYSTEM_INSTRUCTIONS}
        
        CURRENT DATA TRENDS:
        - Recent Weight Log: {weight_df.to_dict()}
        - Recent Run Performance: {run_df.to_dict()}
        - Recent Health Metrics: {metrics_df.to_dict()}
        
        Hinduja just reported a Cognitive Load of {manual_data[4]}.
        
        Directive: Provide the plan for tomorrow. You MUST justify the intensity based on the trends above. 
        If Cog-Load is high, explain why you are prioritizing recovery.
        """
        
        # 4. Call Gemini API
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(URL, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        
        if response.status_code == 200:
            content = response.json()['candidates'][0]['content']['parts'][0]['text']
            
            # 5. Push to Apple Notes via AppleScript
            safe_text = content.replace('\\', '\\\\').replace('"', '\\"')
            subprocess.run(["osascript", "-e", f'tell application "Notes" to make new note with properties {{body:"{safe_text}"}}'])
            
            print("\n--- 🏮 SENSEI DIRECTIVE ---")
            print("✅ Data-backed plan sent to Apple Notes.")
            
            # 6. Automatic Backup to GitHub
            sync_to_github(PROJECT_PATH)
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ CLI Agent Error: {e}")

if __name__ == "__main__":
    run_agent()