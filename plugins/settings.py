# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import asyncio 
import re
from database import db
from script import Script
from pyrogram import Client, filters
from .test import get_configs, update_configs, CLIENT, parse_buttons
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .db import connect_user_db

CLIENT = CLIENT()

@Client.on_message(filters.command('settings'))
async def settings(client, message):
   await message.reply_text(
     "<b>⚙️ Settings Panel</b>\n\nManage your bots and channels.",
     reply_markup=main_buttons()
   )

def main_buttons():
   buttons = [
       [InlineKeyboardButton('🤖 My Bots', callback_data='settings#list_bots')],
       [InlineKeyboardButton('🏷 Channels', callback_data='settings#channels')],
       [InlineKeyboardButton('⫷ Close', callback_data='close_btn')]
   ]
   return InlineKeyboardMarkup(buttons)

@Client.on_callback_query(filters.regex(r'^settings'))
async def settings_query(bot, query):
  user_id = query.from_user.id
  data = query.data.split("#")
  
  if len(data) < 2:
      return
  
  action = data[1]
  
  # ============ MAIN MENU ============
  if action == "main":
     await query.message.edit_text(
       "<b>⚙️ Settings Panel</b>\n\nManage your bots and channels.",
       reply_markup=main_buttons()
     )
  
  # ============ LIST BOTS ============
  elif action == "list_bots":
     bots = await db.get_bots(user_id)
     buttons = []
     for b in bots:
         status = "✅" if b.get('enabled', True) else "❌"
         label = f"{status} {b['name']} (@{b['username']})" if b['username'] else f"{status} {b['name']}"
         buttons.append([InlineKeyboardButton(label, callback_data=f"settings#bot_{b['bot_id']}")])
     buttons.append([InlineKeyboardButton('➕ Add Bot', callback_data='settings#add_bot')])
     buttons.append([InlineKeyboardButton('➕ Add Userbot', callback_data='settings#add_userbot')])
     buttons.append([InlineKeyboardButton('🔙 Back', callback_data='settings#main')])
     await query.message.edit_text(
        "**Your Bots:**\nClick a bot to manage its settings.",
        reply_markup=InlineKeyboardMarkup(buttons)
     )
  
  # ============ ADD BOT ============
  elif action == "add_bot":
     await query.message.delete()
     await CLIENT.add_bot(bot, query)
     await query.message.reply_text(
        "<b>Bot token successfully added!</b>",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔙 Back', callback_data='settings#list_bots')]])
     )
  
  elif action == "add_userbot":
     await query.message.delete()
     await CLIENT.add_session(bot, query)
     await query.message.reply_text(
        "<b>Userbot session successfully added!</b>",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔙 Back', callback_data='settings#list_bots')]])
     )
  
  # ============ BOT SETTINGS ============
  elif action.startswith("bot_"):
     bot_id = int(action.split('_')[1])
     bot_data = await db.get_bot(user_id, bot_id)
     if not bot_data:
         return await query.answer("Bot not found", show_alert=True)
     
     configs = bot_data.get('configs', {})
     status = "✅ ON" if bot_data.get('enabled', True) else "❌ OFF"
     bot_type = "🤖 Bot" if bot_data['is_bot'] else "👤 Userbot"
     
     text = f"**{bot_type}:** {bot_data['name']}\n"
     text += f"**ID:** {bot_data['bot_id']}\n"
     text += f"**Username:** @{bot_data['username'] if bot_data['username'] else 'None'}\n"
     text += f"**Status:** {status}\n\n"
     text += "Choose a setting to edit:"
     
     buttons = [
         [InlineKeyboardButton('📝 Caption', callback_data=f"settings#caption_{bot_id}")],
         [InlineKeyboardButton('🔘 Button', callback_data=f"settings#button_{bot_id}")],
         [InlineKeyboardButton('🔍 Filters', callback_data=f"settings#filters_{bot_id}")],
         [InlineKeyboardButton('📦 Extra Settings', callback_data=f"settings#extra_{bot_id}")],
         [InlineKeyboardButton('🚀 Turbo Mode', callback_data=f"settings#turbo_menu_{bot_id}")],
         [InlineKeyboardButton(f"{'Disable' if bot_data.get('enabled', True) else 'Enable'} Bot", callback_data=f"settings#toggle_bot_{bot_id}")],
         [InlineKeyboardButton('❌ Remove Bot', callback_data=f"settings#remove_bot_{bot_id}")],
         [InlineKeyboardButton('🔙 Back', callback_data='settings#list_bots')]
     ]
     await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))
  
  # ============ TOGGLE BOT ============
  elif action.startswith("toggle_bot_"):
     bot_id = int(action.split('_')[2])
     bot_data = await db.get_bot(user_id, bot_id)
     if bot_data:
         new_status = not bot_data.get('enabled', True)
         await db.update_bot_status(user_id, bot_id, new_status)
         await query.answer(f"Bot {'Enabled' if new_status else 'Disabled'}", show_alert=True)
         query.data = f"settings#bot_{bot_id}"
         await settings_query(bot, query)
  
  # ============ REMOVE BOT ============
  elif action.startswith("remove_bot_"):
     bot_id = int(action.split('_')[2])
     await db.remove_bot(user_id, bot_id)
     await query.answer("Bot removed!", show_alert=True)
     query.data = "settings#list_bots"
     await settings_query(bot, query)
  
  # ============ CHANNELS ============
  elif action == "channels":
     buttons = []
     channels = await db.get_user_channels(user_id)
     for channel in channels:
        buttons.append([InlineKeyboardButton(f"{channel['title']}", callback_data=f"settings#editchannels_{channel['chat_id']}")])
     buttons.append([InlineKeyboardButton('✚ Add Channel ✚', callback_data="settings#addchannel")])
     buttons.append([InlineKeyboardButton('🔙 Back', callback_data="settings#main")])
     await query.message.edit_text(
       "<b><u>My Channels</b></u>\n\nYou can manage your target chats here.",
       reply_markup=InlineKeyboardMarkup(buttons))
  
  elif action == "addchannel":  
     await query.message.delete()
     buttons = [[InlineKeyboardButton('🔙 Back', callback_data="settings#channels")]]
     chat_ids = await bot.ask(chat_id=query.from_user.id, text="<b>❪ SET TARGET CHAT ❫\n\nForward a message from Your target chat\n/cancel - cancel this process</b>")
     if chat_ids.text=="/cancel":
        return await chat_ids.reply_text("<b>process canceled</b>", reply_markup=InlineKeyboardMarkup(buttons))
     elif not chat_ids.forward_date:
        return await chat_ids.reply("**This is not a forward message**")
     else:
        chat_id = chat_ids.forward_from_chat.id
        title = chat_ids.forward_from_chat.title
        username = chat_ids.forward_from_chat.username
        username = "@" + username if username else "private"
     chat = await db.add_channel(user_id, chat_id, title, username)
     await query.message.reply_text(
        "<b>Successfully updated</b>" if chat else "<b>This channel already added</b>",
        reply_markup=InlineKeyboardMarkup(buttons))
  
  elif action.startswith("editchannels"): 
     chat_id = action.split('_')[1]
     chat = await db.get_channel_details(user_id, chat_id)
     buttons = [[InlineKeyboardButton('❌ Remove ❌', callback_data=f"settings#removechannel_{chat_id}")],
                [InlineKeyboardButton('🔙 Back', callback_data="settings#channels")]]
     await query.message.edit_text(
        f"<b><u>📄 CHANNEL DETAILS</b></u>\n\n<b>- TITLE:</b> <code>{chat['title']}</code>\n<b>- CHANNEL ID: </b> <code>{chat['chat_id']}</code>\n<b>- USERNAME:</b> {chat['username']}",
        reply_markup=InlineKeyboardMarkup(buttons))
  
  elif action.startswith("removechannel"):
     chat_id = action.split('_')[1]
     await db.remove_channel(user_id, chat_id)
     await query.answer("Channel removed!", show_alert=True)
     query.data = "settings#channels"
     await settings_query(bot, query)
  
  # ============ CAPTION ============
  elif action.startswith("caption_"):
     bot_id = int(action.split('_')[1])
     buttons = []
     configs = await db.get_bot_configs(user_id, bot_id)
     caption = configs.get('caption')
     
     if caption is None:
        buttons.append([InlineKeyboardButton('✚ Add Caption ✚', callback_data=f"settings#addcaption_{bot_id}")])
     else:
        buttons.append([InlineKeyboardButton('See Caption', callback_data=f"settings#seecaption_{bot_id}")])
        buttons[-1].append(InlineKeyboardButton('🗑️ Delete Caption', callback_data=f"settings#deletecaption_{bot_id}"))
     buttons.append([InlineKeyboardButton('🔙 Back', callback_data=f"settings#bot_{bot_id}")])
     
     await query.message.edit_text(
        "<b><u>CUSTOM CAPTION</b></u>\n\n<b>You can set a custom caption to videos and documents.</b>\n\n<b><u>AVAILABLE FILLINGS:</b></u>\n- <code>{filename}</code> : Filename\n- <code>{size}</code> : File size\n- <code>{caption}</code> : default caption",
        reply_markup=InlineKeyboardMarkup(buttons))
  
  elif action.startswith("seecaption_"):
     bot_id = int(action.split('_')[1])
     configs = await db.get_bot_configs(user_id, bot_id)
     buttons = [[InlineKeyboardButton('🖋️ Edit Caption', callback_data=f"settings#addcaption_{bot_id}")],
                [InlineKeyboardButton('🔙 Back', callback_data=f"settings#caption_{bot_id}")]]
     await query.message.edit_text(
        f"<b><u>YOUR CUSTOM CAPTION</b></u>\n\n<code>{configs.get('caption')}</code>",
        reply_markup=InlineKeyboardMarkup(buttons))
  
  elif action.startswith("deletecaption_"):
     bot_id = int(action.split('_')[1])
     await update_configs(user_id, bot_id, 'caption', None)
     await query.answer("Caption deleted!", show_alert=True)
     query.data = f"settings#caption_{bot_id}"
     await settings_query(bot, query)
  
  elif action.startswith("addcaption_"):
     bot_id = int(action.split('_')[1])
     await query.message.delete()
     buttons = [[InlineKeyboardButton('🔙 Back', callback_data=f"settings#caption_{bot_id}")]]
     caption = await bot.ask(query.message.chat.id, "Send your custom caption\n/cancel - <code>cancel this process</code>")
     if caption.text=="/cancel":
        return await caption.reply_text("<b>process canceled !</b>", reply_markup=InlineKeyboardMarkup(buttons))
     try:
         caption.text.format(filename='', size='', caption='')
     except KeyError as e:
         return await caption.reply_text(f"<b>wrong filling {e} used in your caption. change it</b>", reply_markup=InlineKeyboardMarkup(buttons))
     await update_configs(user_id, bot_id, 'caption', caption.text)
     await caption.reply_text("<b>successfully updated</b>", reply_markup=InlineKeyboardMarkup(buttons))
  
  # ============ BUTTON ============
  elif action.startswith("button_"):
     bot_id = int(action.split('_')[1])
     buttons = []
     configs = await db.get_bot_configs(user_id, bot_id)
     button = configs.get('button')
     
     if button is None:
        buttons.append([InlineKeyboardButton('✚ Add Button ✚', callback_data=f"settings#addbutton_{bot_id}")])
     else:
        buttons.append([InlineKeyboardButton('👀 See Button', callback_data=f"settings#seebutton_{bot_id}")])
        buttons[-1].append(InlineKeyboardButton('🗑️ Remove Button', callback_data=f"settings#deletebutton_{bot_id}"))
     buttons.append([InlineKeyboardButton('🔙 Back', callback_data=f"settings#bot_{bot_id}")])
     
     await query.message.edit_text(
        "<b><u>CUSTOM BUTTON</b></u>\n\n<b>You can set a inline button to messages.</b>\n\n<b><u>FORMAT:</b></u>\n`[Forward bot][buttonurl:https://t.me/mychannelurl]`\n",
        reply_markup=InlineKeyboardMarkup(buttons))
  
  elif action.startswith("addbutton_"):
     bot_id = int(action.split('_')[1])
     await query.message.delete()
     buttons = [[InlineKeyboardButton('🔙 Back', callback_data=f"settings#button_{bot_id}")]]
     ask = await bot.ask(user_id, text="**Send your custom button.\n\nFORMAT:**\n`[forward bot][buttonurl:https://t.me/url]`\n")
     button = parse_buttons(ask.text.html)
     if not button:
        return await ask.reply("**INVALID BUTTON**")
     await update_configs(user_id, bot_id, 'button', ask.text.html)
     await ask.reply("**Successfully button added**", reply_markup=InlineKeyboardMarkup(buttons))
  
  elif action.startswith("seebutton_"):
     bot_id = int(action.split('_')[1])
     configs = await db.get_bot_configs(user_id, bot_id)
     button_text = configs.get('button')
     button = parse_buttons(button_text, markup=False)
     if button:
         button.append([InlineKeyboardButton("🔙 Back", f"settings#button_{bot_id}")])
     else:
         button = [[InlineKeyboardButton("🔙 Back", f"settings#button_{bot_id}")]]
     await query.message.edit_text("**YOUR CUSTOM BUTTON**", reply_markup=InlineKeyboardMarkup(button))
  
  elif action.startswith("deletebutton_"):
     bot_id = int(action.split('_')[1])
     await update_configs(user_id, bot_id, 'button', None)
     await query.answer("Button deleted!", show_alert=True)
     query.data = f"settings#button_{bot_id}"
     await settings_query(bot, query)
  
  # ============ EXTRA SETTINGS ============
  elif action.startswith("extra_"):
     bot_id = int(action.split('_')[1])
     await query.message.edit_text(
        "<b>📦 Extra Settings</b>",
        reply_markup=await extra_buttons(user_id, bot_id))
  
  # ============ TURBO MODE ============
  elif action.startswith("turbo_menu_"):
     bot_id = int(action.split('_')[1])
     configs = await db.get_bot_configs(user_id, bot_id)
     count = configs.get('turbo_count', 20)
     delay = configs.get('forward_delay', 0)
     sleep = configs.get('turbo_sleep', 30)
     delay_display = f"{delay}s" if delay > 0 else "Auto (3s/6s)"
     
     text = f"**🚀 Turbo Mode Settings**\n\n"
     text += f"• **Count**: `{count}` forwards\n"
     text += f"• **Forward Delay**: `{delay_display}`\n"
     text += f"• **Sleep**: `{sleep}` seconds\n\n"
     text += "Adjust using the buttons below."
     
     buttons = [
         [InlineKeyboardButton(f"📊 Count: {count}", callback_data=f"settings#set_turbo_count_{bot_id}")],
         [InlineKeyboardButton(f"⏱️ Forward Delay: {delay_display}", callback_data=f"settings#set_forward_delay_{bot_id}")],
         [InlineKeyboardButton(f"😴 Sleep: {sleep}s", callback_data=f"settings#set_turbo_sleep_{bot_id}")],
         [InlineKeyboardButton("🔙 Back", callback_data=f"settings#extra_{bot_id}")]
     ]
     await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))
  
  elif action.startswith("set_turbo_count_"):
     bot_id = int(action.split('_')[3])
     await query.message.delete()
     msg = await bot.ask(user_id, "**⚙️ Turbo Count**\n\nAfter how many successful forwards should the bot take a break?\nSend `0` to disable.\n\nSend /cancel to abort.")
     if msg.text == '/cancel':
         return await msg.reply("Cancelled.")
     try:
         count = int(msg.text.strip())
         if count < 0: raise ValueError
     except ValueError:
         return await msg.reply("❌ Invalid number!")
     await update_configs(user_id, bot_id, 'turbo_count', count)
     await msg.reply(f"✅ Turbo count set to {count}.")
     query.data = f"settings#turbo_menu_{bot_id}"
     await settings_query(bot, query)
  
  elif action.startswith("set_forward_delay_"):
     bot_id = int(action.split('_')[3])
     await query.message.delete()
     msg = await bot.ask(user_id, "**⏱️ Forward Delay**\n\nDelay in seconds between each forwarded message.\nSend `0` for auto.\n\nSend /cancel to abort.")
     if msg.text == '/cancel':
         return await msg.reply("Cancelled.")
     try:
         delay = int(msg.text.strip())
         if delay < 0: raise ValueError
     except ValueError:
         return await msg.reply("❌ Invalid number!")
     await update_configs(user_id, bot_id, 'forward_delay', delay)
     await msg.reply(f"✅ Forward delay set to {delay} seconds.")
     query.data = f"settings#turbo_menu_{bot_id}"
     await settings_query(bot, query)
  
  elif action.startswith("set_turbo_sleep_"):
     bot_id = int(action.split('_')[3])
     await query.message.delete()
     msg = await bot.ask(user_id, "**⏱️ Turbo Sleep Duration**\n\nHow many seconds should the bot sleep after reaching the turbo count?\n\nSend /cancel to abort.")
     if msg.text == '/cancel':
         return await msg.reply("Cancelled.")
     try:
         sleep_sec = int(msg.text.strip())
         if sleep_sec < 1: raise ValueError
     except ValueError:
         return await msg.reply("❌ Invalid number!")
     await update_configs(user_id, bot_id, 'turbo_sleep', sleep_sec)
     await msg.reply(f"✅ Turbo sleep duration set to {sleep_sec} seconds.")
     query.data = f"settings#turbo_menu_{bot_id}"
     await settings_query(bot, query)
  
  # ============ FILTERS ============
  elif action.startswith("filters_"):
     bot_id = int(action.split('_')[1])
     await query.message.edit_text(
        "<b><u>💠 CUSTOM FILTERS</b></u>\n\nConfigure the type of messages you want to forward.",
        reply_markup=await filters_buttons(user_id, bot_id))
  
  elif action.startswith("nextfilters_"):
     bot_id = int(action.split('_')[1])
     await query.edit_message_reply_markup(
        reply_markup=await next_filters_buttons(user_id, bot_id))
  
  elif action.startswith("updatefilter-"):
     parts = action.split('-')
     bot_id = int(parts[1])
     key = parts[2]
     value = parts[3] == "True"
     await update_configs(user_id, bot_id, key, not value)
     if key in ['poll', 'protect', 'voice', 'animation', 'sticker', 'duplicate']:
         await query.edit_message_reply_markup(
            reply_markup=await next_filters_buttons(user_id, bot_id))
     else:
         await query.edit_message_reply_markup(
            reply_markup=await filters_buttons(user_id, bot_id))

