import os
import asyncio
import re
import random
import time
import datetime
import subprocess
import psutil

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon import events
from telethon.extensions import markdown
from telethon import types
from telethon.tl.types import MessageEntityCustomEmoji

# ✅ كلاس خاص للماركداون
class CustomMarkdown:
    @staticmethod
    def parse(text):
        text, entities = markdown.parse(text)
        for i, e in enumerate(entities):
            if isinstance(e, types.MessageEntityTextUrl):
                if e.url == 'spoiler':
                    entities[i] = types.MessageEntitySpoiler(e.offset, e.length)
                elif e.url.startswith('emoji/'):
                    entities[i] = types.MessageEntityCustomEmoji(e.offset, e.length, int(e.url.split('/')[1]))
        return text, entities

    @staticmethod
    def unparse(text, entities):
        for i, e in enumerate(entities):
            if isinstance(e, types.MessageEntityCustomEmoji):
                entities[i] = types.MessageEntityTextUrl(e.offset, e.length, f'emoji/{e.document_id}')
            if isinstance(e, types.MessageEntitySpoiler):
                entities[i] = types.MessageEntityTextUrl(e.offset, e.length, 'spoiler')
        return markdown.unparse(text, entities)


# ✅ بياناتك
api_id = 15284003
api_hash = "6a9c0e4c844161f44e7f31473ea4931b"
string = "1BJWap1sAUHH9FdkXX5lUPPP5t8b7lIzFBzyqM2tKYTCDime77Z9VM6okPiIwii6e1IQ7SaUYSmsNEXac6l90jJXvPTbeQ0QCXqt3nUvlDQct6Mho5R78b9nw5jwZAxomVP_zvu3rOg5NUr4KRnzNNsE6OqHAjFkdKzjWxYck_q4moFtwQZ-rjmrcY-tNHw-YZHOVEWPgNuDTbsdYX_RqikFvpN7KJdCMw3qV1xGMr1LsKa7QOCbuJs3sktUge0f3cLgvmR7eHRAcc20k5sVjUGfpLEMWFrQjPaYQuZo4kZyIGrxD7SliDa97HlNo7T9kFUqhbdSLm-u-cmaNs8eeOLbMZi1M9eQ="

# ✅ إنشاء العميل
client = TelegramClient(StringSession(string), api_id, api_hash)
client.parse_mode = CustomMarkdown()

# ✅ أمر .فحص لقياس البنك
@client.on(events.NewMessage(outgoing=True, pattern=".فحص"))
async def nr(event):
    start_time = time.time()
    await asyncio.sleep(1)
    end_time = time.time()
    ping = round((end_time - start_time) * 50, 2)
    r1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await event.edit(f"- Source Work Successfully [🇮🇶](emoji/5228888890630224685)\n- Ping: {ping} ms [😌](emoji/5769239009607815382)\n- Time: {r1} [📆](emoji/5431897022456145283)")

# ✅ أمر /info معلومات النظام
@client.on(events.NewMessage(pattern='/info'))
async def info(event):
    ram_usage = psutil.virtual_memory().percent
    cpu_usage = psutil.cpu_percent()
    response = f"info server : [🌟](emoji/5787418193127542105)\nRam : {ram_usage}% [🔥](emoji/5354863081740580440)\nCPU {cpu_usage}%[🔥](emoji/5345941618623005800)"
    await event.edit(response)

# ✅ أمر .idd للحصول على ID الملصق المميز
@client.on(events.NewMessage(pattern=r"\.idd"))
async def handler(event):
    me = await client.get_me()
    if event.sender_id != me.id:
        return

    message = event.message
    if event.message.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        if reply_message:
            message = reply_message

    if message.entities:
        for entity in message.entities:
            if isinstance(entity, MessageEntityCustomEmoji):
                emoji_id = int(entity.document_id)
                emoji_text = message.text[entity.offset:entity.offset + entity.length].replace('[', '')
                response = f"Your Emoji [{emoji_text}](tg://emoji?id={emoji_id}) Document Id Is `{emoji_id}`"
                await event.reply(response)
                return

    await event.reply("This Emoji Is Not Premium")

# ✅ أمر .ping يظهر البنك بدون رد
@client.on(events.NewMessage(pattern=r"\.ping"))
async def ping_handler(event):
    start = time.time()
    await event.edit("🏓 Pinging...")
    end = time.time()
    ping_time = int((end - start) * 1000)
    await event.edit(f"🏓 Ping: {ping_time} ms")

# ✅ أمر .امسحلي لحذف رسائل المستخدم
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
