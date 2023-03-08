# Aaron Grincewicz 02/19/2023

class Product:
    def __init__(self, product_name, product_num, locations):
        self.product_name = product_name.lower()
        self.product_num = product_num.zfill(4)
        # self.on_hand_count = on_hand_count
        self.current_locations = "UNLOCATED"
        if len(locations) > 0:
            if self.current_locations == "UNLOCATED":
                for loc in locations:
                    self.current_locations = f"{loc}\n"
            else:
                for loc in locations:
                    self.current_locations = f"{self.current_locations}\n{loc}\n"

    # Getters
    def get_product_info(self):
        print(f'Name: {self.product_name.upper()}')
        print(f'Product #: {self.product_num}')
        # print(f'On Hand: {self.on_hand_count}')
        print('___Product Locations___')
        if len(self.current_locations) > 0:
            for loc in self.current_locations:
                print(loc)
