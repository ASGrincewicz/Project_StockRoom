from MasterStockRoom import *
from Product import *
from ProductLocation import *
from MasterInventory import *

m_inv = master_inventory


def main():
    while True:
        commands = input('Enter a command:\n').strip().lower()
        match commands:
            case 'search':
                search_inventory(input('Enter your search term:\n').strip().upper())
            case 'num s':
                search_by_prod_num(input('Enter your search term:\n').strip().upper().zfill(4))
            case 'add':
                add_single_product()
            case 'edit':
                edit_product()
            case 'write':
                write_to_master_inventory_csv()
            case 'read':
                read_from_master_inventory_csv()
            case 'sort':
                write_to_master_inventory_csv()
            case 'backstock':
                back_stock_product()
            case 'create loc':
                create_new_location()
            case 'create multi loc':
                create_multiple_locations()
            case 'read loc':
                read_from_stock_room_csv()
            case 'audit':
                audit_location()
            case 'quit':
                print('Have you updated the Master Inventory?\n')
                response = input('Enter Y or N\n').strip().upper()
                if response == 'N':
                    write_to_master_inventory_csv()
                    exit()
                elif response == 'Y':
                    exit()


read_from_stock_room_csv()
read_from_master_inventory_csv()
main()
