# Aaron Grincewicz — 02/19/2023
"""
Crash‑proof Location-Level Inventory Module
"""
import csv
import os
from pathlib import Path

import MasterStockRoom as MSR
import Messages as MSG
import MasterInventory


def user_input(prompt):
    value = input(prompt).strip()
    if value.upper() in ("X", "CANCEL", "BACK"):
        raise KeyboardInterrupt
    return value


def create_new_location_file(location, location_directory = "StockroomLocations"):
    location_csv = Path(f'{location_directory}/{location}.csv')
    field_names = ['Product #', 'Product Name', 'Amount']

    try:
        if location_csv.exists():
            print(MSG.file_exist())
            return

        with open(location_csv, 'w', newline='') as location_file:
            writer = csv.writer(location_file)
            writer.writerow(field_names)

    except Exception:
        print("Error creating location file.")


def overwrite_location_file(location, prod_list, amount, product_num, location_directory = "StockroomLocations"):
    try:
        with open(Path(f'S{location_directory}/{location}.csv'), 'w', newline='') as location_file:
            writer = csv.writer(location_file)
            writer.writerow(['Product #', 'Product Name', 'Amount'])

            for num in prod_list.keys():
                for name, count in prod_list[num].items():
                    try:
                        count = int(count)
                    except ValueError:
                        print(f"Invalid count in CSV for {num}. Skipping.")
                        continue

                    if num == product_num:
                        writer.writerow([num, name, amount])
                    else:
                        writer.writerow([num, name, count])

    except Exception:
        print("Error writing to location file.")


def read_location_file(location, location_directory = "StockroomLocations") -> dict:
    products_in_loc_file = {}
    location_csv = Path(f'{location_directory}/{location}.csv')

    if not location_csv.exists():
        print(MSG.file_not_found())
        return {}

    try:
        with open(location_csv, 'r', newline='') as location_file:
            reader = csv.DictReader(location_file)

            for col in reader:
                num = col.get('Product #', '').strip()
                name = col.get('Product Name', '').strip()
                amt = col.get('Amount', '').strip()

                if not num or not name:
                    print("Malformed CSV row. Skipping.")
                    continue

                try:
                    amt_int = int(amt)
                except ValueError:
                    print(f"Invalid amount '{amt}' in CSV. Using 0.")
                    amt_int = 0

                if num not in products_in_loc_file:
                    products_in_loc_file[num] = {name: amt_int}
                else:
                    current = list(products_in_loc_file[num].values())[0]
                    products_in_loc_file[num] = {name: current + amt_int}

    except Exception:
        print("Error reading location file.")
        return {}

    return products_in_loc_file


