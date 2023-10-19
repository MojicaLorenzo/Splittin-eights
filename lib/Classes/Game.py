import random
from Classes.__init__ import conn, cursor

class Game:

    all = {}

    def __init__(self, player, id = None, result = "Yes", bet = "Eeyore", player_id = None):
        self.player = player
        self.id = id
        self.deck = self.generate_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.result = result
        self.bet = bet 
        self.player_id = player_id
        # Initialize bet to 0

    @property
    def player(self):
        return self._player
    
    @player.setter
    def player(self, player):
        from Classes.Player import Player
        if isinstance(player, Player):
            self._player = player

    def place_bet(self, bet):
        if bet <= self.player.chips:
            self.bet = bet
            self.player.chips -= bet
            return True
        else:
            print("Insufficient chips to place the bet.")
            return False
        
    def generate_new_decks(self):
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        deck = [{"rank": rank, "suit": suit} for rank in ranks for suit in suits]
        decks = deck + deck
        return decks

    def generate_deck(self):
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        deck = [{"rank": rank, "suit": suit} for rank in ranks for suit in suits]
        decks = deck + deck
        if len(decks) < 20:
            self.generate_new_decks()
            random.shuffle(decks)
        else:
            random.shuffle(decks)
        return decks

    def deal_initial_cards(self):
        # Deal two cards to the player and two cards to the dealer
        self.player_hand = []
        self.dealer_hand = []
        for _ in range(2):
            self.player_hand.append(self.deck.pop())
            self.dealer_hand.append(self.deck.pop())

    def player_hit(self):

        #DRAWS CARD

        if not self.is_game_over():
            self.player_hand.append(self.deck.pop())

        #ASCII DISPLAY

        self.display_hand(self.player_hand, title="Player's Hand")

    def dealer_play(self):
        # Dealer plays according to standard rules (stands on 17 or higher)
        while self.calculate_hand_value(self.dealer_hand) < 17 and self.calculate_hand_value(self.player_hand) <21 :
            self.dealer_hand.append(self.deck.pop())
        # print(self.dealer_hand)
        # ascii code
        self.display_hand_ascii(self.player_hand, title="Player's Hand")
        self.display_hand_ascii(self.dealer_hand, title="Dealer's Hand")
        Game.determine_winner(self)
        print(f'WINNER: {Game.determine_winner(self)}')
        print(f'{self.current_player.name} won {self.calc_winnings()} chips')
        self.update_chips()
        self.update_results()
        self.game_menu()

    def determine_winner(self):
        # Determine the winner of the game
        player_value = self.calculate_hand_value(self.player_hand)
        dealer_value = self.calculate_hand_value(self.dealer_hand)
        
        if player_value > 21:
            return "Dealer"
        elif dealer_value > 21:
            return self.current_player.name
        elif player_value == dealer_value:
            return "Tie"
        elif player_value > dealer_value:
            return self.current_player.name
        else:
            return "Dealer"
        
# DATABASE INSTANCES
        
    def delete(self):
        sql = '''
            DELETE FROM games
            WHERE player_id = ?
        '''

        cursor.execute(sql, (self.player_id, ))
        conn.commit()
    
    def save(self):
        sql = '''
            INSERT INTO games (bet, result, player_id)
            VALUES (?, ?, ?)
        '''
        cursor.execute(sql, (self.bet, self.result, self.player_id))
        conn.commit()

# DATABASE METHODS
        
    @classmethod
    def create_table(cls):
        sql = '''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bet INTEGER,
                result TEXT,
                player_id INTEGER,
                FOREIGN KEY (player_id) REFERENCES players(id))
        '''
        cursor.execute(sql)
        conn.commit()
    
    @classmethod
    def create(cls, bet, result, player_id):
        result = cls(player = None, result = result, bet = bet, player_id = player_id)
        result.save()

    @classmethod
    def instance_from_db(cls, row):
        result = cls.all.get(row[0])
        if result:
            result.id = row[0]
            result.bet = row[1]
            result.result = row[2]
            result.player_id = row[3]
        else:
            result = cls(player = None, bet = row[1], result = row[2], player_id = row[3])
            result.id = row[0]
            cls.all[result.id] = result
        return result

    @classmethod
    def find_by_results_id(cls, player_id):
        sql = ''' 
            SELECT *
            FROM games
            WHERE player_id = ?
        '''

        rows = cursor.execute(sql, (player_id, )).fetchall()

        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM games
        """

        rows = cursor.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def drop_table(cls):
        sql = '''
            DROP TABLE IF EXISTS games
        '''
        cursor.execute(sql)
        conn.commit()