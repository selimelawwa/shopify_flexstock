import requests

#simulate a order paid event webhook. Not all JSON data present for simplicity

data = {"variant_id": "37929234137262", "quantity" : 3}
r = requests.post("http://127.0.0.1:5000/order_webhook", json = data)

print(r.content)