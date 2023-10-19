class Card:

# CONSTRUCTOR

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        
# ASCII FORMAT

    def ascii_representation(self):
        lines = ["+-----+"] * 7
        rank = self.rank

        # If the card is a hidden card, represent it differently
        if rank == "X":
            for i in range(1, 6):
                lines[i] = "|     |"
            return lines

        if self.rank == "10":  # Adjust for two-digit ranks
            rank = "10"
        else:
            rank = " " + self.rank

        # Assign suit symbols
        suit_symbols = {
            "Hearts": "\u2665",
            "Diamonds": "\u2666",
            "Clubs": "\u2663",
            "Spades": "\u2660"
        }

        lines[1] = f"|{rank}   |"
        lines[2] = f"| {suit_symbols[self.suit]}   |"
        lines[4] = f"|   {suit_symbols[self.suit]} |"
        lines[5] = f"|   {rank}|"

        return lines

    def __repr__(self):
        return str(self)
