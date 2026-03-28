# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import sys 
import math
import time
import re
import asyncio 
import logging
import random
from .utils import STS
from database import Db, db
from .test import CLIENT, get_client, iter_messages
from config import Config, temp
from script import Script
from pyrogram import Client, filters 
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message 
from .db import connect_user_db
from pyrogram.types import Message
from .linkremoveforwd import strip_urls

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

CLIENT = CLIENT()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
TEXT = Script.TEXT

# ============ FIXED KEYWORD FILTER FUNCTION ============
async def keyword_filter(keywords, content):
    """
    Returns True if the content should be filtered out (skipped).
    Returns False if the content should be kept.
    """
    if keywords is None:
        return False  # No keywords → keep everything
    if not content:
        return True   # No content to check → filter out
    # Return True to skip if keywords NOT found
    return not bool(re.search(keywords, content, re.IGNORECASE))


# ============ FIXED EXTENSION FILTER FUNCTION ============
async def extension_filter(extensions, file_name):
    """
    Returns True if the file should be filtered out (skipped).
    Returns False if the file should be kept.
    """
    if extensions is None:
        return False  # No extension filter → keep everything
    if not file_name:
        return False
    # Return True to skip if extension IS found
    return bool(re.search(extensions, file_name, re.IGNORECASE))


# ============ FUNCTION TO GET ALL CONTENT FOR KEYWORD CHECK ============
def get_keyword_content(message):
    """
    Extract ALL content from message for keyword checking.
    Checks both file name AND caption for all media types.
    Supports: Documents, Videos, Photos, Text, Audio, Animations, Voice, etc.
    """
    content_list = []
    
    # For Documents (files) - check file name AND caption
    if message.document:
        if message.document.file_name:
            content_list.append(message.document.file_name)
        if message.caption:
            content_list.append(message.caption)
    
    # For Videos - check file name AND caption
    elif message.video:
        if message.video.file_name:
            content_list.append(message.video.file_name)
        if message.caption:
            content_list.append(message.caption)
    
    # For Photos - check caption
    elif message.photo:
        if message.caption:
            content_list.append(message.caption)
    
    # For Text Messages - check text content
    elif message.text:
        content_list.append(message.text)
    
    # For Audio files - check file name AND caption
    elif message.audio:
        if message.audio.file_name:
            content_list.append(message.audio.file_name)
        if message.caption:
            content_list.append(message.caption)
    
    # For Animations (GIFs) - check file name AND caption
    elif message.animation:
        if message.animation.file_name:
            content_list.append(message.animation.file_name)
        if message.caption:
            content_list.append(message.caption)
    
    # For Voice messages - check caption (if any)
    elif message.voice:
        if message.caption:
            content_list.append(message.caption)
    
    # For Stickers - check sticker emoji or caption
    elif message.sticker:
        if message.sticker.emoji:
            content_list.append(message.sticker.emoji)
        if message.caption:
            content_list.append(message.caption)
    
    # Combine all content into one string (or return list for multiple checks)
    if content_list:
        return " ".join(content_list)  # Combine all content for checking
    
    return None


# ============ CHECK IF ANY KEYWORD MATCHES IN ANY CONTENT ============
async def should_filter_by_keywords(keywords, message):
    """
    Check if message should be filtered based on keywords.
    Returns True if should filter out (skip), False if should keep.
    """
    if keywords is None:
        return False
    
    # Get all content from message
    all_content = get_keyword_content(message)
    
    if not all_content:
        # No content to check - filter out if keywords are set
        return True if keywords else False
    
    # Check if any keyword matches in any content
    # Return True (filter out) if NO keyword found
    return not bool(re.search(keywords, all_content, re.IGNORECASE))


# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

