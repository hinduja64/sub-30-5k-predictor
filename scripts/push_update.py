import pandas as pd
import os

def generate_telemetry():
    # We define the absolute path to your project folder
    base_path = "/Users/hinduja/sub30-project"
    weight_file = os.path.join(base_path, 'my_secrets.csv')
    run_file = os.path.join(base_path, 'master_running_data.csv')

    if not os.path.exists(weight_file):
        return f"❌ Error: my_secrets.csv not found at {weight_file}"
    if not os.path.exists(run_file):
        return f"❌ Error: master_running_data.csv not found at {run_file}"

    try:
        weight_df = pd.read_csv(weight_file)
        latest_weight = weight_df.iloc[-1]
        
        run_df = pd.read_csv(run_file)
        latest_run = run_df.iloc[-1]

        payload = f"""
SENSEI TELEMETRY UPDATE:
---
DATE: {latest_run['date']}
WEIGHT: {latest_weight['weight_kg']}kg
PACE: {latest_run['pace_per_km']} min/km
DISTANCE: {latest_run['distance_km']}km
---
"""
        return payload
    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == "__main__":
    print(generate_telemetry())