from globals import *

from dotenv import load_dotenv
from discord import app_commands

import discord, os, logging, io

import wordleboard, wordledb

load_dotenv()
GUILD_ID = discord.Object(id=os.getenv('GUILD_ID'))



class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)


    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=GUILD_ID)
        await self.tree.sync(guild=GUILD_ID)


wordle_db = wordledb.WordleDB()

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)


@client.event
async def on_ready():
    wordle_db.init_db()
    print(f'App running. Logged on as {client.user.id}!')


@client.event
async def on_guild_join(guild: discord.guild.Guild):
    print(guild)
    client.tree.copy_global_to(guild=guild)
    await client.tree.sync(guild=guild)


@client.tree.command()
async def wordle(interaction: discord.Interaction, word: str):
    guild_id = interaction.guild_id

    if wordle_db.check_exists(guild_id):
        accuracy_board, letter_board = wordle_db.get_wordle_progress(guild_id)
        board = wordleboard.WordleBoard(accuracy_board=accuracy_board, letter_board=letter_board)
    else:
        board = wordleboard.WordleBoard()

    if wordle_db.check_complete(guild_id):
        await interaction.response.send_message(f'Sorry, {interaction.user.mention}. But the wordle of the day has already been completed.\nTo see the board, type /board.')
        return
    
    try:
        board.process_word(word)
    
        board_file = convert_to_image(board)
        embed = create_embed(interaction)

        if board.isWinner == True:
            wordle_db.update_wordle_progress(guild_id, accuracy_board=board.accuracy_board, letter_board=board.letter_board, completed=True, won=False)
            embed.description = 'You win!'
        elif board.isWinner == False:
            wordle_db.update_wordle_progress(guild_id, accuracy_board=board.accuracy_board, letter_board=board.letter_board, completed=True, won=False)
            embed.description = 'You lose!'
        else:
            wordle_db.update_wordle_progress(guild_id, accuracy_board=board.accuracy_board, letter_board=board.letter_board)
            embed.description = f'Correct Characters: {board.correct_chars}'

        
        await interaction.response.send_message(file=board_file, embed=embed)
    except AssertionError as e:
        await interaction.response.send_message(f'Sorry, {interaction.user.mention}. But the word {e}')


def create_embed(interaction: discord.Interaction):
    embed = discord.Embed(title='Wordle!', description='Testing lol', type='rich')
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
    embed.set_image(url='attachment://wordle.png')
    embed.set_thumbnail(url='https://static01.nyt.com/images/2022/03/02/crosswords/alpha-wordle-icon-new/alpha-wordle-icon-new-square320-v3.png?format=pjpg&quality=75&auto=webp&disable=upscale')
    
    return embed


def convert_to_image(board):
    with io.BytesIO() as image_binary:
        board.create_wordle_board().save(image_binary, 'PNG')
        image_binary.seek(0)
        return discord.File(image_binary, filename='wordle.png')


if __name__ == '__main__':
    handler = logging.FileHandler(filename='logs/debug.log', encoding='utf-8', mode='w')
    client.run(os.getenv('BOT_TOKEN'), log_handler=handler, log_level=logging.DEBUG)