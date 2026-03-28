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

CLIENT = CLIENT()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
TEXT = Script.TEXT

# --------------------------------------------------------------

def clean_html_tags(text):
    if not text:
        return text
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def modify_caption(message, caption, link_remove, replace_link):
    base_caption = custom_caption(message, caption, strip_links=False)
    if not base_caption:
        return None
    if replace_link or link_remove:
        base_caption = clean_html_tags(base_caption)
    if replace_link:
        url_pattern = re.compile(r'(https?://\S+|t\.me/\S+|@\S+)', re.IGNORECASE)
        if replace_link.startswith('@'):
            base_caption = url_pattern.sub(replace_link, base_caption)
        else:
            base_caption = url_pattern.sub(replace_link, base_caption)
    elif link_remove:
        base_caption = strip_urls(base_caption)
    return base_caption

def get_media_info(message):
    """
    Safely extracts media object, file name, file size, and file ID.
    Returns (media, file_name, file_size, file_id)
    """
    media = None
    file_name = None
    file_size = None
    file_id = None

    if message.document:
        media = message.document
    elif message.video:
        media = message.video
    elif message.audio:
        media = message.audio
    elif message.animation:
        media = message.animation
    elif message.photo:
        # photo is a list, take the last (largest) element
        if message.photo:
            media = message.photo[-1] if isinstance(message.photo, list) else message.photo
    elif message.sticker:
        media = message.sticker
    else:
        return None, None, None, None

    if media:
        file_name = getattr(media, 'file_name', None)
        file_size = getattr(media, 'file_size', None)
        file_id = getattr(media, 'file_id', None)

    return media, file_name, file_size, file_id

def should_forward(message, file_name, original_caption, custom_caption,
                   filename_keywords, caption_keywords, custom_caption_keywords,
                   legacy_keywords):
    """
    Returns True if the message should be forwarded based on keyword filters.
    Each keyword set is independent: if any set matches, the message passes.
    If a keyword set is empty/None, it is ignored.
    The legacy_keywords (old global keywords) are used as a fallback if none of
    the new sets are provided.
    """
    # Build a list of text pieces to check, each with its own keyword set
    checks = []
    if filename_keywords and file_name:
        checks.append((file_name, filename_keywords))
    if caption_keywords and original_caption:
        checks.append((original_caption, caption_keywords))
    if custom_caption_keywords and custom_caption:
        checks.append((custom_caption, custom_caption_keywords))
    # Legacy fallback: if no new sets are defined, use legacy_keywords on all texts
    if not (filename_keywords or caption_keywords or custom_caption_keywords) and legacy_keywords:
        all_text = ""
        if file_name:
            all_text += file_name + " "
        if original_caption:
            all_text += original_caption
        if all_text:
            checks.append((all_text, legacy_keywords))

    # If no keyword sets at all, allow the message (no filtering)
    if not checks:
        return True

    # For each check, see if the text contains any of the keywords (case-insensitive)
    for text, kw_string in checks:
        if not kw_string:
            continue
        # kw_string is a pipe‑separated list like "word1|word2|word3"
        if re.search(kw_string, text, re.IGNORECASE):
            return True

    # If none of the checks matched, filter out
    return False

# --------------------------------------------------------------

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
    extensions = datas['extensions']      # pipe‑separated list
    filename_keywords = datas.get('filename_keywords')
    caption_keywords = datas.get('caption_keywords')
    custom_caption_keywords = datas.get('custom_caption_keywords')
    legacy_keywords = datas.get('keywords')   # old global keywords

    if not _bot:
        return await msg_edit(m, "<code>You didn't added any bot. Please add a bot using /settings !</code>", wait=True)
    if _bot['is_bot']:
        data = _bot['token']
    else:
        data = _bot['session']
    try:
        il = True if _bot['is_bot'] else False
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
            pling = 0
            link_remove = datas['link_remove']
            replace_link = datas['replace_link']
            await edit(user, m, 'ᴘʀᴏɢʀᴇssɪɴɢ', 5, sts)
            async for message in iter_messages(client, chat_id=sts.get("FROM"), limit=sts.get("limit"), offset=sts.get("skip"), filters=filter, max_size=max_size):
                if await is_cancelled(client, user, m, sts):
                    if user_have_db:
                        await user_db.drop_all()
                        await user_db.close()
                    return
                if pling % 20 == 0:
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

                # Get media info
                media, file_name, file_size, file_id = get_media_info(message)
                # Original caption (if any)
                original_caption = message.caption or message.text
                # Custom caption (the one the user wants to add)
                custom_caption_text = custom_caption(message, caption, strip_links=False)

                # Apply extension filter
                if extensions and file_name and await extension_filter(extensions, file_name):
                    sts.add('filtered')
                    continue
                # Apply size filter
                if (max_size or min_size) and file_size and await size_filter(max_size, min_size, file_size):
                    sts.add('filtered')
                    continue
                # Apply duplicate filter
                if datas['skip_duplicate'] and file_id and file_id in dup_files:
                    sts.add('duplicate')
                    continue
                if datas['skip_duplicate'] and file_id:
                    dup_files.append(file_id)
                    if user_have_db:
                        await user_db.add_file(file_id)

                # Keyword filtering using the new logic
                if not should_forward(message, file_name, original_caption, custom_caption_text,
                                      filename_keywords, caption_keywords, custom_caption_keywords,
                                      legacy_keywords):
                    sts.add('filtered')
                    continue

                # If we reached here, the message is allowed
                use_batch = forward_tag and not (link_remove or replace_link)

                if use_batch:
                    MSG.append(message.id)
                    notcompleted = len(MSG)
                    completed = sts.get('total') - sts.get('fetched')
                    if notcompleted >= 100 or completed <= 100:
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

# --------------------------------------------------------------
# All other helper functions (copy, forward, msg_edit, edit, is_cancelled,
# stop, send, custom_caption, get_size, keyword_filter, extension_filter,
# size_filter, media, TimeFormatter, retry_btn, terminate_frwding,
# status_msg, close, stop_forward, restart_pending_forwads, store_vars,
# restart_forwards, update_forward, get_bot_uptime, complete_time)
# remain exactly the same as in the previous version.
# For brevity, they are omitted here but you should keep them.
# --------------------------------------------------------------

# ... (copy all the unchanged functions from the previous code)
