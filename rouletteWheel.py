import random
from time import sleep
import argparse
from prettytable import PrettyTable

# Spins the "wheel" and displays the number and the volor of the landed  
def rouletteRandom():
    wheel = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]

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
    
    winingNumber = [wheel[i]]

    # checks if number is black, red or green
    if i == 0:
        winingNumber.append("Green ")
    elif i % 2 == 0:
        winingNumber.append("Black ")
    else:
        winingNumber.append("Red ") 

    print(SHOW_CURSOR, end="")    
    # print(winingNumber)           Debugging line
    return winingNumber
    


def showWinNum(winNum):
    print()
    print(f"winning number: {winNum[0]} ({winNum[1].strip()})")
    print()


def betting(playerMoney):
    betTypes = ['1. odd/even', '2. black/red', '3. high/low', '4. Dozen', '5. Column',
                '6. six number', '7. four number', '8. three number', '9. two number', '10. one number']

    for type in betTypes:
        print(type)

    uBetType = input("what do you want to bet on? (1-10): ")

    if uBetType not in [str(i) for i in range(1, 11)]:
        print("invalid bet type.")
        return playerMoney

    # ask for bet amount
    while True:
        try:
            amount = int(input(f"how much do you want to bet? (you have ${playerMoney}): "))
            if amount <= 0:
                print("bet must be more than $0.")
            elif amount > playerMoney:
                print("you don't have enough money.")
            else:
                break
        except ValueError:
            print("enter a valid number.")

    # deduct bet amount first
    playerMoney -= amount

    multipliers = {
        "1": 1, "2": 1, "3": 1,
        "4": 2, "5": 2,
        "6": 5, "7": 8, "8": 11,
        "9": 17, "10": 35
    }
    multiplier = multipliers[uBetType]

    def winResult(isWin, winNum):
        nonlocal playerMoney

        showWinNum(winNum)

        if isWin:
            winnings = amount * (1 + multiplier)  # return original + profit
            print(f"you win! payout: ${winnings}")
            playerMoney += winnings
        else:
            print("you lose.")

        print(f"your new balance: ${playerMoney}")
        print()

    match uBetType:

        case "1":
            betSubtype = input("bet on odd (1) or even (2): ")
            winNum = rouletteRandom()

            if betSubtype == "1" and winNum[0] % 2 != 0:
                winResult(True, winNum)
            elif betSubtype == "2" and winNum[0] % 2 == 0 and winNum[0] != 0:
                winResult(True, winNum)
            else:
                winResult(False, winNum)

        case "2":
            betSubtype = input("bet on black (1) or red (2): ")
            winNum = rouletteRandom()

            if betSubtype == "1" and winNum[1].strip() == "Black":
                winResult(True, winNum)
            elif betSubtype == "2" and winNum[1].strip() == "Red":
                winResult(True, winNum)
            else:
                winResult(False, winNum)

        case "3":
            betSubtype = input("high (1 = 19–36) or low (2 = 1–18): ")
            winNum = rouletteRandom()

            if betSubtype == "1" and 19 <= winNum[0] <= 36:
                winResult(True, winNum)
            elif betSubtype == "2" and 1 <= winNum[0] <= 18:
                winResult(True, winNum)
            else:
                winResult(False, winNum)

        case "4":
            betSubtype = input("first dozen (1), second (2), third (3): ")
            winNum = rouletteRandom()

            if betSubtype == "1" and 1 <= winNum[0] <= 12:
                winResult(True, winNum)
            elif betSubtype == "2" and 13 <= winNum[0] <= 24:
                winResult(True, winNum)
            elif betSubtype == "3" and 25 <= winNum[0] <= 36:
                winResult(True, winNum)
            else:
                winResult(False, winNum)

        case "5":
            col1 = {1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34}
            col2 = {2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35}
            col3 = {3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36}

            betSubtype = input("column 1, 2 or 3: ")
            winNum = rouletteRandom()

            if betSubtype == "1" and winNum[0] in col1:
                winResult(True, winNum)
            elif betSubtype == "2" and winNum[0] in col2:
                winResult(True, winNum)
            elif betSubtype == "3" and winNum[0] in col3:
                winResult(True, winNum)
            else:
                winResult(False, winNum)

        case "6":
            print("choose a starting number (1–33) for your six-number line (e.g. 1–6):")
            start = int(input("start number: "))
            winNum = rouletteRandom()

            if 1 <= start <= 33 and winNum[0] in range(start, start + 6):
                winResult(True, winNum)
            else:
                winResult(False, winNum)

        case "7":
            print("enter 4 numbers (e.g. 1 2 4 5):")
            four = list(map(int, input("numbers: ").split()))
            winNum = rouletteRandom()

            if len(four) == 4 and winNum[0] in four:
                winResult(True, winNum)
            else:
                winResult(False, winNum)

        case "8":
            print("choose a base number for a street (e.g. 1 = 1,2,3):")
            base = int(input("base: "))
            street = [base, base + 1, base + 2]
            winNum = rouletteRandom()

            if winNum[0] in street:
                winResult(True, winNum)
            else:
                winResult(False, winNum)

        case "9":
            print("enter 2 numbers (split):")
            pair = list(map(int, input("numbers: ").split()))
            winNum = rouletteRandom()

            if len(pair) == 2 and winNum[0] in pair:
                winResult(True, winNum)
            else:
                winResult(False, winNum)

        case "10":
            choice = int(input("number (0–36): "))
            winNum = rouletteRandom()

            if choice == winNum[0]:
                winResult(True, winNum)
            else:
                winResult(False, winNum)

    return playerMoney





def help(type):

    betDeets = [
        ["odd/even", "1:1", "48.65%", "Bet on all odd or even numbers"],
        ["black/red", "1:1", "48.65%", "Bet on all red or all black numbers"],
        ["high/low", "1:1", "48.65%", "Bet on numbers 1–18 (low) or 19–36 (high)"],
        ["Dozen", "2:1", "32.43%", "Bet on 1st (1–12), 2nd (13–24), or 3rd (25–36) dozen"],
        ["Column", "2:1", "32.43%", "Bet on one of the three vertical columns"],
        ["six number", "5:1", "16.22%", "Bet on two adjacent rows (six numbers)"],
        ["four number", "8:1", "10.81%", "Bet on four numbers that meet at one corner"],
        ["three number", "11:1", "8.11%", "Bet on a row of three consecutive numbers"],
        ["two number", "17:1", "5.41%", "Bet on two adjacent numbers"],
        ["one number", "35:1", "2.70%", "Bet on a single number"]
    ]
    
    bet = betDeets[type - 1]

    table = PrettyTable()
    table.field_names = ["Bet Type", "Payout", "Probability", "Description"]
    table.add_row([bet[0], bet[1], bet[2], bet[3]])

    print(table)



if __name__ == "__main__":

    global pMoney

    pMoney = 100

    # rouletteRandom()
    betting(pMoney)
    # help(1)

    parser = argparse.ArgumentParser(prog= "roulette game", 
                                     description= "test 123")
    parser.parse_args()