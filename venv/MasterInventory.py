# Aaron Grincewicz 02/19/2023
import csv
from Product import Product
from pathlib import Path

file_contents_read = False
file_contents_written = False


class MasterInventory:

    def __init__(self, inv_name):
        self.master_inventory = dict()
        self.name = inv_name

    def get_inventory(self):
        return self.master_inventory

    def get_write_status(self):
        return file_contents_written

    def verify_prod_num(self, num) -> bool:
        if num.zfill(4) not in self.master_inventory.keys():
            return True

    def add_single_product(self, product):
        if self.verify_prod_num(product.product_num):
            self.master_inventory[product.product_num] = {product.product_name.upper(): product.on_hand_count}
            print(f'{product.product_name.upper()} added.')
        else:
            print(f'{product.product_num} already exists.')

    def add_multi_product(self, products_to_add):  # parameter is a list of products.
        for product in products_to_add:
            self.add_single_product(product)

    def search_inventory(self, search_term):  # Searches master inventory by string.
        results = 0
        for num, name in self.master_inventory.items():
            for prod_name in self.master_inventory[num].keys():
                if search_term in prod_name:
                    print(
                        f'Product:{prod_name.upper()}\\Item Number:{num}\\On Hand Count:{self.master_inventory[num][prod_name]}')
                    results += 1
        print(f'Search Results: {results}')
        if not file_contents_read and results == 0:
            print('Try your search again after importing the contents of the Master Inventory file')

    def search_by_num(self, num):  # Searches inventory by product number.
        if num in self.master_inventory.keys():
            for name, on_hand in self.master_inventory[num].items():
                print(f'Result:{num}: {name}, On Hand: {on_hand}')
        else:
            print('Item not found.')

    def sort_inventory_by_num(self):
        return sorted(self.master_inventory.keys())

    def edit_product(self):
        product_num = input('Please enter the Product number of the item you want to edit.\n').strip().zfill(4)
        if product_num in self.master_inventory.keys():
            new_prod_name = input('What is the new Product name?\n').strip().lower()
            new_on_hand = int(input('How many are On Hand?\n').strip().lower())
            self.master_inventory.update({product_num: {new_prod_name: new_on_hand}})
        else:
            print('Product not found. Have you imported the Master Inventory?')

    def read_from_csv(self):
        product_num = list()
        product_name = list()
        on_hand_count = list()

        path = Path('/Users/aarongrincewicz/PycharmProjects/StockRoom/venv/master_inventory.csv')
        if Path.is_file(path):
            with open('master_inventory.csv', 'r') as master_file:
                reader = csv.DictReader(master_file)

                for col in reader:
                    product_num.append(col['Product #'])
                    product_name.append(col['Product Name'])
                    on_hand_count.append(col['On Hand Count'])

            i = 0
            for item in product_num:
                prod = Product(f'{product_name[i]}', f'{item}', f'{on_hand_count[i]}')
                self.add_single_product(prod)
                i += 1
            global file_contents_read
            file_contents_read = True
        else:
            print('File Not Found.')

    def write_to_csv(self):
        path = Path('/Users/aarongrincewicz/PycharmProjects/StockRoom/venv/master_inventory.csv')
        field_names = ['Product #', 'Product Name', 'On Hand Count']
        write_mode = 'a'
        if file_contents_read or not Path.is_file(path):
            write_mode = 'w'
        with open(path, write_mode) as master_file:
            print(f'File open with Write Mode: {write_mode}')
            writer = csv.writer(master_file)
            if write_mode == 'w':
                writer.writerow(field_names)
            for num in self.sort_inventory_by_num():
                for name, count in self.master_inventory[num].items():
                    writer.writerow([f'{num}', f'{name}', f'{count}'])
        print('Writing to file completed.')
        global file_contents_written
        file_contents_written = True
