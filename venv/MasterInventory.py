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
unlocated_inventory_file = Path('unlocated_inventory.csv')

file_contents_read = False
file_contents_written = False

master_inventory = dict()
salesfloor_capacity = dict()
# Products that have been received but not yet backstocked or put on the
# salesfloor. Maps SKU -> {name: qty}.
unlocated_inventory = dict()
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

    # Step 5 — Salesfloor capacity
    cap_input = user_input("Enter salesfloor capacity (default 20):\n").strip()
    if cap_input and cap_input.isdigit():
        cap = int(cap_input)
    else:
        cap = 20

    # Step 6 — Add to in-memory inventory
    master_inventory[prod_num] = {name: int(count)}
    salesfloor_capacity[prod_num] = cap

    print(Colorize.colorize_text_blue(
        f"Product added to inventory: {prod_num} - {name} ({category}) [Capacity: {cap}]"
    ))



def add_multi_product_from_file(products_to_add):
    global master_inventory

    try:
        for product in products_to_add:
            # Insert into in-memory inventory
            master_inventory[product.product_num] = {
                product.product_name.upper(): product.on_hand_count
            }
            salesfloor_capacity[product.product_num] = product.salesfloor_capacity
            #print(f'{product.product_name.upper()} added.')

    except Exception as e:
        print("Error importing multiple products.")
        print(f"Details: {e}")




def get_category_name(cat_code):
    """Resolve a category code (e.g. "04") to its name, or "UNKNOWN"."""
    cat_lookup = {code: name for (name, code) in categories}
    return cat_lookup.get(cat_code, "UNKNOWN")


def get_backstock_locations(sku):
    """Return (locs, total_qty) for a SKU across its category's location files.

    `locs` is a list of (location_name, qty) tuples.
    """
    cat_code = sku[:2]
    loc_folder = "StockroomLocations"
    all_locations = os.listdir(loc_folder) if os.path.exists(loc_folder) else []

    locs = []
    total_qty = 0

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
                        # Only report locations that actually hold product.
                        if qty > 0:
                            locs.append((file.replace(".csv", ""), qty))
                            total_qty += qty
        except Exception:
            pass

    return locs, total_qty


# -----------------------------
# Unlocated Inventory
# -----------------------------

def get_unlocated_qty(sku):
    """Return the quantity of a SKU currently sitting in the unlocated pool."""
    entry = unlocated_inventory.get(sku)
    if not entry:
        return 0
    try:
        return int(next(iter(entry.values())))
    except Exception:
        return 0


def add_unlocated(sku, name, amount):
    """Add ``amount`` of a product to the unlocated pool."""
    current = get_unlocated_qty(sku)
    unlocated_inventory[sku] = {name: current + amount}


def reduce_unlocated(sku, amount):
    """Remove ``amount`` from the unlocated pool, dropping empty entries."""
    if sku not in unlocated_inventory:
        return
    name = next(iter(unlocated_inventory[sku].keys()))
    remaining = max(0, get_unlocated_qty(sku) - amount)
    if remaining <= 0:
        unlocated_inventory.pop(sku, None)
    else:
        unlocated_inventory[sku] = {name: remaining}


