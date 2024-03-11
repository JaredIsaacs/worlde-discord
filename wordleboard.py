from globals import *
from PIL import Image, ImageDraw, ImageFont


class WordleBoard():
    def __init__(self, accuracy_board: list = None, letter_board: list = None):
        self.isWinner = None
        self.correct_chars = 0

        if accuracy_board is None:
            self.accuracy_board = [
                [None, None, None, None, None],
                [None, None, None, None, None],
                [None, None, None, None, None],
                [None, None, None, None, None],
                [None, None, None, None, None],
                [None, None, None, None, None]
            ]
        else:
            self.accuracy_board = accuracy_board

        if letter_board is None: 
            self.letter_board = [
                [None, None, None, None, None],
                [None, None, None, None, None],
                [None, None, None, None, None],
                [None, None, None, None, None],
                [None, None, None, None, None],
                [None, None, None, None, None]
            ]
        else:
            self.letter_board = letter_board


    def process_word(self, guess: str, word: str):
        assert len(guess) == 5, f'{guess} is not 5 characters long!' #Check if guess is correct length
        assert guess.lower() in WORD_LIST, f'{guess} is not in the guess list!' #Check if guess is in the guess list. Can maybe combine this with previous check.

        self.correct_chars = 0
        guess = guess.upper()
        unmatched = {}

        letter_row = next(row for row in self.letter_board if None in row)
        for i, char in enumerate(guess): 
            letter_row[i] = char

        accuracy_row = next(row for row in self.accuracy_board if None in row)
        for i in range(len(word)):
            if word[i] == guess[i]:
                accuracy_row[i] = 2
                self.correct_chars += 1
            else:
                unmatched[word[i]] = unmatched.get(word[i], 0) + 1

        for i in range(len(guess)):
            if guess[i] != word[i]:
                if unmatched.get(guess[i], 0) > 0:
                    accuracy_row[i] = 1
                    unmatched[guess[i]] -= 1
                else:
                    accuracy_row[i] = 0
    

        if self.check_for_win(accuracy_row):
            self.isWinner = True

        if self.check_for_loss():
            self.isWinner = False 


    def check_for_loss(self):
        if None not in self.accuracy_board[5] and self.isWinner != True:
            return True  


    def check_for_win(self, row):
        for i in range(len(row)):
            if row[i] != 2:
                return False
            return True


    def create_wordle_square(self, char: str, x: int, y: int) -> Image:
        square_color = WORDLE_COLORS.get(self.accuracy_board[x][y])
        square = Image.new(mode='RGBA', size=(WORD_WIDTH, WORD_HEIGHT), color=(0, 0, 0, 0))

        draw = ImageDraw.Draw(square)
        font = ImageFont.truetype('fonts/helvetica_neue.ttf', FONT_SIZE)

        if char == None:
            draw.rectangle((0, 0, WORD_HEIGHT, WORD_WIDTH), fill=(255, 255, 255), outline=(211,215,219), width=3)
        else:
            draw.rectangle((0,0, WORD_HEIGHT, WORD_WIDTH), fill=square_color)
            draw.text(xy=(WORD_HEIGHT / 2, WORD_WIDTH / 2), anchor='mm', text=char, font=font)

        return square


    def create_wordle_board(self):
        board = Image.new(mode='RGB', size=(BOARD_WIDTH, BOARD_HEIGHT), color=(255, 255, 255))
        
        y_pos = BOARD_GAP
        for row in range(len(self.letter_board)):

            x_pos = BOARD_GAP
            for column in range(5):
                board.paste(self.create_wordle_square(self.letter_board[row][column], row, column), (x_pos, y_pos))
                x_pos += WORD_WIDTH + BOARD_GAP

            y_pos += WORD_WIDTH + BOARD_GAP

        blank_square = Image.new(mode='RGB', size=(WORD_WIDTH, WORD_HEIGHT), color=(255, 255, 255))
        draw = ImageDraw.Draw(blank_square)

        draw.rectangle((0, 0, WORD_HEIGHT, WORD_WIDTH), fill=(255, 255, 255), outline=(211,215,219), width=3)

        return board
