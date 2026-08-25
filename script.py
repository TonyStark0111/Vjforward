import os
from config import Config

class Script(object):
    START_TXT = """<b>Hᴇʏ {} !
    
I'ᴍ ᴀ ᴀᴅᴠᴀɴᴄᴇᴅ ғᴏʀᴡᴀʀᴅɪɴɢ Bᴏᴛ
I ᴄᴀɴ ғᴏʀᴡᴀʀᴅ ᴀʟʟ ᴍᴇssᴀɢᴇs ғʀᴏᴍ ᴏɴᴇ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴀɴᴏᴛʜᴇʀ ᴄʜᴀɴɴᴇʟ</b>

**Cʟɪᴄᴋ Hᴇʟᴘ Bᴜᴛᴛᴏɴ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ᴍᴇ**"""
  
    HELP_TXT = """<b><u>🔶 Help</b></u>

<u>**📚 Available commands:**</u>
<b>⏣ __/start - check I'm alive__ 
⏣ __/forward - forward messages__
⏣ __/settings - configure your settings__
⏣ __/unequify - delete duplicate media messages in chats__
⏣ __/stop - stop your ongoing tasks__
⏣ __/reset - reset your settings__</b>

<b><u>💢 Features:</b></u>
<b>► __Forward message from public channel to your channel without admin permission. if the channel is private need admin permission, if you can't give admin permission then use userbot, but in userbot there is a chance to get your account ban so use fake account__
► __custom caption__
► __custom button__
► __skip duplicate messages__
► __filter type of messages__</b>

<b><u>📌 Starting Point Options:</b></u>
<b>► __Send 0 - Start from the very first message__
► __Send a message ID - Start from that exact message__
► __Send a message link - Start from that message__
► __Forward a message - Start from that message__</b>"""
  
    HOW_USE_TXT = """<b><u>⚠️ Before Forwarding:</b></u>
<b>► __add a bot or userbot__
► __add atleast one to channel__ `(your bot/userbot must be admin in there)`
► __You can add chats or bots by using /settings__
► __if the **From Channel** is private your userbot must be member in there or your bot must need admin permission in there also__
► __Then use /forward to forward messages__

► Hᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ [Tᴜᴛᴏʀɪᴀʟ Vɪᴅᴇᴏ](https://youtu.be/wO1FE-lf35I)</b>"""
  
    ABOUT_TXT = """<b>
╔════❰ Fᴏʀᴡᴀʀᴅɪɴɢ Bᴏᴛ ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼📃Bᴏᴛ : [Fᴏʀᴡᴀʀᴅɪɴɢ Bᴏᴛ](https://t.me/VJForwardBot)
║┣⪼👨‍💻Cʀᴇᴀᴛᴏʀ : [Kɪɴɢ VJ 👑](https://t.me/kingvj01)
║┣⪼🤖Uᴘᴅᴀᴛᴇ : [VJ Bᴏᴛᴢ](https://t.me/vj_botz)
║┣⪼📡Hᴏsᴛᴇᴅ ᴏɴ : Sᴜʙᴇʀ Fᴀsᴛ
║┣⪼🗣️Lᴀɴɢᴜᴀɢᴇ : Pʏᴛʜᴏɴ3
║┣⪼📚Lɪʙʀᴀʀʏ : Pʏʀᴏɢʀᴀᴍ Gᴀᴛʜᴇʀ 2.11.0 
║┣⪼🖊️Vᴇʀsɪᴏɴ : 0.18.3
║╰━━━━━━━━━━━━━━━➣ 
╚════❰ ᴀʙᴏᴜᴛ ❱══❍⊱❁۪۪
</b>"""
  
    STATUS_TXT = """
╔════❰ Bᴏᴛ sᴛᴀᴛᴜs  ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼**⏳ Bᴏᴛ ᴜᴘᴛɪᴍᴇ:**`{}`
║┃
║┣⪼**👱 Tᴏᴛᴀʟ Usᴇʀs:** `{}`
║┃
║┣⪼**🤖 Tᴏᴛᴀʟ Bᴏᴛ:** `{}`
║┃
║┣⪼**🔃 Fᴏʀᴡᴀʀᴅɪɴɢs:** `{}`
║┃
║╰━━━━━━━━━━━━━━━➣ 
╚═══════════════════❍⊱❁۪۪
"""
  
    FROM_MSG = "<b>❮ SET SOURCE CHAT ❯\n\nForward the last message or last message link of source chat.\n/cancel - cancel this process</b>"
    TO_MSG = "<b>❮ CHOOSE TARGET CHAT ❯\n\nChoose your target chat from the given buttons.\n/cancel - Cancel this process</b>"
  
    START_POINT_MSG = """<b>❮ SET STARTING POINT ❯</b>

Now specify where to start forwarding. You can:
• Send <b>0</b> to start from the very first message
• Send a <b>message ID</b> (number) to start from that exact message
• Send a <b>message link</b> from the source chat
• <b>Forward a message</b> from the source chat

The bot will forward from that point up to the last message you set.
Send /cancel to cancel."""
  
    CANCEL = "<b>Process Cancelled Successfully !</b>"
    BOT_DETAILS = "<b><u>📄 BOT DETAILS</b></u>\n\n<b>➣ NAME:</b> <code>{}</code>\n<b>➣ BOT ID:</b> <code>{}</code>\n<b>➣ USERNAME:</b> @{}"
    USER_DETAILS = "<b><u>📄 USERBOT DETAILS</b></u>\n\n<b>➣ NAME:</b> <code>{}</code>\n<b>➣ USER ID:</b> <code>{}</code>\n<b>➣ USERNAME:</b> @{}"  
  
    DOUBLE_CHECK = """<b><u>DOUBLE CHECKING ⚠️</b></u>
<code>Before forwarding the messages Click the Yes button only after checking the following</code>

<b>★ YOUR BOT:</b> [{botname}](t.me/{botuname})
<b>★ FROM CHANNEL:</b> `{from_chat}`
<b>★ TO CHANNEL:</b> `{to_chat}`
<b>★ START MSG ID:</b> `{start_id}`

<i>° [{botname}](t.me/{botuname}) must be admin in **TARGET CHAT**</i> (`{to_chat}`)
<i>° If the **SOURCE CHAT** is private your userbot must be member or your bot must be admin in there also</i>

<b>If the above is checked then the yes button can be clicked</b>"""
  
    SETTINGS_TXT = """<b>change your settings as your wish</b>"""
  
    # ⭐ UPDATED STATUS TEXT WITH BOT NAME ⭐
    TEXT = """
╔════❰ ғᴏʀᴡᴀʀᴅ sᴛᴀᴛᴜs  ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼🤖 BOT: {bot}
║┃
║┣⪼🕵 ғᴇᴄʜᴇᴅ Msɢ : {fetched}
║┃
║┣⪼✅ sᴜᴄᴄᴇғᴜʟʟʏ Fᴡᴅ : {forwarded}
║┃
║┣⪼👥 ᴅᴜᴘʟɪᴄᴀᴛᴇ Msɢ : {duplicate}
║┃
║┣⪼🗑 ᴅᴇʟᴇᴛᴇᴅ Msɢ : {deleted}
║┃
║┣⪼🪆 Sᴋɪᴘᴘᴇᴅ Msɢ : {skip}
║┃
║┣⪼🔁 Fɪʟᴛᴇʀᴇᴅ Msɢ : {filtered}
║┃
║┣⪼📊 Cᴜʀʀᴇɴᴛ Sᴛᴀᴛᴜs: {status}
║┃
║┣⪼⌛ ETA: {eta}
║┃
║┣⪼𖨠 Pᴇʀᴄᴇɴᴛᴀɢᴇ: {percentage} %
║╰━━━━━━━━━━━━━━━➣ 
╚════❰ {title} ❱══❍⊱❁۪۪
"""
  
    DUPLICATE_TEXT = """
╔════❰ ᴜɴᴇǫᴜɪғʏ sᴛᴀᴛᴜs ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼ <b>ғᴇᴛᴄʜᴇᴅ ғɪʟᴇs:</b> <code>{}</code>
║┃
║┣⪼ <b>ᴅᴜᴘʟɪᴄᴀᴛᴇ ᴅᴇʟᴇᴛᴇᴅ:</b> <code>{}</code> 
║╰━━━━━━━━━━━━━━━➣ 
╚════❰ {} ❱══❍⊱❁۪۪
"""
  
    PROGRESS = """
╔════❰ ᴘʀᴏɢʀᴇss sᴛᴀᴛᴜs ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼ <b>📊 Pᴇʀᴄᴇɴᴛᴀɢᴇ:</b> <code>{}%</code>
║┃
║┣⪼ <b>📥 Fᴇᴛᴄʜᴇᴅ:</b> <code>{}</code>
║┃
║┣⪼ <b>✅ Fᴏʀᴡᴀʀᴅᴇᴅ:</b> <code>{}</code>
║┃
║┣⪼ <b>⏳ Rᴇᴍᴀɪɴɪɴɢ:</b> <code>{}</code>
║┃
║┣⪼ <b>📊 Sᴛᴀᴛᴜs:</b> <code>{}</code>
║┃
║┣⪼ <b>⏱️ Tɪᴍᴇ Lᴇғᴛ:</b> <code>{}</code>
║┃
║┣⪼ <b>🕐 Uᴘᴛɪᴍᴇ:</b> <code>{}</code>
║╰━━━━━━━━━━━━━━━➣ 
╚═══════════════════❍⊱❁۪۪
"""
