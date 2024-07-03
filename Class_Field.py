class Field:
    def __init__(self, symbol=" ", live_ships = 0, given_field = None) -> None:
        if given_field == None:
            field = [None for _ in range(11)]
            field[0] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            alpha = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J")
            for i in range(1, 11):
                field[i] = [alpha[i - 1], symbol, symbol, symbol, symbol, symbol, symbol, symbol, symbol, symbol, symbol]
            self.field = field
        else:
            self.field = given_field

        self.live_ships = live_ships
    
    def print_one(self) -> None:
        print("                 Your field                 ")
        for i in range(11):
            for j in range(11):
                print(self.field[i][j], end=" | ")
            print()
            print("-------------------------------------------")

    def print_two(self, second) -> None:
        print("                 Your field                                                    Computer field")
        for i in range(11):
            for j in range(11):
                print(self.field[i][j], end=" | ")
            if i == 0:
                print("                   ", end="")
            else:
                print("                    ", end="")
            for j in range(11):
                print(second.field[i][j], end=" | ")
            print()
            print("-------------------------------------------                     -------------------------------------------")

    def copying(self, field_copy, symbols) -> None:
        for i in range(1, 11):
            for j in range(1, 11):
                if field_copy.field[i][j] in symbols:
                    if self.field[i][j] != field_copy.field[i][j]:
                        self.field[i][j] = field_copy.field[i][j]
