class Round:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.played = False
        self.result = None

    def play_match(self, result):
        if result == "draw":
            self.player1.add_points(0.5)
            self.player2.add_points(0.5)
        elif result == "player1":
            self.player1.add_points(1)
        elif result == "player2":
            self.player2.add_points(1)

        self.played = True
        self.result = result

    def was_played(self):
        return self.played
