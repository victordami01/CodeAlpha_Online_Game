class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0

    def get_player_move(self, p):
        """Returns the move of player p (0 or 1)"""
        return self.moves[p]

    def play(self, player, move):
        """Registers a move for a player"""
        self.moves[player] = move.upper()[0]  # Store only first letter (R, P, S)
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        """Returns True if both players are connected"""
        return self.ready

    def bothWent(self):
        """Returns True if both players have made a move"""
        return self.p1Went and self.p2Went

    def winner(self):
        """Determines the winner"""
        if self.moves[0] is None or self.moves[1] is None:  # Ensure both moves exist
            return -1  # Game not ready to decide winner

        p1, p2 = str(self.moves[0]).upper(), str(self.moves[1]).upper()  # Ensure they are strings

        win_conditions = {
            ("R", "S"): 0,
            ("S", "R"): 1,
            ("P", "R"): 0,
            ("R", "P"): 1,
            ("S", "P"): 0,
            ("P", "S"): 1,
        }

        if p1 == p2:
            return -1  # Tie
        return win_conditions.get((p1, p2), -1)  # Return winner (0 or 1)

    def resetWent(self):
        """Resets player move status for a new round"""
        self.p1Went = False
        self.p2Went = False
        self.moves = [None, None]

    def reset_game(self):
        """Fully resets the game (scores included)"""
        self.resetWent()
        self.wins = [0, 0]
        self.ties = 0

    def to_dict(self):
        """Converts game state to a dictionary for JSON serialization"""
        return {
            "id": self.id,
            "ready": self.ready,
            "moves": self.moves,
            "p1Went": self.p1Went,
            "p2Went": self.p2Went,
            "wins": self.wins,
            "ties": self.ties
        }
