# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import re

# Matches: http://, https://, protocol-less domains, t.me links, @mentions
URL_PATTERN = re.compile(
    r'(?:https?://)?'                     # optional protocol
    r'(?:[a-zA-Z0-9-]+\.)+'               # domain name parts (at least one dot)
    r'[a-zA-Z]{2,}'                       # TLD (2+ letters)
    r'(?:/[^\s]*)?'                       # optional path
    r'|t\.me/\S+'                         # t.me links
    r'|@\S+',                             # @mentions
    re.IGNORECASE
)

# Matches complete HTML anchor tags and removes them entirely (including inner text)
ANCHOR_TAG_PATTERN = re.compile(r'<a\s+[^>]*>.*?</a>', re.IGNORECASE | re.DOTALL)

def strip_anchors_and_urls(text: str) -> str:
    """Remove entire <a> tags (including their content) and standalone URLs.
       Preserves original line breaks and formatting."""
    if not text:
        return text
    # 1. Remove full anchor tags and everything inside them
    text = ANCHOR_TAG_PATTERN.sub('', text)
    # 2. Remove any remaining plain URLs (including t.me links, @mentions)
    text = URL_PATTERN.sub('', text)
    # 3. ✅ Clean up only extra spaces (NOT newlines)
    text = re.sub(r'[ \t]+', ' ', text)  # Only collapse spaces/tabs, not newlines
    text = text.strip()
    return text

def strip_urls(text: str) -> str:
    """Legacy: Remove only URLs, t.me links, and @mentions (keeps anchor tag text).
       Preserves original line breaks and formatting."""
    if not text:
        return text
    text = URL_PATTERN.sub('', text)
    # ✅ Clean up only extra spaces (NOT newlines)
    text = re.sub(r'[ \t]+', ' ', text)
    text = text.strip()
    return text
