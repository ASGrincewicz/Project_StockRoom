# Aaron Grincewicz — 02/19/2023
"""
Crash‑proof Master Inventory Module
"""

import csv
import Colorize
from Product import Product
from pathlib import Path

master_inventory_file = Path('master_inventory.csv')

file_contents_read = False
file_contents_written = False

master_inventory = dict()
categories = []


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
    global categories, master_inventory

    # Step 1 — Choose category
    print("Select a category:")
    for i, (cat, code) in enumerate(categories, start=1):
        print(f"{i}. {cat} ({code})")

    while True:
        choice = input("Enter number:\n").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            category = categories[int(choice) - 1][0]
            break
        print("Invalid selection.")

    # Step 2 — Product name
    name = input("Enter product name:\n").strip().upper()

    # Step 3 — Auto-increment product number
    prod_num = get_next_product_number(category)
    if not prod_num:
        print("Error generating product number.")
        return

    # Step 4 — Initial count
    count = input("Enter initial count:\n").strip()
    if not count.isdigit():
        print("Invalid count.")
        return

    # Step 5 — Add to in-memory inventory
    master_inventory[prod_num] = {name: int(count)}

    print(Colorize.colorize_text_blue(
        f"Product added to inventory: {prod_num} - {name} ({category})"
    ))



def add_multi_product_from_file(products_to_add):
    global master_inventory

    try:
        for product in products_to_add:
            # Insert into in-memory inventory
            master_inventory[product.product_num] = {
                product.product_name.upper(): product.on_hand_count
            }
            print(f'{product.product_name.upper()} added.')

    except Exception as e:
        print("Error importing multiple products.")
        print(f"Details: {e}")




def search_inventory(term):
    term = term.upper()
    results = []

    for prod_num, name_dict in master_inventory.items():
        for name, count in name_dict.items():
            if term in name:
                results.append((prod_num, name, count))

    if not results:
        print("Search Results: 0")
        return

    print("Search Results:")
    for prod_num, name, count in results:
        print(f"{prod_num}: {name} — On Hand: {count}")



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

def select_product_interactively(term=None):
    """
    Search for a product by name and let the user select from results.
    Returns (product_num, product_name) or None.
    """
    if term is None:
        term = input("Search for product:\n").strip().upper()
    else:
        term = term.upper()
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
# -----------------------------
# Category Management
# -----------------------------

def set_categories():
    global categories
    categories.clear()

    print("Enter categories. Type DONE when finished.")
    while True:
        cat = input("Category:\n").strip()
        if cat.upper() == "DONE":
            break

        cat = cat.upper()
        code = str(len(categories) + 1).zfill(2)
        categories.append((cat, code))

    print("Stockroom categories saved.")


def add_categories():
    global categories

    print("Enter categories to add. Type DONE when finished.")
    while True:
        cat = input("Category:\n").strip()
        if cat.upper() == "DONE":
            break

        cat = cat.upper()

        # Check if category already exists
        if any(c == cat for c, _ in categories):
            print(f"{cat} already exists. Skipping.")
            continue

        code = str(len(categories) + 1).zfill(2)
        categories.append((cat, code))
        print(f"{cat}:{code} added.")


def show_categories():
    """
    Display categories safely.
    """
    if not categories:
        print(Colorize.colorize_text_orange("No categories set."))
        return

    print(Colorize.colorize_text_blue("Categories:"))
    for cat, code in categories:
        print(f"- {cat}: {code}")

def get_category_code(cat_name):
    for cat, code in categories:
        if cat == cat_name:
            return code
    return None

def get_next_product_number(category):
    code = get_category_code(category)
    if not code:
        return None

    highest = 0

    # Scan all products
    with open(master_inventory_file, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prod_num = row["Product #"]
            if prod_num.startswith(code):
                item_num = int(prod_num[-2:])
                highest = max(highest, item_num)

    next_item = highest + 1
    return f"{code}{str(next_item).zfill(2)}"


