from ProductLocation import *
import MasterInventory
import csv
from pathlib import Path


file_contents_read = False
file_path = '/Users/aarongrincewicz/PycharmProjects/StockRoom/venv/master_stockroom_location.csv'
ld_stock_locations = list()
hd_stock_locations = list()
g_stock_locations = list()
categories = ['LD', 'HD', 'G']


class MasterStockRoom:

    def __init__(self, stock_name):
        self.name = stock_name
        self.locations = list()

    def create_new_location(self):
        category = input('Please enter the category:\n').strip().upper()
        aisle = input('Please enter the aisle #:\n').strip().zfill(2)
        column = input('Please enter a single letter for the column:\n').strip().upper()
        row = input('Please enter the Row #:\n').strip().zfill(2)
        if category not in categories:
            print(f'{category} does not exist.')
        else:
            match category:
                case 'LD':
                    ld_stock_locations.append({aisle: {column: row}})
                case 'HD':
                    hd_stock_locations.append({aisle: {column: row}})
                case 'G':
                    g_stock_locations.append({aisle: {column: row}})
            self.locations.append({f'{category}-{aisle}-{column}-{row}': list()})
        print(f'Location: {category}-{aisle}-{column}-{row} has been created.')
        self.write_to_csv()

    def back_stock_product(self, location, product_id, prod_name, amount):
        successful = False
        for i in range(0, len(self.locations)):
            if location in self.locations[i].keys():
                self.locations[i][location].append([product_id, prod_name, amount])
                print(f'{amount} of {product_id}: {prod_name} are now in {location}.')
                successful = True
                break
            else:
                successful = False
                continue
        if not successful:
            print('Location not found.')

    def audit_location(self):
        location = input('Please enter the location:\n')
        for i in range(0, len(self.locations)):
            if location in self.locations[i].keys():
                print(f'{location} contains:\n')
                for prod_id, prod_name, amount in self.locations[i][location]:
                    print(f'{prod_id}:{prod_name}: Count: {amount}')

    def write_to_csv(self):
        path = Path(file_path)
        field_names = ['Category', 'Aisle #', 'Column', 'Row #']
        write_mode = 'w'
        if file_contents_read or not Path.is_file(path):
            write_mode = 'w'
        with open(path, write_mode) as master_file:
            print(f'File open with Write Mode: {write_mode}')
            writer = csv.writer(master_file)
            if write_mode == 'w':
                writer.writerow(field_names)
            for category in categories:
                match category:
                    case 'LD':
                        location_list = ld_stock_locations
                    case 'HD':
                        location_list = hd_stock_locations
                    case 'G':
                        location_list = g_stock_locations
                for location in location_list:
                    for aisle in location.keys():
                        for i, j in location[aisle].items():
                            print(f'{category}-{aisle}-{i}-{j}')
                        writer.writerow([f'{category}', f'{aisle}', f'{i}', f'{j}'])

        print('Writing to file completed.')

    def read_from_csv(self):  # imports locations from csv file.
        # temporary lists to store values from each column read from csv file.
        read_categories = list()
        aisles = list()
        columns = list()
        rows = list()

        path = Path(file_path)
        if Path.is_file(path):
            with open(file_path, 'r') as master_file:
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
                self.locations.append({f'{category}-{aisle}-{col}-{row}': list()})
                if category == 'LD':
                    ld_stock_locations.append({aisle: {col: row}})
                elif category == 'HD':
                    hd_stock_locations.append({aisle: {col: row}})
                elif category == 'G':
                    g_stock_locations.append({aisle: {col: row}})
                else:
                    print(f'{category} does not exist.')
                i += 1
            global file_contents_read
            file_contents_read = True
        else:
            print('File Not Found.')
        for location in self.locations:
            print(location)
