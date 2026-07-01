# Aaron Grincewicz 02/24/2023
# Master StockRoom Module
"""
Contains functions to manage stockroom locations and the products they contain.
"""
from ProductLocation import *
import Colorize
import Messages as MSG
import csv
from pathlib import Path

master_stockroom_csv = Path('master_stockroom_location.csv')
file_contents_read = False

locations = list()
categories = list()


def set_categories():
    global categories
    if input("Please enter 'Y' to create categories, or 'N' to use defaults.\n") == 'Y':
        new_categories = list()
        number_of_categories = int(input("Please enter the number of categories you would like to create.\n").strip())
        for i in range(1, number_of_categories + 1):
            category = input(
                f"Category {i}: Please input an abbreviated category name like; LD for Light Duty.\n").strip().upper()
            new_categories.append(category)
        categories = new_categories
    else:
        default_categories = ['LD', 'HD', 'G']
        categories = default_categories


def create_new_location():
    """
    Prompts the user for input and creates a new stockroom location.

    Note: The write_to_stockroom_csv function is called.

    """

    category = MSG.get_category_input()
    aisle = MSG.get_aisle_input()
    column = MSG.get_column_input()
    row = MSG.get_row_input()
    if category not in categories:
        print(MSG.category_not_found())
    else:
        for i in categories:
            if category == i:
                locations.append(f'{category}-{aisle}-{column}-{row}')
                create_new_location_file(f'{category}-{aisle}-{column}-{row}')
                print(Colorize.colorize_text_green(f'Location: {category}-{aisle}-{column}-{row} has been created.'))
    write_to_stockroom_csv()


def create_multiple_locations():
    """
    Prompts user for range of columns and rows to create locations within range.
    :return:
    """
    category = MSG.get_category_input()
    aisle = MSG.get_aisle_input()
    column_range_start, column_range_end = MSG.get_column_range_input()
    row_range_start, row_range_end = MSG.get_row_range_input()

    if category not in categories:
        print(MSG.category_not_found())
    else:
        for c in range(ord(column_range_start), ord(column_range_end) + 1):
            for i in range(row_range_start, row_range_end + 1):
                i = f'{i}'.zfill(2)
                formatted_loc = f'{category}-{aisle}-{chr(c)}-{i}'
                if formatted_loc not in locations:
                    locations.append(formatted_loc)
                    create_new_location_file(formatted_loc)
                else:
                    continue
                print(Colorize.colorize_text_green(f'Location: {category}-{aisle}-{chr(c)}-{i} has been created.'))
    write_to_stockroom_csv()


def write_to_stockroom_csv():
    # master_stockroom_path = Path(master_stockroom_csv)
    field_names = ['Category', 'Aisle #', 'Column', 'Row #']
    write_mode = 'w'
    if file_contents_read or not master_stockroom_csv.exists():
        write_mode = 'w'
    with open(master_stockroom_csv, write_mode, newline='') as master_file:
        print(f'File open with Write Mode: {write_mode}')
        writer = csv.writer(master_file)
        if write_mode == 'w':
            writer.writerow(field_names)

        for location in locations:
            loc_parts = location.split('-', 3)
            i = 0
            writer.writerow([f'{loc_parts[i]}', f'{loc_parts[i + 1]}', f'{loc_parts[i + 2]}', f'{loc_parts[i + 3]}'])

    print('Writing to file completed.')


def read_from_stock_room_csv():
    global categories
    read_categories = list()
    aisles = list()
    columns = list()
    rows = list()

    if master_stockroom_csv.exists():
        with open(master_stockroom_csv, 'r') as master_file:
            reader = csv.DictReader(master_file)

            for col in reader:
                read_categories.append(col['Category'])
                aisles.append(col['Aisle #'])
                columns.append(col['Column'])
                rows.append(col['Row #'])

        i = 0
        for category in read_categories:
            aisle = aisles[i]
            col = columns[i]
            row = rows[i]
            locations.append(f'{category}-{aisle}-{col}-{row}')
            i += 1
        global file_contents_read
        file_contents_read = True
        for cat in read_categories:
            if cat not in categories:
                categories.append(cat)
    else:
        print(MSG.file_not_found())
