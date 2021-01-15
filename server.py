from flask import Flask, request, Response, jsonify
from shopify_client import ShopifyClient
from flexstock_product import FlexStockProduct
import json

app = Flask(__name__)

PASSWORD = "PASSWORD"
API_VERSION = '2021-01'
SHOP_URL = "flexstock-selim.myshopify.com"

# Simulate a database. Products stored in memory in this variable as a db.
PRODUCTS_DB = ShopifyClient(PASSWORD, API_VERSION, SHOP_URL).get_products()
print(PRODUCTS_DB)


@app.route('/', methods=['GET'])
def index():
    return jsonify([product.__dict__ for product in PRODUCTS_DB])

#Every time a product is added at shopify we can add it here
@app.route('/product_creation_webhook', methods=['POST'])
def handle_new_shopify_product():
    client = ShopifyClient(PASSWORD, API_VERSION, SHOP_URL)
    inventory_location_id = client.get_inventory_location_id()
    json_params = request.get_json()

    id = json_params.get("variant_id")
    title = json_params.get("title")
    inventory_quantity = json_params.get("inventory_quantity")
    inventory_item_id = json_params.get("inventory_item_id")

    product = FlexStockProduct(id, title, inventory_quantity, inventory_item_id, inventory_location_id)

    print("Product [{}] was added".format(product))
    PRODUCTS_DB.append(product)

    print("PRODUCTS_DB after adding product: [{}]".format(product.name))
    print(PRODUCTS_DB)

    return jsonify(product=product.__dict__, error=None)

#This is should be called from FlexStock APP
@app.route('/increase_inventory', methods=['POST'])
def increase_inventory():
    client = ShopifyClient(PASSWORD, API_VERSION, SHOP_URL)
    json_params = request.get_json()

    product_id = json_params.get("variant_id")
    quantity = json_params.get("quantity")

    product = next((p for p in PRODUCTS_DB if str(p.id) == str(product_id)), None)

    try:
        client.increase_product_inventory_quantity(product, quantity)
    except Exception:
        error_message = "Could not update product [{}] inventory quantity".format(product.name)
        print(error_message)
        return jsonify(product=product.__dict__, error=error_message)

    print("Product [{}] inventory quantity after update is: {}".format(product.name, product.inventory_quantity))

    return jsonify(product=product.__dict__, error=None)


#to test webhooks on localhost we need to expose localhost server to internet 
# we can use: https://dashboard.ngrok.com/get-started/setup to do so
#and run ./ngrok http 5000 from the command line
#ngrok only support http, shopify require https
@app.route('/order_webhook', methods=['POST'])
def handle_order_received():
    client = ShopifyClient(PASSWORD, API_VERSION, SHOP_URL)
    json_params = request.get_json()
    product_id = json_params.get("variant_id")
    quantity = json_params.get("quantity")

    product = next((p for p in PRODUCTS_DB if str(p.id) == str(product_id)), None)

    #If product not found in db try get it from shopify
    #This can happen in the case our server was down when shopify sent a webhook to add a product
    if not product:
        try:
            product = client.get_product(product_id)
            PRODUCTS_DB.append(product)
        except Exception:
            error_message = "Product with id: {} is not found, please verify product id".format(product_id)
            print(error_message)
            return jsonify(product=None, error=error_message)
    
    print("Order receieved for product: {} - current inventory quantity: {}, order quantity: {}".format(product.name, product.inventory_quantity ,quantity))
    #We assume product is delivered instantly so inventory_quantity should be updated instantly
    try:
        client.decrease_product_inventory_quantity(product, quantity)
    except Exception as e:
        error_message = str(e.message)
        print(error_message)
        return jsonify(product=product.__dict__, error=error_message)
    
    print("Product inventory quantity after order delivery: {}".format(product.inventory_quantity))

    return jsonify(product=product.__dict__, error=None)

if __name__ == "__main__":
    app.run()