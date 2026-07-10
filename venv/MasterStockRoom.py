# Aaron Grincewicz — 02/19/2023
"""
Crash‑proof Master StockRoom Module

Manages:
- Location creation (single + multi)
- Reading/writing Stockroom CSV
"""
import code
import csv
from pathlib import Path
import Messages as MSG
import Colorize
from MasterInventory import categories

master_stockroom_file = Path("master_stockroom_location.csv")
MAX_AISLES = 20 # 01-20
MAX_COLUMNS = 10   # A–J
MAX_ROWS = 20      # 01–20

def user_input(prompt):
    value = input(prompt).strip()
    if value.upper() in ("X", "CANCEL", "BACK"):
        raise KeyboardInterrupt
    return value


# -----------------------------
# Crash‑proof CSV read/write
# -----------------------------

def read_from_stock_room_csv(stockroom_path = master_stockroom_file):
    """
    Load categories from master_stockroom.csv.
    If codes are missing (old format), assign them based on row order.
    """
    global categories

    if not stockroom_path.exists():
        print("Stockroom category file not found.")
        return

    try:
        with open(stockroom_path, "r", newline="") as f:
            reader = csv.DictReader(f)

            categories.clear()
            row_number = 1

            for row in reader:
                cat = row.get("Category", "").strip()
                code = row.get("Code", "").strip()

                if not cat:
                    print(f"Skipping malformed row: {row}")
                    continue

                # If code is missing (old CSV format), assign based on row number
                if not code:
                    code = str(row_number).zfill(2)

                categories.append((cat, code))
                row_number += 1

    except Exception as e:
        print("Error reading Stockroom CSV.")
        print(f"Details: {e}")



