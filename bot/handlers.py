# This file will handle Discord events and route them to the backend
# Handles both slash commands and direct messages

from discord import DMChannel, Thread, TextChannel
import discord
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
                    
                    # Get the response text
                    response_text = response.get("response", "No response from API.")
                    
                    # Split long messages to comply with Discord's 2000 character limit
                    if len(response_text) <= 2000:
                        # Send as a single message if it's within the limit
                        await message.channel.send(response_text)
                    else:
                        # Split into chunks of 2000 characters or less
                        chunks = [response_text[i:i+2000] for i in range(0, len(response_text), 2000)]
                        logger.info(f"Splitting response into {len(chunks)} chunks")
                        
                        # Send each chunk as a separate message
                        for i, chunk in enumerate(chunks):
                            await message.channel.send(chunk)
                            logger.info(f"Sent chunk {i+1}/{len(chunks)}")
                except Exception as e:
                    logger.error(f"Error processing DM: {str(e)}")
                    error_msg = "Sorry, I encountered an error while processing your message. Please try again later."
                    
                    # Add more specific error message for content length issues
                    if "Must be 2000 or fewer in length" in str(e):
                        error_msg = "The response was too long for Discord. This should not happen anymore as messages are now automatically split."
                        
                    await message.channel.send(error_msg)
        
        # Process messages in threads
        elif isinstance(message.channel, Thread):
            logger.info(f"Received message in thread {message.channel.name} from {message.author.name} (ID: {message.author.id}): {message.content}")
            
            # Show typing indicator to provide feedback to the user
            async with message.channel.typing():
                try:
                    # Create a thread-specific user ID to maintain separate memory context
                    thread_user_id = f"{message.author.id}:{message.channel.id}"
                    
                    if message.attachments:
                        # Process file uploads in thread
                        logger.info(f"Processing attachment in thread: {message.attachments[0].filename}")
                        attachment = message.attachments[0]
                        content = await attachment.read()
                        files = {"file": (attachment.filename, content)}
                        payload = {"user_id": thread_user_id}
                        if message.content:
                            payload["question"] = message.content
                        response = await call_api("/upload", payload, files)
                    else:
                        # Process text message in thread
                        payload = {"user_id": thread_user_id, "message": message.content}
                        response = await call_api("/chat", payload)
                    
                    # Get the response text
                    response_text = response.get("response", "No response from API.")
                    
                    # Split long messages to comply with Discord's 2000 character limit
                    if len(response_text) <= 2000:
                        # Send as a single message if it's within the limit
                        await message.channel.send(response_text)
                    else:
                        # Split into chunks of 2000 characters or less
                        chunks = [response_text[i:i+2000] for i in range(0, len(response_text), 2000)]
                        logger.info(f"Splitting response into {len(chunks)} chunks")
                        
                        # Send each chunk as a separate message
                        for i, chunk in enumerate(chunks):
                            await message.channel.send(chunk)
                            logger.info(f"Sent chunk {i+1}/{len(chunks)}")
                except Exception as e:
                    logger.error(f"Error processing thread message: {str(e)}")
                    error_msg = "Sorry, I encountered an error while processing your message. Please try again later."
                    
                    # Add more specific error message for content length issues
                    if "Must be 2000 or fewer in length" in str(e):
                        error_msg = "The response was too long for Discord. This should not happen anymore as messages are now automatically split."
                        
                    await message.channel.send(error_msg)
        