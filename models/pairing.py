import random
from .round import Round


def generate_pairings(players):
    """
    Generate pairings for a round based on the current order of players.
    """
    matches = [Round(players[i], players[i + 1]) for i in range(0, len(players), 2)]
    return matches


def random_pairings(players):
    """
    Generate random pairings for the first round.
    """
    random.shuffle(players)
    return generate_pairings(players)
