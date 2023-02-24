# Create dictionaries for each level of organization: Type of product(bulk = 002, light = 001, grocery = 003),
# aisle number, letter for columns of shelves, number for rows of shelves. Example: XBOX would be back stocked on
# shelf 01 in column A of aisle 05 of light-duty product, giving it a location of 001-05-A01.
# Each product location is like a spreadsheet cell.
# The dictionary for rows will also contain a dictionary of product info.
# Product info includes: name of product, product number, and amount in location.
# Product info would ideally be read from a database or csv file.
# Create a class for Product: use info read from input or csv file. Also have list of current product locations.

from MasterStockRoom import *
from Product import *
from ProductLocation import *
from MasterInventory import *


m_stock = MasterStockRoom('Veganimart')
m_inv = MasterInventory('Veganimart')


def main():

    while True:
        commands = input('Enter a command:\n').strip().lower()
        match commands:
            case 's':
                m_inv.search_inventory(input('Enter your search term:\n').strip().upper())
            case 'num s':
                m_inv.search_by_num(input('Enter your search term:\n').strip().upper().zfill(4))
            case 'a':
                prod_name = input('Enter the product name:\n').strip().upper()
                prod_num_input = input('Enter the product number:\n').strip().lower()
                # prod_num = ''
                while not m_inv.verify_prod_num(prod_num_input):
                    prod_num_input = input('Enter the product number:\n').strip().lower()
                else:
                    prod_num = prod_num_input

                on_hand = int(input('How many are in stock?\n').strip().lower())
                new_prod = Product(prod_name, prod_num, on_hand)
                m_inv.add_single_product(new_prod)
            case 'edit':
                m_inv.edit_product()
            case 'write':
                m_inv.write_to_csv()
            case 'read':
                m_inv.read_from_csv()
            case 'sort':
                m_inv.write_to_csv()
            case 'backstock':
                location = input('Enter the Back Stock Location:\n').strip().upper()
                product_id = input('Enter the Product ID #:\n').strip().lower().zfill(4)
                prod_name = m_inv.search_by_num(product_id)[0]
                amount = int(input('Enter the Amount to Back Stock:\n'))
                m_stock.back_stock_product(location, product_id, prod_name, amount)
            case 'create':
                m_stock.create_new_location()
            case 'read loc':
                m_stock.read_from_csv()
            case 'audit':
                m_stock.audit_location()
            case 'quit':
                print('Have you updated the Master Inventory?\n')
                response = input('Enter Y or N\n').strip().upper()
                if response == 'N':
                    m_inv.write_to_csv()
                    exit()
                elif response == 'Y':
                    exit()


main()
