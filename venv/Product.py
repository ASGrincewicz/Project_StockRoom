# Aaron Grincewicz — 02/19/2023
"""
Crash‑proof Product Class

Represents a product stored in the Master Inventory.
Tracks:
- Product name
- Product number
- On-hand count

Location tracking is handled by ProductLocation.py and location CSVs.
"""

class Product:
    def __init__(self, product_name, product_num, on_hand_count):
        """
        Initialize a Product instance safely.

        :param product_name: Name of the product (string)
        :param product_num: Product number (string or int; zero-padded)
        :param on_hand_count: Integer count of items in stock
        """
        # Normalize product name
        self.product_name = str(product_name).strip().upper() if product_name else "UNKNOWN"

        # Normalize product number
        try:
            self.product_num = str(product_num).zfill(4)
        except Exception:
            self.product_num = "0000"

        # Normalize on-hand count
        try:
            self.on_hand_count = int(on_hand_count)
        except Exception:
            self.on_hand_count = 0

    def get_product_info(self):
        """
        Print formatted product information.
        """
        print(f"Name: {self.product_name}")
        print(f"Product #: {self.product_num}")
        print(f"On Hand: {self.on_hand_count}")
