# Aaron Grincewicz 02/19/2023

class ProductLocation:

    def __init__(self, category, aisle, column, row):
        self.location_id = f'{category}-{aisle}-{column}-{row}'
        self.current_products = dict()
        print(f'{self.location_id} added.')

    def __str__(self):
        return f'{self.category}-{self.aisle}-{self.column}-{self.row}'

    def get_location_id(self):
        return self.location_id

    def add_product(self, product_id, amount):
        if product_id not in self.current_products:
            self.current_products[product_id] = amount

    def remove_product(self, product_id, amount):
        if product_id in self.current_products:
            count = self.current_products[product_id]
            if amount <= count:
                count -= amount
            else:
                print(f'This location contains {count}')

    def show_products(self):
        if len(self.current_products) > 0:
            print(f'{self.location_id} contains:')
            for key, value in self.current_products.items():
                print(f'{key}: {value}')

    def get_product_amount(self, product_id):
        if product_id in self.current_products:
            return self.current_products[product_id]
        else:
            print('This product is not here.')
