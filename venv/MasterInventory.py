# Aaron Grincewicz — 02/19/2023
"""
Crash‑proof Master Inventory Module
"""

import csv
import os

import Colorize
from Product import Product
from pathlib import Path

master_inventory_file = Path('master_inventory.csv')

file_contents_read = False
file_contents_written = False

master_inventory = dict()
categories = []

# Imported after `categories` is defined so the circular chain
# (MasterStockRoom -> MasterInventory -> ProductLocation -> MasterStockRoom)
# can resolve `from MasterInventory import categories` regardless of entry point.
# ProductLocation is only referenced at call time, so a late import is safe.
import ProductLocation

def user_input(prompt):
    value = input(prompt).strip()
    if value.upper() in ("X", "CANCEL", "BACK"):
        raise KeyboardInterrupt
    return value

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
    print(f"{len(categories) + 1}. New Category")

    while True:
        choice = user_input("Enter number:\n").strip()

        if choice.isdigit():
            choice = int(choice)

            # Existing category
            if 1 <= choice <= len(categories):
                category = categories[choice - 1][0]
                break

            # New category option
            elif choice == len(categories) + 1:
                new_cat = input("Enter new category name:\n").strip().upper()

                # Generate next category code
                next_code = str(len(categories) + 1).zfill(2)

                categories.append((new_cat, next_code))
                print(f"Added new category: {new_cat} ({next_code})")

                category = new_cat
                break

        print("Invalid selection.")

    # Step 2 — Product name
    name = user_input("Enter product name:\n").strip().upper()

    # Step 3 — Auto-increment product number
    prod_num = get_next_product_number(category)
    if not prod_num:
        print("Error generating product number.")
        return

    # Step 4 — Initial count
    count = user_input("Enter initial count:\n").strip()
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
            #print(f'{product.product_name.upper()} added.')

    except Exception as e:
        print("Error importing multiple products.")
        print(f"Details: {e}")




