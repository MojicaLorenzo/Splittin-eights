import os
from Classes.Single import Player
from Classes.Single import Game

class Menu:

    def __init__(self):
        self.players = []
        self.current_player = None
        self.game = None

    def main_menu(self):
        while True:
            os.system('clear' if os.name == 'posix' else 'cls')
            print("Blackjack CLI")
            print("1. New Game")
            print("2. Load Player")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.new_game()
            elif choice == "2":
                self.load_player()
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                input("Invalid choice. Press Enter to continue...")

    def new_game(self):
        player_name = input("Enter your player's name: ")
        player_chips = input("Enter the starting chips amount: ")

        if not player_name or not player_chips.isdigit():
            input("Invalid input. Press Enter to continue...")
            return

        player = Player(player_name, int(player_chips))
        self.players.append(player)
        self.current_player = player

        self.game = Game(player)
        self.place_bet()

    def place_bet(self):
        while True:
            bet_amount = input(f"{self.current_player.name}, enter your bet amount: ")
            if bet_amount.isdigit():
                if self.game.place_bet(int(bet_amount)):
                    break
            else:
                print("Invalid bet amount. Please enter a valid number.")

    def load_player(self):
        player_name = input("Enter the player's name to load: ")

        for player in self.players:
            if player.name == player_name:
                self.current_player = player
                self.game = Game(player)
                self.place_bet()
                return

        input("Player not found. Press Enter to continue...")

if __name__ == "__main__":
    menu = Menu()
    menu.main_menu()