from globals import *

from dotenv import load_dotenv
from discord import app_commands

import discord, os, logging, io

import wordleboard

load_dotenv()
GUILD_ID = discord.Object(id=os.getenv('GUILD_ID'))

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)


    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=GUILD_ID)
        await self.tree.sync(guild=GUILD_ID)


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'App running. Logged on as {client.user.id}!')


@client.tree.command()
async def wordle(interaction: discord.Interaction, word: str):
    global BOARD

    if BOARD == None:
        BOARD = wordleboard.WordleBoard()

    try:
        BOARD.process_word(word)
    
        board_file = convert_to_image()
        embed = create_embed(interaction)

        if BOARD.isWinner == True:
            embed.description = 'You win!'
            BOARD = None
        elif BOARD.isWinner == False:
            embed.description = 'You lose!'
            BOARD = None
        else:
            embed.description = f'Correct Characters: {BOARD.correct_chars}'

        await interaction.response.send_message(file=board_file, embed=embed)
    except AssertionError:
        await interaction.response.send_message(f'Sorry, {interaction.user.mention}. But the word {word} is not 5 characters long!')


def create_embed(interaction: discord.Interaction):
    embed = discord.Embed(title='Wordle!', description='Testing lol', type='rich')
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
    embed.set_image(url='attachment://wordle.png')
    embed.set_thumbnail(url='https://static01.nyt.com/images/2022/03/02/crosswords/alpha-wordle-icon-new/alpha-wordle-icon-new-square320-v3.png?format=pjpg&quality=75&auto=webp&disable=upscale')
    
    return embed


def convert_to_image():
    with io.BytesIO() as image_binary:
        BOARD.create_wordle_board().save(image_binary, 'PNG')
        image_binary.seek(0)
        return discord.File(image_binary, filename='wordle.png')


if __name__ == '__main__':
    handler = logging.FileHandler(filename='logs/debug.log', encoding='utf-8', mode='w')
    client.run(os.getenv('BOT_TOKEN'), log_handler=handler, log_level=logging.DEBUG)