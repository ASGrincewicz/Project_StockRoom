# Aaron Grincewicz 02/24/2023
# Master StockRoom Module
"""
Contains functions to manage stockroom locations and the products they contain.
"""
from ProductLocation import *
import MasterInventory
import csv
from pathlib import Path

master_stockroom_csv = Path('master_stockroom_location.csv')
file_contents_read = False

cat_1_stock_locations = list()
cat_2_stock_locations = list()
cat_3_stock_locations = list()
locations = list()
categories = ('LD', 'HD', 'G')


def create_new_location():
    """
    Prompts the user for input and creates a new stockroom location.

    Note: The write_to_stockroom_csv function is called.

    """
    category = input('Please enter the category:\n').strip().upper()
    aisle = input('Please enter the aisle #:\n').strip().zfill(2)
    column = input('Please enter a single letter for the column:\n').strip().upper()
    row = input('Please enter the Row #:\n').strip().zfill(2)
    if category not in categories:
        print(f'{category} does not exist.')
    else:
        match category:
            case 'LD':
                cat_1_stock_locations.append({aisle: {column: row}})
            case 'HD':
                cat_2_stock_locations.append({aisle: {column: row}})
            case 'G':
                cat_3_stock_locations.append({aisle: {column: row}})
        locations.append({f'{category}-{aisle}-{column}-{row}': list()})
        create_new_location_file(f'{category}-{aisle}-{column}-{row}')
    print(f'Location: {category}-{aisle}-{column}-{row} has been created.')
    write_to_stockroom_csv()


def create_multiple_locations():
    """
    Prompts user for range of columns and rows to create locations within range.
    :return:
    """
    category = input('Please enter the category:\n').strip().upper()
    aisle = input('Please enter the aisle #:\n').strip().zfill(2)
    column_range_start = input('Please enter a single letter for the starting column:\n').strip().upper()
    column_range_end = input('Please enter a single letter for the ending column:\n').strip().upper()
    row_range_start = int(input('Enter the starting row number:\n'))
    row_range_end = int(input('Enter the ending row number:\n'))
    if category not in categories:
        print(f'{category} does not exist.')
    else:
        for c in range(ord(column_range_start), ord(column_range_end)+1):
            for i in range(row_range_start, row_range_end + 1):
                i = f'{i}'.zfill(2)
                match category:
                    case 'LD':
                        if {aisle: {chr(c): i}} not in cat_1_stock_locations:
                            cat_1_stock_locations.append({aisle: {chr(c): i}})
                        else:
                            continue
                    case 'HD':
                        if {aisle: {chr(c): i}} not in cat_2_stock_locations:
                            cat_2_stock_locations.append({aisle: {chr(c): i}})
                        else:
                            continue
                    case 'G':
                        if {aisle: {chr(c): i}} not in cat_3_stock_locations:
                            cat_3_stock_locations.append({aisle: {chr(c): i}})
                        else:
                            continue
                if {f'{category}-{aisle}-{chr(c)}-{i}': list()} not in locations:
                    locations.append({f'{category}-{aisle}-{chr(c)}-{i}': list()})
                    create_new_location_file(f'{category}-{aisle}-{chr(c)}-{i}')
                else:
                    continue
                print(f'Location: {category}-{aisle}-{chr(c)}-{i} has been created.')
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
        for category in categories:
            match category:
                case 'LD':
                    location_list = cat_1_stock_locations
                case 'HD':
                    location_list = cat_2_stock_locations
                case 'G':
                    location_list = cat_3_stock_locations
            for location in location_list:
                for aisle in sorted(location.keys()):
                    for i, j in location[aisle].items():
                        writer.writerow([f'{category}', f'{aisle}', f'{i}', f'{j}'])

    print('Writing to file completed.')


def read_from_stock_room_csv():

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
            locations.append({f'{category}-{aisle}-{col}-{row}': list()})
            if category == 'LD':
                cat_1_stock_locations.append({aisle: {col: row}})
            elif category == 'HD':
                cat_2_stock_locations.append({aisle: {col: row}})
            elif category == 'G':
                cat_3_stock_locations.append({aisle: {col: row}})
            else:
                print(f'{category} does not exist.')
            i += 1
        global file_contents_read
        file_contents_read = True
    else:
        print('File Not Found.')