# ============ HELPER FUNCTIONS ============

async def extra_buttons(user_id, bot_id):
    configs = await db.get_bot_configs(user_id, bot_id)
    link_remove = configs.get('link_remove', False)
    replace_link = configs.get('replace_link', None)
    replace_text = 'Set' if not replace_link else 'Change'
    
    buttons = [[
        InlineKeyboardButton('💾 Min Size Limit', callback_data=f'settings#file_size_{bot_id}')
    ],[
        InlineKeyboardButton('💾 Max Size Limit', callback_data=f'settings#maxfile_size_{bot_id}')
    ],[
        InlineKeyboardButton('🚥 Keywords', callback_data=f'settings#get_keyword_{bot_id}'),
        InlineKeyboardButton('🕹 Extensions', callback_data=f'settings#get_extension_{bot_id}')
    ],[
        InlineKeyboardButton('🔗 Link Removal', callback_data=f'settings#link_remove_{bot_id}'),
        InlineKeyboardButton('✅' if link_remove else '❌', callback_data=f'settings#toggle_link_remove_{bot_id}')
    ],[
        InlineKeyboardButton('🔄 Replacement Link', callback_data=f'settings#replace_link_{bot_id}'),
        InlineKeyboardButton(replace_text, callback_data=f'settings#set_replace_link_{bot_id}')
    ],[
        InlineKeyboardButton('🚀 Turbo Mode', callback_data=f'settings#turbo_menu_{bot_id}')
    ],[
        InlineKeyboardButton('⫷ Back', callback_data=f'settings#bot_{bot_id}')
    ]]
    return InlineKeyboardMarkup(buttons)

