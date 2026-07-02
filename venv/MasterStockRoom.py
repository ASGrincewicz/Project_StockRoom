# Aaron Grincewicz — 02/19/2023
"""
Crash‑proof Master StockRoom Module

Manages:
- Categories
- Location creation (single + multi)
- Reading/writing Stockroom CSV
"""

import csv
from pathlib import Path
import Messages as MSG
import Colorize

master_stockroom_file = Path("master_stockroom_location.csv")

categories = []


# -----------------------------
# Crash‑proof CSV read/write
# -----------------------------

def read_from_stock_room_csv():
    """
    Safely read categories from master_stockroom.csv.
    """
    global categories

    if not master_stockroom_file.exists():
        print(MSG.file_not_found())
        return

    try:
        with open(master_stockroom_file, "r", newline="") as f:
            reader = csv.DictReader(f)

            categories = []
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

    except Exception:
        print("Error writing Stockroom CSV.")


# -----------------------------
# Category Management
# -----------------------------

def set_categories():
    """
    Safely set categories (overwrites existing list).
    """
    global categories

    print(Colorize.colorize_text_blue("Enter categories. Type DONE when finished."))

    new_categories = []

    while True:
        cat = input("Category:\n").strip().upper()
        if cat == "DONE":
            break
        if not cat:
            print(MSG.invalid_input("Category cannot be empty."))
            continue
        new_categories.append(cat)

    categories = new_categories
    write_to_stock_room_csv()


# -----------------------------
# Location Creation
# -----------------------------

def create_new_location():
    """
    Create a single location file safely.
    """
    loc = MSG.get_location_input()
    loc_path = Path(f"StockroomLocations/{loc}.csv")

    try:
        loc_path.parent.mkdir(exist_ok=True)

        if loc_path.exists():
            print(MSG.file_exist())
            return

        with open(loc_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Product #", "Product Name", "Amount"])

        print(Colorize.colorize_text_blue(f"Location {loc} created."))

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

def show_categories():
    """
    Display categories safely.
    """
    if not categories:
        print(Colorize.colorize_text_orange("No categories set."))
        return

    print(Colorize.colorize_text_blue("Categories:"))
    for cat in categories:
        print(f"- {cat}")


