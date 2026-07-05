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
        + "SAVE: Save both Master Inventory and Stockroom categories.\n\n"

        + Colorize.colorize_text_green("Product Management Commands:\n----------------------------\n")
        + "ADD: Add a new product.\n"
        + "DELETE PRODUCT: Delete a product.\n"
        + "EDIT: Edit a product.\n"
        + "SEARCH: Search Master Inventory by name.\n"
        + "# SEARCH: Search Master Inventory by product number.\n\n"

        + Colorize.colorize_text_yellow("Category Management Commands:\n----------------------------\n")
        + "ADD CAT: Add a new category.\n"
        + "SET CAT: Set the categories(WARNING! Overwrites ALL categories!.\n"
        + "SHOW CAT: Show the categories.\n"
        + "CAT PROD: Show products in a category.\n\n"

        + Colorize.colorize_text_orange("Location Management Commands:\n----------------------------\n")
        + "AUDIT: Show all products in a location.\n"
        + "BACKSTOCK: Add a product to a location.\n"
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
        raw = input("Enter a command:\n").strip()
        upper_raw = raw.upper()
        parts = upper_raw.split()

        command = parts[0]
        args = parts[1:]

        match upper_raw:

            case 'MENU':
                show_commands()

            case 'ADD CAT':
                add_categories()
                dirty = True

            case 'SET CAT':
                set_categories()
                dirty = True

            case 'SHOW CAT':
                print(categories)

            case 'CAT PROD':
                show_products_in_category()

            case 'BACK STOCK':
                if args:
                    term = " ".join(args)
                    back_stock_product(term)
                else:
                    back_stock_product()

            case 'TAKE STOCK':
                if args:
                    term = " ".join(args)
                    remove_product(term)
                else:
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
                location = select_location_interactively()
                audit_location(location)

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

            # -----------------------------------
            # FALLBACK TO SINGLE-WORD COMMANDS
            # -----------------------------------
            case _:
                match command:

                    case 'SEARCH':
                        if args:
                            term = " ".join(args).upper()
                        else:
                            term = input('Enter your search term:\n').strip().upper()
                        search_inventory(term)

                    case '#':
                        if args and args[0] == 'SEARCH':
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

                    case 'TAKE':
                        remove_product()
                        dirty = True

                    case 'BACKSTOCK':
                        if args:
                            term = " ".join(args)
                            back_stock_product(term)
                        else:
                            back_stock_product()

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