def clean_html_tags(text):
    """Remove HTML tags from text while preserving content."""
    if not text:
        return text
    
    # Remove all HTML tags but keep content
    text = re.sub(r'<[^>]+>', '', text)
    
    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def modify_caption(message, caption, link_remove, replace_link):
    """Return the final caption after applying settings."""
    base_caption = custom_caption(message, caption, strip_links=False)
    if not base_caption:
        return None

    # Clean HTML tags if we're going to modify the caption
    if replace_link or link_remove:
        base_caption = clean_html_tags(base_caption)

    if replace_link:
        # Replace all URLs and @mentions with the given replacement
        url_pattern = re.compile(r'(https?://\S+|t\.me/\S+|@\S+)', re.IGNORECASE)
        
        # Special handling for @username replacement
        if replace_link.startswith('@'):
            # Replace with username format
            base_caption = url_pattern.sub(replace_link, base_caption)
        else:
            # Replace with URL format
            base_caption = url_pattern.sub(replace_link, base_caption)
    elif link_remove:
        base_caption = strip_urls(base_caption)

    return base_caption

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_callback_query(filters.regex(r'^start_public'))
async def pub_(bot, message):
    user = message.from_user.id
    temp.CANCEL[user] = False
    frwd_id = message.data.split("_")[2]
    if temp.lock.get(user) and str(temp.lock.get(user))=="True":
      return await message.answer("please wait until previous task complete", show_alert=True)
    sts = STS(frwd_id)
    if not sts.verify():
      await message.answer("your are clicking on my old button", show_alert=True)
      return await message.message.delete()
    i = sts.get(full=True)
    if i.TO in temp.IS_FRWD_CHAT:
      return await message.answer("In Target chat a task is progressing. please wait until task complete", show_alert=True)
    m = await msg_edit(message.message, "<code>verifying your data's, please wait.</code>")
    _bot, caption, forward_tag, datas, protect, button = await sts.get_data(user)
    filter = datas['filters']
    max_size = datas['max_size']
    min_size = datas['min_size']
    keyword = datas['keywords']
    exten = datas['extensions']
    keywords = ""
    extensions = ""
    if keyword:
        for key in keyword:
            keywords += f"{key}|"
        keywords  = keywords.rstrip("|")
    else:
        keywords = None
    if exten:
        for ext in exten:
            extensions += f"{ext}|"
        extensions = extensions.rstrip("|")
    else:
        extensions = None
    if not _bot:
      return await msg_edit(m, "<code>You didn't added any bot. Please add a bot using /settings !</code>", wait=True)
    if _bot['is_bot'] == True:
        data = _bot['token']
    else:
        data = _bot['session']
    try:
      il = True if _bot['is_bot'] == True else False
      client = await get_client(data, is_bot=il)
      await client.start()
    except Exception as e:  
      return await m.edit(e)
    await msg_edit(m, "<code>processing..</code>")
    try: 
       await client.get_messages(sts.get("FROM"), sts.get("limit"))
    except:
       await msg_edit(m, f"**Source chat may be a private channel / group. Use userbot (user must be member over there) or  if Make Your [Bot](t.me/{_bot['username']}) an admin over there**", retry_btn(frwd_id), True)
       return await stop(client, user)
    try:
       k = await client.send_message(i.TO, "Testing")
       await k.delete()
    except:
       await msg_edit(m, f"**Please Make Your [UserBot / Bot](t.me/{_bot['username']}) Admin In Target Channel With Full Permissions**", retry_btn(frwd_id), True)
       return await stop(client, user)
    user_have_db = False
    dburi = datas['db_uri']
    if dburi is not None:
        connected, user_db = await connect_user_db(user, dburi, i.TO)
        if not connected:
            await msg_edit(m, "<code>Cannot Connected Your db Errors Found Dup files Have Been Skipped after Restart</code>")
        else:
            user_have_db = True
    temp.forwardings += 1
    await db.add_frwd(user)
    await send(client, user, "<b>Fᴏʀᴡᴀʀᴅɪɴɢ sᴛᴀʀᴛᴇᴅ🔥</b>")
    sts.add(time=True)
    default_delay = 1 if _bot['is_bot'] else 10
    user_delay = datas['forward_delay']
    sleep = user_delay if user_delay > 0 else default_delay
    await msg_edit(m, "<code>processing...</code>") 
    temp.IS_FRWD_CHAT.append(i.TO)
    temp.lock[user] = locked = True
    dup_files = []
    if locked:
        try:
          MSG = []
          pling=0
          link_remove = datas['link_remove']
          replace_link = datas['replace_link']
          await edit(user, m, 'ᴘʀᴏɢʀᴇssɪɴɢ', 5, sts)
          async for message in iter_messages(client, chat_id=sts.get("FROM"), limit=sts.get("limit"), offset=sts.get("skip"), filters=filter, max_size=max_size):
                if await is_cancelled(client, user, m, sts):
                   if user_have_db:
                      await user_db.drop_all()
                      await user_db.close()
                   return
                if pling %20 == 0: 
                   await edit(user, m, 'ᴘʀᴏɢʀᴇssɪɴɢ', 5, sts)
                pling += 1
                sts.add('fetched')
                if message == "DUPLICATE":
                   sts.add('duplicate')
                   continue
                elif message == "FILTERED":
                   sts.add('filtered')
                   continue 
                elif message.empty or message.service:
                   sts.add('deleted')
                   continue
                
                # ============ APPLY KEYWORD FILTER (Checks file name AND caption for all media types) ============
                if await should_filter_by_keywords(keywords, message):
                    sts.add('filtered')
                    continue
                
                # ============ APPLY EXTENSION FILTER (Only for documents) ============
                if message.document and await extension_filter(extensions, message.document.file_name):
                    sts.add('filtered')
                    continue 
                
                # ============ APPLY SIZE FILTER (Only for documents) ============
                if message.document and await size_filter(max_size, min_size, message.document.file_size):
                    sts.add('filtered')
                    continue 
                
                # ============ DUPLICATE CHECK ============
                file_id_to_check = None
                if message.document:
                    file_id_to_check = message.document.file_id
                elif message.video:
                    file_id_to_check = message.video.file_id
                elif message.photo:
                    file_id_to_check = message.photo.file_id
                elif message.audio:
                    file_id_to_check = message.audio.file_id
                elif message.animation:
                    file_id_to_check = message.animation.file_id
                
                if file_id_to_check and file_id_to_check in dup_files:
                    sts.add('duplicate')
                    continue
                
                # Add to duplicate tracking
                if file_id_to_check and datas['skip_duplicate']:
                    dup_files.append(file_id_to_check)
                    if user_have_db:
                        await user_db.add_file(file_id_to_check)
                
                # Check if we need to use batch forward or individual copy
                use_batch = forward_tag and not (link_remove or replace_link)
                
                if use_batch:
                   MSG.append(message.id)
                   notcompleted = len(MSG)
                   completed = sts.get('total') - sts.get('fetched')
                   if ( notcompleted >= 100 
                        or completed <= 100): 
                      await forward(user, client, MSG, m, sts, protect)
                      sts.add('total_files', notcompleted)
                      await asyncio.sleep(10)
                      MSG = []
                else:
                   new_caption = modify_caption(message, caption, link_remove, replace_link)
                   details = {"msg_id": message.id, "media": media(message), "caption": new_caption, 'button': button, "protect": protect}
                   await copy(user, client, details, m, sts)
                   sts.add('total_files')
                   await asyncio.sleep(sleep) 
        except Exception as e:
            await msg_edit(m, f'<b>ERROR:</b>\n<code>{e}</code>', wait=True)
            print(e)
            if user_have_db:
                await user_db.drop_all()
                await user_db.close()
            temp.IS_FRWD_CHAT.remove(sts.TO)
            return await stop(client, user)
        temp.IS_FRWD_CHAT.remove(sts.TO)
        await send(client, user, "<b>🎉 ғᴏʀᴡᴀʀᴅɪɴɢ ᴄᴏᴍᴘʟᴇᴛᴇᴅ</b>")
        await edit(user, m, 'ᴄᴏᴍᴘʟᴇᴛᴇᴅ', "completed", sts) 
        if user_have_db:
            await user_db.drop_all()
            await user_db.close()
        await stop(client, user)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def copy(user, bot, msg, m, sts):
   try:                               
     if msg.get("media") and msg.get("caption"):
        await bot.send_cached_media(
              chat_id=sts.get('TO'),
              file_id=msg.get("media"),
              caption=msg.get("caption"),
              reply_markup=msg.get('button'),
              protect_content=msg.get("protect"))
     else:
        await bot.copy_message(
              chat_id=sts.get('TO'),
              from_chat_id=sts.get('FROM'),    
              caption=msg.get("caption"),
              message_id=msg.get("msg_id"),
              reply_markup=msg.get('button'),
              protect_content=msg.get("protect"))
   except FloodWait as e:
     await edit(user, m, 'ᴘʀᴏɢʀᴇssɪɴɢ', e.value, sts)
     await asyncio.sleep(e.value)
     await edit(user, m, 'ᴘʀᴏɢʀᴇssɪɴɢ', 5, sts)
     await copy(user, bot, msg, m, sts)
   except Exception as e:
     print(e)
     sts.add('deleted')

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def forward(user, bot, msg, m, sts, protect):
   try:                             
     await bot.forward_messages(
           chat_id=sts.get('TO'),
           from_chat_id=sts.get('FROM'), 
           protect_content=protect,
           message_ids=msg)
   except FloodWait as e:
     await edit(user, m, 'ᴘʀᴏɢʀᴇssɪɴɢ', e.value, sts)
     await asyncio.sleep(e.value)
     await edit(user, m, 'ᴘʀᴏɢʀᴇssɪɴɢ', 5, sts)
     await forward(user, bot, msg, m, sts, protect)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def msg_edit(msg, text, button=None, wait=None):
    try:
        return await msg.edit(text, reply_markup=button)
    except MessageNotModified:
        pass 
    except FloodWait as e:
        if wait:
           await asyncio.sleep(e.value)
           return await msg_edit(msg, text, button, wait)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def edit(user, msg, title, status, sts):
   i = sts.get(full=True)
   status = 'Forwarding' if status == 5 else f"sleeping {status} s" if str(status).isnumeric() else status
   percentage = "{:.0f}".format(float(i.fetched)*100/float(i.total))
   text = TEXT.format(i.fetched, i.total_files, i.duplicate, i.deleted, i.skip, i.filtered, status, percentage, title)
   await update_forward(user_id=user, last_id=None, start_time=i.start, limit=i.limit, chat_id=i.FROM, toid=i.TO, forward_id=None, msg_id=msg.id, fetched=i.fetched, deleted=i.deleted, total=i.total_files, duplicate=i.duplicate, skip=i.skip, filterd=i.filtered)
   now = time.time()
   diff = int(now - i.start)
   speed = sts.divide(i.fetched, diff)
   elapsed_time = round(diff) * 1000
   time_to_completion = round(sts.divide(i.total - i.fetched, int(speed))) * 1000
   estimated_total_time = elapsed_time + time_to_completion  
   progress = "●{0}{1}".format(
       ''.join(["●" for i in range(math.floor(int(percentage) / 4))]),
       ''.join(["○" for i in range(24 - math.floor(int(percentage) / 4))]))
   button =  [[InlineKeyboardButton(progress, f'fwrdstatus#{status}#{estimated_total_time}#{percentage}#{i.id}')]]
   estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)
   estimated_total_time = estimated_total_time if estimated_total_time != '' else '0 s'
   if status in ["cancelled", "completed"]:
      button.append([InlineKeyboardButton('• ᴄᴏᴍᴘʟᴇᴛᴇᴅ ​•', url='https://t.me/VJ_BOTZ')])
   else:
      button.append([InlineKeyboardButton('• ᴄᴀɴᴄᴇʟ', 'terminate_frwd')])
   await msg_edit(msg, text, InlineKeyboardMarkup(button))

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def is_cancelled(client, user, msg, sts):
   if temp.CANCEL.get(user)==True:
      if sts.TO in temp.IS_FRWD_CHAT:
         temp.IS_FRWD_CHAT.remove(sts.TO)
      await edit(user, msg, 'ᴄᴀɴᴄᴇʟʟᴇᴅ', "cancelled", sts)
      await send(client, user, "<b>❌ ғᴏʀᴡᴀʀᴅɪɴɢ ᴄᴀɴᴄᴇʟʟᴇᴅ</b>")
      await stop(client, user)
      return True 
   return False 

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def stop(client, user):
   try:
     await client.stop()
   except:
     pass 
   await db.rmve_frwd(user)
   temp.forwardings -= 1
   temp.lock[user] = False 

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def send(bot, user, text):
   try:
      await bot.send_message(user, text=text)
   except:
      pass 

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

