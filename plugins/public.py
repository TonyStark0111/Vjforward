# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import re
import asyncio 
from .utils import STS
from database import Db, db
from config import temp 
from script import Script
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait 
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate as PrivateChat
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified, ChannelPrivate
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_message(filters.private & filters.command(["forward"]))
async def run(bot, message):
    buttons = []
    btn_data = {}
    user_id = message.from_user.id
    
    # Get both bot and userbot
    regular_bot = await db.get_bot(user_id)
    userbot = await db.get_userbot(user_id)
    
    # Check if user has any bot configured
    if not regular_bot and not userbot:
        return await message.reply("<code>You didn't added any bot. Please add a bot using /settings !</code>")
    
    channels = await db.get_user_channels(user_id)
    if not channels:
       return await message.reply_text("please set a to channel in /settings before forwarding")
    
    if len(channels) > 1:
       for channel in channels:
          buttons.append([KeyboardButton(f"{channel['title']}")])
          btn_data[channel['title']] = channel['chat_id']
       buttons.append([KeyboardButton("cancel")]) 
       bot_name = regular_bot['name'] if regular_bot else userbot['name']
       bot_username = regular_bot['username'] if regular_bot else userbot['username']
       _toid = await bot.ask(message.chat.id, Script.TO_MSG.format(bot_name, bot_username), reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))
       if _toid.text.startswith(('/', 'cancel')):
          return await message.reply_text(Script.CANCEL, reply_markup=ReplyKeyboardRemove())
       to_title = _toid.text
       toid = btn_data.get(to_title)
       if not toid:
          return await message.reply_text("wrong channel choosen !", reply_markup=ReplyKeyboardRemove())
    else:
       toid = channels[0]['chat_id']
       to_title = channels[0]['title']
    
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
            chat_id  = int(("-100" + chat_id))
    elif fromid.forward_from_chat.type in [enums.ChatType.CHANNEL, 'supergroup']:
        last_msg_id = fromid.forward_from_message_id
        chat_id = fromid.forward_from_chat.username or fromid.forward_from_chat.id
        if last_msg_id == None:
           return await message.reply_text("**This may be a forwarded message from a group and sended by anonymous admin. instead of this please send last message link from group**")
    else:
        await message.reply_text("**invalid !**")
        return 
    
    # ============ AUTO-DETECT CHANNEL TYPE AND SELECT APPROPRIATE BOT ============
    try:
        # Try to get chat info to check if it's private/public
        chat_info = await bot.get_chat(chat_id)
        is_private_channel = False
        
        # Check if channel is private (username is None for private channels)
        if not chat_info.username:
            is_private_channel = True
            
        title = chat_info.title
        
    except (PrivateChat, ChannelPrivate, ChannelInvalid):
        # If we get privacy error, it's definitely a private channel
        is_private_channel = True
        title = "private channel"
        
    except (UsernameInvalid, UsernameNotModified):
        return await message.reply('Invalid Link specified.')
    except Exception as e:
        return await message.reply(f'Errors - {e}')
    
    # ============ SELECT THE CORRECT BOT BASED ON CHANNEL TYPE ============
    selected_bot = None
    bot_type = None
    status_msg = None
    
    if is_private_channel:
        # For private channels: MUST use userbot (member required)
        if userbot:
            selected_bot = userbot
            bot_type = "userbot"
            status_msg = await message.reply(f"<b>🔐 Private channel detected!</b>\n\nUsing <b>Userbot</b> (@{userbot['username']}) to access private channel.\n\n<i>Make sure @{userbot['username']} is a member of the channel.</i>")
        else:
            return await message.reply("<b>❌ Cannot access private channel!</b>\n\nYou need to add a <b>Userbot</b> (not a regular bot) to access private channels.\n\nUse /settings → Bots → Add User bot to add one.")
    else:
        # For public channels: can use regular bot (admin not required for reading)
        if regular_bot:
            selected_bot = regular_bot
            bot_type = "bot"
            status_msg = await message.reply(f"<b>🌐 Public channel detected!</b>\n\nUsing <b>Bot</b> (@{regular_bot['username']}) to forward messages.\n\n<i>Note: Make sure @{regular_bot['username']} has admin access if needed.</i>")
        elif userbot:
            # Fallback to userbot if no regular bot exists
            selected_bot = userbot
            bot_type = "userbot"
            status_msg = await message.reply(f"<b>🌐 Public channel detected!</b>\n\nNo regular bot found. Using <b>Userbot</b> (@{userbot['username']}) instead.")
        else:
            return await message.reply("<b>❌ No bot available!</b>\n\nPlease add a bot using /settings")
    
    # Delete the status message after 3 seconds
    asyncio.create_task(delete_after_delay(status_msg, 3))
    
    skipno = await bot.ask(message.chat.id, Script.SKIP_MSG)
    if skipno.text.startswith('/'):
        await message.reply(Script.CANCEL)
        return
    
    forward_id = f"{user_id}-{skipno.id}"
    
    # Store which bot type to use in STS (so regix.py knows)
    STS(forward_id).store(chat_id, toid, int(skipno.text), int(last_msg_id))
    
    # Store bot selection info in temp storage
    if not hasattr(temp, 'BOT_SELECTION'):
        temp.BOT_SELECTION = {}
    temp.BOT_SELECTION[forward_id] = {
        'bot_type': bot_type,
        'bot_data': selected_bot,
        'chat_id': chat_id,
        'toid': toid
    }
    
    buttons = [[
        InlineKeyboardButton('Yes', callback_data=f"start_public_{forward_id}"),
        InlineKeyboardButton('No', callback_data="close_btn")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    bot_display_name = selected_bot['name']
    bot_display_username = selected_bot['username']
    
    await message.reply_text(
        text=Script.DOUBLE_CHECK.format(botname=bot_display_name, botuname=bot_display_username, from_chat=title, to_chat=to_title, skip=skipno.text),
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def delete_after_delay(message, delay):
    """Delete a message after specified delay"""
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except:
        pass

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
