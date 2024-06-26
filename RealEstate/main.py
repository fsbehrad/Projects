from sample import create_samples
from advertisment import ApartmentRent, ApartmentSell, HouseRent, \
    HouseSell, StoreRent, StoreSell


class Handler:
    ADVERTISEMENT_TYPES = {
        1: ApartmentSell, 2: ApartmentRent,
        3: HouseRent, 4: HouseSell,
        # 5: StoreSell, 6: StoreRent
    }

    SWITCHES = {
        'r': 'get_report',
        's': "show_all"
    }

    def get_report(self):
        for adv in self.ADVERTISEMENT_TYPES.values():
            for obj in adv.objects_list:
                print(obj.show(), adv.manager.count())
        print("\n")
    def show_all(self):
        for adv in self.ADVERTISEMENT_TYPES.values():
            # print(adv, adv.manager.count())
            for obj in adv.objects_list:
                print(obj.show_detail())

    def run(self):
        print("Hello world!")
        for key in self.SWITCHES:
            print(f"press {key} for {self.SWITCHES[key]}")
        user_input = input('Enter your choice: ')
        switch = self.SWITCHES.get(user_input, None)
        if switch is None:
            print("Invalid input")
            self.run()
        choice = getattr(self, switch, None)
        choice()
        self.run()


if __name__ == "__main__":
    create_samples()
    handler = Handler().run()
