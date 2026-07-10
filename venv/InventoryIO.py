# Aaron Grincewicz
"""
CSV persistence for the master and unlocated inventories.

Extracted from ``MasterInventory``. The in-memory state (``master_inventory``,
``unlocated_inventory``, ``salesfloor_capacity``, the ``file_contents_*`` flags)
remains the single source of truth on ``MasterInventory``; these functions read
and write it and are re-exported from ``MasterInventory`` for backward
compatibility.
"""
import csv
from pathlib import Path

from Product import Product
import MasterInventory as MI

__all__ = [
    "read_from_unlocated_csv",
    "write_to_unlocated_csv",
    "read_from_master_inventory_csv",
    "write_to_master_inventory_csv",
    "get_next_product_number",
]


def read_from_unlocated_csv(inventory_path=MI.unlocated_inventory_file):
    """Load the unlocated inventory from its CSV file."""
    MI.unlocated_inventory.clear()

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
                        MI.unlocated_inventory[sku] = {name: qty}
                except Exception:
                    print("Malformed unlocated CSV row. Skipping.")
    except Exception:
        print("Error reading Unlocated Inventory CSV.")


def write_to_unlocated_csv(inventory_path=MI.unlocated_inventory_file):
    """Persist the unlocated inventory to its CSV file."""
    try:
        field_names = ['Product #', 'Product Name', 'Unlocated Count']
        Path(inventory_path).parent.mkdir(parents=True, exist_ok=True)
        with open(inventory_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(field_names)
            for sku in sorted(MI.unlocated_inventory.keys()):
                for name, qty in MI.unlocated_inventory[sku].items():
                    writer.writerow([sku, name, int(qty)])
        print('Unlocated inventory saved.')
    except Exception:
        print("Error writing Unlocated Inventory CSV.")


def read_from_master_inventory_csv(inventory_path=MI.master_inventory_file):
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

        MI.file_contents_read = True
        MI.add_multi_product_from_file(products_to_add)

    except Exception:
        print("Error reading Master Inventory CSV.")


def write_to_master_inventory_csv(inventory_path=MI.master_inventory_file):
    try:
        field_names = ['Product #', 'Product Name', 'On Hand Count', 'Salesfloor Capacity']
        Path(inventory_path).parent.mkdir(parents=True, exist_ok=True)
        write_mode = 'w' if MI.file_contents_read or not inventory_path.exists() else 'a'

        with open(inventory_path, write_mode, newline='') as master_file:
            print(f'File open with Write Mode: {write_mode}')
            writer = csv.writer(master_file)

            if write_mode == 'w':
                writer.writerow(field_names)

            for num in MI.sort_inventory_by_prod_num():
                for name, count in MI.master_inventory[num].items():
                    try:
                        cap = MI.salesfloor_capacity.get(num, 20)
                        writer.writerow([num, name, int(count), cap])
                    except ValueError:
                        print(f"Invalid count for {num}. Skipping.")

        print('Writing to file completed.')
        MI.file_contents_written = True

    except Exception:
        print("Error writing Master Inventory CSV.")


def get_next_product_number(category, inventory_file=MI.master_inventory_file):
    code = MI.get_category_code(category)
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
