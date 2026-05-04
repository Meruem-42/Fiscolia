import json
import requests

url = "http://localhost:8083/api/auth-register"

for i in range(1, 11):
    data = {
        "email": f"test{i}.test@gmail.com",
        "confirm_email": f"test{i}.test@gmail.com",
        "password": f"Test{i}@1234",
        "confirm_password": f"Test{i}@1234",
        "firstname": f"Test{i}",
        "lastname": f"test{i}",
    }
    
    response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
    print(f"test{i} registering - Status: {response.status_code} - {response.text}")


url = "http://localhost:8083/api/auth-login"

for i in range(1, 6):
    data = {
        "email": f"test{i}.test@gmail.com",
        "password": f"Test{i}@1234",
    }

    response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
    print(f"test{i} session - Status: {response.status_code} - {response.text}")



