# Aaron Grincewicz
"""
Category management.

Extracted from ``MasterInventory``. The category list itself remains the single
source of truth on ``MasterInventory`` (``MasterInventory.categories``); these
functions only read/mutate it, and are re-exported from ``MasterInventory`` for
backward compatibility.
"""
import Colorize
import MasterInventory as MI
from InputUtils import user_input

__all__ = [
    "get_category_name",
    "get_category_code",
    "set_categories",
    "add_categories",
    "show_categories",
]


def get_category_name(cat_code):
    """Resolve a category code (e.g. "04") to its name, or "UNKNOWN"."""
    cat_lookup = {code: name for (name, code) in MI.categories}
    return cat_lookup.get(cat_code, "UNKNOWN")


def get_category_code(cat_name):
    for cat, code in MI.categories:
        if cat == cat_name:
            return code
    return None


def set_categories():
    MI.categories.clear()

    print("Enter categories. Type DONE when finished.")
    while True:
        cat = user_input("Category:\n").strip()
        if cat.upper() == "DONE":
            break

        cat = cat.upper()
        code = str(len(MI.categories) + 1).zfill(2)
        MI.categories.append((cat, code))

    print("Stockroom categories saved.")


def add_categories():
    print("Enter categories to add. Type DONE when finished.")
    while True:
        cat = user_input("Category:\n").strip()
        if cat.upper() == "DONE":
            break

        cat = cat.upper()

        # Check if category already exists
        if any(c == cat for c, _ in MI.categories):
            print(f"{cat} already exists. Skipping.")
            continue

        code = str(len(MI.categories) + 1).zfill(2)
        MI.categories.append((cat, code))
        print(f"{cat}:{code} added.")


def show_categories():
    """
    Display categories safely.
    """
    if not MI.categories:
        print(Colorize.colorize_text_orange("No categories set."))
        return

    print(Colorize.colorize_text_blue("Categories:"))
    for cat, code in MI.categories:
        print(f"- {cat}: {code}")
