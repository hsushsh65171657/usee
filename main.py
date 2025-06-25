import os
import lyricsgenius
import yt_dlp
import asyncio
import re
import random
import time
import datetime
import subprocess
import psutil
import pytz
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon import events
from telethon.extensions import markdown
from telethon import types
from telethon.tl.types import MessageEntityCustomEmoji

#  كلاس خاص للماركداون
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
        if not entities: 
            return text, []
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
@client.on(events.NewMessage(outgoing=True, pattern=".cheek"))
async def nr(event):
    start_time = time.time()
    await asyncio.sleep(1)
    end_time = time.time()
    ping = round((end_time - start_time) * 50, 2)

    # ضبط التوقيت على العراق
    iraq_timezone = pytz.timezone("Asia/Baghdad")
    current_time = datetime.datetime.now(iraq_timezone).strftime("%Y-%m-%d %H:%M:%S")

    await event.edit(
        f"- Source Work Successfully [🇮🇶](emoji/5228888890630224685)\n"
        f"- Ping: {ping} ms [😌](emoji/5769239009607815382)\n"
        f"- Time: {current_time} [📆](emoji/5431897022456145283)"
    )

# ✅ أمر /info معلومات النظام
@client.on(events.NewMessage(pattern='/info'))
async def info(event):
    ram_usage = psutil.virtual_memory().percent
    cpu_usage = psutil.cpu_percent()
    response = f"info server : [🌟](emoji/5787418193127542105)\nRam : {ram_usage}% [🔥](emoji/5354863081740580440)\nCPU {cpu_usage}%[🔥](emoji/5345941618623005800)"
    await event.edit(response)


@client.on(events.NewMessage(pattern=r"\.delall"))
async def delete_my_messages(event):
    count = 0
    me = await client.get_me()

    async for message in client.iter_messages(event.chat_id):
        if message.sender_id == me.id:  # تأكد إن الرسالة من حسابك
            try:
                await message.delete()
                count += 1
                await asyncio.sleep(0.3)  # تأخير بسيط للحماية
            except:
                continue

    await client.send_message(event.chat_id, f"- تم حذف ( {count} ) من رسائلك [✅](emoji/5805174945138872447)")
#فلاتر الكلمات
# قائمة الفلاتر: نستخدم dict لتخزينها حسب معرف الكروب
filters_by_chat = {}

# ✅ أمر .filter لإضافة كلمة
@client.on(events.NewMessage(pattern=r"\.filter(?:\s+(.+))?"))
async def add_filter(event):
    word = event.pattern_match.group(1)
    chat_id = event.chat_id

    if chat_id not in filters_by_chat:
        filters_by_chat[chat_id] = set()

    if word:
        filters_by_chat[chat_id].add(word.lower())
        await event.reply(f"✅ تم `{word}` to filter list for this chat.")
    else:
        words = filters_by_chat.get(chat_id, set())
        if not words:
            await event.reply("📭 No filtered words in this chat.")
        else:
            listed = "\n".join(f"- {w}" for w in words)
            await event.reply(f"🧾 Filtered الكلملا in this chat:\n{listed}")

# ✅ أمر .unfilter لحذف كلمة من الفلاتر
@client.on(events.NewMessage(pattern=r"\.unfilter\s+(.+)"))
async def remove_filter(event):
    word = event.pattern_match.group(1).lower()
    chat_id = event.chat_id

    if chat_id in filters_by_chat and word in filters_by_chat[chat_id]:
        filters_by_chat[chat_id].remove(word)
        await event.reply(f"🗑️ Removed `{word}` from filter list.")
    else:
        await event.reply("⚠️ This word is not in the filter list.")

# ✅ هذا الحدث يمسح الرسائل تلقائيًا إن كانت مفلترة (حسب الكروب)

@client.on(events.NewMessage())
async def auto_delete(event):
    chat_id = event.chat_id
    if event.text and chat_id in filters_by_chat:
        for word in filters_by_chat[chat_id]:
            if word in event.text.lower():
                try:
                    await event.delete()
                    await event.reply(f"Deleted message containing '{word}'")  # للتأكد
                    break
                except Exception as e:
                    await event.reply(f"Failed to delete message: {e}")
#جلب كلمات الاغاني

GENIUS_ACCESS_TOKEN = "TK4d53dccU7WH1GDO2GdU9EI39laxrzv340vMrqbq1gxCJvcdUIIabKhlEDhhWY-"
genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"])

@client.on(events.NewMessage(pattern=r"\.lyrics (.+)"))
async def lyrics_handler(event):
    song_name = event.pattern_match.group(1)
    await event.edit("- Loading, searching for the lyrics...")

    try:
        song = genius.search_song(song_name)
        if song and song.lyrics:
            lyrics = song.lyrics
            if len(lyrics) > 4096:
                lyrics = lyrics[:4090] + "\n...\n(lyrics too long, truncated)"
            await event.edit(f"- Lyrics for: {song.title}\n\n{lyrics}")
        else:
            await event.edit("- Could not find the lyrics for this song.")
    except Exception as e:
        await event.edit(f"- Erorr:\n{str(e)}")
#تحميل يوتيوب
@client.on(events.NewMessage(pattern=r"\.youtube (.+)"))
async def youtube_audio(event):
    query = event.pattern_match.group(1)
    msg = await event.edit("- Loading …")

    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': 'HRBY(@s5llll).%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch1',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            if 'entries' in info:
                info = info['entries'][0]
            filename = ydl.prepare_filename(info)

        # معرفة منو طلب التحميل
        sender = await event.get_sender()
        username = f"@{sender.username}" if sender.username else sender.first_name

        # نص الكابشن
        caption = f"Downloaded successfully ✅\n🔴 Song name: {info['title']}\n🎖️By: {username}"

        # إرسال الملف
        await client.send_file(
            event.chat_id,
            filename,
            caption=caption,
            voice_note=False
        )

        await msg.delete()

        # حذف الملف من السيرفر
        if os.path.exists(filename):
            os.remove(filename)

    except Exception as e:
        await msg.edit(
            f"🧩 Erorr:\n`{str(e)}`"
        )
    
client.start()
print("⚡ Bot is running...")
client.run_until_disconnected()
