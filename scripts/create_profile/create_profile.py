import json
import requests
import pandas as pd

# Use the Docker service name instead of localhost for container-to-container communication
url = "http://backend-auth:8000/api/edit-profile"


with open("dataset.csv") as f:
    data = pd.read_csv(f)

print("DEBUG CREATE PROFILES")
print(data)
col_names = data.columns
for index, row in data.iterrows():
        data = {
            "etat_civil": str(row[col_names[1]]),
            "quotient_familial": str(row[col_names[2]]),
            "situation_specifique": str(row[col_names[3]]),
            "rni": str(row[col_names[4]]),
            "csp": str(row[col_names[5]]),
        }
        response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        print(f"test{index} registering profiles - Status: {response.status_code} - {response.text}")




