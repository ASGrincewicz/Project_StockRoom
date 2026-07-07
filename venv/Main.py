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

            case 'MENU':
                show_commands()

            case 'ADD CAT':
                run_command(add_categories)

            case 'SET CAT':
                run_command(set_categories)

            case 'SHOW CAT':
                run_command(print(categories))

            case 'CAT PROD':
                run_command(show_products_in_category)

            case 'BACK STOCK':
                if args:
                    term = " ".join(args)
                    run_command(back_stock_product(term))
                else:
                   run_command(back_stock_product())

            case 'TAKE STOCK':
                if args:
                    term = " ".join(args)
                    run_command(remove_product(term))
                else:
                   run_command(remove_product())
                dirty = True

            case 'DELETE PRODUCT':
                run_command(delete_product)
                dirty = True

            case 'CREATE LOC':
                run_command(create_new_location)
                dirty = True

            case 'CREATE MULTI LOC':
                run_command(create_multiple_locations)
                dirty = True

            case 'READ LOC':
                run_command(read_from_master_inventory_csv())

            case 'AUDIT':
                run_command(audit_location)

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
                            term = user_input('Enter your search term:\n').strip().upper()
                        run_command(search_inventory(term))

                    case '#':
                        if args and args[0] == 'SEARCH':
                            term = user_input('Enter product number:\n').strip().upper().zfill(4)
                            run_command(search_inventory(term))

                    case 'ADD':
                        run_command(add_single_product)
                        dirty = True

                    case 'EDIT':
                        run_command(edit_product)
                        dirty = True

                    case 'WRITE':
                        write_to_master_inventory_csv()

                    case 'READ':
                        read_from_master_inventory_csv()

                    case 'SORT':
                        write_to_master_inventory_csv()

                    case 'TAKE':
                        run_command(remove_product)
                        dirty = True

                    case 'BACKSTOCK':
                        if args:
                            term = " ".join(args)
                            run_command(back_stock_product(term))
                        else:
                            run_command(back_stock_product)

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
