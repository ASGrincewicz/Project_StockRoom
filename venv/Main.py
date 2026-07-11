# Aaron Grincewicz — 02/19/2023
"""
Cleaned & Crash‑Proof Stockroom Application Runner
"""

from MasterStockRoom import *
from ProductLocation import *
from MasterInventory import *
import sys

import Colorize
import Messages as MSG


def show_commands():
    print(Colorize.colorize_text_blue("Welcome to the Stockroom App \n-----------------------------"))
    print(
        "Available Commands:\n\n"
        + Colorize.colorize_text_salmon("Everyday Commands:\n------------------\n")
        + "MENU: Display this list.\n"
        + "SEARCH: Search Master Inventory by name.\n"
        + "# SEARCH: Search Master Inventory by product number.\n"
        + "CAT PROD: Show products in a category.\n\n"
        + "About: Show information about the app.\n"

        + Colorize.colorize_text_green("Stock Commands:\n---------------\n")
        + "BACKSTOCK: Move a product into a backstock location.\n"
        + "TAKE: Take a product from backstock to the salesfloor.\n"
        + "RECEIVE: Receive product into the unlocated pool.\n"
        + "UNLOCATED: Show unlocated product and backstock/place it on the salesfloor.\n"
        + "AUDIT: Show all products in a location.\n\n"

        + Colorize.colorize_text_yellow("App Commands:\n-------------\n")
        + "SAVE: Save both Master Inventory and Stockroom categories.\n"
        + "QUIT: Exit the app.\n"
        + "ADMIN: Show advanced/administration commands.\n"
    )


def show_admin_commands():
    print(Colorize.colorize_text_blue("Admin Commands \n--------------"))
    print(
        Colorize.colorize_text_green("Product Management:\n-------------------\n")
        + "ADD: Add a new product.\n"
        + "EDIT: Edit a product.\n"
        + "DELETE PRODUCT: Delete a product.\n\n"

        + Colorize.colorize_text_yellow("Category Management:\n--------------------\n")
        + "ADD CAT: Add a new category.\n"
        + "SET CAT: Set the categories (WARNING! Overwrites ALL categories!).\n"
        + "SHOW CAT: Show the categories.\n\n"

        + Colorize.colorize_text_orange("Location Management:\n--------------------\n")
        + "CREATE LOC: Create a new location.\n"
        + "CREATE MULTI LOC: Create multiple locations.\n"
        + "READ LOC: Import Master Stockroom CSV.\n\n"

        + Colorize.colorize_text_salmon("Inventory File Management:\n--------------------------\n")
        + "READ: Import Master Inventory CSV.\n"
        + "WRITE: Write Master Inventory to CSV.\n"
        + "SORT: Sort Master Inventory by product number.\n\n"

        + "MENU: Return to the main menu list.\n"
    )
def show_about():
    print("About the Developer")
    print("-------------------")
    print("Name: Aaron Grincewicz")
    print("Location: Massachusetts, USA")
    print("Role: Retail Team Leader & Software Developer")
    print("Focus Areas: Systems architecture, inventory automation, game dev, retro computing")
    print()
    print("About This Project")
    print("------------------")
    print("Stockroom is a portfolio demonstration of a modular inventory management system.")
    print("It showcases state-driven architecture, CSV persistence, and real-world workflows.")
    print()
    print("Future Work")
    print("-----------")
    print("SolidCore expands this concept into a full framework with stronger abstractions.")
    print("Copyright")
    print("---------")
    print("Copyright © 2026 Aaron Grincewicz. All rights reserved.")



def take_product_interactive():
    """Select a product interactively, then take it from backstock."""
    selection = select_product_interactively()
    if not selection:
        return
    sku, name = selection
    remove_product(sku, name)


def edit_product_interactive():
    """Select a product interactively, then edit it."""
    selection = select_product_interactively()
    if not selection:
        return
    sku, name = selection
    edit_product(sku, name)


def user_input(prompt):
    value = input(prompt).strip()
    if value.upper() in ("X", "CANCEL", "BACK"):
        raise KeyboardInterrupt  # clean escape from command
    return value

def run_command(func):
    try:
        func()
    except KeyboardInterrupt:
        print("Command cancelled.")



def main():
    show_commands()
    dirty = False
    prompt = "Enter a command"
    while True:
        if dirty:
            prompt += " (unsaved changes)"
        raw = user_input("Enter a command:\n").strip()
        upper_raw = raw.upper()
        parts = upper_raw.split()

        command = parts[0]
        args = parts[1:]

        match upper_raw:

            # -----------------------------------
            # PRIMARY MENU
            # -----------------------------------
            case 'MENU':
                show_commands()

            case 'ABOUT':
                run_command(show_about)

            case 'ADMIN':
                show_admin_commands()

            case 'CAT PROD':
                run_command(show_products_in_category)

            case 'BACKSTOCK':
                if args:
                    # Treat args as product number
                    product_num = args[0].zfill(4)
                    search_by_prod_num(product_num)
                else:
                    # Launch interactive backstock flow
                    backstock_product_interactive()

            case 'TAKE':
                run_command(take_product_interactive)
                dirty = True

            case 'RECEIVE':
                run_command(receive_product)
                dirty = True

            case 'UNLOCATED':
                run_command(show_unlocated_products)
                dirty = True

            case 'AUDIT':
                run_command(audit_location)

            case 'SAVE':
                write_to_master_inventory_csv()
                write_to_stock_room_csv()
                write_to_unlocated_csv()
                dirty = False

            case 'QUIT':
                if dirty:
                    print("Saving changes before quitting...")
                    write_to_master_inventory_csv()
                    write_to_stock_room_csv()
                    write_to_unlocated_csv()
                print("Goodbye.")
                sys.exit()

            # -----------------------------------
            # ADMIN MENU
            # -----------------------------------
            case 'ADD':
                run_command(add_single_product)
                dirty = True

            case 'EDIT':
                run_command(edit_product_interactive)
                dirty = True

            case 'DELETE PRODUCT':
                run_command(delete_product)
                dirty = True

            case 'ADD CAT':
                run_command(add_categories)

            case 'SET CAT':
                run_command(set_categories)

            case 'SHOW CAT':
                run_command(lambda: print(categories))

            case 'CREATE LOC':
                run_command(create_new_location)
                dirty = True

            case 'CREATE MULTI LOC':
                run_command(create_multiple_locations)
                dirty = True

            case 'READ LOC':
                run_command(read_from_stock_room_csv)

            case 'READ':
                run_command(read_from_master_inventory_csv)

            case 'WRITE':
                write_to_master_inventory_csv()

            case 'SORT':
                write_to_master_inventory_csv()

            # -----------------------------------
            # FALLBACK TO SINGLE-WORD COMMANDS
            # -----------------------------------
            case _:
                match command:

                    case 'SEARCH':
                        if args:
                            term = " ".join(args).upper()
                        else:
                            term = user_input('Enter your search term:\n').strip().upper()
                        search_inventory(term)

                    case '#':
                        if args and args[0] == 'SEARCH':
                            term = user_input('Enter product number:\n').strip().upper().zfill(4)
                            search_inventory(term)
                        else:
                            print("Unknown command. Type MENU to see available commands.")

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

try:
    read_from_unlocated_csv()
except Exception:
    print("Error loading unlocated inventory CSV.")

main()
