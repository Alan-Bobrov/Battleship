from Class_Ship import Ship, Field
from random import choice

def new_ship(field, len_ship, pr, bot) -> Field:
    dict_ships = {
        4: "Battleship",
        3: "Destroyer",
        2: "Submarine",
        1: "Patrol Boat"
    }
    flag = False
    if bot == True:
        while True:
            if len_ship != 1:
                place = Ship(choice(("A", "B", "C", "D", "E", "F", "G", "H", "I", "J")), choice(range(1, 11)), len_ship, choice(("up", "down", "left", "right")))
            else:
                place = Ship(choice(("A", "B", "C", "D", "E", "F", "G", "H", "I", "J")), choice(range(1, 11)), len_ship, "one")

            if place.test_satisfying_choice() and place.test_near_ship(field):
                 if test_all_cells(place, field):
                    break
    else:
        if pr:
            print("Choose the cell when will start your ship and choose direction")
            print("(first a letter of the English alphabet from A to J, and then a number from 1 to 10, directions: up, down, left, right)")
            print("a letter with a number and a direction is separated by a space)")
            print(f"Now will be a {dict_ships[len_ship]} ({len_ship} cells)")
            if len_ship == 1:
                print("You can don't write direction")
        while True:
            place = input("Write here: ").split()
            if len(place) > 2:
                if pr:
                    print("You made a mistake, try again")
                continue
            elif len(place) == 1 and len_ship == 1:
                    place = Ship(place[0][0], place[0][1:], len_ship, direction="one")
            elif len(place) == 2 and len_ship == 1:
                    if pr:
                        flag = True
                    place = Ship(place[0][0], place[0][1:], len_ship, direction="one")
            elif len(place) == 1 and len_ship != 1:
                if pr:
                    print("You forgot to write the direction or you forgot to write a space between the cell coordinates and the direction, try again")
                continue
            elif len(place) == 2:
                place = Ship(place[0][0], place[0][1:], len_ship, place[1])

            if place.test_satisfying_choice():
                place = Ship(place.Y, int(place.X), place.len_ship, place.direction)
                if place.test_near_ship(field):
                    if flag:
                        print("What you wrote as direction will not be taken into account.")
                    if test_all_cells(place, field):
                        break
                    else:
                        print("Is this seat taken or the ship will be behind the playing field or it will be close to another ship, change your move")
                else:
                    if pr:
                        print("There is a ship near this cell, try again")
            else:
                if pr:
                    print("You made a mistake in the text of your message")
    
    for i in place.all_places(False):
        field.field[ord(i.Y) - 64][i.X] = "+"
    if pr:
        field.print_one()
    field = Field(given_field=field.field, live_ships=field.live_ships + 1)
    
    return field

def test_all_cells(place, field) -> bool:
    for i in place.all_places(False):
        if not (i.test_satisfying_choice() and i.test_near_ship(field)):
            return False
    return True
      
def new_ships(field, pr, bot) -> Field:
    field = new_ship(field, 4, pr, bot)
    for _ in range(2):
        field = new_ship(field, 3, pr, bot)
    for _ in range(3):
        field = new_ship(field, 2, pr, bot)
    for _ in range(4):
        field = new_ship(field, 1, pr, bot)
    return field

def player_play(field, pr) -> tuple:
    if pr == True:
        print("Choose the cell when will start your ship and choose direction")
        print("(first a letter of the English alphabet from A to J, and then a number from 1 to 10)")
        print("a letter with a number and a direction is separated by a space)")
    while True:
        place = input("Write here: ")
        if len(place.split()) > 1:
            if pr:
                print("You made a mistake, try again")
            continue
        else:
            place = Ship(place[0], place[1:], 1, "one")
        if place.test_satisfying_choice():
            place = Ship(place.Y, int(place.X), 1, "one")
            if place.test_free_place(field, False):
                break
            else:
                if pr:
                    print("You've already attacked there")
        else:
            print("You made a mistake, try again")
    if field.field[ord(place.Y) - 64][place.X] == "+":
        field.field[ord(place.Y) - 64][place.X] = "X"
        kill, field = test_death(place, field)
        hit = True
    else:
        field.field[ord(place.Y) - 64][place.X] = "/"
        kill = False
        hit = False
    field = Field(given_field=field.field, live_ships=field.live_ships)

    return field, hit, kill

def bot_play(field) -> tuple:
    while True:
            place = Ship(choice(("A", "B", "C", "D", "E", "F", "G", "H", "I", "J")), choice(range(1, 11)), 1, "one")
            if place.test_satisfying_choice() and place.test_free_place(field, False):
                    break
            
    if field.field[ord(place.Y) - 64][place.X] == "+":
        field.field[ord(place.Y) - 64][place.X] = "X"
        kill, field = test_death(place, field)
        hit = True
    else:
        field.field[ord(place.Y) - 64][place.X] = "/"
        kill = False
        hit = False

    field = Field(given_field=field.field, live_ships=field.live_ships)
    
    return field, hit, kill

def test_death(place, field) -> tuple:
    set_lives = set()
    set_damage = set()
    set_damage_places = set()
    set_damage.add(place)
    for i in place.all_places(True):
        if i.test_satisfying_choice():
            if field.field[ord(i.Y) - 64][i.X] == "+":
                set_lives.add(i)
            elif field.field[ord(i.Y) - 64][i.X] == "X":
                set_damage.add(i)
    if len(set_lives) == 0 and len(set_damage) != 0:
            for i in set_damage:
                for j in i.all_places(True):
                    if j.test_satisfying_choice():
                        if field.field[ord(j.Y) - 64][j.X] == "X":
                            set_damage_places.add(j)
            field = place.death(field, many=set_damage_places)
            return True, field
    elif len(set_lives) == 0 and len(set_damage) == 0:
        field = place.death(field, True)
        return True, field
    elif len(set_lives) != 0:
        return False, field
  
def play() -> None:
    print('Now you will play the game "Battleship" with a computer that will make random moves.')
    print('We will find out if you can defeat randomness in this game!')
    print("You will go first")
    field_pl = Field() 
    field_bot_see = Field()
    field_bot_not_see= Field()
    field_pl.print_two(field_bot_see)
    field_pl = new_ships(field_pl, True, False)
    print("You have placed the ships, let's start the game")
    field_bot_not_see= new_ships(field_bot_not_see, False, True)
    field_pl.print_two(field_bot_see)
    br = False
    while True:
        while not br:
            field_bot_not_see, hit, kill = player_play(field_bot_not_see, True)
            field_bot_see.copying(field_bot_not_see, symbols=("X", "/"))
            field_pl.print_two(field_bot_see)
            if not hit:
                break
            else:
                print("You got into the ship!")
                if kill:
                    print("Destroyed!")
            if field_bot_not_see.live_ships == 0:
                print("You won!")
                br = True
                break
        while  not br:
            field_pl, hit, kill = bot_play(field_pl)
            field_pl.print_two(field_bot_see)
            if not hit:
                break
            else:
                print("Bot got into the ship!")
                if kill:
                    print("Destroyed!")
            if field_pl.live_ships == 0:
                print("The bot won, this time the random one was stronger")
                br = True
                break
        if br:
            break