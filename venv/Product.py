# Aaron Grincewicz 02/19/2023

class Product:
    def __init__(self, product_name, product_num, on_hand_count, *locations):
        self.product_name = product_name.lower()
        self.product_num = product_num.zfill(4)
        self.on_hand_count = on_hand_count
        self.current_locations = set()
        if len(locations) > 0:
            for loc in locations:
                self.current_locations.add(loc)

    # Getters
    def get_product_info(self):
        print(f'Name: {self.product_name.upper()}')
        print(f'Product #: {self.product_num}')
        print(f'On Hand: {self.on_hand_count}')
        print('___Product Locations___')
        if len(self.current_locations) > 0:
            for loc in self.current_locations:
                print(loc)
