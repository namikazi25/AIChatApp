import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from bot.commands import setup_commands
from bot.handlers import EventHandler

# Load environment variables
load_dotenv()

# Set up Discord bot with required intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Initialize the bot with a command prefix and description
bot = commands.Bot(command_prefix='!', description="Multimodal LLM Discord Bot", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    await setup_commands(bot)
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game("Chatting")
    )

@bot.event
async def on_message(message):
    await EventHandler.on_message(message, bot)
    # Process commands after handling the message
    await bot.process_commands(message)

async def main():
    async with bot:
        await bot.start(os.getenv("DISCORD_BOT_TOKEN"))

def run_bot():
    import asyncio
    asyncio.run(main())

if __name__ == "__main__":
    run_bot()