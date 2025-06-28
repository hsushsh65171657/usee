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
from telethon.tl.functions.users import GetFullUserRequest
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon import events
import requests
import io
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

# ✅ إنشاء الجلسه
client = TelegramClient(StringSession(string), api_id, api_hash)
client.parse_mode = CustomMarkdown()

#تحديث 

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.is_private and event.photo and event.message.ttl_seconds:
        sender = await event.get_sender()
        sender_name = f"{sender.first_name or ''} {sender.last_name or ''}".strip()
        sender_username = f"@{sender.username}" if sender.username else f"`{sender.id}`"
        time_sent = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # حفظ الصورة
        file_path = await event.download_media()
        
        # إرسال الصورة لرسائل المحفوظة
        caption = (
            f"📸 تم التقاط صورة مؤقتة!\n"
            f"- 👤 من: {sender_name} ({sender_username})\n"
            f"- 🕒 الوقت: {time_sent}"
        )
        await client.send_file("me", file_path, caption=caption)

        # حذف الصورة من الملف المؤقت
        os.remove(file_path)
# ✅ أمر cheek لفحص الصور شغال
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

#سحب النص من الصورهA
API_KEY = "K83161105588957"
@client.on(events.NewMessage(pattern=r"\.ocr"))
async def ocr_handler(event):
    if not event.is_reply:
        await event.edit("- Please reply to an image to extract text.")
        return

    reply = await event.get_reply_message()
    if not reply.photo:
        await event.edit("- The replied message is not an image.")
        return

    photo = await client.download_media(reply.photo, bytes)
    url = "https://api.ocr.space/parse/image"
    headers = {
        "apikey": API_KEY,
    }
    payload_ara = {
        "language": "ara",
        "isOverlayRequired": False,
    }
    payload_eng = {
        "language": "eng",
        "isOverlayRequired": False,
    }
    files = {
        "file": ("image.jpg", photo)
    }

    # طلب اللغة العربية
    response_ara = requests.post(url, headers=headers, data=payload_ara, files=files)
    result_ara = response_ara.json()

    # طلب اللغة الانجليزية
    response_eng = requests.post(url, headers=headers, data=payload_eng, files=files)
    result_eng = response_eng.json()

    # تحقق من الأخطاء
    if result_ara.get("IsErroredOnProcessing"):
        await event.edit("- OCR Arabic failed: " + result_ara.get("ErrorMessage", ["Unknown error"])[0])
        return
    if result_eng.get("IsErroredOnProcessing"):
        await event.edit("- OCR English failed: " + result_eng.get("ErrorMessage", ["Unknown error"])[0])
        return

    text_ara = result_ara["ParsedResults"][0]["ParsedText"].strip()
    text_eng = result_eng["ParsedResults"][0]["ParsedText"].strip()

    combined_text = text_ara + ("\n\n" if text_ara and text_eng else "") + text_eng

    if not combined_text:
        await event.edit("- No text found in the image.")
        return

    await event.edit(f"📝 Extracted Text:\n\n{combined_text}")
#كود الاوامر
@client.on(events.NewMessage(pattern=r"\.comands"))
async def show_commands(event):
    commands_text = """
📋 **Available Commands in Your Userbot:**

1. `.cheek` - Checks if the bot is running properly.
2. `.delall` - Deletes all the messages you have sent.
3. `.userinfo [username or reply]` - Shows information about a user.
4. `.lyrics` - Displays song lyrics.
5. `.youtube <keyword or link>` - Downloads audio from YouTube or searches for videos.
6. `.ocr` - Extracts text from images (reply to a photo).
7. `.comands` - Shows this list of
——————————————————————————————
- Dev Source: @S5llll
"""
    await event.edit(commands_text)


#حذف الرسائل
@client.on(events.NewMessage(pattern=r"\.delall"))
async def delete_my_messages(event):
    msg = await event.respond("🔄 جاري حذف رسائلك...")
    me = await client.get_me()
    chat_id = event.chat_id
    count = 0
    batch = []

    async for message in client.iter_messages(chat_id, from_user=me.id):
        batch.append(message.id)

        if len(batch) >= 100:
            try:
                await client.delete_messages(chat_id, batch)
                count += len(batch)
                batch = []
                await asyncio.sleep(1)  # تأخير خفيف كل 100 رسالة
            except:
                continue

    # حذف الباقي إن وُجد
    if batch:
        try:
            await client.delete_messages(chat_id, batch)
            count += len(batch)
        except:
            pass

    await msg.edit(f"- تم حذف ( {count} ) من رسائلك [✅](emoji/5805174945138872447)")

# جلب معلومات الشخص

@client.on(events.NewMessage(pattern=r"\.userinfo(?:\s+(\S+))?"))
async def userinfo(event):
    input_arg = event.pattern_match.group(1)
    user = None

    try:
        # ✅ إذا أكو رد
        if event.is_reply:
            reply_msg = await event.get_reply_message()
            user = await event.client.get_entity(reply_msg.sender_id)
            full = await event.client(GetFullUserRequest(reply_msg.sender_id))

        # ✅ إذا أكو يوزر أو ID مكتوب
        elif input_arg:
            user = await event.client.get_entity(input_arg)
            full = await event.client(GetFullUserRequest(user.id))

        # ✅ إذا ماكو رد ولا إدخال، رجّع معلوماتك
        else:
            user = await event.get_sender()
            full = await event.client(GetFullUserRequest(user.id))

        # ✅ بيانات احتياطية
        first = user.first_name or ""
        last = user.last_name or ""
        username = f"@{user.username}" if user.username else "None"
        user_id = user.id
        bio = getattr(full.full_user, 'about', 'No bio')
        common_chats = getattr(full.full_user, 'common_chats_count', 'N/A')

        info = (
            f"👤 **User Info:**\n"
            f"- Name: {first} {last}\n"
            f"- Username: {username}\n"
            f"- ID: `{user_id}`\n"
            f"- Profile Link: [Click Here](tg://user?id={user_id})\n"
            f"- Bio: {bio}\n"
            f"- Common Chats: {common_chats}"
        )

        await event.edit(info, link_preview=False)

    except Exception as e:
        await event.reply(f"❌ Error:\n`{str(e)}`")

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
    msg = await event.edit("- Loading...")

    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': 'HRBY (@s5llll).%(ext)s',
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

        # تحميل صورة المصغرة
        thumb_url = info.get('thumbnail')
        thumb_path = "thumb.jpg"
        if thumb_url:
            r = requests.get(thumb_url)
            with open(thumb_path, "wb") as f:
                f.write(r.content)
        else:
            thumb_path = None

        # معرفة منو طلب التحميل
        sender = await event.get_sender()
        username = f"@{sender.username}" if sender.username else sender.first_name

        # نص الكابشن
        caption = f"Downloaded successfully ✅\n🔴 Song name: {info['title']}\n🎖️By: {username}"

        # إرسال الملف مع الصورة المصغرة
        await client.send_file(
            event.chat_id,
            filename,
            caption=caption,
            thumb=thumb_path if os.path.exists(thumb_path) else None,
            voice_note=False
        )

        await msg.delete()

        # حذف الملفات المؤقتة
        if os.path.exists(filename):
            os.remove(filename)
        if os.path.exists(thumb_path):
            os.remove(thumb_path)

    except Exception as e:
        await msg.edit(f"- Error:\n`{str(e)}`")
    
client.start()
print("⚡ Bot is running...")
client.run_until_disconnected()