async def filters_buttons(user_id, bot_id):
    configs = await db.get_bot_configs(user_id, bot_id)
    filters = configs.get('filters', {})
    forward_tag = configs.get('forward_tag', False)
    
    buttons = [[
        InlineKeyboardButton('🏷️ Forward tag', callback_data=f'settings_#updatefilter-{bot_id}-forward_tag-{forward_tag}'),
        InlineKeyboardButton('✅' if forward_tag else '❌', callback_data=f'settings#updatefilter-{bot_id}-forward_tag-{forward_tag}')
    ],[
        InlineKeyboardButton('🖍️ Texts', callback_data=f'settings_#updatefilter-{bot_id}-text-{filters.get("text", True)}'),
        InlineKeyboardButton('✅' if filters.get('text', True) else '❌', callback_data=f'settings#updatefilter-{bot_id}-text-{filters.get("text", True)}')
    ],[
        InlineKeyboardButton('📁 Documents', callback_data=f'settings_#updatefilter-{bot_id}-document-{filters.get("document", True)}'),
        InlineKeyboardButton('✅' if filters.get('document', True) else '❌', callback_data=f'settings#updatefilter-{bot_id}-document-{filters.get("document", True)}')
    ],[
        InlineKeyboardButton('🎞️ Videos', callback_data=f'settings_#updatefilter-{bot_id}-video-{filters.get("video", True)}'),
        InlineKeyboardButton('✅' if filters.get('video', True) else '❌', callback_data=f'settings#updatefilter-{bot_id}-video-{filters.get("video", True)}')
    ],[
        InlineKeyboardButton('📷 Photos', callback_data=f'settings_#updatefilter-{bot_id}-photo-{filters.get("photo", True)}'),
        InlineKeyboardButton('✅' if filters.get('photo', True) else '❌', callback_data=f'settings#updatefilter-{bot_id}-photo-{filters.get("photo", True)}')
    ],[
        InlineKeyboardButton('🎧 Audios', callback_data=f'settings_#updatefilter-{bot_id}-audio-{filters.get("audio", True)}'),
        InlineKeyboardButton('✅' if filters.get('audio', True) else '❌', callback_data=f'settings#updatefilter-{bot_id}-audio-{filters.get("audio", True)}')
    ],[
        InlineKeyboardButton('⫷ Back', callback_data=f"settings#bot_{bot_id}"),
        InlineKeyboardButton('Next ⫸', callback_data=f"settings#nextfilters_{bot_id}")
    ]]
    return InlineKeyboardMarkup(buttons)

