from Another_Functions import play

while True:
    play()
    end = input("ou will be play more? (Yes or No)").lower()
    if end == "yes":
        pass
    elif end == "no":
        print("Okay, goodbye!")
        break
    else:
        print(" I will consider it as no")
        break
