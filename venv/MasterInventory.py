# Aaron Grincewicz 02/19/2023
# Master Inventory Module
"""
Contains functions and variables to manage products in inventory.
"""

import csv
from Product import Product
from pathlib import Path

master_inventory_file = Path('master_inventory.csv')
file_contents_read = False
file_contents_written = False
master_inventory = dict()


def verify_prod_num(nums_to_check) -> bool:
    """
    Searches the master_inventory dictionary for a key equal to the specified product number.
    :param nums_to_check: Product number to verify
    :return: True if key does not exist, False otherwise.
    """
    for num in nums_to_check:
        if num.zfill(4) not in master_inventory.keys():
            return True
        else:
            print(f"{num} found.")
            return False


def add_single_product():
    """
    Adds a new product to the master inventory dictionary.
    """
    prod_name = input('Enter the product name:\n').strip().upper()
    prod_num_input = input('Enter the product number:\n').strip().lower()
    # prod_num = ''
    nums_to_verify = {prod_num_input}
    while not verify_prod_num(nums_to_verify):
        prod_num_input = input('Enter the product number:\n').strip().lower()
    else:
        prod_num = prod_num_input

    # on_hand = int(input('How many are in stock?\n').strip().lower())
    locations = set()
    new_prod = Product(prod_name, prod_num, locations)
    if verify_prod_num(new_prod.product_num):
        master_inventory[new_prod.product_num] = {new_prod.product_name.upper(): new_prod.current_locations}
        print(f'{new_prod.product_name.upper()} added.')


def add_multi_product_from_file(products_to_add):
    """
    Called when the inventory csv file is read. Adds each product to the master inventory list.
    :param products_to_add: A list of products created from the csv file read.

    """
    nums_to_verify = set()
    for num in products_to_add.keys():
        nums_to_verify.add(num)

    if verify_prod_num(nums_to_verify):
        global master_inventory
        master_inventory = products_to_add


def search_inventory(search_term):
    """
    Allows user to search the master inventory for the string entered.

    Outputs a list of all products in which the name contains the string.
    :param search_term: The string to search product names for.
    """
    results = 0
    print("RESULTS:")
    print("___________________________________________________")
    for num, name in master_inventory.items():
        for prod_name in master_inventory[num].keys():
            if search_term in prod_name:
                print(
                    f'+ {prod_name.upper()} | Item Number: {num} \nLocations:\n{master_inventory[num][prod_name]}')
                print("---------------------------------------------------")
                results += 1
    print(f'Search Results: {results}')
    print("___________________________________________________")
    if not file_contents_read and results == 0:
        print('Try your search again after importing the contents of the Master Inventory file')


def search_by_prod_num(product_num):
    """
    Allows user to search the master inventory by product number.
    :param product_num: Product number.
    :return: Returns a tuple of the product name and on hand count.
    """
    product_num = product_num.zfill(4)
    if product_num in master_inventory.keys():
        for name, locations in master_inventory[product_num].items():
            return name, locations
    else:
        print('Item not found.')
        return None


def sort_inventory_by_prod_num() -> list:
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
        for name in master_inventory[product_num].keys():
            locations = master_inventory[product_num][name]
            new_prod_name = input('What is the new Product name?\n').strip().upper()
            # new_on_hand = int(input('How many are On Hand?\n').strip().lower())
            master_inventory.update({product_num: {new_prod_name: locations}})
    else:
        print('Product not found. Have you imported the Master Inventory?')


def update_product_location(add_take, product_num, location):
    if product_num in master_inventory.keys():
        num_key = master_inventory[product_num]
        for name in num_key.keys():
            name_key = num_key[name]
            if add_take:
                if name_key == '' or name_key == "UNLOCATED":
                    master_inventory[product_num] = {name: f"{location}"}
                else:
                    master_inventory[product_num] = {name: f"{name_key}\n{location}"}
            elif not add_take:
                if location in name_key:
                    adjusted_key = name_key.replace(location, '')
                    master_inventory[product_num] = {name: adjusted_key.strip('\n')}


def delete_product():
    product_num = input('Please enter the Product number of the item you want to edit.\n').strip().zfill(4)
    search_by_prod_num(product_num)
    print("Confirm deletion? Enter 'Y' for Yes, 'N' for No:\n")
    confirm = input().strip().upper()
    if confirm == 'Y':
        master_inventory.pop(product_num)
    else:
        return
    if verify_prod_num(product_num):
        print(f"Product number {product_num} has been deleted.")
    else:
        print(f"An error occurred.")


def edit_loc_string(to_edit) -> str:
    loc = to_edit
    replaced = ["\'", "[", "]", "."]
    edited_loc = ""
    for i in loc:
        if i not in replaced:
            edited_loc += i

    return edited_loc


def read_from_master_inventory_csv():
    product_num = list()
    product_name = list()
    # on_hand_count = list()
    locations = list()
    products_to_add = dict()

    if master_inventory_file.exists():
        with open('master_inventory.csv', 'r', newline='') as master_file:
            reader = csv.DictReader(master_file)

            for col in reader:
                if col not in product_num:
                    product_num.append(col['Product #'])
                if col not in product_name:
                    product_name.append(col['Product Name'])
                # on_hand_count.append(col['On Hand Count'])
                if col not in locations:
                    locations.append(edit_loc_string(col['Locations']))

        i = 0
        for item in product_num:
            products_to_add[item] = {product_name[i]: locations[i]}
            i += 1
        global file_contents_read
        file_contents_read = True
        add_multi_product_from_file(products_to_add)
    else:
        print('File Not Found.')


def write_to_master_inventory_csv():
    field_names = ['Product #', 'Product Name', 'Locations']
    write_mode = 'a'
    if file_contents_read or not master_inventory_file.exists():
        write_mode = 'w'
    with open(master_inventory_file, write_mode, newline='') as master_file:
        print(f'File open with Write Mode: {write_mode}')
        writer = csv.writer(master_file)
        if write_mode == 'w':
            writer.writerow(field_names)
        for num in sort_inventory_by_prod_num():
            for name, loc in master_inventory[num].items():
                writer.writerow([f'{num}', f'{name}', f'{loc}'])
    print('Writing to file completed.')
    global file_contents_written
    file_contents_written = True
