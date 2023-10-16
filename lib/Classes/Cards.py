# class Cards:
#     def __init__(self, rank, suit):
#         self.rank = rank
#         self.suit = suit
#         pass

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def get_value(self):
        # Calculate the value of the card for blackjack
        if self.rank.isdigit():
            return int(self.rank)
        elif self.rank in ("K", "Q", "J"):
            return 10
        elif self.rank == "A":
            return 11

    def __repr__(self):
        return str(self)
