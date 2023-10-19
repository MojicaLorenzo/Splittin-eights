import os
from Classes.Player import Player
from Classes.Game import Game
from Classes.Cards import Card

# MENU BOOT UP

if __name__ == "__main__":
    menu = Menu()
    menu.main_menu()

class Menu:

# CONSTRUCTOR

    def __init__(self):
        self.players = []
        self.current_player = None
        self.game = None
        self.player_hand = []
        self.dealer_hand = []
        self.deck = Game.generate_deck(self)
        self.bet_amount = None
        self.player_chips = None

# MENUS

    def main_menu(self):
        # Player.drop_table()
        # Game.drop_table()
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

    def results_menu(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        while True:
            print("RESULTS MENU")
            print("1. Results by name")
            print("2. ALL Game Results")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.results_by_name()
            elif choice == "2":
                self.get_all_results()
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

# PLAYER OPTIONS

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

    def display_chips(self):
        print(f'{self.current_player.name} has {self.current_player.chips} chips.')

# GAMEPLAY

    def new_game(self):
        self.place_bet()
        self.calc_winnings()
        os.system('clear' if os.name == 'posix' else 'cls')
        Game.generate_deck(self)
        Game.deal_initial_cards(self)
        self.calculate_hand_value(self.player_hand)

        #ASCII ART

        hidden_card = {"rank": "X", "suit": "X"}
        dealer_display = [hidden_card] + [self.dealer_hand[1]]
        self.display_hand_ascii(self.player_hand, title="Player's Hand")
        self.display_hand_ascii(dealer_display, title="Dealer's Hand")
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
        hidden_card = {"rank": "X", "suit": "X"}
        dealer_display = [hidden_card] + [self.dealer_hand[1]]
        self.display_hand_ascii(dealer_display, title="Dealer's Hand")


    def place_bet(self):
        while True:
            bet_amount = input(f"{self.current_player.name}, enter your bet amount: ")
            if bet_amount.isdigit():
                if self.game.place_bet(int(bet_amount)):
                    self.bet_amount = bet_amount
                    break
            else:
                print("Invalid bet amount. Please enter a valid number.")

    def player_hit(self):
        # Player requests a hit (draws a card)
        if not self.is_game_over():
            self.player_hand.append(self.deck.pop())
        self.calculate_hand_value(self.player_hand)
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
    
    def calc_winnings(self):
        current_bet = int(self.bet_amount)
        result = Game.determine_winner(self)
        if result == "Tie":
            return current_bet
        elif result == self.current_player.name:
            return (current_bet * 2)
        elif result == "Dealer":
            return 0
        
# DATABASE CHANGES
        
    def update_results(self):
        winner = Game.determine_winner(self)
        player_num = Player.find_by_name(self.current_player.name)
        Game.create(self.bet_amount, winner, player_num.id)
    
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

    def results_by_name(self):
        player_name = input("Enter the player's name to load: ")
        current_search = Player.find_by_name(player_name)
        results = Game.find_by_results_id(current_search.id)
        for result in results:
            print(f'Result:{result.result} \n   {player_name} bet {result.bet} coins')

    def get_all_results(self):
        all_results = Game.get_all()
        print(all_results)
        for result in all_results:
            player = Player.find_by_id(result.player_id)
            if result.result == "Tie":
                print(f'Result of game is a Tie \n    {player.name} bet {result.bet} coins')
            else:
                print(f'{result.result} WON \n   {player.name} bet {result.bet} coins')
