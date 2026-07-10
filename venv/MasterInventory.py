# Aaron Grincewicz — 02/19/2023
"""
Crash‑proof Master Inventory Module.

This module owns the in-memory inventory state (the single source of truth) and
a small set of core helpers. Larger responsibilities have been extracted into
focused modules and re-exported here for backward compatibility:

    * ``CategoryManager`` — category state helpers and menus.
    * ``InventoryIO``     — CSV persistence (master / unlocated / next number).
    * ``InventoryUI``     — interactive console menus.
    * ``InputUtils``      — the shared cancel-aware ``user_input`` helper.

Callers may continue to use ``from MasterInventory import *`` / ``MasterInventory.<name>``
exactly as before.
"""

import csv
import os

import Colorize
from Product import Product
from pathlib import Path

import config

master_inventory_file = config.MASTER_INVENTORY_FILE
unlocated_inventory_file = config.UNLOCATED_INVENTORY_FILE

file_contents_read = False
file_contents_written = False

master_inventory = dict()
salesfloor_capacity = dict()
# Products that have been received but not yet backstocked or put on the
# salesfloor. Maps SKU -> {name: qty}.
unlocated_inventory = dict()
categories = []

# Re-export the shared input helper so existing callers keep working.
from InputUtils import user_input


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


def get_backstock_locations(sku):
    """Return (locs, total_qty) for a SKU across its category's location files.

    `locs` is a list of (location_name, qty) tuples.
    """
    cat_code = sku[:2]
    loc_folder = str(config.LOCATIONS_DIR)
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
# Unlocated Inventory (core state helpers)
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


def sort_inventory_by_prod_num() -> list:
    try:
        return sorted(master_inventory.keys())
    except Exception:
        print("Error sorting inventory.")
        return []


def update_product_location(add: bool, product_num: str, location: str):
    """
    Legacy placeholder for location tracking.
    Exists only to satisfy ProductLocation imports.
    """
    pass


# -----------------------------
# Re-exports of extracted modules
# -----------------------------
# Imported after the state and core helpers above are defined so the extracted
# modules (and the circular chain
# MasterStockRoom -> MasterInventory -> ProductLocation -> MasterStockRoom)
# can resolve their references at call time regardless of entry point.
from CategoryManager import *  # noqa: E402,F401,F403
from InventoryIO import *      # noqa: E402,F401,F403
from InventoryUI import *      # noqa: E402,F401,F403