def read_from_unlocated_csv(inventory_path=unlocated_inventory_file):
    """Load the unlocated inventory from its CSV file."""
    unlocated_inventory.clear()

    if not inventory_path.exists():
        return

    try:
        with open(inventory_path, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    sku = row.get('Product #', '').strip().zfill(4)
                    name = row.get('Product Name', '').strip().upper()
                    qty = max(0, int(row.get('Unlocated Count', '0').strip()))
                    if sku and qty > 0:
                        unlocated_inventory[sku] = {name: qty}
                except Exception:
                    print("Malformed unlocated CSV row. Skipping.")
    except Exception:
        print("Error reading Unlocated Inventory CSV.")


def write_to_unlocated_csv(inventory_path=unlocated_inventory_file):
    """Persist the unlocated inventory to its CSV file."""
    try:
        field_names = ['Product #', 'Product Name', 'Unlocated Count']
        with open(inventory_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(field_names)
            for sku in sorted(unlocated_inventory.keys()):
                for name, qty in unlocated_inventory[sku].items():
                    writer.writerow([sku, name, int(qty)])
        print('Unlocated inventory saved.')
    except Exception:
        print("Error writing Unlocated Inventory CSV.")


def receive_product():
    """Receive product into the unlocated pool (increases On Hand and Unlocated)."""
    selection = select_product_interactively()
    if not selection:
        return
    sku, name = selection

    amount_input = user_input("Enter amount received:\n").strip()
    if not amount_input.isdigit():
        print("Amount must be a positive number.")
        return
    amount = int(amount_input)
    if amount <= 0:
        print("Amount must be a positive number.")
        return

    # Received product increases the master on-hand and lands as unlocated.
    current_on_hand = int(next(iter(master_inventory[sku].values())))
    master_inventory[sku] = {name: current_on_hand + amount}
    add_unlocated(sku, name, amount)

    print(f"\nReceived {amount} of {name} (#{sku}).")
    print(f"On Hand: {current_on_hand + amount}")
    print(f"Unlocated: {get_unlocated_qty(sku)}")


def show_unlocated_products():
    """List unlocated products and let the user backstock or place them on the salesfloor."""
    entries = [
        (sku, next(iter(name_dict.keys())), get_unlocated_qty(sku))
        for sku, name_dict in unlocated_inventory.items()
        if get_unlocated_qty(sku) > 0
    ]

    if not entries:
        print("No unlocated products.")
        return

    print("\nUnlocated Products:")
    for i, (sku, name, qty) in enumerate(entries, start=1):
        print(f"{i}. {sku} — {name} (Unlocated: {qty})")

    while True:
        choice = user_input("Select a product:\n").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(entries):
                break
        print("Invalid selection.")

    sku, name, unloc_qty = entries[idx - 1]

    print(f"\nWhat would you like to do with {name} (#{sku})?")
    print("1. Backstock")
    print("2. Move to Salesfloor")
    print("3. Cancel")

    while True:
        action = user_input("Select an action:\n").strip()
        if action == "1":
            placed = ProductLocation.backstock_product(sku, name, max_amount=unloc_qty)
            if placed:
                reduce_unlocated(sku, placed)
                print(f"Unlocated remaining: {get_unlocated_qty(sku)}")
            return
        elif action == "2":
            move_unlocated_to_salesfloor(sku, name, unloc_qty)
            return
        elif action == "3":
            print("Cancelled.")
            return
        else:
            print("Invalid selection.")


def move_unlocated_to_salesfloor(sku, name, unloc_qty):
    """Move product from the unlocated pool onto the salesfloor, respecting capacity."""
    master_qty = int(next(iter(master_inventory[sku].values())))
    _, total_loc_qty = get_backstock_locations(sku)
    cap = salesfloor_capacity.get(sku, 20)
    salesfloor_qty = max(0, master_qty - total_loc_qty - unloc_qty)
    remaining_cap = max(0, cap - salesfloor_qty)

    if remaining_cap <= 0:
        print(f"Salesfloor is at capacity ({cap}). Cannot move more stock.")
        return

    max_movable = min(remaining_cap, unloc_qty)
    print(f"Salesfloor Capacity: {cap}")
    print(f"Currently on Salesfloor: {salesfloor_qty}")
    print(f"Max you can move: {max_movable}")

    amount_input = user_input("Enter amount to move to salesfloor:\n").strip()
    if not amount_input.isdigit():
        print("Amount must be a positive number.")
        return
    amount = int(amount_input)
    if amount <= 0:
        print("Amount must be a positive number.")
        return
    if amount > max_movable:
        print(f"Amount exceeds available capacity/stock. Max allowed: {max_movable}")
        return

    # Moving from unlocated to the salesfloor does not change master on-hand;
    # it simply stops being unlocated, which the salesfloor calculation reflects.
    reduce_unlocated(sku, amount)
    print(f"\nMoved {amount} of {name} to the salesfloor.")
    print(f"Unlocated remaining: {get_unlocated_qty(sku)}")


def print_product_view(sku, name, master_qty):
    """Print the detailed product view: category, on-hand, backstock, salesfloor."""
    cat_code = sku[:2]
    cat_name = get_category_name(cat_code)
    locs, total_loc_qty = get_backstock_locations(sku)
    unlocated_qty = get_unlocated_qty(sku)
    salesfloor_qty = max(0, master_qty - total_loc_qty - unlocated_qty)

    print("\n" + "-"*40)
    print(f"SKU: {sku}")
    print(f"Name: {name}")
    print(f"Category: {cat_name} ({cat_code})")
    cap = salesfloor_capacity.get(sku, 20)
    print(f"Master On Hand: {master_qty}")
    print(f"Salesfloor Capacity: {cap}")
    print(f"Unlocated: {unlocated_qty}")

    if locs:
        print("\nBackstock Locations:")
        for loc, qty in locs:
            print(f" - {loc}: {qty}")
    else:
        print("\nBackstock Locations: None")

    print(f"\nTotal Backstock: {total_loc_qty}")
    print(f"Salesfloor: {salesfloor_qty}")
    print("-"*40 + "\n")


def product_action_menu(sku, name):
    """Show the product action menu and dispatch the chosen action."""
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


def search_inventory(term, inventory_path = master_inventory_file):
    term = term.lower()
    matches = []

    # Search in-memory master inventory
    for sku, name_dict in master_inventory.items():
        for name, on_hand in name_dict.items():
            if term in sku.lower() or term in name.lower():
                matches.append((sku, name, int(on_hand)))

    if not matches:
        print("No matching products found.")
        return

    print("\nSearch Results:")
    for i, (sku, name, _) in enumerate(matches, start=1):
        print(f"{i}. {sku} — {name}")

    # If only one product matches, go straight to it.
    if len(matches) == 1:
        sku, name, master_qty = matches[0]
        print(f"\nOnly one match — selecting {sku} — {name}.")
    else:
        # Select a product
        while True:
            choice = user_input("Select a product:\n").strip()
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(matches):
                    break
            print("Invalid selection.")

        sku, name, master_qty = matches[choice - 1]

    print_product_view(sku, name, master_qty)
    product_action_menu(sku, name)


def search_by_prod_num(product_num):
    try:
        product_num = product_num.zfill(4)

        if product_num not in master_inventory:
            print("Item not found.")
            return None

        # Extract name + on-hand from master inventory
        name, master_qty = next(iter(master_inventory[product_num].items()))

        print_product_view(product_num, name, master_qty)
        product_action_menu(product_num, name)

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

        current_cap = salesfloor_capacity.get(sku, 20)
        print(f"Current On Hand: {current_on_hand}")
        print(f"Current Salesfloor Capacity: {current_cap}")

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

        # New salesfloor capacity
        new_cap_input = user_input("New Salesfloor Capacity (leave blank to keep current):\n").strip()
        if new_cap_input:
            try:
                new_cap = int(new_cap_input)
            except ValueError:
                print("Capacity must be a number.")
                return
        else:
            new_cap = current_cap

        # Update master inventory
        master_inventory[sku] = {new_name: new_on_hand}
        salesfloor_capacity[sku] = new_cap

        print(f"\nUpdated {sku}:")
        print(f"Name: {new_name}")
        print(f"On Hand: {new_on_hand}")
        print(f"Salesfloor Capacity: {new_cap}")

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


def read_from_master_inventory_csv(inventory_path = master_inventory_file):
    global file_contents_read

    if not inventory_path.exists():
        print('File Not Found.')
        return

    products_to_add = set()

    try:
        with open(inventory_path, 'r', newline='') as master_file:
            reader = csv.DictReader(master_file)

            for row in reader:
                try:
                    cap_val = row.get('Salesfloor Capacity', '20').strip()
                    # On-hand can never be negative; clamp any bad/legacy values to 0.
                    on_hand = max(0, int(row.get('On Hand Count', '0').strip()))
                    prod = Product(
                        row.get('Product Name', '').strip(),
                        row.get('Product #', '').strip(),
                        on_hand,
                        int(cap_val) if cap_val.isdigit() else 20
                    )
                    products_to_add.add(prod)
                except Exception:
                    print("Malformed CSV row. Skipping.")

        file_contents_read = True
        add_multi_product_from_file(products_to_add)

    except Exception:
        print("Error reading Master Inventory CSV.")


def write_to_master_inventory_csv(inventory_path = master_inventory_file):
    global file_contents_written

    try:
        field_names = ['Product #', 'Product Name', 'On Hand Count', 'Salesfloor Capacity']
        write_mode = 'w' if file_contents_read or not inventory_path.exists() else 'a'

        with open(inventory_path, write_mode, newline='') as master_file:
            print(f'File open with Write Mode: {write_mode}')
            writer = csv.writer(master_file)

            if write_mode == 'w':
                writer.writerow(field_names)

            for num in sort_inventory_by_prod_num():
                for name, count in master_inventory[num].items():
                    try:
                        cap = salesfloor_capacity.get(num, 20)
                        writer.writerow([num, name, int(count), cap])
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

    # If only one product matches, select it automatically.
    if len(matches) == 1:
        num, name, _ = matches[0]
        print(f"Only one match — selecting {name} (#{num}).")
        return num, name

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

def get_next_product_number(category, inventory_file = master_inventory_file):
    code = get_category_code(category)
    if not code:
        return None

    highest = 0

    # Scan all products
    with open(inventory_file, "r", newline="") as f:
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