def search_inventory(term):
    term = term.lower()
    matches = []

    # Load master inventory
    with open("master_inventory.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 3:
                sku, name, on_hand = row[0], row[1], row[2]
                if term in sku.lower() or term in name.lower():
                    matches.append((sku, name, int(on_hand)))

    if not matches:
        print("No matching products found.")
        return

    print("\nSearch Results:")
    for i, (sku, name, _) in enumerate(matches, start=1):
        print(f"{i}. {sku} — {name}")

    # Select a product
    while True:
        choice = user_input("Select a product:\n").strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(matches):
                break
        print("Invalid selection.")

    sku, name, master_qty = matches[choice - 1]

    # Category lookup
    cat_lookup = {code: name for (name, code) in categories}
    cat_code = sku[:2]
    cat_name = cat_lookup.get(cat_code, "UNKNOWN")

    # Load backstock locations for this category only
    loc_folder = "StockroomLocations"
    all_locations = os.listdir(loc_folder) if os.path.exists(loc_folder) else []

    locs = []
    total_loc_qty = 0

    for file in all_locations:
        if not file.endswith(".csv"):
            continue
        if not file.startswith(cat_code + "-"):
            continue

        loc_path = os.path.join(loc_folder, file)

        try:
            with open(loc_path, "r") as lf:
                reader = csv.reader(lf)
                for row in reader:
                    if len(row) >= 3 and row[0] == sku:
                        qty = int(row[2])
                        locs.append((file.replace(".csv", ""), qty))
                        total_loc_qty += qty
        except:
            pass

    # Salesfloor calculation
    salesfloor_qty = master_qty - total_loc_qty
    if salesfloor_qty < 0:
        salesfloor_qty = 0

    # Detailed view
    print("\n" + "-"*40)
    print(f"SKU: {sku}")
    print(f"Name: {name}")
    print(f"Category: {cat_name} ({cat_code})")
    print(f"Master On Hand: {master_qty}")

    if locs:
        print("\nBackstock Locations:")
        for loc, qty in locs:
            print(f" - {loc}: {qty}")
    else:
        print("\nBackstock Locations: None")

    print(f"\nTotal Backstock: {total_loc_qty}")
    print(f"Salesfloor: {salesfloor_qty}")
    print("-"*40 + "\n")

    # Action menu
    print("Actions:")
    print("1. Backstock")
    print("2. Take")
    print("3. Edit")
    print("4. Audit")
    print("5. Cancel")

    while True:
        action = user_input("Select an action:\n").strip()
        if action == "1":
            ProductLocation.backstock_product(sku, name)
            return
        elif action == "2":
            ProductLocation.remove_product(sku, name)
            return
        elif action == "3":
            edit_product(sku, name)
            return
        elif action == "4":
            ProductLocation.audit_location()
            return
        elif action == "5":
            print("Cancelled.")
            return
        else:
            print("Invalid selection.")


def search_by_prod_num(product_num):
    try:
        product_num = product_num.zfill(4)

        if product_num not in master_inventory:
            print("Item not found.")
            return None

        # Extract name + on-hand from master inventory
        name, master_qty = next(iter(master_inventory[product_num].items()))

        # Category lookup
        cat_lookup = {code: name for (name, code) in categories}
        cat_code = product_num[:2]
        cat_name = cat_lookup.get(cat_code, "UNKNOWN")

        # Load backstock locations for this category only
        loc_folder = "StockroomLocations"
        all_locations = os.listdir(loc_folder) if os.path.exists(loc_folder) else []

        locs = []
        total_loc_qty = 0

        for file in all_locations:
            if not file.endswith(".csv"):
                continue
            if not file.startswith(cat_code + "-"):
                continue

            loc_path = os.path.join(loc_folder, file)

            try:
                with open(loc_path, "r") as lf:
                    reader = csv.reader(lf)
                    for row in reader:
                        if len(row) >= 3 and row[0] == product_num:
                            qty = int(row[2])
                            locs.append((file.replace(".csv", ""), qty))
                            total_loc_qty += qty
            except:
                pass

        # Salesfloor calculation
        salesfloor_qty = master_qty - total_loc_qty
        if salesfloor_qty < 0:
            salesfloor_qty = 0

        # Detailed view
        print("\n" + "-"*40)
        print(f"SKU: {product_num}")
        print(f"Name: {name}")
        print(f"Category: {cat_name} ({cat_code})")
        print(f"Master On Hand: {master_qty}")

        if locs:
            print("\nBackstock Locations:")
            for loc, qty in locs:
                print(f" - {loc}: {qty}")
        else:
            print("\nBackstock Locations: None")

        print(f"\nTotal Backstock: {total_loc_qty}")
        print(f"Salesfloor: {salesfloor_qty}")
        print("-"*40 + "\n")

        # Action menu
        print("Actions:")
        print("1. Backstock")
        print("2. Take")
        print("3. Edit")
        print("4. Audit")
        print("5. Cancel")

        while True:
            action = user_input("Select an action:\n").strip()
            if action == "1":
                ProductLocation.backstock_product(product_num, name)
                return
            elif action == "2":
                ProductLocation.remove_product(product_num, name)
                return
            elif action == "3":
                edit_product(product_num, name)
                return
            elif action == "4":
                ProductLocation.audit_location()
                return
            elif action == "5":
                print("Cancelled.")
                return
            else:
                print("Invalid selection.")

    except Exception as e:
        print(f"Error searching by product number: {e}")
        return None


def sort_inventory_by_prod_num() -> list:
    try:
        return sorted(master_inventory.keys())
    except Exception:
        print("Error sorting inventory.")
        return []


def edit_product(sku, name):
    try:
        # Show current values
        print(f"\nEditing Product {sku}")
        print(f"Current Name: {name}")

        current_on_hand = master_inventory.get(sku, {}).get(name, None)
        if current_on_hand is None:
            print("Error: Product not found in master inventory.")
            return

        print(f"Current On Hand: {current_on_hand}")

        # New name
        new_name = user_input("New Product name (leave blank to keep current):\n").strip().upper()
        if not new_name:
            new_name = name  # keep current

        # New on-hand
        new_on_hand_input = user_input("New On Hand count (leave blank to keep current):\n").strip()
        if new_on_hand_input:
            try:
                new_on_hand = int(new_on_hand_input)
            except ValueError:
                print("On-hand count must be a number.")
                return
        else:
            new_on_hand = current_on_hand  # keep current

        # Update master inventory
        master_inventory[sku] = {new_name: new_on_hand}

        print(f"\nUpdated {sku}:")
        print(f"Name: {new_name}")
        print(f"On Hand: {new_on_hand}")

    except Exception as e:
        print(f"Error editing product: {e}")


def delete_product():
    try:
        product_num = input('Enter the Product number to delete:\n').strip().zfill(4)
        search_by_prod_num(product_num)

        confirm = user_input("Confirm deletion? (Y/N):\n").strip().upper()
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
        term = user_input("Search for product:\n").strip().upper()
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
        choice = user_input("Enter number:\n").strip()
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
        cat = user_input("Category:\n").strip()
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
        cat = user_input("Category:\n").strip()
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

def show_products_in_category():
    global categories, master_inventory

    print("Select a category to view its products:")
    for i, (cat, code) in enumerate(categories, start=1):
        print(f"{i}. {cat} ({code})")

    while True:
        choice = user_input("Enter number:\n").strip()

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(categories):
                selected_cat, selected_code = categories[choice - 1]
                break

        print("Invalid selection.")

    print(f"\nProducts in category: {selected_cat} ({selected_code})")

    found = False
    for product_num, product_data in master_inventory.items():
        if product_num.startswith(selected_code):
            for name, count in product_data.items():
                print(f"{product_num} - {name} ({count})")
                found = True

    if not found:
        print("No products found in this category.")



