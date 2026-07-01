# Aaron Grincewicz — 02/19/2023
"""
Product Class

Represents a product stored in the inventory system.

Features:
- Normalizes product names and product numbers
- Tracks all stockroom locations where the product is stored
- Provides a formatted display of product information

Data Model:
product_name: lowercase string
product_num: zero-padded 4-digit string
current_locations: string containing one or more newline-separated locations
"""

class Product:
    def __init__(self, product_name, product_num, locations):
        """
        Initialize a Product instance.

        :param product_name: Name of the product (string)
        :param product_num: Product number (string or int; will be zero-padded)
        :param locations: Iterable of location identifiers (strings)
        """
        self.product_name = product_name.lower()
        self.product_num = product_num.zfill(4)

        # Store locations as a newline-separated string
        self.current_locations = "UNLOCATED"

        if len(locations) > 0:
            # If product is unlocated, replace with first location
            if self.current_locations == "UNLOCATED":
                self.current_locations = ""
            for loc in locations:
                self.current_locations += f"{loc}\n"

    def get_product_info(self):
        """
        Print formatted product information, including all known locations.
        """
        print(f'Name: {self.product_name.upper()}')
        print(f'Product #: {self.product_num}')
        print('___Product Locations___')

        if len(self.current_locations) > 0:
            # Print each location on its own line
            for loc in self.current_locations.splitlines():
                print(loc)
