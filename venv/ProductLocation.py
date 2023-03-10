# Aaron Grincewicz 02/19/2023
from pathlib import Path
import csv
from MasterInventory import search_by_prod_num, verify_prod_num, update_product_location


def get_location_input() -> str:
    location = input('Please enter the location:\n').strip().upper()
    return location


def get_prod_num_input() -> str:
    prod_num = input('Enter the product number:\n').zfill(4)
    return prod_num


def get_amount_input(take) -> int:
    amount = 0
    if take:
        amount = int(input('Enter the amount to take (To take all enter a negative integer):\n'))
    elif not take:
        amount = int(input('Enter the amount to back stock:\n'))
    return amount


def create_new_location_file(location):
    location_csv = Path(f'StockroomLocations/{location}.csv')

    field_names = ['Product #', 'Product Name', 'Amount']

    if location_csv.exists():
        print('File already exists.')
        return
    with open(location_csv, 'w', newline='') as location_file:
        writer = csv.writer(location_file)
        writer.writerow(field_names)
        return


def overwrite_location_file(location, prod_list, *args):
    prod_in_loc_file = prod_list
    amount = args[0]

    with open(Path(f'StockroomLocations/{location}.csv'), 'w', newline='') as location_file:
        writer = csv.writer(location_file)
        field_names = ['Product #', 'Product Name', 'Amount']
        writer.writerow(field_names)
        for num in prod_in_loc_file.keys():
            for name, count in prod_in_loc_file[num].items():
                if int(count) > 0:
                    writer.writerow([f'{num}', f'{name}', f'{amount}'])
        return


def read_location_file(location) -> dict:
    products_in_loc_file = dict()

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
            if item not in products_in_loc_file.keys():
                products_in_loc_file[item] = {product_name[i]: amount_in_loc[i]}
            elif item in products_in_loc_file.keys():
                current_amount = products_in_loc_file[item][product_name[i]]
                products_in_loc_file[item] = {product_name[i]: int(amount_in_loc[i]) + int(current_amount)}
            i += 1
        return products_in_loc_file
    else:
        print('File not found.')
        return dict()


def audit_location():
    location = get_location_input()
    prod_in_loc = read_location_file(location)
    product_count = 0
    if len(prod_in_loc) > 0:
        for num in prod_in_loc.keys():
            for prod, amount in prod_in_loc[num].items():
                print(f'{num}: {prod}: Amount here: {amount}')
                product_count = product_count + int(amount)
        print(f"Total Located Here: {product_count}")
    else:
        print(f"{location} does not contain any products.")


def audit_product():
    # Search all location files for product number
    # add each location to list
    #
    pass


def back_stock_product():
    # Need to read from location file first, then combine amounts if item exists.
    location = get_location_input()
    product_num = get_prod_num_input()
    amount = get_amount_input(False)
    product = None
    location_csv = Path(f'StockroomLocations/{location}.csv')
    if not location_csv.exists():
        print('File not found.')
        return
    confirmation = 'N'
    while confirmation[0] != 'Y':
        num_to_verify = {product_num}
        if not verify_prod_num(num_to_verify):
            product = search_by_prod_num(product_num)
            print(f'{amount} of {product[0]} will be placed in {location}.')
            confirmation = input('Confirm? Enter Y or N\n').strip().upper()
        else:
            print(f'{product_num} not found.')

    update_product_location(True, product_num, location)
    prod_in_loc_file = read_location_file(location)
    if product_num in prod_in_loc_file.keys():
        for name, count in prod_in_loc_file[product_num].items():
            amount += int(count)
            prod_in_loc_file[product_num] = {name: amount}
    elif product_num not in prod_in_loc_file.keys():
        prod_in_loc_file[product_num] = {product[0]: amount}

    overwrite_location_file(location, prod_in_loc_file, amount)


def remove_product():
    location = get_location_input()
    product_num = get_prod_num_input()
    amount = get_amount_input(True)
    prod_in_loc = read_location_file(location)
    prod_count = 0
    if product_num in prod_in_loc.keys():
        for name, count in prod_in_loc[product_num].items():
            prod_name = name
            initial_count = int(count)
            if amount < 0:
                amount = initial_count  # remove all
            if amount <= int(initial_count):
                prod_count = initial_count - amount
                if prod_count <= 0:
                    update_product_location(False, product_num, location)
                print(f"Taking: {amount}| {prod_name} of {initial_count}")
            else:
                print(f'This location contains {initial_count}')
                return
    overwrite_location_file(location, prod_in_loc, prod_count)


def get_product_amount() -> int:
    location = get_location_input()
    prod_in_loc = read_location_file(location)
    product_num = get_prod_num_input()
    if product_num in prod_in_loc:
        return prod_in_loc[product_num]
    else:
        print('This product is not here.')
        return 0