async def next_filters_buttons(user_id, bot_id):
    configs = await db.get_bot_configs(user_id, bot_id)
    filters = configs.get('filters', {})
    duplicate = configs.get('duplicate', True)
    protect = configs.get('protect', False)
    
    buttons = [[
        InlineKeyboardButton('🎤 Voices', callback_data=f'settings_#updatefilter-{bot_id}-voice-{filters.get("voice", True)}'),
        InlineKeyboardButton('✅' if filters.get('voice', True) else '❌', callback_data=f'settings#updatefilter-{bot_id}-voice-{filters.get("voice", True)}')
    ],[
        InlineKeyboardButton('🎭 Animations', callback_data=f'settings_#updatefilter-{bot_id}-animation-{filters.get("animation", True)}'),
        InlineKeyboardButton('✅' if filters.get('animation', True) else '❌', callback_data=f'settings#updatefilter-{bot_id}-animation-{filters.get("animation", True)}')
    ],[
        InlineKeyboardButton('🃏 Stickers', callback_data=f'settings_#updatefilter-{bot_id}-sticker-{filters.get("sticker", True)}'),
        InlineKeyboardButton('✅' if filters.get('sticker', True) else '❌', callback_data=f'settings#updatefilter-{bot_id}-sticker-{filters.get("sticker", True)}')
    ],[
        InlineKeyboardButton('▶️ Skip duplicate', callback_data=f'settings_#updatefilter-{bot_id}-duplicate-{duplicate}'),
        InlineKeyboardButton('✅' if duplicate else '❌', callback_data=f'settings#updatefilter-{bot_id}-duplicate-{duplicate}')
    ],[
        InlineKeyboardButton('📊 Poll', callback_data=f'settings_#updatefilter-{bot_id}-poll-{filters.get("poll", True)}'),
        InlineKeyboardButton('✅' if filters.get('poll', True) else '❌', callback_data=f'settings#updatefilter-{bot_id}-poll-{filters.get("poll", True)}')
    ],[
        InlineKeyboardButton('🔒 Secure message', callback_data=f'settings_#updatefilter-{bot_id}-protect-{protect}'),
        InlineKeyboardButton('✅' if protect else '❌', callback_data=f'settings#updatefilter-{bot_id}-protect-{protect}')
    ],[
        InlineKeyboardButton('⫷ Back', callback_data=f"settings#filters_{bot_id}"),
        InlineKeyboardButton('End ⫸', callback_data=f"settings#bot_{bot_id}")
    ]]
    return InlineKeyboardMarkup(buttons)

