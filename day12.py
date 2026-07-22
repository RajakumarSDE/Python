def make_chai():
    if not kettle_has_water():
        fill_kettle()
        plug_in_kettle()
        boil_water()

    if not is_cup_clean():
        clean_cup()

    add_to_cup("tea leaves")
    add_to_cup("milk")
    pour("boiled water")
    stir(cup)
    serve("tea")


def kettle_has_water():
    return True


def fill_kettle():
    print("Filling the kettle")


def plug_in_kettle():
    print("Plugging in the kettle")


def boil_water():
    print("Boiling the water")


def is_cup_clean():
    return True


def clean_cup():
    print("Cleaning the cup")


def add_to_cup(item):
    print(f"Adding {item} to the cup")


def pour(item):
    print(f"Pouring {item}")


def stir(cup):
    print(f"Stirring the {cup}")


def serve(drink):
    print(f"Serving {drink}")


cup = "cup"
make_chai()
