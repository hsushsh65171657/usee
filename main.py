
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

@client.on(events.NewMessage(outgoing=True, pattern=".فحص"))
async def nr(event):
    start_time = time.time()
    await asyncio.sleep(1)
    end_time = time.time()
    ping = round((end_time - start_time) * 50, 2)
    r1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await event.edit(f"sourse work Successfully [👁](emoji/5263006706375342926)\nPinG : {ping} ms [👁️](emoji/5474508767389303120)\nTiMe : {r1} [😈](emoji/5474475837875044294)\n  — — — — — — \n DeV : @dohavoice [🦇](emoji/5443009168002788185)")

@client.on(events.NewMessage(pattern=r"\.ping"))
async def ping_handler(event):
    start = time.time()
    await event.edit("🏓 Pinging...")
    end = time.time()
    ping_time = int((end - start) * 1000)
    await event.edit(f"🏓 Ping: {ping_time} ms")
# ✅ .امسحلي يحذف رسائل المستخدم نفسه
@client.on(events.NewMessage(pattern=r"\.امسحلي"))
async def delete_my_messages(event):
    count = 0
    async for message in client.iter_messages(event.chat_id):
        if message.sender_id == event.sender_id:
            try:
                await message.delete()
                count += 1
            except:
                continue
    await client.send_message(event.chat_id, f"✅ تم حذف {count} رسالة\nBy: @S5llll")

# ✅ تشغيل البوت
client.start()
print("⚡ Bot is running...")
client.run_until_disconnected()