# ============ SIZE, KEYWORD, EXTENSION HANDLERS ============
# (These follow similar pattern with bot_id - I'll add the key ones)

@Client.on_callback_query(filters.regex(r'^settings#file_size_'))
async def size_settings(bot, query):
    bot_id = int(query.data.split('_')[2])
    configs = await db.get_bot_configs(query.from_user.id, bot_id)
    size = configs.get('min_size', 0)
    await query.message.edit_text(
       f'<b><u>SIZE LIMIT</b></u>\n\nFiles with size greater than `{size} MB` will be forwarded.',
       reply_markup=size_button(bot_id, size, 'min'))

@Client.on_callback_query(filters.regex(r'^settings#maxfile_size_'))
async def maxsize_settings(bot, query):
    bot_id = int(query.data.split('_')[2])
    configs = await db.get_bot_configs(query.from_user.id, bot_id)
    size = configs.get('max_size', 0)
    await query.message.edit_text(
       f'<b><u>MAX SIZE LIMIT</b></u>\n\nFiles with size less than `{size} MB` will be forwarded.',
       reply_markup=size_button(bot_id, size, 'max'))

def size_button(bot_id, size, type):
    update_type = 'update_size' if type == 'min' else 'maxupdate_size'
    buttons = [[
        InlineKeyboardButton('+1', callback_data=f'settings#{update_type}-{bot_id}-{size + 1}'),
        InlineKeyboardButton('-1', callback_data=f'settings#{update_type}-{bot_id}-{size - 1}')
    ],[
        InlineKeyboardButton('+5', callback_data=f'settings#{update_type}-{bot_id}-{size + 5}'),
        InlineKeyboardButton('-5', callback_data=f'settings#{update_type}-{bot_id}-{size - 5}')
    ],[
        InlineKeyboardButton('+10', callback_data=f'settings#{update_type}-{bot_id}-{size + 10}'),
        InlineKeyboardButton('-10', callback_data=f'settings#{update_type}-{bot_id}-{size - 10}')
    ],[
        InlineKeyboardButton('+50', callback_data=f'settings#{update_type}-{bot_id}-{size + 50}'),
        InlineKeyboardButton('-50', callback_data=f'settings#{update_type}-{bot_id}-{size - 50}')
    ],[
        InlineKeyboardButton('+100', callback_data=f'settings#{update_type}-{bot_id}-{size + 100}'),
        InlineKeyboardButton('-100', callback_data=f'settings#{update_type}-{bot_id}-{size - 100}')
    ],[
        InlineKeyboardButton('🔙 Back', callback_data=f"settings#extra_{bot_id}")
    ]]
    return InlineKeyboardMarkup(buttons)

