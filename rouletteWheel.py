import random
from time import sleep

def entry():
    global bet

    bet= input("Enter your lucky number to bet on (0-36): ")
    while True:
        if bet.isdigit() and 0 <= int(bet) <= 36:
            print("You have placed a bet on number", bet)
            sleep(2) 
            break
        else:
            print("Invalid input. Please enter a number between 0 and 36.")
            bet = input("Enter your lucky number to bet on (0-36): ")  

def rouletteRandom():
    wheel = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
    global bet
    # ANSI escape sequences
    CLEAR = "\x1b[2K"
    HIDE_CURSOR = "\033[?25l"
    SHOW_CURSOR = "\033[?25h"

    i = 0
    steps = random.randint(20, 60)   

    for _ in range(steps):

        numColor = ""

        print(HIDE_CURSOR, end="")
        b = 0.8
        sleepTime = 1 / (steps ** b)                    # gradually slows down the display of numbers

        print(wheel[i], end="\r")
        sleep(sleepTime)  
        print(CLEAR, end="")

        i = (i + 1) % len(wheel)
        steps -= 1 
    
    # checks if number is black, red or green
    if i == 0:
        numColor = "Green"
    elif i % 2 == 0:
        numColor = "Black"
    else:
        numColor = "Red"

    print(SHOW_CURSOR, end="")    
    print(numColor, wheel[i] )
    
    global winingNumber
    winingNumber = wheel[i]
    return winingNumber
    
    
        
def betting():
    print("You can bet on the following options:")
    print("1. Red")
    print("2. Black")
    print("3.Even")
    print("4.Odd")
    print("5. Low (1-18)")
    print("6. High (19-36)")
    print("7. Dozen (1-12, 13-24, 25-36)")
    print("8. Column (1st, 2nd, 3rd)")
    print("9. Single number (0-36)")
    print("10. Split (0-1, 0-2, 0-3, 1-2, 1-4, 2-3, 2-5, 3-6, 4-5, 4-7, 5-6, 5-8, 6-7, 6-9, 7-8, 7-10, 8-9, 8-11, 9-10, 9-12)")
    print("11. Street (0-3, 1-4, 2-5, 3-6, 4-7, 5-8, 6-9, 7-10, 8-11, 9-12)")
    print("12. Corner (0-1-2-3, 1-2-4-5, 2-3-5-6, 4-5-7-8, 5-6-8-9, 7-8-10-11, 8-9-11-12)")
    print("13. Line (0-1-2-3-4-5, 1-2-3-4-5-6, 2-3-4-5-6-7, 3-4-5-6-7-8, 4-5-6-7-8-9, 5-6-7-8-9-10, 6-7-8-9-10-11, 7-8-9-10-11-12)")
    entry_bet= input()
    
    if entry_bet == "3":

        print("You have placed a bet on Even")
        if winingNumber % 2 == 0:
            print("You have won the bet on Even")
        elif winingNumber == 0:
            print("You have lost the bet on Even")
        else:
            print("You have lost the bet on Even")
            
    elif entry_bet == "4":
        print("You have placed a bet on Odd")
        if winingNumber % 2 == 1:
            print("You have won the bet on Odd")
        elif winingNumber == 0:
            print("You have lost the bet on Odd")
        else:
            print("You have lost the bet on Odd")

    elif entry_bet == "5":
        print("You have placed a bet on Low (1-18)")
        if 1 <= winingNumber <= 18:
            print("You have won the bet on Low")
        elif winingNumber == 0:
            print("You have lost the bet on Low")
        else:
            print("You have lost the bet on Low")

    elif entry_bet == "6":
        print("You have placed a bet on High (19-36)")
        if 19 <= winingNumber <= 36:
            print("You have won the bet on High")
        elif winingNumber == 0:
            print("You have lost the bet on High")
        else:
            print("You have lost the bet on High")

    elif entry_bet == "7":
        print("You have placed a bet on Dozen (1-12, 13-24, 25-36)")
        if 1 <= winingNumber <= 12:
            print("You have won the bet on 1st Dozen")
        elif 13 <= winingNumber <= 24:
            print("You have won the bet on 2nd Dozen")
        elif 25 <= winingNumber <= 36:
            print("You have won the bet on 3rd Dozen")
        elif winingNumber == 0:
            print("You have lost the bet on Dozen")
        else:
            print("You have lost the bet on Dozen")

    elif entry_bet == "8":
        print("You have placed a bet on Column (1st, 2nd, 3rd)")
        print("which column do you want to bet on? (1st, 2nd, 3rd)")
        column_bet = input()
        column_1 = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
        column_2 = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
        column_3 = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
        if column_bet == "1":
            if winingNumber in column_1:
                print("You have won the bet on 1st Column")
            elif winingNumber == 0:
                print("You have lost the bet on 1st Column")
            else:
                print("You have lost the bet on 1st Column")
        elif column_bet == "2":
            if winingNumber in column_2:
                print("You have won the bet on 2nd Column")
            elif winingNumber == 0:
                print("You have lost the bet on 2nd Column")
            else:
                print("You have lost the bet on 2nd Column")
        elif column_bet == "3":
            if winingNumber in column_3:
                print("You have won the bet on 3rd Column")
            elif winingNumber == 0:
                print("You have lost the bet on 3rd Column")
            else:
                print("You have lost the bet on 3rd Column")

    rouletteRandom()

            



    
    
    



if __name__ == "__main__":
    entry()
    betting()
    winningNumber = rouletteRandom()  # Store the winning number