import requests
import json

url = "https://kystdatahuset.no/ws/api/auth/login"
headers = {"accept": "*/*", "Content-Type": "application/json"}
payload = {"username": "christian.lura@nrk.no", "password": "0ns3gur1"}

response = requests.post(url, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    # Suksess
    #print(response.json())
    token = response.json()["data"]["JWT"]
    print(f"Nøkkel: {token}")
    with open("token.txt", "w") as f:
        f.write(token)
    print("Nøkkel lagret i filen token.txt")
else:
    # Authentication failed
    print(f"Autentisering feilet med statuskode {response.status_code}")