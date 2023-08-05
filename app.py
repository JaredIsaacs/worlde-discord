from dotenv import load_dotenv
import discord, os, logging

load_dotenv()

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'App running.Logged on as {self.user}!')

    
    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')


if __name__ == '__main__':
    handler = logging.FileHandler(filename='logs/debug.log', encoding='utf-8', mode='w')

    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents)
    client.run(os.getenv('BOT_TOKEN'), log_handler=handler, log_level=logging.DEBUG)