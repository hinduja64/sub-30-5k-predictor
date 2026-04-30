import pandas as pd
fitbit = pd.read_csv('fitbit_health_metrics.csv')
running = pd.read_csv('running_logs.csv')
master = pd.merge(running, fitbit, on='date', how='outer')
master.to_csv('master_running_data.csv', index=False)
