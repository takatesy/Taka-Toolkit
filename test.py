import requests

url = "http://httpbin.org/admin"
response = requests.get(url, timeout=3)
print(response.status_code)