def custom_caption(msg, caption, strip_links=False):
  if msg.media:
    if (msg.video or msg.document or msg.audio or msg.photo):
      media = getattr(msg, msg.media.value, None)
      if media:
        file_name = getattr(media, 'file_name', '')
        file_size = getattr(media, 'file_size', '')
        fcaption = getattr(msg, 'caption', '')
        if fcaption:
          fcaption = fcaption.html
        if strip_links:
          fcaption = strip_urls(fcaption)
        if caption:
          return caption.format(filename=file_name, size=get_size(file_size), caption=fcaption)
        return fcaption
  return None

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

def get_size(size):
  units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
  size = float(size)
  i = 0
  while size >= 1024.0 and i < len(units):
     i += 1
     size /= 1024.0
  return "%.2f %s" % (size, units[i]) 

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def size_filter(max_size, min_size, file_size):
    file_size = file_size / 1024 / 1024
    if max_size and min_size == 0:
        return False
    if max_size == 0:
        return file_size < min_size
    if min_size == 0:
        return file_size > max_size
    if not min_size <= file_size <= max_size:
        return True
    else:
        return False

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

def media(msg):
  if msg.media:
     media = getattr(msg, msg.media.value, None)
     if media:
        return getattr(media, 'file_id', None)
  return None 

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

