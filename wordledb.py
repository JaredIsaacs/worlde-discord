import sqlite3, datetime, pickle, random
from os import path, makedirs
from globals import *

class WordleDB():
    def __init__(self) -> None:
        if not path.exists('db'):
            makedirs('db')
        self.conn = sqlite3.connect(DB_PATH)
        self.cur = self.conn.cursor()

    
    def close(self) -> None:
        self.conn.close()
        self.cur.close()


    def init_db(self) -> None:
        self.cur.execute('''CREATE TABLE IF NOT EXISTS wordle
                    (date TEXT NOT NULL, guild_id INTEGER NOT NULL, completed TEXT,
                    won TEXT, accuracy_board BINARY NOT NULL, letter_board BINARY NOT NULL)''')
        
        self.cur.execute('''CREATE TABLE IF NOT EXISTS wordle_word (date TEXT NOT NULL, word TEXT NOT NULL)''')

        self.conn.commit()


    def check_guild_exists(self, guild_id: int) -> bool:
        today = datetime.date.today()
        guild = self.cur.execute('''SELECT * FROM wordle
                            WHERE guild_id = ? AND date = ?''', (guild_id, today))
        if guild.fetchone():
            return True
        return False


    def check_complete(self, guild_id: int) -> bool:
        today = datetime.date.today()
        complete = self.cur.execute('''SELECT completed FROM wordle
                            WHERE guild_id = ? AND date = ?''', (guild_id, today))
        
        res = complete.fetchone()
        if not res:
            return False
        
        return bool(int(res[0]))


    def check_won(self, guild_id: int) -> bool:
        today = datetime.date.today()
        won = self.cur.execute('''SELECT won FROM wordle
                            WHERE guild_id = ? AND date = ?''', (guild_id, today))
        
        res = won.fetchone()
        if not res:
            raise KeyError
        if isinstance(res[0], None):
            raise AssertionError('Game has not been completed yet!')
        
        return bool(int(res[0]))


    def update_wordle_progress(self, guild_id: int, accuracy_board: list, letter_board: list, completed: bool = False, won: bool = None):
        today = datetime.date.today()

        p_accuracy = pickle.dumps(accuracy_board, protocol=pickle.HIGHEST_PROTOCOL)
        p_letter = pickle.dumps(letter_board, protocol=pickle.HIGHEST_PROTOCOL)

        if self.check_guild_exists(guild_id):
            self.cur.execute('''UPDATE wordle 
                        SET completed = ?, won = ?, accuracy_board = ?, letter_board = ?
                        WHERE guild_id = ? AND date = ?''', (completed, won, p_accuracy, p_letter, guild_id, today))
        else:
            self.cur.execute('''INSERT INTO wordle (date, guild_id, completed, won, accuracy_board, letter_board)
                                    values (?, ?, ?, ?, ?, ?)''', (today, guild_id, completed, won, p_accuracy, p_letter))
        self.conn.commit()


    def get_wordle_progress(self, guild_id: int):
        today = datetime.date.today()

        self.cur.execute('''SELECT accuracy_board, letter_board FROM wordle
                        WHERE guild_id = ? AND date = ?''', (guild_id, today))
        boards = self.cur.fetchone()
        
        accuracy_board = pickle.loads(boards[0])
        letter_board = pickle.loads(boards[1])

        return accuracy_board, letter_board 
    

    def update_word(self) -> str:
        today = datetime.date.today()
        word = random.choice(list(WORD_LIST))

        self.cur.execute('''INSERT INTO wordle_word (date, word) values (?, ?)''', (today, word))
        self.conn.commit()

        return word


    def check_word_exists(self):
        today = datetime.date.today()

        guild = self.cur.execute('''SELECT * FROM wordle_word
                            WHERE date = ?''', (today,))
        
        if guild.fetchone():
            return True
        return False


    def get_word(self) -> str:
        today = datetime.date.today()

        if self.check_word_exists():
            word = self.cur.execute("SELECT word FROM wordle_word WHERE date = ?", (today,)).fetchone()[0]
        else:
            word = self.update_word()

        return word.upper()


    def get_all_wordles(self):
        # For Debug purposes
        self.cur.execute('SELECT date, guild_id, completed, won FROM wordle')
        for e in self.cur:
            print(e)
