import discord
import random
from src.conversation_manager import ConversationManager
from src.settings import CONVERSATION_CHANCE, LAUGH_REACT_CHANCE, DISCORD_TOKEN
from src.utils import ready_table

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

conversation_manager = ConversationManager()

@bot.event
async def on_ready():
    """Called when the bot is ready to start receiving events."""
    print(f"Logged in as {bot.user}")
    ready_table()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if random.random() < LAUGH_REACT_CHANCE:
        try:
            await message.add_reaction("😂")
        except Exception as e:
            print(f"Error adding reaction: {e}")

    if random.random() < CONVERSATION_CHANCE and conversation_manager.can_trigger_conversation(message.channel.id):
        print(f"Randomly triggering new conversation in channel {message.channel.id}.")
        await conversation_manager.handle_conversation(message.channel, message.content)
        conversation_manager.triggered_recently[message.channel.id] = True
        return 

    if bot.user.mentioned_in(message):
        await conversation_manager.handle_conversation(message.channel, message.content)
        conversation_manager.triggered_recently[message.channel.id] = False
        return 

    if message.channel.id in conversation_manager.active_conversations:
        conversation = conversation_manager.get_conversation(message.channel.id)
        if conversation_manager.is_conversation_active(message.channel.id):
            conversation_manager.append_message(message.channel.id, "user", message.content)
            response = await conversation_manager.generate_ai_response(conversation["messages"])
            if response:
                await message.channel.send(response)
                conversation_manager.append_message(message.channel.id, "assistant", response)
            return
        conversation_manager.end_conversation(message.channel.id)

@bot.event
async def on_message_edit(before, after):
    """Handle edited messages."""
    if after.author == bot.user:
        return

    if after.channel.id in conversation_manager.active_conversations:
        await conversation_manager.handle_message_edit(after.channel, after.content)


bot.run(DISCORD_TOKEN)
