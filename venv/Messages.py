# Aaron Grincewicz — 02/19/2023
"""
Messages & Input Helpers Module

Provides:
- Standardized user input functions for the Stockroom system
- Normalization of category, aisle, column, row, product name, and product number inputs
- Colorized error and status messages for consistent CLI feedback

This module acts as the user-facing interface layer for the inventory system.
"""

import Colorize


# -----------------------------
# Input Functions
# -----------------------------

def get_location_input() -> str:
    """
    Prompt the user for a stockroom location identifier.

    :return: Uppercase location string
    """
    return input('Please enter the location:\n').strip().upper()


def get_category_input() -> str:
    """
    Prompt the user for a category abbreviation.

    :return: Uppercase category string
    """
    return input('Please enter the category:\n').strip().upper()


def get_aisle_input() -> str:
    """
    Prompt the user for an aisle number.

    :return: Zero-padded 2-digit aisle string
    """
    return input('Please enter the aisle #:\n').strip().zfill(2)


def get_column_input() -> str:
    """
    Prompt the user for a single column letter.

    :return: Uppercase column letter
    """
    return input('Please enter a single letter for the column:\n').strip().upper()


def get_column_range_input() -> tuple:
    """
    Prompt the user for a starting and ending column letter.

    :return: (start, end) tuple of uppercase letters
    """
    start = input('Please enter the starting column letter:\n').strip().upper()
    end = input('Please enter the ending column letter:\n').strip().upper()
    return start, end


def get_row_input() -> str:
    """
    Prompt the user for a row number.

    :return: Zero-padded 2-digit row string
    """
    return input('Please enter the Row #:\n').strip().zfill(2)


def get_row_range_input() -> tuple:
    """
    Prompt the user for a starting and ending row number.

    :return: (start, end) tuple of integers
    """
    start = int(input('Enter the starting row number:\n'))
    end = int(input('Enter the ending row number:\n'))
    return start, end


def get_prod_name_input() -> str:
    """
    Prompt the user for a product name.

    :return: Uppercase product name string
    """
    return input('Enter the product name:\n').strip().upper()


def get_prod_num_input() -> str:
    """
    Prompt the user for a product number.

    Ensures:
    - Zero-padding to 4 digits
    - Normalized formatting

    :return: Zero-padded product number string
    """
    return input('Enter the product number (Max 4 digits, must start with 0):\n').strip().zfill(4)


def get_amount_input(take: bool) -> int:
    """
    Prompt the user for an amount to add or remove.

    :param take: If True, prompt for removal amount; if False, prompt for backstock amount.
    :return: Integer amount
    """
    if take:
        return int(input('Enter the amount to take (negative integer removes all):\n'))
    else:
        return int(input('Enter the amount to back stock:\n'))


# -----------------------------
# Error / Status Messages
# -----------------------------

def category_not_found() -> str:
    """Return a standardized 'Category Not Found' message."""
    return Colorize.colorize_text_red("Category Not Found")


def product_not_found() -> str:
    """Return a standardized 'Product Not Found' message."""
    return Colorize.colorize_text_red("Product Not Found")


def location_empty() -> str:
    """Return a standardized 'Location Is Empty' message."""
    return Colorize.colorize_text_red("This Location Is Empty")


def file_not_found() -> str:
    """Return a standardized 'File Not Found' message."""
    return Colorize.colorize_text_red("File Not Found")


def file_exist() -> str:
    """Return a standardized 'File Exists' message."""
    return Colorize.colorize_text_orange("File Exist")
