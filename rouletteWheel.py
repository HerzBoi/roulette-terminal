import random
from time import sleep
import argparse
import json
import os
import sys
from prettytable import PrettyTable
from rich import print
from rich.console import Console

# --- Constants and Setup ---
PLAYER_FILE = "players.json"
console = Console()


# --- Player Data Handling ---
def load_players():
    if os.path.exists(PLAYER_FILE):
        with open(PLAYER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_players(data):
    with open(PLAYER_FILE, "w") as f:
        json.dump(data, f, indent=4)


# --- Roulette Wheel Logic ---
def roulette_random():
    wheel = [
        0, 32, 15, 19, 4, 21, 2, 25, 17, 34,
        6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
        24, 16, 33, 1, 20, 14, 31, 9, 22, 18,
        29, 7, 28, 12, 35, 3, 26
    ]

    i = 0
    steps = random.randint(20, 60)

    sys.stdout.write("\033[?25l")  # Hide cursor
    sys.stdout.flush()

    for _ in range(steps):
        sleep_time = 1 / (steps ** 0.8)
        number = wheel[i]

        color = (
            "green" if number == 0 else
            "red" if number in [1, 3, 5, 7, 9, 12, 14, 16, 18,
                                 19, 21, 23, 25, 27, 30, 32, 34, 36] else
            "black"
        )

        color_code = {
            "red": "[bold red]",
            "black": "[bold black]",
            "green": "[bold green]"
        }[color]

        sys.stdout.write("\r\033[K")  # Clear line
        sys.stdout.flush()

        console.print(f"{color_code}{number}[/]", end="", highlight=False, soft_wrap=True)
        sleep(sleep_time)

        i = (i + 1) % len(wheel)
        steps -= 1

    sys.stdout.write("\r\033[K\n\033[?25h")  # Clear line + Show cursor
    sys.stdout.flush()

    win_num = [wheel[i]]

    win_num.append(
        "Green" if wheel[i] == 0 else "Red" if wheel[i] in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36] else "Black"
    )

    return win_num


# --- Help Table Display ---
def show_help_table():
    betDeets = [
        ["odd/even", "1:1", "48.65%", "Bet on all odd or even numbers"],
        ["black/red", "1:1", "48.65%", "Bet on all red or all black numbers"],
        ["high/low", "1:1", "48.65%", "Bet on 1–18 (low) or 19–36 (high)"],
        ["Dozen", "2:1", "32.43%", "Bet on 1st (1–12), 2nd (13–24), or 3rd (25–36) dozen"],
        ["Column", "2:1", "32.43%", "Bet on one of the three vertical columns"],
        ["six number", "5:1", "16.22%", "Bet on two adjacent rows (six numbers)"],
        ["four number", "8:1", "10.81%", "Bet on four numbers that meet at one corner"],
        ["three number", "11:1", "8.11%", "Bet on a row of three consecutive numbers"],
        ["two number", "17:1", "5.41%", "Bet on two adjacent numbers"],
        ["one number", "35:1", "2.70%", "Bet on a single number"]
    ]

    table = PrettyTable()
    table.field_names = ["Bet Type", "Payout", "Probability", "Description"]

    for row in betDeets:
        table.add_row(row)

    print(table)


# --- Maps for Bet Types and Payouts ---
bet_type_map = {
    "1": "odd/even",
    "2": "black/red",
    "3": "high/low",
    "4": "Dozen",
    "5": "Column",
    "6": "six number",
    "7": "four number",
    "8": "three number",
    "9": "two number",
    "10": "one number"
}

payout_map = {
    "odd/even": 1,
    "black/red": 1,
    "high/low": 1,
    "Dozen": 2,
    "Column": 2,
    "six number": 5,
    "four number": 8,
    "three number": 11,
    "two number": 17,
    "one number": 35
}

