import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon import events
import asyncio
import re
import random
from telethon.extensions import markdown
from telethon import types
import time
import datetime
import subprocess
import psutil

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
string = os.environ.get("STRING_SESSION")

client = TelegramClient(StringSession(string), api_id, api_hash)

@client.on(events.NewMessage(pattern="/ping"))
async def handler(event):
    await event.reply("🏓 Bot is alive!")

client.start()
print("⚡ Bot is running...")
client.run_until_disconnected()