def write_to_stock_room_csv(stockroom_path = master_stockroom_file):
    """
    Safely write categories to master_stockroom.csv.
    """
    try:
        with open(stockroom_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Category", "Code"])

            for cat, code in categories:
                writer.writerow([cat,code])

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

def compute_next_location(index, category, max_rows=20, max_columns=10, max_aisles=30):
    cat_name, cat_code = category  # ("PET", "03")

    # If no locations exist yet for this category
    if cat_code not in index or not index[cat_code]:
        return f"{cat_code}-01-A-01", None

    aisles = sorted(index[cat_code].keys(), key=lambda x: int(x))

    # --- Scan aisles in order ---
    for aisle in aisles:
        columns = sorted(index[cat_code][aisle].keys())

        # --- Scan columns in order ---
        for column in columns:
            rows = sorted(index[cat_code][aisle][column], key=lambda x: int(x))

            # --- Find first missing row ---
            expected = 1
            for r in rows:
                if int(r) != expected:
                    # Found a gap
                    next_row = str(expected).zfill(2)
                    return f"{cat_code}-{aisle}-{column}-{next_row}", None
                expected += 1

            # No gaps, append next row if within limit
            if expected <= max_rows:
                next_row = str(expected).zfill(2)
                return f"{cat_code}-{aisle}-{column}-{next_row}", None

        # --- No open rows in any column of this aisle ---
        # Try next column
        last_column = columns[-1]
        next_column_ord = ord(last_column) + 1
        if (next_column_ord - ord('A') + 1) <= max_columns:
            next_column = chr(next_column_ord)
            return f"{cat_code}-{aisle}-{next_column}-01", f"Row limit reached for aisle {aisle}."

    # --- No open columns in any aisle ---
    # Try next aisle
    last_aisle = aisles[-1]
    next_aisle_int = int(last_aisle) + 1
    if next_aisle_int <= max_aisles:
        next_aisle = str(next_aisle_int).zfill(2)
        return f"{cat_code}-{next_aisle}-A-01", f"Column limit reached for aisle {last_aisle}."

    # No more locations possible
    return None, f"Aisle limit reached ({max_aisles})."


def select_from_list(options, prompt, new_label="NEW"):
    """
    Generic numbered selector.
    options: list of existing items (strings)
    prompt: text to show before listing options
    new_label: label for the 'new' option (e.g., NEW AISLE)
    """
    print(f"\n{prompt}")
    for i, item in enumerate(options, start=1):
        print(f"{i}. {item}")
    print(f"{len(options) + 1}. {new_label}")

    while True:
        choice = user_input("Enter number:\n").strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(options):
                return options[choice - 1], False  # selected existing
            elif choice == len(options) + 1:
                return None, True  # user wants NEW
        print("Invalid selection.")


def select_location_interactively():
    global categories

    index = build_location_index()

    # Step 1 — Category
    category = select_category(categories)
    cat_name, cat_code = category

    # Step 2 — Next-location suggestion
    suggested, cap_message = compute_next_location(index, category)
    if suggested:
        if cap_message:
            print(f"\n{cap_message}")
        print(f"Next suggested location: {suggested}")
        yn = user_input("Create this location? (Y/N): ").strip().upper()
        if yn == "Y":
            return suggested

    # Step 3 — Manual selection
    aisle = select_aisle(index, cat_code)
    column = select_column(index, cat_code, aisle)
    row = select_row(index, cat_code, aisle, column)

    return f"{cat_code}-{aisle}-{column}-{row}"

def select_category(categories):
    # Use the generic selector
    selected, is_new = select_from_list(
        categories,
        "Select a category:",
        "NEW CATEGORY"
    )

    # Existing category selected
    if not is_new:
        return selected

    # Create new category
    name = user_input("Enter new category name:\n").strip().upper()
    next_code = str(len(categories) + 1).zfill(2)
    category = (name, next_code)
    categories.append(category)
    write_to_stock_room_csv()
    return category

def select_aisle(index, cat_code):
    if cat_code in index:
        aisles = sorted(index[cat_code].keys(), key=lambda x: int(x))
        aisle, is_new = select_from_list(aisles, "Select an aisle:", "NEW AISLE")
        if not is_new:
            return aisle
        return user_input("Enter new aisle (e.g., 01):\n").strip().upper().zfill(2)
    else:
        return user_input("\nEnter new aisle (e.g., 01):\n").strip().upper().zfill(2)

def select_column(index, cat_code, aisle):
    if cat_code in index and aisle in index[cat_code]:
        columns = sorted(index[cat_code][aisle].keys())
        column, is_new = select_from_list(columns, "Select a column:", "NEW COLUMN")
        if not is_new:
            return column
        return user_input("Enter new column (e.g., A):\n").strip().upper()
    else:
        return user_input("\nEnter new column (e.g., A):\n").strip().upper()

def select_row(index, cat_code, aisle, column):
    if cat_code in index and aisle in index[cat_code] and column in index[cat_code][aisle]:
        rows = sorted(index[cat_code][aisle][column], key=lambda x: int(x))
        row, is_new = select_from_list(rows, "Select a row:", "NEW ROW")
        if not is_new:
            return row
        return user_input("Enter new row (e.g., 01):\n").strip().upper().zfill(2)
    else:
        return user_input("\nEnter new row (e.g., 01):\n").strip().upper().zfill(2)

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
    global categories

    index = build_location_index()

    # Step 1 — Category
    category = select_category(categories)
    cat_name, cat_code = category

    # Step 2 — Aisle
    aisle = select_aisle(index, cat_code)

    # Aisle cap enforcement
    aisle_int = int(aisle)
    if aisle_int < 1 or aisle_int > MAX_AISLES:
        print(f"Aisle exceeds max allowed aisle ({MAX_AISLES}).")
        return

    # Step 3 — Column range
    print("\nEnter column range (e.g., A to D):")
    start_col = user_input("Start column:\n").strip().upper()
    end_col = user_input("End column:\n").strip().upper()

    start_col_ord = ord(start_col)
    end_col_ord = ord(end_col)

    # Cap enforcement
    if start_col_ord < ord('A') or start_col_ord > ord('A') + (MAX_COLUMNS - 1):
        print(f"Start column exceeds max allowed column ({MAX_COLUMNS}).")
        return

    if end_col_ord < ord('A') or end_col_ord > ord('A') + (MAX_COLUMNS - 1):
        print(f"End column exceeds max allowed column ({MAX_COLUMNS}).")
        return

    if end_col_ord < start_col_ord:
        print("Invalid column range.")
        return

        # Step 4 — Row range
    print("\nEnter row range (e.g., 01 to 20):")
    start_row = int(user_input("Start row:\n").strip())
    end_row = int(user_input("End row:\n").strip())

    # Row cap enforcement
    if start_row < 1 or start_row > MAX_ROWS:
        print(f"Start row exceeds max allowed row ({MAX_ROWS}).")
        return

    if end_row < 1 or end_row > MAX_ROWS:
        print(f"End row exceeds max allowed row ({MAX_ROWS}).")
        return

    if end_row < start_row:
        print("Invalid row range.")
        return


    created = 0
    skipped = 0

    for col_ord in range(start_col_ord, end_col_ord + 1):
        column = chr(col_ord)

        for row_int in range(start_row, end_row + 1):
            row = str(row_int).zfill(2)
            loc = f"{cat_code}-{aisle}-{column}-{row}"
            file_path = Path("StockroomLocations") / f"{loc}.csv"

            if file_path.exists():
                skipped += 1
                continue

            # Create the file
            with open(file_path, "w") as f:
                f.write("Product #,Product Name,Amount\n")

            created += 1

    print(f"\nCreated {created} new locations.")
    print(f"Skipped {skipped} existing locations.")
