# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import re

# Regular expression to match http://, https://, t.me/, and @mentions
URL_PATTERN = re.compile(
    r'(https?://\S+|t\.me/\S+|@\S+)',
    re.IGNORECASE
)

def strip_urls(text: str) -> str:
    """Remove all URLs, t.me links, and @mentions from the given text."""
    if not text:
        return text
    return URL_PATTERN.sub('', text).strip()
