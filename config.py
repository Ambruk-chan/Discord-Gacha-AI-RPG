import discord
from dotenv import load_dotenv
import asyncio


load_dotenv()
global text_api
global image_api
global character_card
global tts_config, tts_model, gpt_cond_latent, speaker_embedding

character_creation_queue = asyncio.Queue()
dungeon_creation_queue = asyncio.Queue()
dungeon_action_queue = asyncio.Queue()
dungeon_enter_queue = asyncio.Queue()

bot_display_name = "Aktiva-AI"
bot_default_avatar = "https://i.imgur.com/mxlcovm.png"

# Dictionary to keep track of the bot's last message time and last mentioned channel by guild
bot_last_message_time = {}
bot_last_mentioned_channel = {}
intents: discord.Intents = discord.Intents.all()
client: discord.Client = discord.Client(command_prefix='/', intents=intents)

