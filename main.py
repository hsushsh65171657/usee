import aiohttp
import os
import lyricsgenius
import yt_dlp
import asyncio
import re
import random
import time
import json
import datetime
import subprocess
import psutil
import pytz
from telethon.tl.functions.users import GetFullUserRequest
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon import events
import requests
from io import BytesIO
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
#تحميل تيك توك

@client.on(events.NewMessage(pattern=r"\.تيك (https?://[^\s]+)"))
async def tiktok_download(event):
    url = event.pattern_match.group(1)
    await event.reply("⏳ جاري التحميل من TikTok...")

    try:
        async with aiohttp.ClientSession() as session:
            api_url = f"https://api.tikwm.com/video/info?url={url}"
            async with session.get(api_url) as resp:
                data = await resp.json()

        if not data.get("data"):
            return await event.reply("❌ ما كدرت أجيب الفيديو، الرابط ممكن غلط أو الفيديو خاص.")

        result = data["data"]
        caption = result.get("title", "لا يوجد وصف")
        media_type = result.get("type")

        if media_type == "video":
            video_url = result["play"]
            await client.send_file(event.chat_id, video_url, caption=f"🎬 {caption}")

        elif media_type == "image":
            images = result.get("images")
            if images:
                media_group = [InputMediaPhotoExternal(url) for url in images]
                await client.send_file(event.chat_id, file=media_group, caption=f"🖼️ {caption}")
            else:
                await event.reply("❌ فشل في جلب الصور.")

        else:
            await event.reply("❌ نوع المحتوى غير مدعوم.")

    except Exception as e:
        await event.reply(f"❌ خطأ أثناء التحميل:\n`{str(e)}`")
#الابديت

# دالة مخصصة لتحويل أنواع غير قابلة للتسلسل (مثل datetime)
def custom_serializer(obj):
    import datetime

    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    if isinstance(obj, bytes):
        try:
            # نحاول نفكّه كنص UTF-8
            return obj.decode('utf-8')
        except:
            # إذا ما نكدر نفكّه، نرجعه كـ list أرقام
            return list(obj)
    return str(obj)

@client.on(events.NewMessage(pattern=r"\.json"))
async def show_json(event):
    reply = await event.get_reply_message()
    target_message = reply if reply else event.message

    if not target_message:
        await event.reply("❌ ماكو رسالة أرد عليها.")
        return

    try:
        # تحويل الرسالة إلى dict مع معالجة datetime وغيرها
        raw = target_message.to_dict()
        formatted = json.dumps(raw, indent=4, ensure_ascii=False, default=custom_serializer)

        if len(formatted) > 4096:
            with open("update.json", "w", encoding="utf-8") as f:
                f.write(formatted)
            await client.send_file(event.chat_id, "update.json", caption="📦 هذه بيانات الرسالة بصيغة JSON")
            os.remove("update.json")
        else:
            await event.reply(f"📦 هذه بيانات الرسالة:\n\n<code>{formatted}</code>", parse_mode="html")
    except Exception as e:
        await event.reply(f"❌ خطأ أثناء جلب الـ JSON:\n<code>{str(e)}</code>", parse_mode="html")
#تحويل
TARGET_GROUP = -1002833881470  # غروب التنبيهات
OWNER_ID = 6099048919  # معرفك الشخصي

