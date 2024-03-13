# models/match.py

class Match:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.played = False
        self.result = None

    def is_played(self):
        return self.played

    def play_match(self, winner):
        if not self.played:
            self.played = True
            self.result = winner
            if winner == "player1":
                self.player1.points += 1.0
                self.player2.points += 0.0
            elif winner == "player2":
                self.player1.points += 0.0
                self.player2.points += 1.0
            else:
                self.player1.points += 0.5
                self.player2.points += 0.5
