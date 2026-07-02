# Aaron Grincewicz — 02/19/2023
"""
Cleaned & Crash‑Proof Stockroom Application Runner
"""

from MasterStockRoom import *
from ProductLocation import *
from MasterInventory import *
import Colorize
import Messages as MSG


def show_commands():
    print(Colorize.colorize_text_blue("Welcome to the Stockroom App \n-----------------------------"))
    print(
        "Available Commands:\n\n"
        + Colorize.colorize_text_salmon("Main App Commands:\n------------------\n")
        + "MENU: Display this list.\n"
        + "QUIT: Exit the app.\n"
        + "READ: Import Master Inventory CSV.\n"
        + "SORT: Sort Master Inventory by product number.\n"
        + "WRITE: Write Master Inventory to CSV.\n"
        + "SAVE: Save both Master Inventory and Stockroom categories.\n"

        + Colorize.colorize_text_green("Product Management Commands:\n----------------------------\n")
        + "ADD: Add a new product.\n"
        + "DELETE PRODUCT: Delete a product.\n"
        + "EDIT: Edit a product.\n"
        + "SEARCH: Search Master Inventory by name.\n"
        + "# SEARCH: Search Master Inventory by product number.\n\n"
        + Colorize.colorize_text_orange("Location Management Commands:\n----------------------------\n")
        + "AUDIT: Show all products in a location.\n"
        + "BACK STOCK: Add a product to a location.\n"
        + "TAKE: Remove a product from a location.\n"
        + "CREATE LOC: Create a new location.\n"
        + "CREATE MULTI LOC: Create multiple locations.\n"
        + "READ LOC: Import Master Stockroom CSV.\n"
    )


def main():
    show_commands()
    dirty = False
    prompt = "Enter a command"
    while True:
        if dirty:
            prompt += " (unsaved changes)"
        commands = input(Colorize.colorize_text_orange(f"{prompt}:\n")).strip().upper()

        match commands:
            case 'MENU':
                show_commands()

            case 'SET CAT':
                set_categories()
                dirty = True

            case 'SHOW CAT':
                print(categories)

            case 'SEARCH':
                term = input('Enter your search term:\n').strip().upper()
                search_inventory(term)

            case '# SEARCH':
                term = input('Enter product number:\n').strip().upper().zfill(4)
                search_by_prod_num(term)

            case 'ADD':
                add_single_product()
                dirty = True

            case 'EDIT':
                edit_product()
                dirty = True

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
                dirty = True

            case 'DELETE PRODUCT':
                delete_product()
                dirty = True

            case 'CREATE LOC':
                create_new_location()
                dirty = True

            case 'CREATE MULTI LOC':
                create_multiple_locations()
                dirty = True

            case 'READ LOC':
                read_from_stock_room_csv()

            case 'AUDIT':
                audit_location()

            case 'SAVE':
                write_to_master_inventory_csv()
                write_to_stock_room_csv()
                dirty = False
            case 'QUIT':
                if dirty:
                    print("Saving changes before quitting...")
                    write_to_master_inventory_csv()
                    write_to_stock_room_csv()
                print("Goodbye.")
                exit()

            case _:
                print("Unknown command. Type MENU to see available commands.")


# Initial safe data load
try:
    read_from_stock_room_csv()
except Exception:
    print("Error loading stockroom CSV.")

try:
    read_from_master_inventory_csv()
except Exception:
    print("Error loading master inventory CSV.")

main()
