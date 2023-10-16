from Classes.Menu import Menu
from Classes.Single import Game, Player

# def database():
#     database = Database()

def data():
    game = Game()
    player = Player()
    game.create_table()
    player.create_table()

def main():
    menu = Menu()
    menu.main_menu()

if __name__ == "__main__":
    data()
    main()
