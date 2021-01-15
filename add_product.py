import requests, uuid
from random import randrange

#simulate a product creation event webhook.
#Not all JSON data present for simplicity. Assume data is sent for variant instead of product

variant_id = uuid.uuid4().node
variant_title = "product_{}".format(randrange(100000))
inventory_quantity = randrange(100)

data = {"variant_id": variant_id, 
        "title" : variant_title, 
        "inventory_quantity": inventory_quantity,
        "inventory_item_id": 40022469982830}

r = requests.post("http://127.0.0.1:5000/product_creation_webhook", json = data)

print(r.content)