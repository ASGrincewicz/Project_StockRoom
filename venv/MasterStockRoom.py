# Aaron Grincewicz — 02/19/2023
"""
Crash‑proof Master StockRoom Module

Manages:
- Location creation (single + multi)
- Reading/writing Stockroom CSV
"""

import csv
from pathlib import Path
import Messages as MSG
import Colorize
from MasterInventory import categories

master_stockroom_file = Path("master_stockroom_location.csv")

# -----------------------------
# Crash‑proof CSV read/write
# -----------------------------

def read_from_stock_room_csv():
    if not master_stockroom_file.exists():
        print(MSG.file_not_found())
        return

    try:
        with open(master_stockroom_file, "r", newline="") as f:
            reader = csv.DictReader(f)

            categories.clear()   # ← FIX: do NOT reassign the list
            for row in reader:
                cat = row.get("Category", "").strip()
                if cat:
                    categories.append(cat)
                else:
                    print("Malformed CSV row. Skipping.")

        print(Colorize.colorize_text_blue("Stockroom categories imported."))

    except Exception:
        print("Error reading Stockroom CSV.")



def write_to_stock_room_csv():
    """
    Safely write categories to master_stockroom.csv.
    """
    try:
        with open(master_stockroom_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Category"])

            for cat in categories:
                writer.writerow([cat])

        print(Colorize.colorize_text_blue("Stockroom categories saved."))

    except Exception as e:
        print("Error writing Stockroom CSV.")
        print(f"Details: {e}")



from pathlib import Path

def parse_location(loc):
    parts = loc.split("-")
    if len(parts) != 4:
        return None

    category, aisle, column, row = parts

    # Normalize row formatting (01, 02, 03…)
    if row.isdigit():
        row = row.zfill(2)

    return category, aisle, column, row



def build_location_index():
    """
    Build nested dict:
    {
        category: {
            aisle: {
                column: [rows]
            }
        }
    }
    """
    index = {}
    loc_dir = Path("StockroomLocations")

    for file in loc_dir.glob("*.csv"):
        loc = file.stem
        parsed = parse_location(loc)
        if not parsed:
            continue

        category, aisle, column, row = parsed

        index.setdefault(category, {})
        index[category].setdefault(aisle, {})
        index[category][aisle].setdefault(column, [])
        index[category][aisle][column].append(row)

    return index


def select_location_interactively():
    """Hybrid hierarchical selector that supports new categories."""
    global categories

    index = build_location_index()

    # -----------------------------
    # Step 1 — Category (from categories list)
    # -----------------------------
    print("\nSelect a category:")
    for i, cat in enumerate(categories, start=1):
        print(f"{i}. {cat}")

    while True:
        choice = input("Enter number:\n").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            category = categories[int(choice) - 1]
            break
        print("Invalid selection.")

    # -----------------------------
    # Step 2 — Aisle
    # -----------------------------
    if category in index:
        aisles = sorted(index[category].keys())
        print("\nSelect an aisle:")
        for i, aisle in enumerate(aisles, start=1):
            print(f"{i}. {aisle}")
        print(f"{len(aisles)+1}. NEW AISLE")

        while True:
            choice = input("Enter number:\n").strip()
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(aisles):
                    aisle = aisles[choice - 1]
                    break
                elif choice == len(aisles) + 1:
                    aisle = input("Enter new aisle (e.g., 01):\n").strip().upper().zfill(2)
                    break
            print("Invalid selection.")
    else:
        # No aisles exist yet for this category
        aisle = input("\nEnter new aisle (e.g., 01):\n").strip().upper().zfill(2)

    # -----------------------------
    # Step 3 — Column
    # -----------------------------
    if category in index and aisle in index[category]:
        columns = sorted(index[category][aisle].keys())
        print("\nSelect a column:")
        for i, col in enumerate(columns, start=1):
            print(f"{i}. {col}")
        print(f"{len(columns)+1}. NEW COLUMN")

        while True:
            choice = input("Enter number:\n").strip()
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(columns):
                    column = columns[choice - 1]
                    break
                elif choice == len(columns) + 1:
                    column = input("Enter new column (e.g., A):\n").strip().upper()
                    break
            print("Invalid selection.")
    else:
        column = input("\nEnter new column (e.g., A):\n").strip().upper()

    # -----------------------------
    # Step 4 — Row
    # -----------------------------
    if category in index and aisle in index[category] and column in index[category][aisle]:
        rows = sorted(index[category][aisle][column])
        print("\nSelect a row:")
        for i, row in enumerate(rows, start=1):
            print(f"{i}. {row}")
        print(f"{len(rows)+1}. NEW ROW")

        while True:
            choice = input("Enter number:\n").strip()
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(rows):
                    row = rows[choice - 1]
                    break
                elif choice == len(rows) + 1:
                    row = input("Enter new row (e.g., 01):\n").strip().upper().zfill(2)
                    break
            print("Invalid selection.")
    else:
        row = input("\nEnter new row (e.g., 01):\n").strip().upper().zfill(2)

    return f"{category}-{aisle}-{column}-{row}"



# -----------------------------
# Location Creation
# -----------------------------

def create_new_location():
    """
    Create a single location file safely.
    """
    location = select_location_interactively()
    if not location:
        return

    loc_path = Path(f"StockroomLocations/{location}.csv")

    try:
        loc_path.parent.mkdir(exist_ok=True)

        if loc_path.exists():
            print(MSG.file_exist())
            return

        with open(loc_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Product #", "Product Name", "Amount"])

        print(Colorize.colorize_text_blue(f"Location {location} created."))

    except Exception:
        print("Error creating location.")


def create_multiple_locations():
    """
    Create multiple locations in a numeric range.
    Example: LD-01-A-01 through LD-01-A-10
    """
    base = input("Enter base location prefix (e.g., LD-01-A-):\n").strip().upper()
    if not base:
        print(MSG.invalid_input("Base prefix cannot be empty."))
        return

    start, end = MSG.get_range_input()

    try:
        for i in range(start, end + 1):
            loc = f"{base}{str(i).zfill(2)}"
            loc_path = Path(f"StockroomLocations/{loc}.csv")
            loc_path.parent.mkdir(exist_ok=True)

            if loc_path.exists():
                print(Colorize.colorize_text_orange(f"{loc} already exists. Skipping."))
                continue

            with open(loc_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Product #", "Product Name", "Amount"])

            print(Colorize.colorize_text_blue(f"Created: {loc}"))

    except Exception:
        print("Error creating multiple locations.")


# -----------------------------
# Utility
# -----------------------------




