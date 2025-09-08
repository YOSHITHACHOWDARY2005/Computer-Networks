import requests

url = "https://httpbin.org"

# GET request
try:
    response = requests.get(url + "/get")
    print("GET Status Code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text[:200], "...")  # show first 200 chars
except Exception as e:
    print("GET request failed:", e)

# POST request
try:
    data = {"name": "Yoshi", "number": 42}
    response = requests.post(url + "/post", json=data)
    print("\nPOST Status Code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text[:200], "...")
except Exception as e:
    print("POST request failed:", e)
