# This file will handle Discord events and route them to the backend
# For now, we're using slash commands in commands.py, but this file can be expanded
# to handle regular messages, reactions, and other Discord events

class EventHandler:
    """Handles Discord events and routes them to the backend"""
    
    @staticmethod
    async def on_message(message, bot):
        """Handle incoming messages"""
        # Ignore messages from the bot itself
        if message.author == bot.user:
            return
        
        # Add additional message handling logic here
        # For example, you could implement a prefix-based command system
        # or handle direct messages differently
        if isinstance(message.channel, DMChannel):
            payload = {
                "user_id": str(message.author.id),
                "message": message.content
            }
            response = await call_api("/chat", payload)
            reply = response.get("response", "No response from API.")
            await message.channel.send(reply)
        