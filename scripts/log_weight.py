import csv
import os
from datetime import datetime

def log_weight():
    # 1. Get current date
    date = datetime.now().strftime('%Y-%m-%d')
    
    # 2. Get weight input
    try:
        weight = float(input("Enter current weight in kg: "))
    except ValueError:
        print("❌ Invalid input. Please enter a number (e.g., 75.8).")
        return

    file_path = 'my_secrets.csv'
    file_exists = os.path.isfile(file_path)

    # 3. Append to the secret CSV
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        # Add header if the file is being created for the first time
        if not file_exists:
            writer.writerow(['date', 'weight_kg'])
        
        writer.writerow([date, weight])
        print(f"✅ Logged {weight}kg for {date} in my_secrets.csv")

if __name__ == "__main__":
    log_weight()