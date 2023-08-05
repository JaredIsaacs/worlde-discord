from dotenv import load_dotenv
from discord import app_commands

import discord, os, logging

load_dotenv()
GUILD_ID = discord.Object(id=os.getenv('GUILD_ID'))


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)


    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=GUILD_ID)
        await self.tree.sync(guild=GUILD_ID)


class Worlde(discord.Embed):
    def __init__(self):
        super().__init__(title='Worlde!', description='Testing lol', type='rich')


handler = logging.FileHandler(filename='logs/debug.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'App running. Logged on as {client.user.id}!')


@client.tree.command()
async def wordle(interaction: discord.Interaction):
    embed = Worlde()
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)

    await interaction.response.send_message(embed=embed)

    print(f'Message from {message.author}: {message.content}')


if __name__ == '__main__':
    client.run(os.getenv('BOT_TOKEN'), log_handler=handler, log_level=logging.DEBUG)