def retry_btn(id):
    return InlineKeyboardMarkup([[InlineKeyboardButton('♻️ RETRY ♻️', f"start_public_{id}")]])

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_callback_query(filters.regex(r'^terminate_frwd$'))
async def terminate_frwding(bot, m):
    user_id = m.from_user.id 
    temp.lock[user_id] = False
    temp.CANCEL[user_id] = True 
    await m.answer("Forwarding cancelled !", show_alert=True)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_callback_query(filters.regex(r'^fwrdstatus'))
async def status_msg(bot, msg):
    _, status, est_time, percentage, frwd_id = msg.data.split("#")
    sts = STS(frwd_id)
    if not sts.verify():
       fetched, forwarded, remaining = 0
    else:
       fetched, limit, forwarded = sts.get('fetched'), sts.get('limit'), sts.get('total_files')
       remaining = limit - fetched 
    est_time = TimeFormatter(milliseconds=est_time)
    start_time = sts.get('start')
    uptime = await get_bot_uptime(start_time)
    total = sts.get('limit') - sts.get('fetched')
    time_to_comple = await complete_time(total)
    est_time = est_time if (est_time != '' or status not in ['completed', 'cancelled']) else '0 s'
    return await msg.answer(PROGRESS.format(percentage, fetched, forwarded, remaining, status, time_to_comple, uptime), show_alert=True)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_callback_query(filters.regex(r'^close_btn$'))
