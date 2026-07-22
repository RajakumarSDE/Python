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

make_chai()            