# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import re
import asyncio 
from .utils import STS
from database import db
from config import temp 
from script import Script
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, ChannelInvalid, ChannelPrivate
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate as PrivateChat
from pyrogram.errors.exceptions.bad_request_400 import UsernameInvalid, UsernameNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

@Client.on_message(filters.private & filters.command(["forward"]))
async def run(bot, message):
    user_id = message.from_user.id
    
    # ============ BOT SELECTION ============
    all_bots = await db.get_bots(user_id)
    enabled_bots = [b for b in all_bots if b.get('enabled', True)]
    
    if not enabled_bots:
        return await message.reply("<code>You don't have any enabled bots. Please add a bot using /settings</code>")
    
    selected_bot = None
    
    if len(enabled_bots) == 1:
        selected_bot = enabled_bots[0]
    else:
        buttons = []
        for b in enabled_bots:
            label = f"{b['name']} (@{b['username']})" if b['username'] else b['name']
            buttons.append([InlineKeyboardButton(label, callback_data=f"select_bot_{b['bot_id']}")])
        buttons.append([InlineKeyboardButton("Cancel", callback_data="close_btn")])
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await bot.send_message(
            user_id,
            "**You have multiple bots available.**\n\nWhich one would you like to use for this forward?",
            reply_markup=reply_markup
        )
        
        temp.BOT_SELECTION[user_id] = None
        for _ in range(60):
            await asyncio.sleep(1)
            if temp.BOT_SELECTION.get(user_id) is not None:
                bot_id = temp.BOT_SELECTION[user_id]
                selected_bot = await db.get_bot(user_id, bot_id)
                break
        
        if selected_bot is None:
            return await message.reply("Selection timed out or cancelled.")
        temp.BOT_SELECTION.pop(user_id, None)
    
    bot_id = selected_bot['bot_id']
    is_bot = selected_bot['is_bot']
    
    # ============ TARGET CHANNEL SELECTION ============
    channels = await db.get_user_channels(user_id)
    if not channels:
       return await message.reply_text("Please set a target channel in /settings before forwarding")
    
    buttons = []
    btn_data = {}
    
    if len(channels) > 1:
       for channel in channels:
          buttons.append([KeyboardButton(f"{channel['title']}")])
          btn_data[channel['title']] = channel['chat_id']
       buttons.append([KeyboardButton("cancel")]) 
       _toid = await bot.ask(message.chat.id, Script.TO_MSG, reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))
       if _toid.text.startswith(('/', 'cancel')):
          return await message.reply_text(Script.CANCEL, reply_markup=ReplyKeyboardRemove())
       to_title = _toid.text
       toid = btn_data.get(to_title)
       if not toid:
          return await message.reply_text("Wrong channel chosen!", reply_markup=ReplyKeyboardRemove())
    else:
       toid = channels[0]['chat_id']
       to_title = channels[0]['title']
    
    # ============ SOURCE CHAT ============
    fromid = await bot.ask(message.chat.id, Script.FROM_MSG, reply_markup=ReplyKeyboardRemove())
    if fromid.text and fromid.text.startswith('/'):
        await message.reply(Script.CANCEL)
        return 
    
    if fromid.text and not fromid.forward_date:
        regex = re.compile("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
        match = regex.match(fromid.text.replace("?single", ""))
        if not match:
            return await message.reply('Invalid link')
        chat_id = match.group(4)
        last_msg_id = int(match.group(5))
        if chat_id.isnumeric():
            chat_id = int(("-100" + chat_id))
    elif fromid.forward_from_chat.type in [enums.ChatType.CHANNEL, 'supergroup']:
        last_msg_id = fromid.forward_from_message_id
        chat_id = fromid.forward_from_chat.username or fromid.forward_from_chat.id
        if last_msg_id == None:
           return await message.reply_text("**This may be a forwarded message from a group and sent by anonymous admin. Instead, please send the last message link from the group**")
    else:
        await message.reply_text("**Invalid!**")
        return 
    
    # ============ VALIDATE CHAT ACCESS (FIXED) ============
    title = None
    
    # First try with the selected bot
    try:
        from .test import get_client
        if is_bot:
            client = await get_client(selected_bot['token'], is_bot=True)
        else:
            client = await get_client(selected_bot['session'], is_bot=False)
        await client.start()
        chat_info = await client.get_chat(chat_id)
        title = chat_info.title
        await client.stop()
    except (ChannelPrivate, PrivateChat, ChannelInvalid) as e:
        # Selected bot cannot access – try userbot (if available)
        userbots = await db.get_bots(user_id, is_bot=False)
        userbot = next((u for u in userbots if u.get('enabled', True)), None)
        if userbot:
            try:
                client = await get_client(userbot['session'], is_bot=False)
                await client.start()
                chat_info = await client.get_chat(chat_id)
                title = chat_info.title
                await client.stop()
                # Switch to userbot for this forward
                selected_bot = userbot
                bot_id = selected_bot['bot_id']
                is_bot = False
            except Exception as e2:
                return await message.reply_text(f"❌ Both bot and userbot cannot access this chat.\nBot error: {e}\nUserbot error: {e2}")
        else:
            return await message.reply_text(
                f"❌ The selected bot cannot access this chat. It may be private.\n"
                f"Please add and enable a userbot in /settings, or ensure your bot is an admin and has the correct permissions."
            )
    except Exception as e:
        return await message.reply_text(f"Error: {str(e)[:100]}")
    
    # ============ SKIP NUMBER ============
    skipno = await bot.ask(message.chat.id, Script.SKIP_MSG)
    if skipno.text.startswith('/'):
        await message.reply(Script.CANCEL)
        return
    
    # ============ CREATE FORWARD SESSION ============
    forward_id = f"{user_id}-{skipno.id}"
    buttons = [[
        InlineKeyboardButton('✅ Yes', callback_data=f"start_public_{forward_id}"),
        InlineKeyboardButton('❌ No', callback_data="close_btn")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    bot_name = selected_bot['name']
    bot_uname = selected_bot['username'] if selected_bot['username'] else "None"
    await message.reply_text(
        text=Script.DOUBLE_CHECK.format(botname=bot_name, botuname=bot_uname, from_chat=title, to_chat=to_title, skip=skipno.text),
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )
    STS(forward_id).store(chat_id, toid, int(skipno.text), int(last_msg_id), bot_id)

# ============ CALLBACK FOR BOT SELECTION ============
@Client.on_callback_query(filters.regex(r'^select_bot_(\d+)'))
async def select_bot_callback(bot, query):
    user_id = query.from_user.id
    bot_id = int(query.data.split('_')[2])
    temp.BOT_SELECTION[user_id] = bot_id
    await query.answer("Bot selected!")
    await query.message.delete()

# ============ CLOSE BUTTON ============
@Client.on_callback_query(filters.regex(r'^close_btn$'))
async def close(bot, update):
    await update.answer()
    await update.message.delete()
