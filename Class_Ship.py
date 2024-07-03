from Class_Field import Field

class Ship:
    def __init__(self, Y, X, len_ship, direction) -> None:
        self.Y = Y.upper()
        self.X = X
        self.len_ship = len_ship
        if len_ship == 1:
            self.direction = "one"
        else:
            self.direction = direction.lower()

    def all_places(self, around) -> list:
        set_places = set()
        if self.direction == "up":
            for i in range(self.len_ship):
                set_places.add(Ship(chr(ord(self.Y) - i), self.X, self.len_ship, "up"))
        elif self.direction == "down":
            for i in range(self.len_ship):
                set_places.add(Ship(chr(ord(self.Y) + i), self.X, self.len_ship, "down"))
        elif self.direction == "left":
            for i in range(self.len_ship):
                set_places.add(Ship(self.Y, self.X - i, self.len_ship, "left"))
        elif self.direction == "right":
            for i in range(self.len_ship):
                set_places.add(Ship(self.Y, self.X + i, self.len_ship, "right"))
        elif self.direction == "one":
            set_places.add(self)
        
        if around:
            set_places_2 = set()
            for i in set_places:
                set_places_2.add(Ship(chr(ord(i.Y) - 1), i.X - 1, i.len_ship, "one"))
                set_places_2.add(Ship(chr(ord(i.Y) - 1), i.X + 1, i.len_ship, "one"))
                set_places_2.add(Ship(chr(ord(i.Y) + 1), i.X - 1, i.len_ship, "one"))
                set_places_2.add(Ship(chr(ord(i.Y) + 1), i.X + 1 , i.len_ship, "one"))
                set_places_2.add(Ship(chr(ord(i.Y) - 1), i.X, i.len_ship, "one"))
                set_places_2.add(Ship(chr(ord(i.Y) + 1), i.X, i.len_ship, "one"))
                set_places_2.add(Ship(i.Y, i.X - 1, i.len_ship, "one"))
                set_places_2.add(Ship(i.Y, i.X + 1 , i.len_ship, "one"))
            set_places = set_places | set_places_2

        return set_places 

    def test_near_ship(self, field) -> bool:
        for i in self.all_places(True):
            if i.Y in ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J") and 1 <=  i.X <= 10:
                if field.field[ord(i.Y) - 64][i.X] == "+":
                    return False
        return True
    
    def test_satisfying_choice(self) -> bool:
        if self.Y not in ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J"):
            return False
        if type(self.X) == int:
            if not 1 <= self.X <= 10:
                return False
        else:
            if self.X not in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"):
                return False
        if self.direction not in ("up", "down", "left", "right", "one"):
            return False
        return True
    
    def test_free_place(self, field, new) -> bool:
        if new:
            if field.field[ord(self.Y) - 64][self.X] != " ":
                return False
        else:
            if field.field[ord(self.Y) - 64][self.X] in ["/", "X"]:
                return False
        return True

    def death(self, field, many = None) -> Field:
        if many == None:
            for i in self.all_places(True):
                if i.test_satisfying_choice():
                    if field.field[ord(i.Y) - 64][i.X] == " ":
                        field.field[ord(i.Y) - 64][i.X] = "/"
            field = Field(given_field=field.field, live_ships=field.live_ships - 1)
        else:
            for i in many:
                for j in i.all_places(True):
                    if j.test_satisfying_choice():
                        if field.field[ord(j.Y) - 64][j.X] == " ":
                            field.field[ord(j.Y) - 64][j.X] = "/"
            field = Field(given_field=field.field, live_ships=field.live_ships - 1)
        return field