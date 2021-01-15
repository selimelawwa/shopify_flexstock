import shopify

class FlexStockProduct:
    def __init__(self, id, title, inventory_quantity, inventory_item_id, inventory_location_id):
        self.id = id 
        self.name = title
        self.inventory_quantity = inventory_quantity
        self.inventory_item_id = inventory_item_id
        self.inventory_location_id = inventory_location_id

    def increase_quantity(self, change):
        if self.inventory_quantity + change < 0:
            raise Exception("Inventory quantity can not be less than 0")
        self.inventory_quantity+=change

    def __str__(self):
        return "Product Name: {} - ID: {} - Inventory Quantity: {} - Inventory Item Id: {}".format(self.name, self.id, self.inventory_quantity, self.inventory_item_id)

    def __repr__(self):
        return self.__str__()
    
    def __iter__(self):
        for key in self.__dict__:
            yield key, getattr(self, key)