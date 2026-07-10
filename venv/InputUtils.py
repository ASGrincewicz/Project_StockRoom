# Aaron Grincewicz
"""
Shared console input helper.

Extracted from ``MasterInventory`` so that every module can reuse the same
cancel-aware prompt without creating import cycles.
"""


def user_input(prompt):
    value = input(prompt).strip()
    if value.upper() in ("X", "CANCEL", "BACK"):
        raise KeyboardInterrupt
    return value
