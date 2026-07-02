# Aaron Grincewicz — 02/19/2023
"""
Crash‑proof Messages & Input Handling Module
"""

import Colorize


# -----------------------------
# Error / Status Message Helpers
# -----------------------------

def file_exist():
    return Colorize.colorize_text_orange("File already exists.")

def file_not_found():
    return Colorize.colorize_text_orange("File not found.")

def location_empty():
    return Colorize.colorize_text_orange("This location has no products.")

def product_not_found():
    return Colorize.colorize_text_orange("Product not found.")

def invalid_input(msg="Invalid input. Try again."):
    return Colorize.colorize_text_orange(msg)


# -----------------------------
# Crash‑Proof Input Functions
# -----------------------------

def get_location_input():
    """
    Always returns a valid, non-empty location string.
    """
    while True:
        loc = input("Enter location (e.g., LD-01-A-03):\n").strip().upper()
        if loc:
            return loc
        print(invalid_input("Location cannot be empty."))


def get_prod_num_input():
    """
    Always returns a valid 4-digit product number.
    """
    while True:
        num = input("Enter product number:\n").strip()
        if num.isdigit():
            return num.zfill(4)
        print(invalid_input("Product number must be digits only."))


def get_amount_input(allow_negative: bool):
    """
    Always returns a valid integer amount.
    If allow_negative=False, negative numbers are rejected.
    """
    while True:
        raw = input("Enter amount:\n").strip()
        try:
            amt = int(raw)
            if not allow_negative and amt < 0:
                print(invalid_input("Amount cannot be negative."))
                continue
            return amt
        except ValueError:
            print(invalid_input("Amount must be a number."))


def get_category_input():
    """
    Safe category input for MasterStockRoom.
    """
    while True:
        cat = input("Enter category name:\n").strip().upper()
        if cat:
            return cat
        print(invalid_input("Category cannot be empty."))


def get_range_input():
    """
    Safe numeric range input for CREATE MULTI LOC.
    """
    while True:
        raw = input("Enter range (e.g., 1-10):\n").strip()
        if "-" not in raw:
            print(invalid_input("Range must be in format X-Y."))
            continue

        start, end = raw.split("-", 1)

        if not start.isdigit() or not end.isdigit():
            print(invalid_input("Range values must be digits."))
            continue

        start, end = int(start), int(end)

        if start > end:
            print(invalid_input("Start of range cannot be greater than end."))
            continue

        return start, end


def confirm_action(prompt="Confirm? Enter Y or N\n"):
    """
    Safe confirmation input.
    """
    while True:
        ans = input(prompt).strip().upper()
        if ans in ("Y", "N"):
            return ans
        print(invalid_input("Please enter Y or N."))
