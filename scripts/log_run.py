import csv
import os
from datetime import datetime

def log_new_run():
    print("--- 🏃 New Run Log ---")
    
    # 1. Date
    date_input = input("Date (YYYY-MM-DD) [Enter for today]: ")
    date = date_input if date_input else datetime.now().strftime('%Y-%m-%d')

    try:
        # 2. Distance & Duration
        distance = float(input("Distance in km (e.g., 3.0 or 5.0): "))
        duration = float(input("Total duration in minutes (e.g., 24.5): "))
        
        # 3. Auto-calculate Pace
        pace = round(duration / distance, 2)
        print(f"-> Calculated Pace: {pace} min/km")

        # 4. Other Metrics
        hr = int(input("Average Heart Rate (BPM): "))
        sleep = float(input("Sleep hours last night: "))
        notes = input("Notes: ")

        # 5. Save to CSV
        file_exists = os.path.isfile('running_logs.csv')
        with open('running_logs.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['date','distance_km','duration_minutes','pace_per_km','heart_rate','sleep_hours','notes'])
            
            writer.writerow([date, distance, duration, pace, hr, sleep, notes])

        print(f"--- ✅ Success! Data saved to running_logs.csv ---")

    except ValueError:
        print("❌ Error: Please enter numbers for distance, duration, and heart rate.")

if __name__ == "__main__":
    log_new_run()
