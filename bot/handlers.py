# This file will handle Discord events and route them to the backend
# Handles both slash commands and direct messages

from discord import DMChannel
from bot.commands import call_api
from utils.logger import get_logger

# Set up logger
logger = get_logger("event_handler")

class EventHandler:
    """Handles Discord events and routes them to the backend"""
    
    @staticmethod
    async def on_message(message, bot):
        """Handle incoming messages"""
        # Ignore messages from the bot itself
        if message.author == bot.user:
            return
        
        # Process direct messages
        if isinstance(message.channel, DMChannel):
            logger.info(f"Received DM from {message.author.name} (ID: {message.author.id}): {message.content}")
            
            # Show typing indicator to provide feedback to the user
            async with message.channel.typing():
                try:
                    if message.attachments:
                        # Process file uploads
                        logger.info(f"Processing attachment: {message.attachments[0].filename}")
                        attachment = message.attachments[0]
                        content = await attachment.read()
                        files = {"file": (attachment.filename, content)}
                        payload = {"user_id": str(message.author.id)}
                        if message.content:
                            payload["question"] = message.content
                        response = await call_api("/upload", payload, files)
                    else:
                        # Process text message
                        payload = {"user_id": str(message.author.id), "message": message.content}
                        response = await call_api("/chat", payload)
                    
                    # Send the response back to the user
                    await message.channel.send(response.get("response", "No response from API."))
                except Exception as e:
                    logger.error(f"Error processing DM: {str(e)}")
                    await message.channel.send(f"Sorry, I encountered an error while processing your message. Please try again later.")
        