# Roulette CLI Tool

A colorful and interactive command-line roulette game written in Python. Bet on your favorite numbers or colors and watch the wheel spin with live animation in your terminal.

---

## Features

- European-style roulette with a single zero
- 10 types of bets (Odd/Even, Red/Black, Dozen, Column, etc.)
- Real-time animated number rolling  
- Colored number display (red, black, green)
- Persistent player profiles with balance tracking
- Play in interactive mode or via CLI arguments
- Help table with odds and payout details

---

## Quick Start

### 1. Install dependencies

```bash
pip install rich prettytable
```

### 2. Run interactively

```bash
python rouletteWheel.py
```

Follow the prompts to select your player, choose a bet, and watch the wheel spin.

### 3. Command Line Usage

```bash
rouletteWheel.py [-h] [-n NAME] [-b BALANCE] [-t BET_TYPE] [-a AMOUNT] [-c CHOICE] [{add-player,play,help-table}]
```

#### Add a player: 

```bash
python rouletteWheel.py add-player -n Alice -b 100
```

#### Place a bet: 

```bash
python rouletteWheel.py play -n Alice -t "black/red" -a 20 -c red
```

#### Show betting guide: 

```bash
python rouletteWheel.py help-table
```

---

## Player Data

Player balances are saved in a local `players.json` file. Balances persist across sessions.

---

## Dependencies

- `rich` – for colored terminal output
- `prettytable` – for table display

Install them with:

```bash
pip install rich prettytable
```

---

## Future updates: 

- Try to add actual wheel spinning
  