# --- Game Logic ---
def play_game(player_name, bet_type, amount, choice):
    players = load_players()

    if player_name not in players:
        print("[red]Player not found. Use --add-player to create one.[/red]")
        return

    if players[player_name] < amount:
        print("[red]Insufficient balance.[/red]")
        return

    players[player_name] -= amount
    win_num = roulette_random()
    num = win_num[0]
    win_color = win_num[1].lower()

    color_display = {
        "red": f"[bold red]{num} (Red)[/bold red]",
        "black": f"[bold white]{num} (Black)[/bold white]",
        "green": f"[bold green]{num} (Green)[/bold green]"
    }

    print(f"Winning number: {color_display.get(win_color, color_display['green'])}")

    win = False

    if bet_type == "odd/even":
        win = (
            (choice in ["1", "odd"] and num % 2 != 0) or
            (choice in ["2", "even"] and num % 2 == 0 and num != 0)
        )

    elif bet_type == "black/red":
        win = (
            (choice.lower() in ["1", "black"] and win_color == "black") or
            (choice.lower() in ["2", "red"] and win_color == "red")
        )

    elif bet_type == "high/low":
        win = (
            (choice in ["1", "high"] and 19 <= num <= 36) or
            (choice in ["2", "low"] and 1 <= num <= 18)
        )

    elif bet_type == "Dozen":
        win = (
            (choice == "1" and 1 <= num <= 12) or
            (choice == "2" and 13 <= num <= 24) or
            (choice == "3" and 25 <= num <= 36)
        )

    elif bet_type == "Column":
        col1 = {1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34}
        col2 = {2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35}
        col3 = {3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36}
        win = (
            (choice == "1" and num in col1) or
            (choice == "2" and num in col2) or
            (choice == "3" and num in col3)
        )

    elif bet_type == "six number":
        start = int(choice)
        win = 1 <= start <= 33 and num in range(start, start + 6)

    elif bet_type == "four number":
        quad = list(map(int, choice.split()))
        win = len(quad) == 4 and num in quad

    elif bet_type == "three number":
        base = int(choice)
        win = num in [base, base + 1, base + 2]

    elif bet_type == "two number":
        pair = tuple(map(int, choice.split()))

        h_splits = {(n, n + 1) for n in range(1, 36) if n % 3 != 0}
        v_splits = {(n, n + 3) for n in range(1, 34)}
        valid_splits = h_splits | v_splits | {(b, a) for (a, b) in h_splits | v_splits}

        win = pair in valid_splits and num in pair

    elif bet_type == "one number":
        win = str(num) == choice

    if win:
        payout = amount * payout_map.get(bet_type, 1)
        players[player_name] += amount + payout
        print(f"[green]You win! +${payout} -> New Balance: ${players[player_name]}[/green]")
    else:
        print(f"[red]You lose. -${amount} -> Remaining Balance: ${players[player_name]}[/red]")

    save_players(players)


# --- CLI Interface ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Roulette CLI Game")

    parser.add_argument("command", nargs="?", choices=["add-player", "play", "help-table"], help="Command to run")
    parser.add_argument("-n", "--name", help="Player name")
    parser.add_argument("-b", "--balance", type=int, help="Initial balance for new player")
    parser.add_argument("-t", "--bet-type", help="Type of bet")
    parser.add_argument("-a", "--amount", type=int, help="Amount to bet")
    parser.add_argument("-c", "--choice", help="Your bet choice")

    args = parser.parse_args()
    players = load_players()

    if not args.command:
        print("[bold cyan]Welcome to Roulette CLI![/bold cyan]")

        name = input("Enter your name: ")

        if name in players:
            print(f"[bold green]Welcome back, {name}! Your current balance is: ${players[name]}[/]")
        else:
            balance = int(input("New player! Enter starting balance: "))
            players[name] = balance
            save_players(players)
            print(f"Player '{name}' added with balance ${balance}.")

        print("[bold magenta]Bet types:[/bold magenta]")
        for k, v in bet_type_map.items():
            print(f"{k}. {v}")

        bet_input = input("Choose bet type: ").strip()
        bet_type = bet_type_map.get(bet_input, bet_input)

        if bet_type not in payout_map:
            print("[red]Invalid bet type.[/red]")
            exit()

        prompts = {
            "odd/even": "Enter 1 for 'odd' or 2 for 'even': ",
            "black/red": "Enter 1 for 'black' or 2 for 'red': ",
            "high/low": "Enter 1 for 'high' or 2 for 'low': ",
            "Dozen": "Choose 1, 2, or 3 for dozen: ",
            "Column": "Choose 1, 2, or 3 for column: ",
            "six number": "Enter starting number for six-number line (1–33): ",
            "four number": "Enter four numbers separated by space: ",
            "three number": "Enter base number for three-number street: ",
            "two number": "Enter two adjacent numbers separated by space: ",
            "one number": "Enter number (0–36): "
        }

        choice = input(prompts.get(bet_type, "Enter your choice: "))
        amount = int(input("Enter amount to bet: "))

        play_game(name, bet_type, amount, choice)

    elif args.command == "add-player":
        if not args.name or args.balance is None:
            print("[red]--name and --balance are required to add a player.[/red]")
        elif args.name in players:
            print("[yellow]Player already exists.[/yellow]")
        else:
            players[args.name] = args.balance
            save_players(players)
            print(f"[green]Player '{args.name}' added with balance ${args.balance}.[/green]")

    elif args.command == "play":
        if not all([args.name, args.bet_type, args.amount, args.choice]):
            print("[red]--name, --bet-type, --amount, and --choice are required to play.[/red]")
        else:
            bet_type = bet_type_map.get(args.bet_type, args.bet_type)
            play_game(args.name, bet_type, args.amount, args.choice)

    elif args.command == "help-table":
        show_help_table()
