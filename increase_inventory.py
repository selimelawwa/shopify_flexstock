import requests

#increase_inventory for a certain variant

data = {"variant_id": "37929234137262", "quantity" : 10}
r = requests.post("http://127.0.0.1:5000/increase_inventory", json = data)

print(r.content)