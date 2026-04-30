import csv
import os
from datetime import datetime

def log_new_run():
    print("--- 🏃 New Run Log (AI Agent Sync) ---")
    
    # 1. Date
    date_input = input("Date (YYYY-MM-DD) [Enter for today]: ")
    date = date_input if date_input else datetime.now().strftime('%Y-%m-%d')

    try:
        # 2. Distance & Duration
        distance = float(input("Distance in km (e.g., 5.0): "))
        duration = float(input("Total duration in minutes: "))
        
        # 3. Auto-calculate Pace
        pace = round(duration / distance, 2) if distance > 0 else 0
        print(f"-> Calculated Pace: {pace} min/km")

        # 4. Metrics
        hr = int(input("Average Heart Rate (BPM): "))
        sleep = float(input("Sleep hours last night: "))
        
        # 5. SECRET METRIC (Stays on your computer)
        weight = float(input("Current Weight in kg (Secret): "))
        
        notes = input("Notes: ")

        # --- SAVE PUBLIC DATA TO GITHUB FILE ---
        public_file = 'master_running_data.csv'
        public_exists = os.path.isfile(public_file)
        with open(public_file, 'a', newline='') as f:
            writer = csv.writer(f)
            if not public_exists:
                writer.writerow(['date','distance_km','duration_minutes','pace_per_km','heart_rate','sleep_hours','notes'])
            writer.writerow([date, distance, duration, pace, hr, sleep, notes])

        # --- SAVE PRIVATE DATA LOCALLY (Hidden by .gitignore) ---
        secret_file = 'my_secrets.csv'
        secret_exists = os.path.isfile(secret_file)
        with open(secret_file, 'a', newline='') as f:
            writer = csv.writer(f)
            if not secret_exists:
                writer.writerow(['date', 'weight_kg'])
            writer.writerow([date, weight])

        print(f"\n--- ✅ Success! ---")
        print(f"1. Public stats saved to {public_file} (Ready for GitHub)")
        print(f"2. Weight saved to {secret_file} (Private to this machine)")

    except ValueError:
        print("❌ Error: Please enter valid numbers.")

if __name__ == "__main__":
    log_new_run()
