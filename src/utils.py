import random
from src.settings import MAX_RESPONSE_RANGE, CONVERSATION_CHANCE, LAUGH_REACT_CHANCE
from src.personality import personalities
from rich.table import Table
from rich.box import ROUNDED
from rich.console import Console

console = Console()

def get_random_max_responses():
    return random.randint(*MAX_RESPONSE_RANGE)

def ready_table():
    table = Table(title="Personality Traits and Random Chance Variables", box=ROUNDED, padding=(1, 1))
    table.add_column("Variable", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    table.add_row("depressed", personalities["depressed"])
    table.add_row("history_buff", personalities["history_buff"])
    table.add_row("informative", personalities["informative"])
    table.add_row("favorite_movies", personalities["favorite_movies"])
    table.add_row("favorite_games", personalities["favorite_games"])
    table.add_row("interests", personalities["interests"])
    table.add_row("CONVERSATION_CHANCE", f"{CONVERSATION_CHANCE * 100:.0f}%")
    table.add_row("LAUGH_REACT_CHANCE", f"{LAUGH_REACT_CHANCE * 100:.0f}%")
    table.add_row("MAX_RESPONSES", f"{MAX_RESPONSE_RANGE[0]} - {MAX_RESPONSE_RANGE[1]}")
    console.print(table)