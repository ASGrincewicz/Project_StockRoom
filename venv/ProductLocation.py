# Aaron Grincewicz 02/19/2023
from pathlib import Path
import csv
from MasterInventory import search_by_num, verify_prod_num


class ProductLocation:

    def __init__(self, category, aisle, column, row):
        self.location_id = f'{category}-{aisle}-{column}-{row}'
        self.current_products = dict()
        print(f'{self.location_id} added.')

    def __str__(self):
        return f'{self.category}-{self.aisle}-{self.column}-{self.row}'


file_contents_read = False
current_products = dict()


def create_new_location_file(location):
    path = Path(f'/Users/aarongrincewicz/PycharmProjects/StockRoom/venv/StockroomLocations/{location}.csv')

    field_names = ['Product #', 'Product Name', 'Amount']

    if Path.is_file(path):
        print('File already exists.')
        return
    with open(path, 'w') as location_file:
        writer = csv.writer(location_file)
        writer.writerow(field_names)


def read_location_file():
    current_products.clear()
    location = input('Please enter the location:\n')
    product_num = list()
    product_name = list()
    amount_in_loc = list()
    # products_in_loc = list()
    path = Path(f'/Users/aarongrincewicz/PycharmProjects/StockRoom/venv/StockroomLocations/{location}.csv')
    if Path.is_file(path):
        with open(path, 'r') as location_file:
            reader = csv.DictReader(location_file)

            for col in reader:
                product_num.append(col['Product #'])
                product_name.append(col['Product Name'])
                amount_in_loc.append(col['Amount'])

        i = 0
        for item in product_num:
            if item not in current_products.keys():
                current_products[item] = {product_name[i]: amount_in_loc[i]}
            elif item in current_products.keys():
                current_amount = current_products[item][product_name[i]]
                current_products[item] = {product_name[i]: int(amount_in_loc[i]) + int(current_amount)}
            i += 1

    else:
        print('File not found.')
    for num in current_products.keys():
        for prod, amount in current_products[num].items():
            print(f'{num}: {prod}: Amount here: {amount}')


def add_product():  # Need to read from location file first, then combine amounts if item exists.
    location = input('Enter the location:\n')
    product_id = ''
    amount = 0
    product = None
    path = Path(f'/Users/aarongrincewicz/PycharmProjects/StockRoom/venv/StockroomLocations/{location}.csv')
    confirmation = 'N'
    while confirmation[0] != 'Y':
        product_id = input('Enter the product number:\n').zfill(4)
        amount = input('Enter the amount to back stock:\n')
        if not verify_prod_num(product_id):
            print('Product Found')
            product = search_by_num(product_id)
            print(f'{amount} of {product[0]} will be placed in {location}.')
            confirmation = input('Confirm? Enter Y or N\n').strip().upper()
        else:
            print(f'{product_id} not found.')
    if not Path.is_file(path):
        print('File not found.')
        return
    with open(path, 'a') as location_file:
        writer = csv.writer(location_file)
        writer.writerow([f'{product_id}', f'{product[0]}', f'{amount}'])


def remove_product(product_id, amount):
    if product_id in current_products:
        count = current_products[product_id]
        if amount <= count:
            count -= amount
        else:
            print(f'This location contains {count}')


def get_product_amount(product_id):
    if product_id in current_products:
        return current_products[product_id]
    else:
        print('This product is not here.')
