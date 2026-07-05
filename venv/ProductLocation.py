# Aaron Grincewicz — 02/19/2023
"""
Crash‑proof Location-Level Inventory Module
"""
import os
from pathlib import Path
import csv
from MasterInventory import search_by_prod_num, verify_prod_num, update_product_location,select_product_interactively
from MasterStockRoom import select_location_interactively, categories
import Colorize
import Messages as MSG


def create_new_location_file(location):
    location_csv = Path(f'StockroomLocations/{location}.csv')
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


def overwrite_location_file(location, prod_list, amount, product_num):
    try:
        with open(Path(f'StockroomLocations/{location}.csv'), 'w', newline='') as location_file:
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


def read_location_file(location) -> dict:
    products_in_loc_file = {}
    location_csv = Path(f'StockroomLocations/{location}.csv')

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


def audit_location():
    global categories

    print("Select a category to audit:")
    for i, (cat, code) in enumerate(categories, start=1):
        print(f"{i}. {cat} ({code})")

    # Category selection
    while True:
        choice = input("Enter number:\n").strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(categories):
                selected_cat, selected_code = categories[choice - 1]
                break
        print("Invalid selection.")

    # Load all locations for this category
    loc_folder = f"locations/{selected_code}"

    # Protection: no folder yet
    if not os.path.exists(loc_folder):
        print(f"No locations found for category {selected_cat}.")
        return

    loc_files = [f for f in os.listdir(loc_folder) if f.endswith(".csv")]

    # Protection: folder exists but no CSVs
    if not loc_files:
        print(f"No locations found for category {selected_cat}.")
        return

    print(f"\nLocations in category {selected_cat} ({selected_code}):")
    for i, filename in enumerate(loc_files, start=1):
        loc_name = filename.replace(".csv", "")
        print(f"{i}. {loc_name}")

    # Location selection
    while True:
        loc_choice = input("Select a location:\n").strip()
        if loc_choice.isdigit():
            loc_choice = int(loc_choice)
            if 1 <= loc_choice <= len(loc_files):
                selected_loc_file = loc_files[loc_choice - 1]
                break
        print("Invalid selection.")

    # Load products from the selected location
    loc_path = os.path.join(loc_folder, selected_loc_file)
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
    selection = select_product_interactively()
    if not selection:
        return
    product_num, product_name = selection

    location = select_location_interactively()
    if not location:
        return

    amount = MSG.get_amount_input()


def back_stock_product(term=None):
    # Step 1 — Product selection
    if term:
        selection = select_product_interactively(term)
    else:
        selection = select_product_interactively()

    if not selection:
        return

    product_num, product_name = selection
    print(f"Selected: {product_name} (#{product_num})")

    location = select_location_interactively()
    if not location:
        return
    print(f"Selected location: {location}")

    amount = MSG.get_amount_input(False)

    location_csv = Path(f'StockroomLocations/{location}.csv')
    if not location_csv.exists():
        print(MSG.file_not_found())
        return

    confirmation = 'N'
    product = None

    while confirmation != 'Y':
        if not verify_prod_num({product_num}):
            product = search_by_prod_num(product_num)
            if not product:
                print(MSG.product_not_found())
                return

            print(Colorize.colorize_text_blue(f'{amount} of {product[0]} will be placed in {location}.'))
            confirmation = input('Confirm? Enter Y or N\n').strip().upper()
        else:
            print(MSG.product_not_found())
            return

    update_product_location(True, product_num, location)

    prod_in_loc_file = read_location_file(location)

    if product_num in prod_in_loc_file:
        name, count = list(prod_in_loc_file[product_num].items())[0]
        try:
            amount += int(count)
        except ValueError:
            print("Invalid count in CSV. Using only new amount.")
        prod_in_loc_file[product_num] = {name: amount}
    else:
        prod_in_loc_file[product_num] = {product[0]: amount}

    overwrite_location_file(location, prod_in_loc_file, amount, product_num)


def remove_product():
    selection = select_product_interactively()
    if not selection:
        return
    product_num, product_name = selection
    print(f"Selected: {product_name} (#{product_num})")

    location = select_location_interactively()
    if not location:
        return
    print(f"Selected location: {location}")

    amount = MSG.get_amount_input(True)

    prod_in_loc = read_location_file(location)

    if product_num not in prod_in_loc:
        print(MSG.product_not_found())
        return

    name, count = list(prod_in_loc[product_num].items())[0]

    try:
        initial_count = int(count)
    except ValueError:
        print("Invalid count in CSV. Cannot remove.")
        return

    if amount < 0:
        amount = initial_count

    if amount > initial_count:
        print(f'This location contains only {initial_count}.')
        return

    new_count = initial_count - amount

    if new_count <= 0:
        update_product_location(False, product_num, location)

    print(Colorize.colorize_text_blue(f"Taking: {amount} | {name} of {initial_count}"))

    prod_in_loc[product_num] = {name: new_count}

    overwrite_location_file(location, prod_in_loc, new_count, product_num)


def get_product_amount() -> int:
    location = select_location_interactively()
    if not location:
        return 0
    print(f"Selected location: {location}")

    prod_in_loc = read_location_file(location)
    selection = select_product_interactively()
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
