__author__ = 'Administrator'

import requests

response = requests.get(url='http://127.0.0.1:8000/api/asset.html',headers={"OpenKey":"e05eec4bf729b80e6d60cfec01ff0e30|1501474102.8840663"})
print(response.text)