@Client.on_callback_query(filters.regex(r'^settings#update_size-'))
async def update_size(bot, query):
    parts = query.data.split('-')
    bot_id = int(parts[1])
    size = int(parts[2])
    if size < 0: size = 0
    if size > 4000: return await query.answer("Size limit exceeded!", show_alert=True)
    await update_configs(query.from_user.id, bot_id, 'min_size', size)
    query.data = f"settings#file_size_{bot_id}"
    await size_settings(bot, query)

@Client.on_callback_query(filters.regex(r'^settings#maxupdate_size-'))
async def update_maxsize(bot, query):
    parts = query.data.split('-')
    bot_id = int(parts[1])
    size = int(parts[2])
    if size < 0: size = 0
    if size > 4000: return await query.answer("Size limit exceeded!", show_alert=True)
    await update_configs(query.from_user.id, bot_id, 'max_size', size)
    query.data = f"settings#maxfile_size_{bot_id}"
    await maxsize_settings(bot, query)

# ============ KEYWORDS ============
@Client.on_callback_query(filters.regex(r'^settings#get_keyword_'))
async def get_keyword(bot, query):
    bot_id = int(query.data.split('_')[2])
    configs = await db.get_bot_configs(query.from_user.id, bot_id)
    keywords = configs.get('keywords', [])
    text = "<b><u>KEYWORDS</b></u>\n\n"
    if keywords:
       for key in keywords:
          text += f"<code>- {key}</code>\n"
    else:
       text += "No keywords added yet."
    buttons = [
        [InlineKeyboardButton('✚ Add', callback_data=f"settings#add_keyword_{bot_id}")],
        [InlineKeyboardButton('Remove All', callback_data=f"settings#rmve_all_keyword_{bot_id}")],
        [InlineKeyboardButton('🔙 Back', callback_data=f"settings#extra_{bot_id}")]
    ]
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex(r'^settings#add_keyword_'))
async def add_keyword(bot, query):
    bot_id = int(query.data.split('_')[2])
    await query.message.delete()
    ask = await bot.ask(query.from_user.id, "**Send your keywords (one per line or use | to separate):**\n\nSend /cancel to cancel")
    if ask.text == '/cancel':
       return await ask.reply("Cancelled.")
    text = ask.text.strip()
    keywords = []
    if '|' in text:
        keywords = [kw.strip() for kw in text.split('|') if kw.strip()]
    else:
        keywords = [line.strip() for line in text.split('\n') if line.strip()]
    if not keywords:
        return await ask.reply("No valid keywords found!")
    existing = (await db.get_bot_configs(query.from_user.id, bot_id)).get('keywords', [])
    if existing:
        for kw in keywords:
            if kw not in existing:
                existing.append(kw)
        final = existing
    else:
        final = keywords
    await update_configs(query.from_user.id, bot_id, 'keywords', final)
    await ask.reply(f"✅ Added {len(keywords)} keywords!")

