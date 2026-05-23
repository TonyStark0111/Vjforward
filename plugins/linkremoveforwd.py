# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import re
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import MessageEntityType

# Keep your original regex to catch any remaining plain-text links or @mentions
URL_PATTERN = re.compile(
    r'(?:https?://)?'                     # optional protocol
    r'(?:[a-zA-Z0-9-]+\.)+'               # domain name parts (at least one dot)
    r'[a-zA-Z]{2,}'                       # TLD (2+ letters)
    r'(?:/[^\s]*)?'                       # optional path
    r'|t\.me/\S+'                         # t.me links
    r'|@\S+',                             # @mentions
    re.IGNORECASE
)

def strip_urls_and_entities(message: Message) -> str:
    """Removes both hidden blue text links (entities) and raw text URLs."""
    if not message.text:
        return ""

    text = message.text

    # 1. Handle hidden "blue text" hyperlinks using Pyrogram Entities
    if message.entities:
        # We loop in REVERSE order. If we loop forward, cutting text changes 
        # the character positions (offsets) of the remaining entities, causing bugs.
        for entity in reversed(message.entities):
            # MessageEntityType.TEXT_LINK is the hidden "blue text" URL
            # MessageEntityType.URL is a standard clickable plain text URL
            if entity.type in [MessageEntityType.TEXT_LINK, MessageEntityType.URL]:
                start = entity.offset
                end = entity.offset + entity.length
                # Completely slice out the text that contains the link
                text = text[:start] + text[end:]

    # 2. Clean up any remaining plain text URLs, t.me links, or @mentions via Regex
    text = URL_PATTERN.sub('', text)
    
    # 3. Clean up extra spaces/newlines left behind from deletions
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# --- Example of how to use it in your handler ---
@Client.on_message(filters.text & ~filters.command)
async def message_handler(client: Client, message: Message):
    # Pass the whole message object, not just message.text
    cleaned_text = strip_urls_and_entities(message)
    
    if cleaned_text:
        await message.reply_text(cleaned_text)
    else:
        await message.reply_text("Message became empty after removing all links.")
