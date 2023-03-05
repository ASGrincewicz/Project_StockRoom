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
    location_csv = Path(f'StockroomLocations/{location}.csv')

    field_names = ['Product #', 'Product Name', 'Amount']

    if location_csv.exists():
        print('File already exists.')
        return
    with open(location_csv, 'w', newline='') as location_file:
        writer = csv.writer(location_file)
        writer.writerow(field_names)


def read_location_file(location):
    current_products.clear()

    product_num = list()
    product_name = list()
    amount_in_loc = list()
    # products_in_loc = list()
    location_csv = Path(f'StockroomLocations/{location}.csv')
    if location_csv.exists():
        with open(location_csv, 'r', newline='') as location_file:
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


def audit_location():
    location = input('Please enter the location:\n')
    read_location_file(location)
    if len(current_products) > 0:
        for num in current_products.keys():
            for prod, amount in current_products[num].items():
                print(f'{num}: {prod}: Amount here: {amount}')
    else:
        print(f"{location} does not contain any products.")

def back_stock_product():  # Need to read from location file first, then combine amounts if item exists.
    location = input('Enter the location:\n')
    product_id = ''
    amount = 0
    product = None
    location_csv = Path(f'StockroomLocations/{location}.csv')
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
    if not location_csv.exists():
        print('File not found.')
        return
    with open(location_csv, 'a', newline='') as location_file:
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
