# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import re

# 1. Matches Markdown links: [text](url)
MARKDOWN_LINK_PATTERN = re.compile(r'\[.*?\]\((.*?)\)')

# 2. Matches HTML links: <a href="url">text</a>
HTML_LINK_PATTERN = re.compile(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"[^>]*>([\s\S]*?)</a>', re.IGNORECASE)

# 3. Matches standard URLs, t.me links, and @mentions
URL_PATTERN = re.compile(
    r'(?:https?://)?'                     # optional protocol
    r'(?:[a-zA-Z0-9-]+\.)+'               # domain name parts (at least one dot)
    r'[a-zA-Z]{2,}'                       # TLD (2+ letters)
    r'(?:/[^\s]*)?'                       # optional path
    r'|t\.me/\S+'                         # t.me links
    r'|@\S+',                             # @mentions
    re.IGNORECASE
)

def strip_urls(text: str) -> str:
    """Remove all URLs, markdown links (including anchor text), HTML links, and @mentions."""
    if not text:
        return text
    
    # First, completely remove Markdown links including their text
    text = MARKDOWN_LINK_PATTERN.sub('', text)
    
    # Second, completely remove HTML links including their text
    text = HTML_LINK_PATTERN.sub('', text)
    
    # Finally, clean up any remaining plain text URLs or @mentions
    text = URL_PATTERN.sub('', text)
    
    # Remove double spaces/newlines that might remain
    text = re.sub(r'\s+', ' ', text).strip()
    return text
