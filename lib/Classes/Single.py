import random
from Classes.__init__ import conn, cursor

class Game:
    def __init__(self, player, id = None, result = "Yes", bet = "Eeyore", player_id = None):
        self.player = player
        self.id = id
        self.deck = self.generate_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.result = result
        self.bet = bet 
        self.player_id = player_id
        # Initialize bet to 0; Eleanor fix

    # ... rest of the Game class ...

    @property
    def player(self):
        return self._player
    
    @player.setter
    def player(self, player):
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

    def generate_deck(self):
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        deck = [{"rank": rank, "suit": suit} for rank in ranks for suit in suits]
        random.shuffle(deck)
        print('Deck Generated')
        return deck

    def deal_initial_cards(self):
        # Deal two cards to the player and two cards to the dealer
        self.player_hand = []
        self.dealer_hand = []
        for _ in range(2):
            self.player_hand.append(self.deck.pop())
            self.dealer_hand.append(self.deck.pop())
        print(self.player_hand)
        # print(self.dealer_hand)

  


    def player_hit(self):
        # Player requests a hit (draws a card)
        if not self.is_game_over():
            self.player_hand.append(self.deck.pop())

    def dealer_play(self):
        # Dealer plays according to standard rules (stands on 17 or higher)
        while self.calculate_hand_value(self.dealer_hand) < 17 and self.calculate_hand_value(self.player_hand) <21 :
            self.dealer_hand.append(self.deck.pop())
        print(self.dealer_hand)
        Game.determine_winner(self)
        print(Game.determine_winner(self))
        self.update_results()
        self.game_menu()


        
    def is_game_over(self):
        # Check if the game is over (player or dealer has blackjack or busted)
        player_value = self.calculate_hand_value(self.player_hand)
        dealer_value = self.calculate_hand_value(self.dealer_hand)
        return player_value >= 21 or dealer_value >= 21

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
    
    def save(self):
        sql = '''
            INSERT INTO games (bet, result, player_id)
            VALUES (?, ?, ?)
        '''
        cursor.execute(sql, (self.bet, self.result, self.player_id))
        conn.commit()

    
    @classmethod
    def create(cls, bet, result, player_id):
        print(f'Bet Amount: {bet}')
        # result = cls(player, player_id, result, bet)
        result = cls(player = None, result = result, bet = bet, player_id = player_id) #Eleasor fix
        print(result.bet)
        # print(result.bet)
        result.save()

        
        
class Player:

    all = {}

    def __init__(self, name = None, chips=1000, id = None):
        self.name = name
        self.chips = chips
        self.id = id
        self.hand = []

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name) > 0:
            # if not self.name_exists('data.db'):
                self._name = name
            # else:
            #     raise Exception('Name exists, enter new name')
        else:
            raise Exception('Invalid Name')
        
    # def name_exists(self):
    #     cursor.execute('SELECT COUNT(*) FROM players WHERE name = ?', (self._name,))
    #     result = cursor.fetchone()
    #     conn.close()
    #     return result[0] > 0


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
    
    @classmethod
    def drop_table(cls):
        sql = '''
            DROP TABLE IF EXISTS players
        '''
        cursor.execute(sql)
        conn.commit()
    
    @classmethod
    def create_table(cls):
        sql = '''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                chips INTEGER
            )
        '''
        cursor.execute(sql)
        conn.commit()

    @classmethod
    def instance_from_db(cls, row):
        player = cls.all.get(row[0])

        if player:
            player.id = row[0]
            player.name = row[1]
            player.chips = row[2]
        else:
            player = cls(row[1], row[2])
            player.id = row[0]
            cls.all[player.id] = player
        return player

    
    @classmethod
    def get_by_id(cls, id):
        # Query the database to retrieve a player by ID
        sql = '''
            SELECT *
            FROM players 
            WHERE id = ?
        '''
        row = cursor.execute(sql, (id,)).fetchone()

        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_name(cls, name):
        sql = '''
            SELECT *
            FROM players
            WHERE name = ?
        '''
        row = cursor.execute(sql, (name, )).fetchone()

        return cls.instance_from_db(row) if row else None


    def __str__(self):
        return f"Player {self.name}: Chips {self.chips}"
    
    def save(self):
        sql = '''
            INSERT INTO players (name, chips)
            VALUES (?, ?)
        '''
        cursor.execute(sql, (self.name, self.chips))
        conn.commit()

    
    @classmethod
    def create(cls, name, chips):
        player = cls(name, chips)
        player.save()
        return player
    
    
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