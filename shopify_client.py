import shopify
import binascii, os, requests, time
from flexstock_product import FlexStockProduct

class ShopifyClient:
    def __init__(self, password, api_version, shop_url):
        self.session = shopify.Session(shop_url, api_version, password)
        shopify.ShopifyResource.activate_session(self.session)

    def get_products(self):
        inventory_location_id = self.get_inventory_location_id()
        variants = shopify.Variant.find()

        flex_stock_products = [FlexStockProduct(variant.id, variant.title, variant.inventory_quantity, variant.inventory_item_id, inventory_location_id) for variant in variants]

        return flex_stock_products

    def get_product(self, product_id):
        inventory_location_id = self.get_inventory_location_id()
        variant = shopify.Variant.find(id_=product_id)[0]
        return FlexStockProduct(variant.id, variant.title, variant.inventory_quantity, variant.inventory_item_id, inventory_location_id)

    def decrease_product_inventory_quantity(self, product, value):
        value = value * -1
        return self.increase_product_inventory_quantity(product, value)

    def increase_product_inventory_quantity(self, product, value):
        product.increase_quantity(value)
        shopify.InventoryLevel.set(product.inventory_location_id, product.inventory_item_id, product.inventory_quantity)
        return product

    def get_inventory_location_id(self):
        return shopify.Location.find()[0].id

