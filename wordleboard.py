from globals import *
from PIL import Image, ImageDraw, ImageFont
from enum import Enum


class WordleBoard():
    def __init__(self):
        self.accuracy_board = [
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None]
        ]

        self.letter_board = [
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None]
    ]


    def process_word(self, word: str):
        assert len(word) == 5, 'Invalid Word Length'
        word = word.upper()

        letter_row = next(row for row in self.letter_board if None in row)
        for i, char in enumerate(word): 
            letter_row[i] = char

        print(self.letter_board)

        #accuracy_row = next(row for row in self.accuracy_board if None in row)
        #for i, char in enumerate(word): 
            #logic here.


    def create_wordle_square(self, char: str, status: tuple) -> Image:
        square = Image.new(mode='RGBA', size=(WORD_WIDTH, WORD_HEIGHT), color=(0, 0, 0, 0))

        draw = ImageDraw.Draw(square)
        font = ImageFont.truetype('fonts/helvetica_neue.ttf', FONT_SIZE)

        if char == None:
            draw.rectangle((0, 0, WORD_HEIGHT, WORD_WIDTH), fill=(255, 255, 255), outline=(211,215,219), width=3)
        else:
            draw.rectangle((0,0, WORD_HEIGHT, WORD_WIDTH), fill=status)
            draw.text(xy=(WORD_HEIGHT / 2, WORD_WIDTH / 2), anchor='mm', text=char, font=font)

        return square


    def create_wordle_board(self):
        board = Image.new(mode='RGB', size=(BOARD_WIDTH, BOARD_HEIGHT), color=(255, 255, 255))
        
        y_pos = BOARD_GAP
        for row in range(len(self.letter_board)):

            x_pos = BOARD_GAP
            for column in range(5):
                board.paste(self.create_wordle_square(self.letter_board[row][column], INCORRECT_CHAR), (x_pos, y_pos))
                x_pos += WORD_WIDTH + BOARD_GAP

            y_pos += WORD_WIDTH + BOARD_GAP

        blank_square = Image.new(mode='RGB', size=(WORD_WIDTH, WORD_HEIGHT), color=(255, 255, 255))
        draw = ImageDraw.Draw(blank_square)

        draw.rectangle((0, 0, WORD_HEIGHT, WORD_WIDTH), fill=(255, 255, 255), outline=(211,215,219), width=3)

        return board

