# Aaron Grincewicz — 02/19/2023
"""
Stockroom Application Runner

This module serves as the main entry point for the Stockroom Inventory System.
It provides:
- A command-driven CLI interface
- Routing to inventory and stockroom management functions
- Initialization of master inventory and stockroom data
- A persistent main loop for user interaction

Commands are grouped into:
- Main App Commands
- Product Management Commands
- Location Management Commands
"""

from MasterStockRoom import *
from ProductLocation import *
from MasterInventory import *
import Colorize


def show_commands():
    """
    Display all available commands grouped by category.
    """
    print(Colorize.colorize_text_blue("Welcome to the Stockroom App \n-----------------------------"))
    print(
        "Available Commands:\n\n"
        + Colorize.colorize_text_salmon("Main App Commands:\n------------------\n")
        + "MENU: Display this list.\n"
        + "QUIT: Exit the app.\n"
        + "READ: Import data from the Master Inventory CSV file.\n"
        + "SORT: Sort the Master Inventory by product number.\n"
        + "WRITE: Overwrite the Master Inventory CSV file with updated data.\n\n"
        + Colorize.colorize_text_green("Product Management Commands:\n----------------------------\n")
        + "ADD: Add a new product to the Master Inventory.\n"
        + "DELETE PRODUCT: Delete a product from the Master Inventory.\n"
        + "EDIT: Edit the name of a product.\n"
        + "SEARCH: Search the Master Inventory for product names containing a term.\n"
        + "# SEARCH: Search the Master Inventory by product number.\n\n"
        + Colorize.colorize_text_orange("Location Management Commands:\n----------------------------\n")
        + "AUDIT: Show all products in a location.\n"
        + "BACK STOCK: Add a product to a location.\n"
        + "CREATE LOC: Create a new stockroom location.\n"
        + "CREATE MULTI LOC: Create multiple locations in a range.\n"
        + "SET CAT: Customize stockroom categories.\n"
        + "SHOW CAT: Display categories from the Master Stockroom CSV.\n"
        + "TAKE: Remove a specified amount of a product from a location.\n"
        + "READ LOC: Import data from the Master Stockroom CSV file.\n"
    )


def main():
    """
    Main application loop.

    Continuously prompts the user for commands and routes them to the appropriate
    inventory or stockroom management functions.
    """
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


# Initial data load
read_from_stock_room_csv()
read_from_master_inventory_csv()

# Start application
main()
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
