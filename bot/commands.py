import discord
import aiohttp
import os
from discord import app_commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Backend API URL
API_URL = "http://localhost:8000"

async def call_api(endpoint, json_data, files=None):
    """Helper function to call the backend API"""
    async with aiohttp.ClientSession() as session:
        if files:
            # Handle file uploads
            form_data = aiohttp.FormData()
            for key, value in json_data.items():
                form_data.add_field(key, str(value))
            
            for file_key, file_tuple in files.items():
                filename, content = file_tuple
                form_data.add_field(file_key, content, filename=filename)
            
            async with session.post(f"{API_URL}{endpoint}", data=form_data) as response:
                return await response.json()
        else:
            # Regular JSON request
            async with session.post(f"{API_URL}{endpoint}", json=json_data) as response:
                return await response.json()

async def setup_commands(bot):
    """Set up slash commands for the Discord bot"""
    
    # Create a command tree for slash commands
    @bot.tree.command(name="chat", description="Chat with the AI assistant")
    async def chat(interaction: discord.Interaction, message: str):
        await interaction.response.defer()
        response = await call_api("/chat", {"user_id": str(interaction.user.id), "message": message})
        await interaction.followup.send(response["response"])

    @bot.tree.command(name="upload", description="Upload an image or document and optionally ask a question about it")
    async def upload(interaction: discord.Interaction, file: discord.Attachment, question: str = None):
        await interaction.response.defer()
        content = await file.read()
        files = {"file": (file.filename, content)}
        
        # Include the question in the API call if provided
        json_data = {"user_id": str(interaction.user.id)}
        if question:
            json_data["question"] = question
            
        res = await call_api("/upload", json_data, files)
        await interaction.followup.send(res["response"])

    @bot.tree.command(name="set_model", description="Change the AI model")
    @app_commands.choices(model=[
        app_commands.Choice(name="GPT-4o", value="gpt-4o"),
        app_commands.Choice(name="Gemini 2.0 Flash", value="gemini-2.0-flash"),
        app_commands.Choice(name="Gemini 2.5 Pro Experimental", value="gemini-2.5-pro-experimental"),
        app_commands.Choice(name="DeepSeek V3", value="deepseek-v3")
    ])
    async def set_model(interaction: discord.Interaction, model: str):
        await interaction.response.defer()
        res = await call_api("/set_model", {"user_id": str(interaction.user.id), "model": model})
        await interaction.followup.send(res["response"])
    
    # Sync the command tree with Discord
    await bot.tree.sync()