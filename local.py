import requests


res = requests.post("http://127.0.0.1:5000/api/accounts/Giver225", json={"password": "2222222"})

print(res.json())