@Client.on_callback_query(filters.regex(r'^settings#rmve_all_keyword_'))
async def rmve_all_keyword(bot, query):
    bot_id = int(query.data.split('_')[2])
    await update_configs(query.from_user.id, bot_id, 'keywords', None)
    await query.answer("All keywords deleted!", show_alert=True)
    query.data = f"settings#get_keyword_{bot_id}"
    await get_keyword(bot, query)

# ============ EXTENSIONS ============
@Client.on_callback_query(filters.regex(r'^settings#get_extension_'))
async def get_extension(bot, query):
    bot_id = int(query.data.split('_')[2])
    configs = await db.get_bot_configs(query.from_user.id, bot_id)
    extensions = configs.get('extension', [])
    text = "<b><u>EXTENSIONS</b></u>\n\n"
    if extensions:
       for ext in extensions:
          text += f"<code>- {ext}</code>\n"
    else:
       text += "No extensions added yet."
    buttons = [
        [InlineKeyboardButton('✚ Add', callback_data=f"settings#add_extension_{bot_id}")],
        [InlineKeyboardButton('Remove All', callback_data=f"settings#rmve_all_extension_{bot_id}")],
        [InlineKeyboardButton('🔙 Back', callback_data=f"settings#extra_{bot_id}")]
    ]
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex(r'^settings#add_extension_'))
async def add_extension(bot, query):
    bot_id = int(query.data.split('_')[2])
    await query.message.delete()
    ext = await bot.ask(query.from_user.id, "**Send your extensions (separated by space):**")
    if ext.text == '/cancel':
       return await ext.reply("Cancelled.")
    extensions = ext.text.split()
    existing = (await db.get_bot_configs(query.from_user.id, bot_id)).get('extension', [])
    if existing:
        for e in extensions:
            if e not in existing:
                existing.append(e)
        final = existing
    else:
        final = extensions
    await update_configs(query.from_user.id, bot_id, 'extension', final)
    await ext.reply(f"✅ Added {len(extensions)} extensions!")

