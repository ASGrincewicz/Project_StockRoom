# Aaron Grincewicz
"""
Interactive console UI for the master inventory.

Extracted from ``MasterInventory``. These functions drive the terminal menus
(``input``/``print`` loops). State lives on ``MasterInventory`` and is accessed
via ``MI.*`` at call time; every function here is re-exported from
``MasterInventory`` for backward compatibility.
"""
import Colorize
import MasterInventory as MI
import ProductLocation
from InputUtils import user_input

__all__ = [
    "add_single_product",
    "receive_product",
    "show_unlocated_products",
    "move_unlocated_to_salesfloor",
    "print_product_view",
    "product_action_menu",
    "search_inventory",
    "search_by_prod_num",
    "edit_product",
    "delete_product",
    "select_product_interactively",
    "show_products_in_category",
]


def add_single_product():
    # Step 1 — Choose category
    print("Select a category:")
    for i, (cat, code) in enumerate(MI.categories, start=1):
        print(f"{i}. {cat} ({code})")
    print(f"{len(MI.categories) + 1}. New Category")

    while True:
        choice = user_input("Enter number:\n").strip()

        if choice.isdigit():
            choice = int(choice)

            # Existing category
            if 1 <= choice <= len(MI.categories):
                category = MI.categories[choice - 1][0]
                break

            # New category option
            elif choice == len(MI.categories) + 1:
                new_cat = input("Enter new category name:\n").strip().upper()

                # Generate next category code
                next_code = str(len(MI.categories) + 1).zfill(2)

                MI.categories.append((new_cat, next_code))
                print(f"Added new category: {new_cat} ({next_code})")

                category = new_cat
                break

        print("Invalid selection.")

    # Step 2 — Product name
    name = user_input("Enter product name:\n").strip().upper()

    # Step 3 — Auto-increment product number
    prod_num = MI.get_next_product_number(category)
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
    MI.master_inventory[prod_num] = {name: int(count)}
    MI.salesfloor_capacity[prod_num] = cap

    print(Colorize.colorize_text_blue(
        f"Product added to inventory: {prod_num} - {name} ({category}) [Capacity: {cap}]"
    ))


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
    current_on_hand = int(next(iter(MI.master_inventory[sku].values())))
    MI.master_inventory[sku] = {name: current_on_hand + amount}
    MI.add_unlocated(sku, name, amount)

    print(f"\nReceived {amount} of {name} (#{sku}).")
    print(f"On Hand: {current_on_hand + amount}")
    print(f"Unlocated: {MI.get_unlocated_qty(sku)}")


def show_unlocated_products():
    """List unlocated products and let the user backstock or place them on the salesfloor."""
    entries = [
        (sku, next(iter(name_dict.keys())), MI.get_unlocated_qty(sku))
        for sku, name_dict in MI.unlocated_inventory.items()
        if MI.get_unlocated_qty(sku) > 0
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
                MI.reduce_unlocated(sku, placed)
                print(f"Unlocated remaining: {MI.get_unlocated_qty(sku)}")
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
    master_qty = int(next(iter(MI.master_inventory[sku].values())))
    _, total_loc_qty = MI.get_backstock_locations(sku)
    cap = MI.salesfloor_capacity.get(sku, 20)
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
    MI.reduce_unlocated(sku, amount)
    print(f"\nMoved {amount} of {name} to the salesfloor.")
    print(f"Unlocated remaining: {MI.get_unlocated_qty(sku)}")


def print_product_view(sku, name, master_qty):
    """Print the detailed product view: category, on-hand, backstock, salesfloor."""
    cat_code = sku[:2]
    cat_name = MI.get_category_name(cat_code)
    locs, total_loc_qty = MI.get_backstock_locations(sku)
    unlocated_qty = MI.get_unlocated_qty(sku)
    salesfloor_qty = max(0, master_qty - total_loc_qty - unlocated_qty)

    print("\n" + "-"*40)
    print(f"SKU: {sku}")
    print(f"Name: {name}")
    print(f"Category: {cat_name} ({cat_code})")
    cap = MI.salesfloor_capacity.get(sku, 20)
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


def search_inventory(term, inventory_path=MI.master_inventory_file):
    term = term.lower()
    matches = []

    # Search in-memory master inventory
    for sku, name_dict in MI.master_inventory.items():
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

        if product_num not in MI.master_inventory:
            print("Item not found.")
            return None

        # Extract name + on-hand from master inventory
        name, master_qty = next(iter(MI.master_inventory[product_num].items()))

        print_product_view(product_num, name, master_qty)
        product_action_menu(product_num, name)

    except Exception as e:
        print(f"Error searching by product number: {e}")
        return None


def edit_product(sku, name):
    try:
        # Show current values
        print(f"\nEditing Product {sku}")
        print(f"Current Name: {name}")

        current_on_hand = MI.master_inventory.get(sku, {}).get(name, None)
        if current_on_hand is None:
            print("Error: Product not found in master inventory.")
            return

        current_cap = MI.salesfloor_capacity.get(sku, 20)
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
        MI.master_inventory[sku] = {new_name: new_on_hand}
        MI.salesfloor_capacity[sku] = new_cap

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
            MI.master_inventory.pop(product_num, None)
            print(f"Product number {product_num} has been deleted.")
        else:
            print("Deletion canceled.")

    except Exception:
        print("Error deleting product.")


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

    for num, name_dict in MI.master_inventory.items():
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


def show_products_in_category():
    print("Select a category to view its products:")
    for i, (cat, code) in enumerate(MI.categories, start=1):
        print(f"{i}. {cat} ({code})")

    while True:
        choice = user_input("Enter number:\n").strip()

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(MI.categories):
                selected_cat, selected_code = MI.categories[choice - 1]
                break

        print("Invalid selection.")

    print(f"\nProducts in category: {selected_cat} ({selected_code})")

    found = False
    for product_num, product_data in MI.master_inventory.items():
        if product_num.startswith(selected_code):
            for name, count in product_data.items():
                print(f"{product_num} - {name} ({count})")
                found = True

    if not found:
        print("No products found in this category.")
