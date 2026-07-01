# Aaron Grincewicz — 02/19/2023
# Master Inventory Module
"""
Master Inventory Module

This module manages product records for a simple stockroom inventory system.
It supports:
- Adding single or multiple products
- Searching by name or product number
- Editing and deleting products
- Reading/writing inventory data to a CSV file

Data Model:
master_inventory = {
    "0001": {"HAMMER": 12},
    "0002": {"WRENCH": 5},
    ...
}

Each product number is zero-padded to 4 digits to maintain consistency.
"""

import csv
from Product import Product
from pathlib import Path

master_inventory_file = Path('master_inventory.csv')

# State flags
file_contents_read = False
file_contents_written = False

# Main inventory dictionary
master_inventory = dict()


def verify_prod_num(nums_to_check) -> bool:
    """
    Check whether the given product numbers exist in master_inventory.

    :param nums_to_check: Iterable of product numbers to verify.
    :return: True if ALL product numbers do NOT exist (safe to add),
             False if ANY product number already exists.
    """
    for num in nums_to_check:
        padded = num.zfill(4)
        if padded in master_inventory:
            print(f"{num} found.")
            return False
    return True


def add_single_product():
    """
    Prompt the user for product details and add a new product to master_inventory.
    Ensures product numbers are unique before adding.
    """
    prod_name = input('Enter the product name:\n').strip().upper()
    prod_num_input = input('Enter the product number:\n').strip().lower()

    nums_to_verify = {prod_num_input}
    while not verify_prod_num(nums_to_verify):
        prod_num_input = input('Enter a different product number:\n').strip().lower()

    prod_num = prod_num_input.zfill(4)
    on_hand = int(input('How many are in stock?\n').strip())

    new_prod = Product(prod_name, prod_num, on_hand)

    master_inventory[new_prod.product_num] = {new_prod.product_name: new_prod.on_hand_count}
    print(f'{new_prod.product_name} added.')


def add_multi_product_from_file(products_to_add):
    """
    Add multiple Product objects to master_inventory.

    :param products_to_add: Iterable of Product instances created from CSV input.
    """
    nums_to_verify = {p.product_num for p in products_to_add}

    if verify_prod_num(nums_to_verify):
        for product in products_to_add:
            master_inventory[product.product_num] = {product.product_name.upper(): product.on_hand_count}
            print(f'{product.product_name.upper()} added.')


def search_inventory(search_term):
    """
    Search master_inventory for products whose names contain the given search term.

    :param search_term: Substring to match against product names.
    """
    results = 0
    for num, name_dict in master_inventory.items():
        for prod_name, count in name_dict.items():
            if search_term.upper() in prod_name:
                print(f'Product: {prod_name} | Item Number: {num} | On Hand: {count}')
                results += 1

    print(f'Search Results: {results}')

    if not file_contents_read and results == 0:
        print('Try your search again after importing the Master Inventory file.')


def search_by_prod_num(product_num):
    """
    Search master_inventory by product number.

    :param product_num: Product number string (will be zero-padded).
    :return: (name, on_hand) tuple if found, otherwise None.
    """
    product_num = product_num.zfill(4)

    if product_num in master_inventory:
        for name, on_hand in master_inventory[product_num].items():
            print(f'Result: {product_num}: {name}, On Hand: {on_hand}')
            return name, on_hand

    print('Item not found.')
    return None


def sort_inventory_by_prod_num() -> list:
    """
    Return a sorted list of product numbers.
    """
    return sorted(master_inventory.keys())


def edit_product():
    """
    Edit an existing product's name and on-hand count.
    """
    product_num = input('Enter the Product number to edit:\n').strip().zfill(4)

    if product_num in master_inventory:
        new_name = input('New Product name:\n').strip().upper()
        new_on_hand = int(input('New On Hand count:\n').strip())
        master_inventory[product_num] = {new_name: new_on_hand}
    else:
        print('Product not found. Have you imported the Master Inventory?')


def delete_product():
    """
    Delete a product from master_inventory after user confirmation.
    """
    product_num = input('Enter the Product number to delete:\n').strip().zfill(4)
    search_by_prod_num(product_num)

    confirm = input("Confirm deletion? (Y/N):\n").strip().upper()
    if confirm == 'Y':
        master_inventory.pop(product_num, None)
        print(f"Product number {product_num} has been deleted.")
    else:
        print("Deletion canceled.")


def read_from_master_inventory_csv():
    """
    Read inventory data from master_inventory.csv and populate master_inventory.
    """
    if not master_inventory_file.exists():
        print('File Not Found.')
        return

    products_to_add = set()

    with open(master_inventory_file, 'r', newline='') as master_file:
        reader = csv.DictReader(master_file)

        for row in reader:
            prod = Product(
                row['Product Name'],
                row['Product #'],
                int(row['On Hand Count'])
            )
            products_to_add.add(prod)

    global file_contents_read
    file_contents_read = True

    add_multi_product_from_file(products_to_add)


def write_to_master_inventory_csv():
    """
    Write the current master_inventory to master_inventory.csv.

    If the file was previously read, overwrite it.
    Otherwise, append or create a new file.
    """
    field_names = ['Product #', 'Product Name', 'On Hand Count']
    write_mode = 'w' if file_contents_read or not master_inventory_file.exists() else 'a'

    with open(master_inventory_file, write_mode, newline='') as master_file:
        print(f'File open with Write Mode: {write_mode}')
        writer = csv.writer(master_file)

        if write_mode == 'w':
            writer.writerow(field_names)

        for num in sort_inventory_by_prod_num():
            for name, count in master_inventory[num].items():
                writer.writerow([num, name, count])

    print('Writing to file completed.')
    global file_contents_written
    file_contents_written = True