@client.on(events.NewMessage(incoming=True))
async def notify_owner_mentions_and_replies(event):
    if not event.is_group:
        return

    try:
        sender = await event.get_sender()
        if not sender or sender.bot or sender.id == OWNER_ID:
            return  # تجاهل البوتات و الرسائل من نفسك

        chat = await event.get_chat()
        reason = []

        # تحقق من المنشن الموجه إليك
        if event.message.entities:
            for entity in event.message.entities:
                if hasattr(entity, 'user_id') and entity.user_id == OWNER_ID:
                    reason.append("🏷️ Mention")
                    break

        # تحقق من الرد على رسالتك
        if event.is_reply:
            replied_msg = await event.get_reply_message()
            if replied_msg and replied_msg.sender_id == OWNER_ID:
                reason.append("💬 Reply")

        # إذا في سبب، سوي الإشعار
        if reason:
            user_name = sender.first_name or "No Name"
            user_mention = f"[{user_name}](tg://user?id={sender.id})"
            group_link = f"https://t.me/{chat.username}" if chat.username else "Private Group"
            group_name = chat.title or "No Title"
            msg_link = f"https://t.me/{chat.username}/{event.id}" if chat.username else "No Message Link"
            time = event.message.date.strftime("%Y-%m-%d %H:%M:%S")
            reason_text = " + ".join(reason)

            msg = f"""
📥 **New Interaction Detected!**

📌 Type: {reason_text}

👤 From: {user_mention}  
🏷️ Group: [{group_name}]({group_link})  
🔗 Message: [Click to View]({msg_link})  
🕰️ Time: `{time}`
"""
            await client.send_message(TARGET_GROUP, msg.strip(), link_preview=False)

    except Exception as e:
        print(f"خطأ أثناء إشعار المنشن أو الرد: {e}")
#تيست

@client.on(events.NewMessage(pattern=r"\.mycount"))
async def count_my_messages(event):
    await event.edit("- جاري الحساب...")

    me = await client.get_me()
    count = 0

    async for msg in client.iter_messages(event.chat_id, from_user=me.id):
        count += 1

    await event.edit(f"- عدد رسائلك هنا: {count}")
#كود سحب نص من قنوات

@client.on(events.NewMessage(pattern=r'\.get (https:\/\/t\.me\/[^\s]+\/\d+)', outgoing=True))
async def _(event):
    match = re.match(r'https:\/\/t\.me\/([^\s\/]+)/(\d+)', event.pattern_match.group(1))
    if not match:
        return await event.edit("Invalid link format.")

    channel_username = match.group(1)
    msg_id = int(match.group(2))

    try:
        status_msg = await event.edit("Downloading media from protected channel...")
        msg = await client.get_messages(channel_username, ids=msg_id)
        if not msg:
            return await status_msg.edit("Message not found.")

        messages = []
        if msg.grouped_id:
            messages = await client.get_messages(
                channel_username,
                ids=None,
                min_id=msg_id - 20,
                max_id=msg_id + 20
            )
            messages = [m for m in messages if m.grouped_id == msg.grouped_id]
            messages = sorted(messages, key=lambda x: x.id)
        else:
            messages = [msg]

        # 🧠 دالة استخراج الكابشن الحقيقية
        def extract_caption(m):
            raw_text = m.text or m.message
            if isinstance(raw_text, str):
                return raw_text.strip() if raw_text.strip() else "No caption"
            elif isinstance(raw_text, tuple):
                return raw_text[0].strip() if raw_text and isinstance(raw_text[0], str) and raw_text[0].strip() else "No caption"
            return "No caption"

        # 📦 Media group
        if any(m.media for m in messages) and len(messages) > 1:
            files = []
            for m in messages:
                if not m.media:
                    continue

                file = BytesIO()
                file.name = "file"
                await client.download_media(m, file=file)
                file.seek(0)

                if m.photo:
                    file.name = "image.jpg"
                elif m.video:
                    file.name = "video.mp4"
                elif m.document:
                    file.name = m.file.name or "file"
                elif m.audio:
                    file.name = "audio.mp3"

                files.append(file)

            message_link = f"https://t.me/{channel_username}/{msg.id}"
            caption = extract_caption(msg)
            final_caption = (
                f"Media group from [@{channel_username}]({message_link})\n"
                f"Message ID: `{msg.id}`\n\n"
                f"Caption:\n{caption}"
            )

            await client.send_file(
                event.chat_id,
                files,
                caption=final_caption,
                parse_mode="md",
                link_preview=False,
                force_document=False,
                supports_streaming=True
            )
            return await status_msg.delete()

        # 🖼️ Single media
        for m in messages:
            if not m.media:
                continue

            file = BytesIO()
            file.name = "file"
            await client.download_media(m, file=file)
            file.seek(0)

            media_type = "Media"
            if m.photo:
                media_type = "Image"
                file.name = "image.jpg"
            elif m.video:
                media_type = "Video"
                file.name = "video.mp4"
            elif m.document:
                media_type = "Document"
                file.name = m.file.name or "file"
            elif m.audio:
                media_type = "Audio"
                file.name = "audio.mp3"

            caption = extract_caption(m)
            message_link = f"https://t.me/{channel_username}/{m.id}"
            final_caption = (
                f"{media_type} from [@{channel_username}]({message_link})\n"
                f"Message ID: `{m.id}`\n\n"
                f"Caption:\n{caption}"
            )

            await client.send_file(
                event.chat_id,
                file,
                caption=final_caption,
                parse_mode="md",
                link_preview=False,
                force_document=False,
                supports_streaming=True
            )
            return await status_msg.delete()

        # 💬 Just text
        caption = extract_caption(msg)
        message_link = f"https://t.me/{channel_username}/{msg.id}"
        final_text = (
            f"Text from [@{channel_username}]({message_link})\n"
            f"Message ID: `{msg.id}`\n\n"
            f"Content:\n{caption}"
        )
        await status_msg.edit(final_text, link_preview=False)

    except Exception as e:
        await event.edit(f"Error occurred:\n`{e}`")

