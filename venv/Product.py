# Aaron Grincewicz 02/19/2023

class Product:
    def __init__(self, product_name, product_num, on_hand_count):
        self.product_name = product_name.lower()
        self.product_num = product_num.zfill(4)
        self.on_hand_count = on_hand_count
        self.current_loc = set()

    # Getters
    def get_locations(self) -> set:
        print(f'{self.product_name} is in the following locations:')
        if len(self.current_loc) < 1:
            print('No current locations.')
            return set()
        else:
            for loc in self.current_loc:
                print(f'{loc}')
            return self.current_loc

    def get_product_info(self):
        print(f'Name: {self.product_name.upper()}')
        print(f'Product #: {self.product_num}')
        print(f'On Hand: {self.on_hand_count}')
        print('________________________________')

    # Setters
    def update_loc(self, location):
        if location not in self.current_loc:
            self.current_loc.add(location)
        else:
            self.get_locations()


