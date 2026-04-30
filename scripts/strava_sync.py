import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def get_new_access_token():
    payload = {
        'client_id': os.getenv('STRAVA_CLIENT_ID'),
        'client_secret': os.getenv('STRAVA_CLIENT_SECRET'),
        'refresh_token': os.getenv('STRAVA_REFRESH_TOKEN'),
        'grant_type': "refresh_token"
    }
    # Security handshake to refresh the expired access token
    res = requests.post("https://www.strava.com/oauth/token", data=payload)
    res.raise_for_status()
    return res.json()['access_token']

def sync_latest_runs():
    token = get_new_access_token()
    headers = {'Authorization': f'Bearer {token}'}
    
    # 1. Fetch activities
    res = requests.get("https://www.strava.com/api/v3/athlete/activities", headers=headers)
    activities = res.json()
    
    # DEBUG: If Strava sends an error, this will tell us why
    if isinstance(activities, dict) and 'message' in activities:
        print(f"❌ Strava API Error: {activities['message']}")
        print("Check if your Refresh Token in .env is correct!")
        return

    for activity in activities:
        # 2. Filter for Runs ONLY
        if activity.get('type') == 'Run':
            date = activity['start_date_local'].split('T')[0]
            # ... rest of your code ...
            print(f"✅ Found Run: {date}")

if __name__ == "__main__":
    sync_latest_runs()