#كود كتم

MUTED_FILE = "muted.json"

def load_muted():
    if not os.path.exists(MUTED_FILE):
        return {}
    with open(MUTED_FILE, "r") as f:
        return json.load(f)

def save_muted(data):
    with open(MUTED_FILE, "w") as f:
        json.dump(data, f, indent=4)

def mute_user(chat_id, user_id):
    data = load_muted()
    chat_id = str(chat_id)
    if chat_id not in data:
        data[chat_id] = []
    if user_id not in data[chat_id]:
        data[chat_id].append(user_id)
        save_muted(data)
        return True
    return False

def unmute_user(chat_id, user_id):
    data = load_muted()
    chat_id = str(chat_id)
    if chat_id in data and user_id in data[chat_id]:
        data[chat_id].remove(user_id)
        if not data[chat_id]:
            del data[chat_id]
        save_muted(data)
        return True
    return False

def get_muted(chat_id):
    data = load_muted()
    return data.get(str(chat_id), [])


# .mute (reply, user ID, or username)
@client.on(events.NewMessage(pattern=r"\.mute(?:\s+(.+))?"))
async def mute_handler(event):
    chat_id = event.chat_id
    arg = event.pattern_match.group(1)
    user_id = None

    if arg:
        try:
            entity = await event.client.get_entity(arg)
            user_id = entity.id
        except Exception as e:
            return await event.edit(f"- Invalid user or ID.\n`{e}`")
    elif event.is_reply:
        reply = await event.get_reply_message()
        user_id = reply.sender_id
    else:
        return await event.edit("- Please reply to a message or provide a user ID or @username.")

    if mute_user(chat_id, user_id):
        await event.edit(f"- User [ID: {user_id}](tg://user?id={user_id}) has been muted in this chat.")
    else:
        await event.edit("- User is already muted in this chat.")


# .unmute (reply, user ID, or username)
@client.on(events.NewMessage(pattern=r"\.unmute(?:\s+(.+))?"))
async def unmute_handler(event):
    chat_id = event.chat_id
    arg = event.pattern_match.group(1)
    user_id = None

    if arg:
        try:
            entity = await event.client.get_entity(arg)
            user_id = entity.id
        except Exception as e:
            return await event.edit(f"- Invalid user or ID.\n`{e}`")
    elif event.is_reply:
        reply = await event.get_reply_message()
        user_id = reply.sender_id
    else:
        return await event.edit("- Please reply to a message or provide a user ID or @username.")

    if unmute_user(chat_id, user_id):
        await event.edit(f"- User [ID: {user_id}](tg://user?id={user_id}) has been unmuted.")
    else:
        await event.edit("- User is not muted in this chat.")


