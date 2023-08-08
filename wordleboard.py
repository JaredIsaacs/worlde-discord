from globals import *
from PIL import Image, ImageDraw, ImageFont
from enum import Enum
from wordlerequest import get_wordle_info


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


    def process_word(self, word: str):
        assert len(word) == 5, f'{word} is not 5 characters long!'
        self.correct_chars = 0
        word = word.upper()
        wordle_info = get_wordle_info(word)

        letter_row = next(row for row in self.letter_board if None in row)
        for i, char in enumerate(word): 
            letter_row[i] = char

        accuracy_row = next(row for row in self.accuracy_board if None in row)
        if wordle_info['was_correct']:
            for i, char in enumerate(word):
                accuracy_row[i] = 2
                self.isWinner = True
        else:
            i = 0
            accuracy = 0
 
            while len(wordle_info['character_info']) != 0:
                character_scoring = wordle_info['character_info'].pop(0)['scoring']

                if character_scoring['in_word'] and character_scoring['correct_idx']:
                    accuracy = 2
                    self.correct_chars += 1
                elif character_scoring['in_word'] and not character_scoring['correct_idx']:
                    accuracy = 1
                else:
                    accuracy = 0

                accuracy_row[i] = accuracy
                i += 1  
                
        if self.check_for_loss():
            self.isWinner = False 


    def check_for_loss(self):
         if None not in self.accuracy_board[5] and self.isWinner != True:
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
