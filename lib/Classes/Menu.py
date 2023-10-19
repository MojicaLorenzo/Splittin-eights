import os
from Classes.Player import Player
from Classes.Game import Game
from Classes.Cards import Card

class Menu:

    def __init__(self):
        self.players = []
        self.current_player = None
        self.game = None
        self.player_hand = []
        self.dealer_hand = []
        self.deck = Game.generate_deck(self)
        self.bet_amount = None
        self.player_chips = None

    def main_menu(self):
        Player.drop_table()
        Game.drop_table()
        Player.create_table()
        Game.create_table()
        while True:
            os.system('clear' if os.name == 'posix' else 'cls')
            print("MAIN MENU")
            print("1. New Player\n")
            print("2. Load Player\n")
            print("3. View Results\n")
            print("4. Exit\n")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.new_player()
            elif choice == "2":
                self.load_player()
            elif choice == "3":
                self.results_menu()
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                input("Invalid choice. Press Enter to continue...")
                
    def new_player(self):
        player_name = input("Enter your player's name: ")
        player_chips = input("Enter the starting chips amount: ")

        if not player_name or not player_chips.isdigit():
            input("Invalid input. Press Enter to continue...")
            return

        player = Player.create(player_name, int(player_chips))
        self.players.append(player)
        self.current_player = player
        self.player_chips = int(player_chips)

        self.game = Game(player)
        self.game_menu()

    def load_player(self):
        player_name = input("Enter the player's name to load: ")
        searched_name = Player.find_by_name(player_name)
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f'Welcome Back {searched_name.name}!')
        if searched_name.name == player_name:
                self.current_player = searched_name
                self.game = Game(searched_name)
                self.game_menu()
                return

        input("Player not found. Press Enter to continue...")

    def results_menu(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        while True:
            print("RESULTS MENU")
            print("1. Results by name")
            print("2. ALL Game Results")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                print('Under Construction')
            elif choice == "2":
                print('Under Construction')
            elif choice == "3":
                self.main_menu()
                break

    def game_menu(self):
        while True:
            print("PLAYER MENU")
            print("1. New Game")
            print("2. Check Chip Count")
            print("3. Cash Out")
            print("4. DELETE PLAYER")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.new_game()
            elif choice == "2":
                self.display_chips()
            elif choice == "3":
                self.main_menu()
            elif choice == "4":
                self.delete_player()
                break
            else:
                input("Invalid choice. Press Enter to continue...")

    def new_game(self):
        self.place_bet()
        self.calc_winnings()
        Game.generate_deck(self)
        os.system('clear' if os.name == 'posix' else 'cls')
        Game.deal_initial_cards(self)
        self.calculate_hand_value(self.player_hand)
        # self.show_dealers_top_card()
        #ascii art
        hidden_card = {"rank": "X", "suit": "X"}
        dealer_display = [hidden_card] + [self.dealer_hand[1]]
        self.display_hand_ascii(self.player_hand, title="Player's Hand")
        self.display_hand_ascii(dealer_display, title="Dealer's Hand")
        #ascii art
        # self.display_hand_ascii(self.player_hand, title="Player's Hand")
        # self.display_hand_ascii(self.dealer_hand, title="Dealer's Hand")
        self.in_game_menu()

        pass

    def calculate_hand_value(self, hand):
        # Calculate the total value of a hand, accounting for Aces
        hand_value = 0
        num_aces = 0

        for card in hand:
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
    
    def show_dealers_top_card(self):
        # print(self.dealer_hand[1])
        hidden_card = {"rank": "X", "suit": "X"}
        dealer_display = [hidden_card] + [self.dealer_hand[1]]
        self.display_hand_ascii(dealer_display, title="Dealer's Hand")

    def display_chips(self):
        print(f'{self.current_player.name} has {self.current_player.chips} chips.')

    def place_bet(self):
        while True:
            bet_amount = input(f"{self.current_player.name}, enter your bet amount: ")
            if bet_amount.isdigit():
                if self.game.place_bet(int(bet_amount)):
                    self.bet_amount = bet_amount
                    break
            else:
                print("Invalid bet amount. Please enter a valid number.")

    def in_game_menu(self):
        while True:
            print("PLAY MENU")
            print("1. Hit")
            print("2. Stay")
            print("3. Quit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.player_hit()
            elif choice == "2":
                Game.dealer_play(self)
            elif choice == "3":
                self.game_menu()
                break
            else:
                input("Invalid choice. Press Enter to continue...")

    def player_hit(self):
        # Player requests a hit (draws a card)
        if not self.is_game_over():
            self.player_hand.append(self.deck.pop())
        self.calculate_hand_value(self.player_hand)
        # print(self.player_hand)
        # print(self.dealer_hand[1])
        self.display_hand_ascii(self.player_hand, title="Player's Hand")
        self.show_dealers_top_card()

    def display_hand_ascii(self, hand, title=""):
        cards_ascii = [Card(card["rank"], card["suit"]).ascii_representation() for card in hand]
        for i in range(7):
            print(" ".join(card[i] for card in cards_ascii))
        print(title)


    def is_game_over(self):
        # Check if the game is over (player or dealer has blackjack or busted)
        player_value = self.calculate_hand_value(self.player_hand)
        dealer_value = self.calculate_hand_value(self.dealer_hand)
        return player_value >= 21 or dealer_value >= 21
    
    def update_results(self):
        winner = Game.determine_winner(self)
        player_num = Player.find_by_name(self.current_player.name)
        Game.create(self.bet_amount, winner, player_num.id)
    
    def calc_winnings(self):
        current_bet = int(self.bet_amount)
        result = Game.determine_winner(self)
        if result == "Tie":
            return current_bet
        elif result == self.current_player.name:
            return (current_bet * 2)
        elif result == "Dealer":
            return 0
        
    def update_chips(self):
        current = Player.find_by_name(self.current_player.name)
        new_chips = int(self.current_player.chips) + (self.calc_winnings())
        self.current_player.name = self.current_player.name
        self.current_player.chips = new_chips
        self.current_player.id = current.id
        self.current_player.update()

    def delete_player(self):
        current = Player.find_by_name(self.current_player.name)
        results = Game.find_by_results_id(current.id)
        for result in results:
            Game.delete(result)
        Player.delete(current)
        self.main_menu()

if __name__ == "__main__":
    menu = Menu()
    menu.main_menu()