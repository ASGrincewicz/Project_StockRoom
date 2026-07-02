# Aaron Grincewicz — 02/19/2023
"""
Crash‑proof Master Inventory Module
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
    Return True if ALL product numbers do NOT exist.
    Return False if ANY already exist.
    Crash‑proof: handles malformed inventory and non-digit input.
    """
    for num in nums_to_check:
        padded = num.zfill(4)
        if padded in master_inventory:
            print(f"{num} found.")
            return False
    return True


def add_single_product():
    try:
        prod_name = input('Enter the product name:\n').strip().upper()
        if not prod_name:
            print("Invalid product name.")
            return

        prod_num_input = input('Enter the product number:\n').strip().lower()
        if not prod_num_input.isdigit():
            print("Product number must be digits only.")
            return

        nums_to_verify = {prod_num_input}
        while not verify_prod_num(nums_to_verify):
            prod_num_input = input('Enter a different product number:\n').strip().lower()
            if not prod_num_input.isdigit():
                print("Product number must be digits only.")
                return
            nums_to_verify = {prod_num_input}

        prod_num = prod_num_input.zfill(4)

        try:
            on_hand = int(input('How many are in stock?\n').strip())
        except ValueError:
            print("On-hand count must be a number.")
            return

        new_prod = Product(prod_name, prod_num, on_hand)
        master_inventory[new_prod.product_num] = {new_prod.product_name: new_prod.on_hand_count}
        print(f'{new_prod.product_name} added.')

    except Exception:
        print("Unexpected error adding product.")


def add_multi_product_from_file(products_to_add):
    try:
        nums_to_verify = {p.product_num for p in products_to_add}

        if verify_prod_num(nums_to_verify):
            for product in products_to_add:
                master_inventory[product.product_num] = {
                    product.product_name.upper(): product.on_hand_count
                }
                print(f'{product.product_name.upper()} added.')
        else:
            print("Duplicate product numbers found. Skipping batch import.")

    except Exception:
        print("Error importing multiple products.")


def search_inventory(search_term):
    try:
        results = 0
        for num, name_dict in master_inventory.items():
            for prod_name, count in name_dict.items():
                if search_term.upper() in prod_name:
                    print(f'Product: {prod_name} | Item Number: {num} | On Hand: {count}')
                    results += 1

        print(f'Search Results: {results}')

        if not file_contents_read and results == 0:
            print('Try your search again after importing the Master Inventory file.')

    except Exception:
        print("Error searching inventory.")


def search_by_prod_num(product_num):
    try:
        product_num = product_num.zfill(4)

        if product_num in master_inventory:
            for name, on_hand in master_inventory[product_num].items():
                print(f'Result: {product_num}: {name}, On Hand: {on_hand}')
                return name, on_hand

        print('Item not found.')
        return None

    except Exception:
        print("Error searching by product number.")
        return None


def sort_inventory_by_prod_num() -> list:
    try:
        return sorted(master_inventory.keys())
    except Exception:
        print("Error sorting inventory.")
        return []


def edit_product():
    try:
        product_num = input('Enter the Product number to edit:\n').strip().zfill(4)

        if product_num in master_inventory:
            new_name = input('New Product name:\n').strip().upper()
            if not new_name:
                print("Invalid product name.")
                return

            try:
                new_on_hand = int(input('New On Hand count:\n').strip())
            except ValueError:
                print("On-hand count must be a number.")
                return

            master_inventory[product_num] = {new_name: new_on_hand}
        else:
            print('Product not found. Have you imported the Master Inventory?')

    except Exception:
        print("Error editing product.")


def delete_product():
    try:
        product_num = input('Enter the Product number to delete:\n').strip().zfill(4)
        search_by_prod_num(product_num)

        confirm = input("Confirm deletion? (Y/N):\n").strip().upper()
        if confirm == 'Y':
            master_inventory.pop(product_num, None)
            print(f"Product number {product_num} has been deleted.")
        else:
            print("Deletion canceled.")

    except Exception:
        print("Error deleting product.")


def read_from_master_inventory_csv():
    global file_contents_read

    if not master_inventory_file.exists():
        print('File Not Found.')
        return

    products_to_add = set()

    try:
        with open(master_inventory_file, 'r', newline='') as master_file:
            reader = csv.DictReader(master_file)

            for row in reader:
                try:
                    prod = Product(
                        row.get('Product Name', '').strip(),
                        row.get('Product #', '').strip(),
                        int(row.get('On Hand Count', '0').strip())
                    )
                    products_to_add.add(prod)
                except Exception:
                    print("Malformed CSV row. Skipping.")

        file_contents_read = True
        add_multi_product_from_file(products_to_add)

    except Exception:
        print("Error reading Master Inventory CSV.")


def write_to_master_inventory_csv():
    global file_contents_written

    try:
        field_names = ['Product #', 'Product Name', 'On Hand Count']
        write_mode = 'w' if file_contents_read or not master_inventory_file.exists() else 'a'

        with open(master_inventory_file, write_mode, newline='') as master_file:
            print(f'File open with Write Mode: {write_mode}')
            writer = csv.writer(master_file)

            if write_mode == 'w':
                writer.writerow(field_names)

            for num in sort_inventory_by_prod_num():
                for name, count in master_inventory[num].items():
                    try:
                        writer.writerow([num, name, int(count)])
                    except ValueError:
                        print(f"Invalid count for {num}. Skipping.")

        print('Writing to file completed.')
        file_contents_written = True

    except Exception:
        print("Error writing Master Inventory CSV.")


def update_product_location(add: bool, product_num: str, location: str):
    """
    Legacy placeholder for location tracking.
    Exists only to satisfy ProductLocation imports.
    """
    pass

def select_product_interactively():
    """
    Search for a product by name and let the user select from results.
    Returns (product_num, product_name) or None.
    """
    term = input("Search for product:\n").strip().upper()
    matches = []

    for num, name_dict in master_inventory.items():
        for name, count in name_dict.items():
            if term in name:
                matches.append((num, name, count))

    if not matches:
        print("No products found.")
        return None

    print("\nSelect a product:")
    for i, (num, name, count) in enumerate(matches, start=1):
        print(f"{i}. {name} (#{num}) — On Hand: {count}")

    while True:
        choice = input("Enter number:\n").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(matches):
                num, name, _ = matches[idx - 1]
                return num, name
        print("Invalid selection.")

def select_location_interactively():
    loc_dir = Path("StockroomLocations")
    files = sorted(loc_dir.glob("*.csv"))

    if not files:
        print("No locations found.")
        return None

    print("\nSelect a location:")
    for i, f in enumerate(files, start=1):
        print(f"{i}. {f.stem}")

    while True:
        choice = input("Enter number:\n").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(files):
                return files[idx - 1].stem
        print("Invalid selection.")


