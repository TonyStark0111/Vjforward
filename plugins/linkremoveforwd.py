# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import re

# Improved regex that matches:
# - Full URLs (http://, https://)
# - Protocol-less domains (example.com, sub.domain.co.uk)
# - t.me/ links
# - @mentions
# - Common autolinked patterns like "duckde.me"
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
    """Remove entire <a> tags (including their content) and standalone URLs."""
    if not text:
        return text
    # 1. Remove full anchor tags and everything inside them
    text = ANCHOR_TAG_PATTERN.sub('', text)
    # 2. Remove any remaining plain URLs (including t.me links, @mentions)
    text = URL_PATTERN.sub('', text)
    # 3. Clean up extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def strip_urls(text: str) -> str:
    """Remove all URLs (including protocol-less domains), t.me links, and @mentions."""
    if not text:
        return text
    # Replace matched URLs with empty string and clean up extra spaces
    text = URL_PATTERN.sub('', text)
    # Remove double spaces that might remain
    text = re.sub(r'\s+', ' ', text).strip()
    return text
