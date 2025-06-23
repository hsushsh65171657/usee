from telethon.sync import TelegramClient
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
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_string = os.environ.get("STRING_SESSION")

client = TelegramClient(StringSession(session_string), api_id, api_hash)

client.parse_mode = CustomMarkdown()
shd = False
@client.on(events.NewMessage(outgoing=True, pattern=".فشر"))
async def stop_wkte(event):
    rep = await event.get_reply_message()
    global shd
    shd = True
    for s in open("sc.txt","r").read().split("\n"):
     if shd == False:
      break
     await rep.reply(s)
     
async def send_to_all_groups(message):
    async for dialog in client.iter_dialogs():
        if dialog.is_group:
            await client.send_message(dialog.id, message)

@client.on(events.NewMessage(pattern=r'^\.للكروبات(.*)'))
async def gcast(event):
    jmisbest = event.pattern_match.group(1).strip()
    if jmisbest:
        msg = jmisbest
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        await event.respond("Please , respond to media or text to send in all groups [🔪](emoji/5787203590791631463)")
        return
    roz = await event.respond("wait i send the all groups [⚠️](emoji/5787656288934564517)")
    er = 0
    done = 0
    async for x in client.iter_dialogs():
        if x.is_group:
            chat = x.id
            try:
                await client.send_message(chat, msg)
                done += 1
            except BaseException:
                er += 1
    await roz.edit(
       f"Done send group : {done} [🚨](emoji/5787350568867467099) \nError send group : {er} [👍](emoji/5787240789503381376)"
    )
@client.on(events.NewMessage(outgoing=True, pattern=".بصم"))
async def bsm(event):
 reply = await event.get_reply_message()
 await client.send_file(event.chat_id, f"https://t.me/jshdhdycyyc/{random.randint(2, 165)}", reply_to=reply)
 await event.delete()
@client.on(events.NewMessage(outgoing=True, pattern=".ايقاف"))
async def stop_wkte(event):
    global shd
    shd = False
    await event.edit("Done Stopped [✈️](emoji/5350711759625795085)")
@client.on(events.NewMessage(outgoing=True, pattern=".الاوامر"))
async def ir(event):await event.edit("Hi DraGoN The list is commands [🚀](emoji/5411580731929411768)\n\n ¹ امسحلي ليمسح جميع رسائلك في المجموعه [🌲](emoji/5447249559149367631)\n\n ² بصم : ليرسل بصمه شد بالرد على الاخرون [🔤](emoji/5278407591515406257)\n\n ³ فشر : بالرد ليقوم بأرسال السب الى الاخرون [🔥](emoji/5345941618623005800)\n\n⁴ ايقاف : لايقاف امر فشر [🔴](emoji/5073651519669143988)\n\n⁵ شد : يقوم بالشد عن طريق اليوزر مثال | .شد 60 0 @test [💔](emoji/5474642010159725283)\n\n⁶ للكروبات : يقوم حينما ترد على رساله سيرسلها بجميع المجموعات الموجوده في الحساب [🔥](emoji/5787498156828660380)")
@client.on(events.NewMessage(pattern='.امسحلي'))
async def jmthondel(event):
    zz = 0
    xx = 0
    
    async for message in client.iter_messages(event.chat_id):
        if message.sender_id == event.sender_id:
            await message.delete()
            xx += 1
    
    await client.send_message(event.chat_id, f"[✅](emoji/5352938317916683303) Done delete : {xx} message\n By : @vipjalai")
async def spam_function(chat_id, messages, count, delay, username):
    for message in messages:
        await client.send_message(chat_id, f"{message} {username}")
        await asyncio.sleep(delay)


    await event.reply(word)

@client.on(events.NewMessage(outgoing=True, pattern=".فحص"))
async def nr(event):
    start_time = time.time()
    await asyncio.sleep(1)
    end_time = time.time()
    ping = round((end_time - start_time) * 50, 2)
    r1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await event.edit(f"sourse work Successfully [👁](emoji/5263006706375342926)\nPinG : {ping} ms [👁️](emoji/5474508767389303120)\nTiMe : {r1} [😈](emoji/5474475837875044294)\n  — — — — — — \n DeV : @dohavoice [🦇](emoji/5443009168002788185)")

    
@client.on(events.NewMessage(pattern='/info'))
async def info(event):
    ram_usage = psutil.virtual_memory().percent
    cpu_usage = psutil.cpu_percent()
    response = f"info server : [🌟](emoji/5787418193127542105)\nRam : {ram_usage}% [🔥](emoji/5354863081740580440)\nCPU {cpu_usage}%[🔥](emoji/5345941618623005800)"
    await event.edit(response)
@client.on(events.NewMessage(pattern='.شد (\d+) (\d+) (\S+)'))
async def test_message(event):
    message_text = event.message.text
    matches = re.match(r'.شد (\d+) (\d+) (\S+)', message_text)
    if matches:
        dr = int(matches.group(1))
        rr = int(matches.group(2))
        muh = matches.group(3)
        with open("sc.txt", "r") as file:
            xx = file.readlines()
        
        
        await spam_function(event.chat_id, xx, dr, rr, muh)

async def main():
    await client.start()
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
asyncio.run(main())