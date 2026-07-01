# Aaron Grincewicz — 02/24/2023
# Master StockRoom Module
"""
Master Stockroom Module

This module manages stockroom locations and the categories they belong to.
It supports:
- Creating single or multiple stockroom locations
- Managing category definitions (custom or default)
- Reading/writing location data to a CSV file
- Ensuring consistent formatting for location identifiers

Data Model:
locations = [
    "LD-01-A-03",
    "HD-02-C-12",
    ...
]

categories = ["LD", "HD", "G"] or user-defined values.

CSV Format:
Category | Aisle # | Column | Row #
"""

from ProductLocation import *
import Colorize
import Messages as MSG
import csv
from pathlib import Path

master_stockroom_csv = Path('master_stockroom_location.csv')

# State flag indicating whether CSV contents have been loaded
file_contents_read = False

# Main data structures
locations = list()
categories = list()


def set_categories():
    """
    Configure the category list used for stockroom locations.

    Allows the user to define custom categories or fall back to defaults.
    """
    global categories

    user_choice = input("Enter 'Y' to create categories, or 'N' to use defaults.\n").strip().upper()

    if user_choice == 'Y':
        new_categories = []
        number_of_categories = int(input("How many categories would you like to create?\n").strip())

        for i in range(1, number_of_categories + 1):
            category = input(f"Category {i}: Enter an abbreviation (e.g., LD for Light Duty).\n").strip().upper()
            new_categories.append(category)

        categories = new_categories
    else:
        categories = ['LD', 'HD', 'G']


def create_new_location():
    """
    Create a single stockroom location based on user input.

    Location format: CATEGORY-AISLE-COLUMN-ROW
    Example: LD-01-A-03

    Also creates a corresponding location file and writes the updated list to CSV.
    """
    category = MSG.get_category_input()
    aisle = MSG.get_aisle_input()
    column = MSG.get_column_input()
    row = MSG.get_row_input()

    if category not in categories:
        print(MSG.category_not_found())
        return

    formatted_loc = f'{category}-{aisle}-{column}-{row}'
    locations.append(formatted_loc)

    create_new_location_file(formatted_loc)
    print(Colorize.colorize_text_green(f'Location {formatted_loc} has been created.'))

    write_to_stockroom_csv()


def create_multiple_locations():
    """
    Create multiple stockroom locations based on column and row ranges.

    Useful for generating large batches of locations quickly.
    """
    category = MSG.get_category_input()
    aisle = MSG.get_aisle_input()
    column_range_start, column_range_end = MSG.get_column_range_input()
    row_range_start, row_range_end = MSG.get_row_range_input()

    if category not in categories:
        print(MSG.category_not_found())
        return

    for c in range(ord(column_range_start), ord(column_range_end) + 1):
        for r in range(row_range_start, row_range_end + 1):
            row_str = f'{r}'.zfill(2)
            formatted_loc = f'{category}-{aisle}-{chr(c)}-{row_str}'

            if formatted_loc not in locations:
                locations.append(formatted_loc)
                create_new_location_file(formatted_loc)

            print(Colorize.colorize_text_green(f'Location {formatted_loc} has been created.'))

    write_to_stockroom_csv()


def write_to_stockroom_csv():
    """
    Write all stockroom locations to master_stockroom_location.csv.

    Overwrites the file if it was previously read or does not exist.
    """
    field_names = ['Category', 'Aisle #', 'Column', 'Row #']
    write_mode = 'w'  # Always overwrite for consistency

    with open(master_stockroom_csv, write_mode, newline='') as master_file:
        print(f'File open with Write Mode: {write_mode}')
        writer = csv.writer(master_file)

        writer.writerow(field_names)

        for location in locations:
            category, aisle, column, row = location.split('-', 3)
            writer.writerow([category, aisle, column, row])

    print('Writing to file completed.')


def read_from_stock_room_csv():
    """
    Read stockroom location data from master_stockroom_location.csv.

    Populates the locations list and updates the categories list if new categories are found.
    """
    global file_contents_read
    global categories

    if not master_stockroom_csv.exists():
        print(MSG.file_not_found())
        return

    read_categories = []
    aisles = []
    columns = []
    rows = []

    with open(master_stockroom_csv, 'r') as master_file:
        reader = csv.DictReader(master_file)

        for row in reader:
            read_categories.append(row['Category'])
            aisles.append(row['Aisle #'])
            columns.append(row['Column'])
            rows.append(row['Row #'])

    for i in range(len(read_categories)):
        formatted_loc = f'{read_categories[i]}-{aisles[i]}-{columns[i]}-{rows[i]}'
        locations.append(formatted_loc)

    file_contents_read = True

    # Add any new categories found in the CSV
    for cat in read_categories:
        if cat not in categories:
            categories.append(cat)
