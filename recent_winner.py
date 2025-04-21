# recent_winner.py
import json

# Filväg för att lagra de senaste vinnarna
RECENT_WINNERS_FILE = 'recent_winners.json'

def save_recent_winner(winner_name, score, tank, country):
    try:
        with open(RECENT_WINNERS_FILE, 'r') as file:
            recent_winners = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        recent_winners = []

    # Lägg till den nya posten först
    recent_winners.append({
        'name': winner_name,
        'score': score,
        'tank': tank,
        'country': country
    })

    # Spara endast de 6 senaste posterna
    recent_winners = recent_winners[-6:][::-1]

    # Skriv tillbaka till filen
    with open(RECENT_WINNERS_FILE, 'w') as file:
        json.dump(recent_winners, file, indent=4)

def get_recent_winners():
    try:
        with open(RECENT_WINNERS_FILE, 'r') as file:
            recent_winners = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        recent_winners = []

    return recent_winners
