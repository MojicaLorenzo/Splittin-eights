from Classes.__init__ import conn, cursor

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
                self._name = name
        else:
            raise Exception('Invalid Name')


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

    def __str__(self):
        return f"Player {self.name}: Chips {self.chips}"
    
    def save(self):
        sql = '''
            INSERT INTO players (name, chips)
            VALUES (?, ?)
        '''
        cursor.execute(sql, (self.name, self.chips))
        conn.commit()
    
    def update(self):
        sql = '''
            UPDATE players
            SET name = ?, chips = ?
            WHERE id = ?
        '''

        cursor.execute(sql, (self.name, self.chips, self.id))
        conn.commit()

    def delete(self):
        sql = '''
            DELETE FROM players
            WHERE id = ?
        '''

        cursor.execute(sql, (self.id, ))
        conn.commit()

        del Player.all[self.id]
        self.id = None

    @classmethod
    def create(cls, name, chips):
        player = cls(name, chips)
        player.save()
        return player
    
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
    def find_by_name(cls, name):
        sql = '''
            SELECT *
            FROM players
            WHERE name = ?
        '''
        row = cursor.execute(sql, (name, )).fetchone()

        return cls.instance_from_db(row) if row else None