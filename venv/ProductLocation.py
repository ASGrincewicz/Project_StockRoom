# Aaron Grincewicz — 02/19/2023
"""
Location-Level Inventory Module

This module manages inventory stored within individual stockroom location files.
Each location has its own CSV file stored under:
    StockroomLocations/<LOCATION>.csv

Features:
- Create new location inventory files
- Read and merge product quantities within a location
- Backstock (add) products to a location
- Remove products from a location
- Audit location contents
- Synchronize changes with the MasterInventory module

CSV Format (per location):
Product # | Product Name | Amount
"""

from pathlib import Path
import csv
from MasterInventory import search_by_prod_num, verify_prod_num, update_product_location
import Colorize
import Messages as MSG


def create_new_location_file(location):
    """
    Create a new CSV file for a stockroom location.

    :param location: Location identifier string (e.g., 'LD-01-A-03')
    """
    location_csv = Path(f'StockroomLocations/{location}.csv')
    field_names = ['Product #', 'Product Name', 'Amount']

    if location_csv.exists():
        print(MSG.file_exist())
        return

    with open(location_csv, 'w', newline='') as location_file:
        writer = csv.writer(location_file)
        writer.writerow(field_names)


def overwrite_location_file(location, prod_list, *args):
    """
    Overwrite the location CSV file with updated product quantities.

    :param location: Location identifier
    :param prod_list: Dictionary of products stored in the location
    :param args: amount, product_num — used to update a specific product
    """
    amount = args[0]
    product_num = args[1]

    with open(Path(f'StockroomLocations/{location}.csv'), 'w', newline='') as location_file:
        writer = csv.writer(location_file)
        field_names = ['Product #', 'Product Name', 'Amount']
        writer.writerow(field_names)

        for num in prod_list.keys():
            for name, count in prod_list[num].items():
                # Update only the targeted product
                if int(count) > 0 and product_num == num:
                    writer.writerow([num, name, amount])
                else:
                    writer.writerow([num, name, count])


def read_location_file(location) -> dict:
    """
    Read all products stored in a location CSV file.

    :param location: Location identifier
    :return: Dictionary mapping product numbers to {name: amount}
    """
    products_in_loc_file = dict()
    location_csv = Path(f'StockroomLocations/{location}.csv')

    if not location_csv.exists():
        print(MSG.file_not_found())
        return {}

    product_num = []
    product_name = []
    amount_in_loc = []

    with open(location_csv, 'r', newline='') as location_file:
        reader = csv.DictReader(location_file)

        for col in reader:
            product_num.append(col['Product #'])
            product_name.append(col['Product Name'])
            amount_in_loc.append(col['Amount'])

    # Merge duplicate product entries
    for i, num in enumerate(product_num):
        if num not in products_in_loc_file:
            products_in_loc_file[num] = {product_name[i]: amount_in_loc[i]}
        else:
            current_amount = products_in_loc_file[num][product_name[i]]
            products_in_loc_file[num] = {
                product_name[i]: int(amount_in_loc[i]) + int(current_amount)
            }

    return products_in_loc_file


def audit_location():
    """
    Print all products stored in a location and the total quantity.
    """
    location = MSG.get_location_input()
    prod_in_loc = read_location_file(location)
    product_count = 0

    if len(prod_in_loc) > 0:
        for num in prod_in_loc.keys():
            for prod, amount in prod_in_loc[num].items():
                print(Colorize.colorize_text_orange(f'{num}: {prod}: Amount here: {amount}'))
                product_count += int(amount)

        print(f"Total Located Here: {product_count}")
    else:
        print(MSG.location_empty())


def audit_product():
    """
    TODO: Search all location files for a specific product number.
    """
    pass


def back_stock_product():
    """
    Add product quantity to a location.

    Workflow:
    - Verify product exists in MasterInventory
    - Confirm placement
    - Update MasterInventory location mapping
    - Merge quantities in location file
    """
    location = MSG.get_location_input()
    product_num = MSG.get_prod_num_input()
    amount = MSG.get_amount_input(False)

    location_csv = Path(f'StockroomLocations/{location}.csv')
    if not location_csv.exists():
        print(MSG.file_not_found())
        return

    confirmation = 'N'
    product = None

    while confirmation[0] != 'Y':
        num_to_verify = {product_num}

        if not verify_prod_num(num_to_verify):
            product = search_by_prod_num(product_num)
            print(Colorize.colorize_text_blue(f'{amount} of {product[0]} will be placed in {location}.'))
            confirmation = input('Confirm? Enter Y or N\n').strip().upper()
        else:
            print(MSG.product_not_found())

    update_product_location(True, product_num, location)

    prod_in_loc_file = read_location_file(location)

    # Merge or add new product
    if product_num in prod_in_loc_file:
        for name, count in prod_in_loc_file[product_num].items():
            amount += int(count)
            prod_in_loc_file[product_num] = {name: amount}
    else:
        prod_in_loc_file[product_num] = {product[0]: amount}

    overwrite_location_file(location, prod_in_loc_file, amount, product_num)


def remove_product():
    """
    Remove product quantity from a location.

    If amount < 0, remove all.
    If resulting quantity <= 0, update MasterInventory to remove location mapping.
    """
    location = MSG.get_location_input()
    product_num = MSG.get_prod_num_input()
    amount = MSG.get_amount_input(True)

    prod_in_loc = read_location_file(location)
    prod_count = 0

    if product_num in prod_in_loc:
        for name, count in prod_in_loc[product_num].items():
            initial_count = int(count)

            if amount < 0:
                amount = initial_count  # remove all

            if amount <= initial_count:
                prod_count = initial_count - amount

                if prod_count <= 0:
                    update_product_location(False, product_num, location)

                print(Colorize.colorize_text_blue(f"Taking: {amount} | {name} of {initial_count}"))
            else:
                print(f'This location contains {initial_count}')
                return

    overwrite_location_file(location, prod_in_loc, prod_count, product_num)


def get_product_amount() -> int:
    """
    Return the quantity of a product stored in a location.

    :return: Amount or 0 if not found.
    """
    location = MSG.get_location_input()
    prod_in_loc = read_location_file(location)
    product_num = MSG.get_prod_num_input()

    if product_num in prod_in_loc:
        return prod_in_loc[product_num]

    print(MSG.product_not_found())
    return 0
