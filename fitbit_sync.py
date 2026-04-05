import os
import fitbit
import pandas as pd
from dotenv import load_dotenv
import webbrowser
import cherrypy

load_dotenv()

CLIENT_ID = os.getenv('FITBIT_CLIENT_ID')
CLIENT_SECRET = os.getenv('FITBIT_CLIENT_SECRET')

class OAuth2Server:
    def __init__(self, client_id, client_secret, redirect_uri='http://127.0.0.1:8080/'):
        self.success_html = """<h1>Success!</h1><p>You can close this window and return to the terminal.</p>"""
        self.fitbit = fitbit.Fitbit(client_id, client_secret, redirect_uri=redirect_uri)

    @cherrypy.expose
    def index(self, state, code=None, error=None):
        if error: return f"Error: {error}"
        self.fitbit.client.fetch_access_token(code)
        cherrypy.engine.exit()
        return self.success_html

def get_auth_client():
    server = OAuth2Server(CLIENT_ID, CLIENT_SECRET)
    url, _ = server.fitbit.client.authorize_token_url()
    webbrowser.open(url)
    cherrypy.quickstart(server, config={'global': {'server.socket_port': 8080, 'log.screen': False}})
    return server.fitbit

if __name__ == "__main__":
    client = get_auth_client()
    
    # 1. Fetch Resting Heart Rate (RHR) - Works via time_series
    print("Fetching Heart Rate data...")
    hr_data = client.time_series('activities/heart', base_date='today', period='30d')
    rhr_records = [{'date': e['dateTime'], 'resting_hr': e['value'].get('restingHeartRate', 0)} for e in hr_data['activities-heart']]

    # 2. Fetch Sleep data - FIXED: Using get_sleep instead of time_series
    print("Fetching Sleep data...")
    start_date = pd.Timestamp.now() - pd.Timedelta(days=30)
    sleep_logs = client.get_sleep(start_date)
    
    sleep_records = []
    for s in sleep_logs['sleep']:
        sleep_records.append({
            'date': s['dateOfSleep'],
            'minutes_asleep': s['minutesAsleep'],
            'sleep_score': s.get('efficiency', 0)
        })

    # 3. Create DataFrames and Save
    df_hr = pd.DataFrame(rhr_records)
    df_sleep = pd.DataFrame(sleep_records)
    
    if not df_sleep.empty:
        df_health = pd.merge(df_hr, df_sleep, on='date', how='outer')
    else:
        df_health = df_hr

    df_health.to_csv('fitbit_health_metrics.csv', index=False)
    
    print("\n--- ✅ Data Pipeline Complete ---")
    print(df_health.tail())