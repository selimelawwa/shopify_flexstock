This is a basic flask app to integrate with shopify admin api: [https://shopify.dev/docs/admin-api]
To run the app, type [python server.py] in the command line

Open http://localhost:5000/ in the browser you will find list of shopify product variants as JSON

To simulate a shopify order paid/completed webhook, run python order.py
To simulate a shopify new product/variant created webhook, run python add_product.py

You increase inventory for a certain variant by running: python increase_inventory.py

FlexStockProduct class represents shopify variant in our app and contain all needed info for our app purposes
ShopifyClient class handles all api calls to shopify
Shopify Python API [https://github.com/Shopify/shopify_python_api] is used to connect to shopify admin api