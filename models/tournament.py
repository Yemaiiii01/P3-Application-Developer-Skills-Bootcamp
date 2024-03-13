import random
from .round import Round
from .pairing import generate_pairings, random_pairings


class Tournament:

    def __init__(self, name, venue, start_date, end_date, players, max_round):
        if not name:
            raise ValueError("Player name is required!")

        self.name = name
        self.venue = venue
        self.start_date = start_date
        self.end_date = end_date
        self.players = players
        self.max_round = max_round
        self.rounds = []
        self.current_round = 0
        self.is_round_setup_done = False

    def shuffle_players(self):
        random.shuffle(self.players)

    def sort_players(self):
        self.players.sort(key=lambda player: player.points, reverse=True)

    def play_round(self):
        if self.current_round >= self.max_round:
            print("Maximum number of rounds reached. No new rounds will occur.")
            return False

        if not self.is_round_setup_done:
            self.current_round += 1
            self.is_round_setup_done = True

            if not self.rounds or len(self.rounds) < self.current_round:
                # Initialize rounds list or add a new round if needed
                matches = random_pairings(self.players)
                self.rounds.append(matches)
            else:
                self.sort_players()
                matches = generate_pairings(self.players)
                self.rounds[self.current_round - 1] = matches  # Update the current round

        self.is_round_setup_done = False
        return True

    def is_completed(self):
        return self.current_round >= self.max_round

    def declare_winner(self):
        if not self.is_completed():
            print("The tournament is not completed yet.")
            return

        self.sort_players()
        winner = self.players[0]

        print(f"{'\n*** Tournament Winner ***\n'}")
        print(f"Congratulations to {winner.name} for winning the tournament!")
        print(f"{'Final Standings:'}")
        self.display_rankings()

    def display_player_info(self):
        for player in sorted(self.players, key=lambda p: p.points, reverse=True):
            print(player)

    def display_rankings(self):
        sorted_players = sorted(self.players, key=lambda x: x.points, reverse=True)
        for player in sorted_players:
            print(f"Name: {player.name}, Points: {player.points}")