@Client.on_callback_query(filters.regex(r'^settings#rmve_all_extension_'))
async def rmve_all_extension(bot, query):
    bot_id = int(query.data.split('_')[2])
    await update_configs(query.from_user.id, bot_id, 'extension', None)
    await query.answer("All extensions deleted!", show_alert=True)
    query.data = f"settings#get_extension_{bot_id}"
    await get_extension(bot, query)

# ============ LINK REMOVAL ============
@Client.on_callback_query(filters.regex(r'^settings#toggle_link_remove_'))
async def toggle_link_remove(bot, query):
    bot_id = int(query.data.split('_')[3])
    configs = await db.get_bot_configs(query.from_user.id, bot_id)
    current = configs.get('link_remove', False)
    await update_configs(query.from_user.id, bot_id, 'link_remove', not current)
    await query.answer(f"Link removal {'enabled' if not current else 'disabled'}", show_alert=True)
    query.data = f"settings#extra_{bot_id}"
    await settings_query(bot, query)

@Client.on_callback_query(filters.regex(r'^settings#set_replace_link_'))
async def set_replace_link(bot, query):
    bot_id = int(query.data.split('_')[3])
    await query.message.delete()
    msg = await bot.ask(query.from_user.id, "**Send replacement text:**\n\n• `@username` - Telegram username\n• `https://example.com` - URL\n• `none` - disable\n\nSend /cancel to abort.")
    if msg.text == "/cancel":
        return await msg.reply("Cancelled.")
    link = msg.text.strip()
    if link.lower() == "none":
        link = None
    elif link.startswith('@'):
        if not re.match(r'^@[a-zA-Z][a-zA-Z0-9_]{4,}$', link):
            return await msg.reply("Invalid username format.")
    elif not link.startswith(('http://', 'https://')):
        return await msg.reply("Invalid input.")
    await update_configs(query.from_user.id, bot_id, 'replace_link', link)
    await msg.reply(f"Replacement set to: `{link if link else 'disabled'}`")
