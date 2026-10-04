import requests

BASE = "http://127.0.0.1:8000"

print(requests.get(f"{BASE}/health").json())

response = requests.post(
    f"{BASE}/chat",
    json={"messages": [{"role": "user", "content": "Olá, tudo bem?"}]},
)
print(response.status_code)
print(response.json())