def audit_location(location_directory = "StockroomLocations"):
    print("Select a category to audit:")
    for i, (cat, code) in enumerate(MasterInventory.categories, start=1):
        print(f"{i}. {cat} ({code})")

    # Category selection
    while True:
        choice = user_input("Enter number:\n").strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(MasterInventory.categories):
                selected_cat, selected_code = MasterInventory.categories[choice - 1]
                break
        print("Invalid selection.")

    # Load all locations for this category
    if not os.path.exists(location_directory):
        print(f"No locations found for category {selected_cat}.")
        return

    # Filter only this category's locations
    category_files = [
        f for f in os.listdir(location_directory)
        if f.startswith(selected_code + "-") and f.endswith(".csv")
    ]

    # Only include locations that actually hold product (any qty > 0).
    loc_files = []
    for f in category_files:
        loc_path = os.path.join(location_directory, f)
        has_product = False
        try:
            with open(loc_path, "r") as lf:
                reader = csv.reader(lf)
                for row in reader:
                    if len(row) >= 3:
                        try:
                            if int(row[2]) > 0:
                                has_product = True
                                break
                        except ValueError:
                            # Header or non-numeric row; skip.
                            continue
        except Exception:
            continue
        if has_product:
            loc_files.append(f)

    if not loc_files:
        print(f"No locations with product found for category {selected_cat}.")
        return

    print(f"\nLocations in category {selected_cat} ({selected_code}):")
    for i, filename in enumerate(loc_files, start=1):
        loc_name = filename.replace(".csv", "")
        print(f"{i}. {loc_name}")

    # Location selection
    while True:
        loc_choice = user_input("Select a location:\n").strip()
        if loc_choice.isdigit():
            loc_choice = int(loc_choice)
            if 1 <= loc_choice <= len(loc_files):
                selected_loc_file = loc_files[loc_choice - 1]
                break
        print("Invalid selection.")

    # Load products from the selected location
    loc_path = os.path.join(location_directory, selected_loc_file)
    print(f"\nProducts in location {selected_loc_file.replace('.csv','')}:")
    found = False

    try:
        with open(loc_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3:
                    product_num, name, count = row[0], row[1], row[2]
                    print(f"{product_num} - {name} ({count})")
                    found = True
    except Exception as e:
        print(f"Error reading location file: {e}")
        return

    if not found:
        print("This location is empty.")


def audit_product():
    selection = MasterInventory.select_product_interactively()
    if not selection:
        return
    product_num, product_name = selection

    location = MSR.select_location_interactively()
    if not location:
        return

    amount = MSG.get_amount_input()

def backstock_product_interactive():
    # Ask user to search for a product
    term = user_input("Search for product:\n").strip()
    MasterInventory.search_inventory(term)

def find_existing_backstock_locations(index, cat_code, sku, location_directory="StockroomLocations"):
    existing = []

    # Loop through aisles
    for aisle in index.get(cat_code, {}):
        # Loop through columns
        for column in index[cat_code][aisle]:
            # Loop through rows
            for row in index[cat_code][aisle][column]:
                loc = f"{cat_code}-{aisle}-{column}-{row}"
                file_path = Path(location_directory) / f"{loc}.csv"

                if file_path.exists():
                    with open(file_path, "r") as f:
                        reader = csv.reader(f)
                        for r in reader:
                            if len(r) >= 1 and r[0] == sku:
                                existing.append(loc)
                                break

    return existing


def backstock_product(sku, name, location_directory="StockroomLocations"):
    try:
        print(f"\nBackstocking {sku} — {name}")

        # Get current on-hand
        current_on_hand = next(iter(MasterInventory.master_inventory[sku].values()))
        print(f"Current On Hand: {current_on_hand}")

        # Ask amount
        try:
            amount = int(user_input("Enter amount:\n").strip())
        except ValueError:
            print("Amount must be a number.")
            return

        # Derive category from SKU
        cat_code = sku[:2]  # "01" from "0101", "03" from "0301"

        # Look up category name from MasterInventory.categories
        cat_name = next((c for c, code in MasterInventory.categories if code == cat_code), None)

        if cat_name is None:
            raise ValueError(f"Category code {cat_code} not found in categories list.")

        category = (cat_name, cat_code)

        # Build index
        index = MSR.build_location_index()

        # 1. Check for existing backstock locations for this SKU
        existing_locs = find_existing_backstock_locations(index, cat_code, sku, location_directory)

        if existing_locs:
            # Suggest the FIRST existing location
            suggested_loc = existing_locs[0]
            print(f"\nSuggested Location (existing): {suggested_loc}")
            confirm = user_input("Use this location? (Y/N): ").strip().lower()

            if confirm == "y":
                loc = suggested_loc
            else:
                # Move on to next open location
                next_loc, reason = MSR.compute_next_location(index, category)
                print(f"\nNext Open Location: {next_loc}")
                if reason:
                    print(f"Note: {reason}")

                confirm2 = user_input("Use this location? (Y/N): ").strip().lower()

                if confirm2 == "y":
                    loc = next_loc
                else:
                    # Manual fallback
                    aisle = MSR.select_aisle(index, cat_code)
                    column = MSR.select_column(index, cat_code, aisle)
                    row = MSR.select_row(index, cat_code, aisle, column)
                    loc = f"{cat_code}-{aisle}-{column}-{row}"

        else:
            # No existing backstock — suggest next open location immediately
            suggested_loc, reason = MSR.compute_next_location(index, category)
            print(f"\nSuggested Location: {suggested_loc}")
            if reason:
                print(f"Note: {reason}")

            confirm = user_input("Use this location? (Y/N): ").strip().lower()

            if confirm == "y":
                loc = suggested_loc
            else:
                aisle = MSR.select_aisle(index, cat_code)
                column = MSR.select_column(index, cat_code, aisle)
                row = MSR.select_row(index, cat_code, aisle, column)
                loc = f"{cat_code}-{aisle}-{column}-{row}"

        file_path = Path(location_directory) / f"{loc}.csv"

        # Ensure file exists
        if not file_path.exists():
            with open(file_path, "w") as f:
                f.write("SKU,DESCRIPTION,ON_HAND\n")

        # Update location file
        updated = False
        rows = []

        with open(file_path, "r") as f:
            reader = csv.reader(f)
            for r in reader:
                rows.append(r)

        for r in rows:
            if len(r) >= 3 and r[0] == sku:
                r[2] = str(int(r[2]) + amount)
                updated = True

        if not updated:
            rows.append([sku, name, str(amount)])

        with open(file_path, "w") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        print(f"\n{amount} of {name} placed in {loc}.")
        print(f"On Hand: {current_on_hand}")

    except Exception as e:
        print(f"Error in backstock_product: {e}")




def remove_product(sku, name, location_directory = "StockroomLocations"):

    try:
        print(f"\nRemoving product {sku} — {name}")

        # Current on-hand
        current_on_hand = next(iter(MasterInventory.master_inventory[sku].values()))
        print(f"Current On Hand: {current_on_hand}")

        # Salesfloor capacity limit
        cap = MasterInventory.salesfloor_capacity.get(sku, 20)
        locs, total_loc_qty = MasterInventory.get_backstock_locations(sku)
        salesfloor_qty = max(0, current_on_hand - total_loc_qty)
        remaining_cap = max(0, cap - salesfloor_qty)

        if remaining_cap <= 0:
            print(f"Salesfloor is at capacity ({cap}). Cannot take more stock.")
            return

        # Taking product moves it from backstock to the salesfloor. You can
        # only take what is actually sitting in backstock, and only up to the
        # remaining salesfloor capacity.
        max_takeable = max(0, min(remaining_cap, total_loc_qty))

        if total_loc_qty <= 0:
            print("No backstock available to take for this product.")
            return

        if max_takeable <= 0:
            print("No stock available to take.")
            return

        print(f"Salesfloor Capacity: {cap}")
        print(f"Currently on Salesfloor: {salesfloor_qty}")
        print(f"Max you can take: {max_takeable}")

        # Ask amount
        try:
            amount = int(user_input("Enter amount to remove:\n").strip())
        except ValueError:
            print("Amount must be a number.")
            return

        if amount <= 0:
            print("Amount must be a positive number.")
            return

        if amount > max_takeable:
            print(f"Amount exceeds available stock. Max allowed: {max_takeable}")
            return

        # Only offer locations that actually hold this product in backstock.
        loc_files = []
        for loc_name, qty in locs:
            if qty > 0:
                loc_files.append(f"{loc_name}.csv")

        if not loc_files:
            print("No backstock locations found for this product.")
            return

        print("\nSelect a location to remove from:")
        for i, file in enumerate(loc_files, start=1):
            print(f"{i}. {file.replace('.csv','')}")

        while True:
            choice = user_input("Enter number:\n").strip()
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(loc_files):
                    break
            print("Invalid selection.")

        selected_file = loc_files[choice - 1]
        loc_path = os.path.join(location_directory, selected_file)

        # Load location file
        rows = []
        with open(loc_path, "r") as f:
            reader = csv.reader(f)
            for r in reader:
                rows.append(r)

        # Update location file
        updated = False
        for r in rows:
            if len(r) >= 3 and r[0] == sku:
                qty = int(r[2])
                if qty < amount:
                    print("Not enough stock in this location.")
                    return
                r[2] = str(qty - amount)
                updated = True

        if not updated:
            print("Product not found in this location.")
            return

        # Write updated location file
        with open(loc_path, "w") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        # Taking product from backstock does NOT change the master on-hand
        # count. The stock is simply moved onto the salesfloor; only a sale
        # would reduce on-hand, which is not a feature here.
        print(f"\nMoved {amount} from {selected_file.replace('.csv','')} to the salesfloor.")
        print(f"On Hand: {current_on_hand}")

    except Exception as e:
        print(f"Error in remove_product: {e}")


def get_product_amount() -> int:
    location = MSR.select_location_interactively()
    if not location:
        return 0
    print(f"Selected location: {location}")

    prod_in_loc = read_location_file(location)
    selection = MasterInventory.select_product_interactively()
    if not selection:
        return 0
    product_num, product_name = selection
    print(f"Selected: {product_name} (#{product_num})")

    if product_num in prod_in_loc:
        try:
            return int(list(prod_in_loc[product_num].values())[0])
        except ValueError:
            print("Invalid amount in CSV.")
            return 0

    print(MSG.product_not_found())
    return 0
