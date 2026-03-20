import pandas as pd
import os
from datetime import datetime

FILE_NAME = 'running_logs.csv'

def log_new_run ():
    print ("---🏃 New 5KM Run Log ---")
    date_str = input("Date (YYYY-MM-DD) [Enter for today]: ") or  datetime.now().strftime ('%Y-%m-%d')
    duration = float(input("Duration in minutes (e.g., 40.5): "))
    hr = int(input("Average Heart Rate: "))
    sleep = float(input("Sleep last night (hours): "))
    notes = input("Notes: ")
	
    # Calculate Pace automatically (Duration / 5km)
    pace = round(duration / 5.0,2)

    new_data = {
        'date': [date_str],
        'distance_km': [5.0],
        'duration_minutes': [duration],
        'pace_per_km': [pace],
        'heart_rate': [hr],
        'sleep_hours': [sleep],
        'notes': [notes]
    }

    new_df = pd.DataFrame(new_data)

    # This checks if the file exists. If not, it creates it with headers.
    if not os.path.isfile(FILE_NAME):
        new_df.to_csv(FILE_NAME, index=False)
    else:
     	new_df.to_csv(FILE_NAME, mode='a', header=False, index=False)

    print(f"\n✅ Logged! Your pace was {pace} min/km.")

if __name__ == "__main__":
    	log_new_run()
