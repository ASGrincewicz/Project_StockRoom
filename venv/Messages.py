import Colorize


def get_location_input() -> str:
    location = input('Please enter the location:\n').strip().upper()
    return location


def get_category_input() -> str:
    category = input('Please enter the category:\n').strip().upper()
    return category


def get_aisle_input() -> str:
    aisle = input('Please enter the aisle #:\n').strip().zfill(2)
    return aisle


def get_column_input() -> str:
    column = input('Please enter a single letter for the column:\n').strip().upper()
    return column


def get_column_range_input() -> tuple:
    start = input('Please enter a single letter for the starting column:\n').strip().upper()
    end = input('Please enter a single letter for the ending column:\n').strip().upper()
    return start, end


def get_row_input() -> str:
    row = input('Please enter the Row #:\n').strip().zfill(2)
    return row


def get_row_range_input() -> tuple:
    start = int(input('Enter the starting row number:\n'))
    end = int(input('Enter the ending row number:\n'))
    return start, end


def get_prod_name_input() -> str:
    prod_name = input('Enter the product name:\n').strip().upper()
    return prod_name


def get_prod_num_input() -> str:
    prod_num = input('Enter the product number(Max 4 digits and must start w/ 0):\n').strip().zfill(4)
    return prod_num


def get_amount_input(take) -> int:
    amount = 0
    if take:
        amount = int(input('Enter the amount to take (To take all enter a negative integer):\n'))
    elif not take:
        amount = int(input('Enter the amount to back stock:\n'))
    return amount


def category_not_found() -> str:
    return Colorize.colorize_text_red("Category Not Found")


def product_not_found() -> str:
    return Colorize.colorize_text_red("Product Not Found")


def location_empty() -> str:
    return Colorize.colorize_text_red("This Location Is Empty")


def file_not_found() -> str:
    return Colorize.colorize_text_red("File Not Found")


def file_exist() -> str:
    return Colorize.colorize_text_orange("File Exist")
