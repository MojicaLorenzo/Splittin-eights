import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        # Create database tables if they don't exist
        cursor = self.conn.cursor()

        # Player table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                chips INTEGER
            )
        ''')

        # Game table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER,
                bet INTEGER,
                result TEXT,
                FOREIGN KEY (player_id) REFERENCES players(id)
            )
        ''')

        self.conn.commit()

    def add_player(self, name, chips):
        # Add a new player to the database
        cursor = self.conn.cursor()
        try:
            cursor.execute('INSERT INTO players (name, chips) VALUES (?, ?)', (name, chips))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print("Player with this name already exists.")
            return False

    def find_player_by_name(self, name):
        # Find a player by name in the database
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM players WHERE name = ?', (name,))
        return cursor.fetchone()

    def update_player_chips(self, player_id, chips):
        # Update a player's chips in the database
        cursor = self.conn.cursor()
        cursor.execute('UPDATE players SET chips = ? WHERE id = ?', (chips, player_id))
        self.conn.commit()
        
    def add_game(self, player_id, bet, result):
        # Add a new game to the database
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO games (player_id, bet, result) VALUES (?, ?, ?)', (player_id, bet, result))
        self.conn.commit()

    def display_all_players(self):
        # Display all players from the database
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM players')
        players = cursor.fetchall()
        return players

    def display_all_games(self):
        # Display all games from the database
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM games')
        games = cursor.fetchall()
        return games

    def close_connection(self):
        # Close the database connection
        self.conn.close()