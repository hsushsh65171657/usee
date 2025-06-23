
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

# 🔒 بياناتك هنا مباشرة
api_id = 15284003  # ← استبدل هذا بالـ API_ID الحقيقي
api_hash = "6a9c0e4c844161f44e7f31473ea4931b"  # ← استبدل بالـ API_HASH الحقيقي
string = "1BJWap1sAUHH9FdkXX5lUPPP5t8b7lIzFBzyqM2tKYTCDime77Z9VM6okPiIwii6e1IQ7SaUYSmsNEXac6l90jJXvPTbeQ0QCXqt3nUvlDQct6Mho5R78b9nw5jwZAxomVP_zvu3rOg5NUr4KRnzNNsE6OqHAjFkdKzjWxYck_q4moFtwQZ-rjmrcY-tNHw-YZHOVEWPgNuDTbsdYX_RqikFvpN7KJdCMw3qV1xGMr1LsKa7QOCbuJs3sktUge0f3cLgvmR7eHRAcc20k5sVjUGfpLEMWFrQjPaYQuZo4kZyIGrxD7SliDa97HlNo7T9kFUqhbdSLm-u-cmaNs8eeOLbMZi1M9eQ="  # ← استبدل بالـ String Session الحقيقي

client = TelegramClient(StringSession(string), api_id, api_hash)

@client.on(events.NewMessage(pattern="/ping"))
async def handler(event):
    await event.reply("🏓 Bot is alive!")

client.start()
print("⚡ Bot is running...")
client.run_until_disconnected()
