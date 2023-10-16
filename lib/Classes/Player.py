# class Player:
#     def __init__(self, name, cards):
#         self.name = name
#         self.cards = cards
#         pass
class Player:
    def __init__(self, name, chips=1000):
        self.name = name
        self.chips = chips
        self.hand = []

    def bet(self, amount):
        # Place a bet
        if amount <= self.chips:
            self.chips -= amount
            return amount
        else:
            print("Insufficient chips to place the bet.")
            return 0

    def receive_winnings(self, amount):
        # Receive winnings after winning a round
        self.chips += amount

    def receive_card(self, card):
        # Receive a card and add it to the player's hand
        self.hand.append(card)

    def clear_hand(self):
        # Clear the player's hand after each round
        self.hand = []

    def get_hand_value(self):
        # Calculate the total value of the player's hand
        hand_value = 0
        num_aces = 0

        for card in self.hand:
            rank = card["rank"]
            if rank.isdigit():
                hand_value += int(rank)
            elif rank in ("K", "Q", "J"):
                hand_value += 10
            elif rank == "A":
                hand_value += 11
                num_aces += 1

        # Adjust the value of Aces if the hand value exceeds 21
        while hand_value > 21 and num_aces > 0:
            hand_value -= 10
            num_aces -= 1

        return hand_value

    def is_busted(self):
        # Check if the player's hand value exceeds 21
        return self.get_hand_value() > 21

    def __str__(self):
        return f"Player {self.name}: Chips {self.chips}"