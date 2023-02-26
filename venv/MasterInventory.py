# Aaron Grincewicz 02/19/2023
# Master Inventory Module
"""
Contains functions and variables to manage products in inventory.
"""

import csv
from Product import Product
from pathlib import Path

file_contents_read = False
file_contents_written = False
master_inventory = dict()


def verify_prod_num(num) -> bool:
    """
    Searches the master_inventory dictionary for a key equal to the specified product number.
    :param num: Product number to verify
    :return: True if key does not exist, False otherwise.
    """
    if num.zfill(4) not in master_inventory.keys():
        return True


def add_single_product():
    """
    Adds a new product to the master inventory dictionary.
    """
    prod_name = input('Enter the product name:\n').strip().upper()
    prod_num_input = input('Enter the product number:\n').strip().lower()
    # prod_num = ''
    while not verify_prod_num(prod_num_input):
        prod_num_input = input('Enter the product number:\n').strip().lower()
    else:
        prod_num = prod_num_input

    on_hand = int(input('How many are in stock?\n').strip().lower())
    new_prod = Product(prod_name, prod_num, on_hand)
    if verify_prod_num(new_prod.product_num):
        master_inventory[new_prod.product_num] = {new_prod.product_name.upper(): new_prod.on_hand_count}
        print(f'{new_prod.product_name.upper()} added.')
    else:
        print(f'{new_prod.product_num} already exists.')


def add_multi_product_from_file(products_to_add):
    """
    Called when the inventory csv file is read. Adds each product to the master inventory list.
    :param products_to_add: A list of products created from the csv file read.

    """
    for product in products_to_add:
        if verify_prod_num(product.product_num):
            master_inventory[product.product_num] = {product.product_name.upper(): product.on_hand_count}
            print(f'{product.product_name.upper()} added.')
        else:
            print(f'{product.product_num} already exists.')


def search_inventory(search_term):
    """
    Allows user to search the master inventory for the string entered.

    Outputs a list of all products in which the name contains the string.
    :param search_term: The string to search product names for.
    """
    results = 0
    for num, name in master_inventory.items():
        for prod_name in master_inventory[num].keys():
            if search_term in prod_name:
                print(
                    f'Product:{prod_name.upper()}\\Item Number:{num}\\On Hand Count:{master_inventory[num][prod_name]}')
                results += 1
    print(f'Search Results: {results}')
    if not file_contents_read and results == 0:
        print('Try your search again after importing the contents of the Master Inventory file')


def search_by_num(num):
    """
    Allows user to search the master inventory by product number.
    :param num: Product number.
    :return: Returns a tuple of the product name and on hand count.
    """
    num = num.zfill(4)
    if num in master_inventory.keys():
        for name, on_hand in master_inventory[num].items():
            print(f'Result:{num}: {name}, On Hand: {on_hand}')
            return name, on_hand
    else:
        print('Item not found.')
        return None


def sort_inventory_by_num():
    """
    Returns the master inventory list sorted by product number.
    :return:
    """
    return sorted(master_inventory.keys())


def edit_product():
    """
    Allows user to edit product name and on hand count after searching by product number.

    """
    product_num = input('Please enter the Product number of the item you want to edit.\n').strip().zfill(4)
    if product_num in master_inventory.keys():
        new_prod_name = input('What is the new Product name?\n').strip().lower()
        new_on_hand = int(input('How many are On Hand?\n').strip().lower())
        master_inventory.update({product_num: {new_prod_name: new_on_hand}})
    else:
        print('Product not found. Have you imported the Master Inventory?')


def read_from_master_inventory_csv():
    product_num = list()
    product_name = list()
    on_hand_count = list()
    products_to_add = list()

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
            products_to_add.append(prod)
            i += 1
        global file_contents_read
        file_contents_read = True
        add_multi_product_from_file(products_to_add)
    else:
        print('File Not Found.')


def write_to_master_inventory_csv():
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
        for num in sort_inventory_by_num():
            for name, count in master_inventory[num].items():
                writer.writerow([f'{num}', f'{name}', f'{count}'])
    print('Writing to file completed.')
    global file_contents_written
    file_contents_written = True