# .muted
@client.on(events.NewMessage(pattern=r"\.muted$"))
async def show_muted(event):
    chat_id = event.chat_id
    muted_list = get_muted(chat_id)

    if not muted_list:
        return await event.edit("- No muted users in this chat.")

    msg = "🔇 Muted users in this chat:\n\n"
    for user_id in muted_list:
        try:
            user = await event.client.get_entity(user_id)
            name = f"@{user.username}" if user.username else user.first_name
            msg += f"- {name} ([{user_id}](tg://user?id={user_id}))\n"
        except:
            msg += f"- [Unknown User] ({user_id})\n"

    await event.edit(msg)


# Delete messages from muted users
@client.on(events.NewMessage())
async def delete_muted_messages(event):
    chat_id = event.chat_id
    sender_id = event.sender_id
    muted_list = get_muted(chat_id)

    if sender_id in muted_list:
        try:
            await event.delete()
            print(f"[Muted] Deleted message from {sender_id} in chat {chat_id}")
        except Exception as e:
            print(f"❌ Failed to delete message: {e}")
#صوره ذاتيه
iraq_timezone = pytz.timezone("Asia/Baghdad")

@client.on(events.NewMessage(func=lambda e: e.is_private and e.media and getattr(e.media, 'ttl_seconds', None)))
async def downloader(event):
    try:
        result = await event.download_media()
        if not result:
            return  # If media can't be downloaded, silently ignore

        sender = await event.get_sender()
        sender_name = f"{sender.first_name or ''} {sender.last_name or ''}".strip()
        sender_username = f"@{sender.username}" if sender.username else f"`{sender.id}`"
        current_time = datetime.datetime.now(iraq_timezone).strftime("%Y-%m-%d %H:%M:%S")

        caption = (
            "📸 Temporary photo captured\n\n"
            f"👤 From: {sender_name} ({sender_username})\n"
            f"🕒 Time: {current_time}"
        )

        await client.send_file("me", result, caption=caption)

    except Exception as e:
        # No public reply, just quietly send error to saved messages
        await client.send_message("me", f"- Error saving temporary photo:\n`{str(e)}`")


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
    # تعديل رسالة الأمر نفسها بدل إنشاء رسالة جديدة
    msg = await event.edit("🔄 جاري حذف رسائلك...")
    me = await client.get_me()
    chat_id = event.chat_id
    count = 0
    batch = []

    async for message in client.iter_messages(chat_id, from_user=me.id):
        # تجاهل رسالة الأمر نفسه حتى ما يمسحها
        if message.id == event.id:
            continue
        
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
#تحويل الصوره الى ستيكر
from telethon import events
from io import BytesIO

@client.on(events.NewMessage(pattern=r'\.sticker$', outgoing=True))
async def convert_to_sticker(event):
    reply = await event.get_reply_message()
    if not reply or not reply.photo:
        return await event.edit("Reply to an image to convert it to a sticker.")

    try:
        img = BytesIO()
        img.name = "sticker.webp"  # مهم جداً: الاسم لازم يكون .webp حتى يعتبره ستيكر
        await client.download_media(reply.photo, file=img)
        img.seek(0)

        await client.send_file(
            event.chat_id,
            img,
            reply_to=reply.id,
            force_document=False,
            allow_cache=False
        )

        await event.delete()

    except Exception as e:
        await event.edit(f"Error converting to sticker:\n`{e}`")

client.start()
print("⚡ Bot is running...")
client.run_until_disconnected()
