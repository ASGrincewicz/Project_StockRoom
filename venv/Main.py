from MasterStockRoom import *
from ProductLocation import *
from MasterInventory import *
import Colorize


def show_commands():
    print(Colorize.colorize_text_blue("Welcome to the Stockroom App \n-----------------------------"))
    print("Available Commands:\n\n" +
          Colorize.colorize_text_salmon("Main App Commands:\n" +
                                        "------------------\n") +
          "MENU: Display this list.\n" +
          "QUIT: Exit the app.\n" +
          "READ: Imports the data from the Master Inventory csv file.\n" +
          "SORT: Sorts the Master Inventory by product number.\n" +
          "WRITE: Overwrites the Master Inventory csv file with updated data.\n\n" +
          Colorize.colorize_text_green("Product Management Commands:\n" +
                                       "----------------------------\n") +
          "ADD: Add a new product to the Master Inventory.\n" +
          "DELETE PRODUCT: Deletes the specified product from the Master Inventory.\n" +
          "EDIT: Allows you to edit the name of the specified product.\n" +
          "# SEARCH: Search the Master Inventory for the specified product number.\n" +
          "SEARCH: Search the Master Inventory for product names containing search term.\n\n" +
          Colorize.colorize_text_orange("Location Management Commands:\n" +
                                        "----------------------------\n") +
          "AUDIT: Shows all products in the specified location.\n" +
          "BACK STOCK: Adds the specified product to desired location.\n" +
          "CREATE LOC: Add a new location to the Master Stockroom file.\n" +
          "CREATE MULTI LOC: Add multiple locations to a single aisle and the Master Stockroom file.\n" +
          "SET CAT: Allows you to customize the categories.\n" +
          "SHOW CAT: Displays categories read from current Master Stockroom Location csv file.\n" +
          "TAKE: Remove the specified amount of a product from desired location.\n" +
          "READ LOC: Imports the data from the Master Stockroom csv file.\n"
          )


def main():
    show_commands()
    while True:
        commands = input(Colorize.colorize_text_orange('Enter a command:\n')).strip().upper()
        match commands:
            case 'MENU':
                show_commands()
            case 'SET CAT':
                set_categories()
            case 'SHOW CAT':
                print(categories)
            case 'SEARCH':
                search_inventory(input('Enter your search term:\n').strip().upper())
            case '# SEARCH':
                search_by_prod_num(input('Enter your search term:\n').strip().upper().zfill(4))
            case 'ADD':
                add_single_product()
            case 'EDIT':
                edit_product()
            case 'WRITE':
                write_to_master_inventory_csv()
            case 'READ':
                read_from_master_inventory_csv()
            case 'SORT':
                write_to_master_inventory_csv()
            case 'BACK STOCK':
                back_stock_product()
            case 'TAKE':
                remove_product()
            case 'DELETE PRODUCT':
                delete_product()
            case 'CREATE LOC':
                create_new_location()
            case 'CREATE MULTI LOC':
                create_multiple_locations()
            case 'READ LOC':
                read_from_stock_room_csv()
            case 'AUDIT':
                audit_location()
            case 'NO LOC':
                find_unlocated()
            case 'QUIT':
                write_to_master_inventory_csv()
                exit()


read_from_stock_room_csv()
read_from_master_inventory_csv()
main()