async def close(bot, update):
    await update.answer()
    await update.message.delete()

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_message(filters.private & filters.command(['stop']))
async def stop_forward(client, message):
    user_id = message.from_user.id
    sts = await message.reply('<code>Stoping...</code>')
    await asyncio.sleep(0.5)
    if not await db.is_forwad_exit(message.from_user.id):
        return await sts.edit('**No Ongoing Forwards To Cancel**')
    temp.lock[user_id] = False
    temp.CANCEL[user_id] = True
    mst = await db.get_forward_details(user_id)
    msg = await client.get_messages(user_id, mst['msg_id'])
    link = f"tg://openmessage?user_id={6648261085}&message_id={mst['msg_id']}"
    await sts.edit(f"<b>Successfully Canceled </b>", disable_web_page_preview=True)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def restart_pending_forwads(bot, user):
    user = user['user_id']
    settings = await db.get_forward_details(user)
    try:
       skiping = settings['offset']
       fetch = settings['fetched'] - settings['skip']
       temp.forwardings += 1
       forward_id = await store_vars(user)
       sts = STS(forward_id)
       if settings['chat_id'] is None:
           return await db.rmve_frwd(user)
           temp.forwardings -= 1
       if not sts.verify():
          temp.forwardings -=1
          return 
       sts.add('fetched', value=fetch)
       sts.add('duplicate', value=settings['duplicate'])
       sts.add('filtered', value=settings['filtered'])
       sts.add('deleted', value=settings['deleted'])
       sts.add('total_files', value=settings['total'])
       m = await bot.get_messages(user, settings['msg_id'])#
       _bot, caption, forward_tag, datas, protect, button = await sts.get_data(user)
       i = sts.get(full=True)
       filter = datas['filters']
       max_size = datas['max_size']
       min_size = datas['min_size']
       keyword = datas['keywords']
       exten = datas['extensions']
       keywords = ""
       extensions = ""
       if keyword:
           for key in keyword:
               keywords += f"{key}|"
           keywords  = keywords.rstrip("|")
       else:
           keywords = None
       if exten:
           for ext in exten:
               extensions += f"{ext}|"
           extensions = extensions.rstrip("|")
       else:
           extensions = None
       if not _bot:
          return await msg_edit(m, "<code>You didn't added any bot. Please add a bot using /settings !</code>", wait=True)
       if _bot['is_bot'] == True:
          data = _bot['token']
       else:
          data = _bot['session']
       try:
          il = True if _bot['is_bot'] == True else False
          client = await get_client(data, is_bot=il)
          await client.start()
       except Exception as e:  
          return await m.edit(e)
       try:
          await msg_edit(m, "<code>processing..</code>")
       except:
          return await db.rmve_frwd(user)
       try: 
          await client.get_messages(sts.get("FROM"), sts.get("limit"))
       except:
          await msg_edit(m, f"**Source chat may be a private channel / group. Use userbot (user must be member over there) or  if Make Your [Bot](t.me/{_bot['username']}) an admin over there**", retry_btn(forward_id), True)
          return await stop(client, user)
       try:
          k = await client.send_message(i.TO, "Testing")
          await k.delete()
       except:
          await msg_edit(m, f"**Please Make Your [UserBot / Bot](t.me/{_bot['username']}) Admin In Target Channel With Full Permissions**", retry_btn(forward_id), True)
          return await stop(client, user)
    except:
       return await db.rmve_frwd(user)
    user_have_db = False
    dburi = datas['db_uri']
    if dburi is not None:
        connected, user_db = await connect_user_db(user, dburi, i.TO)
        if not connected:
            await msg_edit(m, "<code>Cannot Connected Your db Errors Found Dup files Have Been Skipped after Restart</code>")
        else:
            user_have_db = True
    try:
        start = settings['start_time']
    except KeyError:
        start = None
    sts.add(time=True, start_time=start)
    default_delay = 1 if _bot['is_bot'] else 10
    user_delay = datas['forward_delay']
    sleep = user_delay if user_delay > 0 else default_delay
    #await msg_edit(m, "<code>processing...</code>") 
    temp.IS_FRWD_CHAT.append(i.TO)
    temp.lock[user] = locked = True
    dup_files = []
    if user_have_db and datas['skip_duplicate']:
        old_files = await user_db.get_all_files()
        async for ofile in old_files:
            dup_files.append(ofile["file_id"])
    if locked:
        try:
          MSG = []
          pling=0
          link_remove = datas['link_remove']
          replace_link = datas['replace_link']
          await edit(user, m, 'ᴘʀᴏɢʀᴇssɪɴɢ', 5, sts)
          async for message in iter_messages(client, chat_id=sts.get("FROM"), limit=sts.get("limit"), offset=skiping, filters=filter, max_size=max_size):
                if await is_cancelled(client, user, m, sts):
                    if user_have_db:
                       await user_db.drop_all()
                       await user_db.close()
                       return
                    return
                if pling %20 == 0: 
                   await edit(user, m, 'ᴘʀᴏɢʀᴇssɪɴɢ', 5, sts)
                pling += 1
                sts.add('fetched')
                if message == "DUPLICATE":
                   sts.add('duplicate')
                   continue
                elif message == "FILTERED":
                   sts.add('filtered')
                   continue 
                elif message.empty or message.service:
                   sts.add('deleted')
                   continue
                
                # ============ APPLY KEYWORD FILTER (Checks file name AND caption for all media types) ============
                if await should_filter_by_keywords(keywords, message):
                    sts.add('filtered')
                    continue
                
                # ============ APPLY EXTENSION FILTER (Only for documents) ============
                if message.document and await extension_filter(extensions, message.document.file_name):
                    sts.add('filtered')
                    continue 
                
                # ============ APPLY SIZE FILTER (Only for documents) ============
                if message.document and await size_filter(max_size, min_size, message.document.file_size):
                    sts.add('filtered')
                    continue 
                
                # ============ DUPLICATE CHECK ============
                file_id_to_check = None
                if message.document:
                    file_id_to_check = message.document.file_id
                elif message.video:
                    file_id_to_check = message.video.file_id
                elif message.photo:
                    file_id_to_check = message.photo.file_id
                elif message.audio:
                    file_id_to_check = message.audio.file_id
                elif message.animation:
                    file_id_to_check = message.animation.file_id
                
                if file_id_to_check and file_id_to_check in dup_files:
                    sts.add('duplicate')
                    continue
                
                # Add to duplicate tracking
                if file_id_to_check and datas['skip_duplicate']:
                    dup_files.append(file_id_to_check)
                    if user_have_db:
                        await user_db.add_file(file_id_to_check)
                
                use_batch = forward_tag and not (link_remove or replace_link)
                
                if use_batch:
                   MSG.append(message.id)
                   notcompleted = len(MSG)
                   completed = sts.get('total') - sts.get('fetched')
                   if ( notcompleted >= 100 
                        or completed <= 100): 
                      await forward(user, client, MSG, m, sts, protect)
                      sts.add('total_files', notcompleted)
                      await asyncio.sleep(10)
                      MSG = []
                else:
                   new_caption = modify_caption(message, caption, link_remove, replace_link)
                   details = {"msg_id": message.id, "media": media(message), "caption": new_caption, 'button': button, "protect": protect}
                   await copy(user, client, details, m, sts)
                   sts.add('total_files')
                   await asyncio.sleep(sleep) 
        except Exception as e:
            await msg_edit(m, f'<b>ERROR:</b>\n<code>{e}</code>', wait=True)
            if user_have_db:
                await user_db.drop_all()
                await user_db.close()
            temp.IS_FRWD_CHAT.remove(sts.TO)
            return await stop(client, user)
        temp.IS_FRWD_CHAT.remove(sts.TO)
        await send(client, user, "<b>🎉 ғᴏʀᴡᴀʀᴅɪɴɢ ᴄᴏᴍᴘʟᴇᴛᴇᴅ</b>")
        if user_have_db:
            await user_db.drop_all()
            await user_db.close()
        await edit(user, m, 'ᴄᴏᴍᴘʟᴇᴛᴇᴅ', "completed", sts) 
        await stop(client, user)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def store_vars(user_id):
    settings = await db.get_forward_details(user_id)
    fetch = settings['fetched']
    forward_id = f'{user_id}-{fetch}'
    print(fetch)
    STS(id=forward_id).store(settings['chat_id'], settings['toid'], settings['skip'], settings['limit'])
    return forward_id

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def restart_forwards(client):
    users = await db.get_all_frwd()
    count = await db.forwad_count()
    tasks = []
    async for user in users:
        tasks.append(restart_pending_forwads(client, user))
    random_seconds = random.randint(0, 300)
    minutes = random_seconds // 60
    seconds = random_seconds % 60
    await asyncio.gather(*tasks)
    print('Done')

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def update_forward(user_id, chat_id, start_time, toid, last_id, limit, forward_id, msg_id, fetched, total, duplicate, deleted, skip, filterd):
    details = {
        'chat_id': chat_id,
        'toid': toid,
        'forward_id': forward_id,
        'last_id': last_id,
        'limit': limit,
        'msg_id': msg_id,
        'start_time': start_time,
        'fetched': fetched,
        'offset': fetched,
        'deleted': deleted,
        'total': total,
        'duplicate': duplicate,
        'skip': skip,
        'filtered':filterd
    }
    await db.update_forward(user_id, details)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def get_bot_uptime(start_time):
    # Calculate the uptime in seconds
    uptime_seconds = int(time.time() - start_time)
    uptime_minutes = uptime_seconds // 60
    uptime_hours = uptime_minutes // 60
    uptime_days = uptime_hours // 24
    uptime_weeks = uptime_days // 7
    uptime_string = ""
    if uptime_weeks != 0:
        uptime_string += f"{uptime_weeks % 7}w, "
    if uptime_days != 0:
        uptime_string += f"{uptime_days % 24}d, "
    if uptime_hours != 0:
        uptime_string += f"{uptime_hours % 24}h, "
    if uptime_minutes != 0:
        uptime_string += f"{uptime_minutes % 60}m, "
    uptime_string += f"{uptime_seconds % 60}s"
    return uptime_string  

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def complete_time(total_files, files_per_minute=30):
    minutes_required = total_files / files_per_minute
    seconds_required = minutes_required * 60
    weeks = seconds_required // (7 * 24 * 60 * 60)
    days = (seconds_required % (7 * 24 * 60 * 60)) // (24 * 60 * 60)
    hours = (seconds_required % (24 * 60 * 60)) // (60 * 60)
    minutes = (seconds_required % (60 * 60)) // 60
    seconds = seconds_required % 60
    time_format = ""
    if weeks > 0:
        time_format += f"{int(weeks)}w, "
    if days > 0:
        time_format += f"{int(days)}d, "
    if hours > 0:
        time_format += f"{int(hours)}h, "
    if minutes > 0:
        time_format += f"{int(minutes)}m, "
    if seconds > 0:
        time_format += f"{int(seconds)}s"
    return time_format

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
