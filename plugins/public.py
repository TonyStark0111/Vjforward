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
from pyrogram.errors import FloodWait, ChannelInvalid, ChannelPrivate
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate as PrivateChat
from pyrogram.errors.exceptions.bad_request_400 import UsernameInvalid, UsernameNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_message(filters.private & filters.command(["forward"]))
async def run(bot, message):
    buttons = []
    btn_data = {}
    user_id = message.from_user.id
    
    # Get user's bots
    _bot = await db.get_bot(user_id)
    userbot = await db.get_userbot(user_id)
    
    # Check if user has any bot
    if not _bot and not userbot:
        return await message.reply("<code>You didn't added any bot. Please add a bot using /settings !</code>")
    
    # Check if user has target channels
    channels = await db.get_user_channels(user_id)
    if not channels:
       return await message.reply_text("Please set a target channel in /settings before forwarding")
    
    # Select target channel
    if len(channels) > 1:
       for channel in channels:
          buttons.append([KeyboardButton(f"{channel['title']}")])
          btn_data[channel['title']] = channel['chat_id']
       buttons.append([KeyboardButton("cancel")]) 
       _toid = await bot.ask(message.chat.id, Script.TO_MSG.format(_bot['name'] if _bot else "Bot", _bot['username'] if _bot else "userbot"), reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))
       if _toid.text.startswith(('/', 'cancel')):
          return await message.reply_text(Script.CANCEL, reply_markup=ReplyKeyboardRemove())
       to_title = _toid.text
       toid = btn_data.get(to_title)
       if not toid:
          return await message.reply_text("Wrong channel chosen!", reply_markup=ReplyKeyboardRemove())
    else:
       toid = channels[0]['chat_id']
       to_title = channels[0]['title']
    
    # Get source chat info
    fromid = await bot.ask(message.chat.id, Script.FROM_MSG, reply_markup=ReplyKeyboardRemove())
    if fromid.text and fromid.text.startswith('/'):
        await message.reply(Script.CANCEL)
        return 
    
    # Parse source chat from link or forwarded message
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
    
    # ============ IMPROVED: Validate chat access using userbot first ============
    title = None
    use_userbot = userbot and userbot.get('enabled', True)
    
    if use_userbot:
        try:
            from .test import get_client
            ub_client = await get_client(userbot['session'], is_bot=False)
            await ub_client.start()
            chat_info = await ub_client.get_chat(chat_id)
            title = chat_info.title
            await ub_client.stop()
        except (ChannelPrivate, PrivateChat, ChannelInvalid):
            await message.reply_text("❌ Your userbot cannot access this private chat.\n\nMake sure:\n1. Your userbot account is a member of that channel/group\n2. The channel/group exists\n3. You're using the correct link")
            return
        except Exception as e:
            await message.reply_text(f"⚠️ Userbot error: {str(e)[:100]}\n\nTrying with main bot (public channels only)...")
            use_userbot = False
    
    # Fallback to main bot (only for public chats)
    if not title:
        try:
            chat_info = await bot.get_chat(chat_id)
            title = chat_info.title
        except (ChannelPrivate, PrivateChat):
            return await message.reply_text("**This is a private channel/group. Please add and enable a userbot in /settings, then try again.**")
        except (UsernameInvalid, UsernameNotModified):
            return await message.reply('Invalid link specified.')
        except Exception as e:
            return await message.reply(f'Error: {e}')
    
    # Get skip number
    skipno = await bot.ask(message.chat.id, Script.SKIP_MSG)
    if skipno.text.startswith('/'):
        await message.reply(Script.CANCEL)
        return
    
    # Create forward session
    forward_id = f"{user_id}-{skipno.id}"
    buttons = [[
        InlineKeyboardButton('✅ Yes', callback_data=f"start_public_{forward_id}"),
        InlineKeyboardButton('❌ No', callback_data="close_btn")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    bot_name = _bot['name'] if _bot else "Bot"
    bot_uname = _bot['username'] if _bot else "None"
    await message.reply_text(
        text=Script.DOUBLE_CHECK.format(botname=bot_name, botuname=bot_uname, from_chat=title, to_chat=to_title, skip=skipno.text),
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )
    STS(forward_id).store(chat_id, toid, int(skipno.text), int(last_msg_id))

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
